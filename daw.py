import pygame
import os
import json
import shutil
from PyQt6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QWidget, QPushButton, QLabel, QInputDialog
from PyQt6.QtGui import QIcon
import logging
from pydub import AudioSegment  # For mp3 or other formats

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Initialize Pygame
pygame.init()  # Initialize Pygame
pygame.font.init()  # Ensure the font module is initialized
pygame.mixer.init()  # Initialize the Pygame mixer module for sound playback

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 30
PDAW_DIR = os.path.expanduser("~/pydaw")
WORKSPACES_DIR = os.path.join(PDAW_DIR, "workspaces")
SETTINGS_FILE = os.path.join(PDAW_DIR, "pydawsettings.json")

# Workspace directory and file handling
os.makedirs(PDAW_DIR, exist_ok=True)
os.makedirs(WORKSPACES_DIR, exist_ok=True)

# Load settings or initialize new settings
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
        logger.info("Settings loaded successfully.")
else:
    settings = {"vst_plugins": [], "vst_params": {}, "vst_install_location": ""}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
        logger.info("Settings file created.")

# UI Colors
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Initialize Main Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("pydaw - Python DAW")
clock = pygame.time.Clock()

# Workspace window for managing tracks, timeline, and more
class WorkspaceWindow(QWidget):
    def __init__(self, workspace_name="New Workspace", workspace_path=""):
        super().__init__()
        self.setWindowTitle(f"{workspace_name} - pydaw")
        self.setGeometry(200, 200, 1000, 600)
        self.workspace_path = workspace_path
        self.setWindowIcon(QIcon("icon.png"))

        self.layout = QVBoxLayout()

        # Timeline label
        self.timeline_label = QLabel("Timeline")
        self.layout.addWidget(self.timeline_label)

        self.setLayout(self.layout)

        self.load_workspace()

    def load_workspace(self):
        logger.info(f"Attempting to load workspace from {self.workspace_path}")
        manifest_path = os.path.join(self.workspace_path, "manifest.json")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                manifest_data = json.load(f)
                logger.info(f"Workspace loaded: {manifest_data}")
            # Initialize basic timeline rendering
            self.render_timeline()

            # Automatically initialize instruments
            self.load_instruments(manifest_data)
        else:
            logger.warning("No manifest found. This is a new workspace.")

    def render_timeline(self):
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(0, 50, SCREEN_WIDTH, 100))  # Timeline background
        text_surface = font.render("Timeline", True, TEXT_COLOR)  # Render the text
        screen.blit(text_surface, (60, 55))  # Blit the text onto the screen
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(50, 80, 200, 20))  # A clip on the timeline
        pygame.display.update()

    def load_instruments(self, manifest_data):
        # Check if the workspace has any instruments defined in its manifest
        if "tracks" in manifest_data:
            for track in manifest_data["tracks"]:
                if "instrument" in track:
                    instrument_name = track["instrument"]
                    note = track.get("note", "A1")  # Default to "A1" if note is not specified
                    self.load_instrument(instrument_name, note)

    def load_instrument(self, instrument_name, note):
        # Define the path to the instrument and note file
        instrument_folder = os.path.join(self.workspace_path, "instruments", instrument_name)
        note_file = os.path.join(instrument_folder, f"{note}.wav")

        # Check if the instrument and note exist
        if os.path.exists(note_file):
            logger.info(f"Instrument '{instrument_name}' - Note '{note}' loaded successfully.")
            self.load_audio_file(note_file)  # Load and play the note
        else:
            # Check for .mp3 and .ogg files as fallback
            note_file_mp3 = os.path.splitext(note_file)[0] + ".mp3"
            note_file_ogg = os.path.splitext(note_file)[0] + ".ogg"

            if os.path.exists(note_file_mp3):
                logger.info(f"Instrument '{instrument_name}' - Note '{note}' loaded successfully from MP3.")
                self.load_audio_file(note_file_mp3, is_mp3=True)
            elif os.path.exists(note_file_ogg):
                logger.info(f"Instrument '{instrument_name}' - Note '{note}' loaded successfully from OGG.")
                self.load_audio_file(note_file_ogg)
            else:
                logger.warning(f"Note '{note}' for instrument '{instrument_name}' not found.")

    def load_audio_file(self, file_path, is_mp3=False):
        if is_mp3:
            # Load and play MP3 using Pygame music module
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        else:
            # Load and play WAV or OGG using Pygame sound module
            sound = pygame.mixer.Sound(file_path)
            sound.play()

# Function to open the workspace window
def open_workspace():
    workspace_path = QFileDialog.getExistingDirectory(None, "Open Workspace", WORKSPACES_DIR)
    if workspace_path:
        workspace_name = os.path.basename(workspace_path)
        workspace_window = WorkspaceWindow(workspace_name, workspace_path)
        workspace_window.show()
        logger.info(f"Workspace '{workspace_name}' opened.")

# Function to create a new workspace
def create_new_workspace():
    workspace_name, ok = QFileDialog.getSaveFileName(None, "Create New Workspace", WORKSPACES_DIR, "Workspace Folder (*.*)")
    if ok and workspace_name:
        workspace_name = os.path.splitext(workspace_name)[0]  # Remove file extension if present
        workspace_path = os.path.join(WORKSPACES_DIR, workspace_name)

        # Create workspace folder if it doesn't exist
        os.makedirs(workspace_path, exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "instruments"), exist_ok=True)  # Instrument folder

        # Create workspace manifest
        create_workspace_manifest(workspace_path)

        workspace_window = WorkspaceWindow(workspace_name, workspace_path)
        workspace_window.show()
        logger.info(f"New workspace '{workspace_name}' created at {workspace_path}.")

# Function to create workspace manifest
def create_workspace_manifest(workspace_path):
    manifest = {
        "name": os.path.basename(workspace_path),
        "tracks": [{"name": "Track 1", "type": "audio", "instrument": "Piano", "note": "A1"}],  # Example track with instrument
        "settings": {"bpm": 120, "sample_rate": 44100},
        "version": "1.0.0"  # Version information
    }
    manifest_path = os.path.join(workspace_path, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)
        logger.info(f"Workspace manifest created at {manifest_path}")

# Function to save a folder of instrument files to the workspace
def save_instruments_folder_to_workspace(workspace_path, folder_path, instrument_name):
    # Ensure the instruments directory exists
    instruments_dir = os.path.join(workspace_path, "instruments", instrument_name)
    os.makedirs(instruments_dir, exist_ok=True)

    # Copy all files from the selected folder into the instruments directory
    try:
        for filename in os.listdir(folder_path):
            source_file = os.path.join(folder_path, filename)
            if os.path.isfile(source_file):
                # Copy each file (wav/mp3/ogg)
                shutil.copy(source_file, os.path.join(instruments_dir, filename))
                logger.info(f"Instrument file '{filename}' saved to workspace.")
    except Exception as e:
        logger.error(f"Error saving instrument files: {e}")

# Function to handle saving instrument files
def save_instrument_files(workspace_path):
    folder_path = QFileDialog.getExistingDirectory(None, "Select Folder with Instrument Files")
    if folder_path:
        # Use QInputDialog to get the instrument name
        instrument_name, ok = QInputDialog.getText(None, "Enter Instrument Name", "Instrument Name:")
        if ok and instrument_name:  # Ensure a name is entered
            save_instruments_folder_to_workspace(workspace_path, folder_path, instrument_name)

# Main Menu and Event Loop
def main():
    app = QApplication([])
    main_window = QWidget()
    main_window.setWindowTitle("PyDAW Main Menu")
    main_window.setGeometry(200, 200, 600, 400)

    create_workspace_button = QPushButton("Create Workspace")
    create_workspace_button.clicked.connect(create_new_workspace)

    open_workspace_button = QPushButton("Open Workspace")
    open_workspace_button.clicked.connect(open_workspace)

    save_instrument_button = QPushButton("Save Instruments to Workspace")
    save_instrument_button.clicked.connect(lambda: save_instrument_files(
        QFileDialog.getExistingDirectory(None, "Select Workspace to Save Instruments")))

    layout = QVBoxLayout()
    layout.addWidget(create_workspace_button)
    layout.addWidget(open_workspace_button)
    layout.addWidget(save_instrument_button)
    main_window.setLayout(layout)

    main_window.show()
    app.exec()

if __name__ == "__main__":
    main()
