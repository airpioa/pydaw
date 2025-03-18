import os
import json
import logging
import subprocess
import pygame
from PyQt6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QWidget, QPushButton, QLabel, QInputDialog, QMessageBox
from PyQt6.QtGui import QIcon
import mido  # MIDI handling
from mido import MidiFile
import dawdreamer  # VST plugin hosting

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Initialize Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 30
PDAW_DIR = os.path.expanduser("~/pydaw")
WORKSPACES_DIR = os.path.join(PDAW_DIR, "workspaces")
INSTRUMENTS_DIR = os.path.join(PDAW_DIR, "instruments")
SETTINGS_FILE = os.path.join(PDAW_DIR, "pydawsettings.json")

# Ensure necessary directories exist
os.makedirs(PDAW_DIR, exist_ok=True)
os.makedirs(WORKSPACES_DIR, exist_ok=True)
os.makedirs(INSTRUMENTS_DIR, exist_ok=True)

# Load settings or initialize new settings
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {"vst_plugins": [], "vst_params": {}, "vst_install_location": ""}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

# Initialize DawDreamer Engine for VST plugins
try:
    engine = dawdreamer.RenderEngine(44100, 512)
    engine.set_bpm(120)
except Exception as e:
    logger.error(f"Error initializing DAW Dreamer: {e}")

# Workspace Management and UI
class WorkspaceWindow(QWidget):
    def __init__(self, workspace_name="New Workspace", workspace_path=""):
        super().__init__()
        self.setWindowTitle(f"{workspace_name} - pydaw")
        self.setGeometry(200, 200, 1000, 600)
        self.workspace_path = workspace_path
        self.setWindowIcon(QIcon("icon.png"))
        self.layout = QVBoxLayout()
        
        self.timeline_label = QLabel("Timeline")
        self.layout.addWidget(self.timeline_label)

        # Add more UI components as needed (timeline, track info, etc.)
        self.setLayout(self.layout)
        self.chuck_processes = []
        
        # Load workspace contents
        self.load_workspace()

    def load_workspace(self):
        manifest_path = os.path.join(self.workspace_path, "manifest.json")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                manifest_data = json.load(f)
            self.load_midi_tracks(manifest_data)
            self.load_vst_plugins(manifest_data)
            self.load_chuck_instruments(manifest_data)

    def load_midi_tracks(self, manifest_data):
        if "tracks" in manifest_data:
            for track in manifest_data["tracks"]:
                if track["type"] == "midi":
                    self.load_midi_file(track["file"])

    def load_midi_file(self, midi_file_path):
        try:
            midi = MidiFile(midi_file_path)
            for msg in midi.play():
                print(msg)
        except Exception as e:
            logger.error(f"Failed to load MIDI file: {e}")

    def load_vst_plugins(self, manifest_data):
        if "vst_plugins" in manifest_data:
            for vst_path in manifest_data["vst_plugins"]:
                self.load_vst(vst_path)

    def load_vst(self, vst_path):
        try:
            plugin = engine.make_plugin_processor("vst", vst_path)
            engine.load_graph({"nodes": [{"id": "vst", "processor": plugin}]})
        except Exception as e:
            logger.error(f"Failed to load VST {vst_path}: {e}")

    def load_chuck_instruments(self, manifest_data):
        if "chuck_scripts" in manifest_data:
            for script_path in manifest_data["chuck_scripts"]:
                self.start_chuck_script(script_path)

    def start_chuck_script(self, script_path):
        try:
            process = subprocess.Popen(
                ['chuck', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            logger.info(f"Started ChucK script: {script_path}")
            self.chuck_processes.append(process)
        except Exception as e:
            logger.error(f"Failed to start ChucK script '{script_path}': {e}")

# Functions
def create_new_workspace():
    workspace_name, ok = QInputDialog.getText(None, "Create New Workspace", "Workspace Name:")
    if ok and workspace_name:
        workspace_path = os.path.join(WORKSPACES_DIR, workspace_name)
        try:
            os.makedirs(workspace_path, exist_ok=False)
            os.makedirs(os.path.join(workspace_path, "instruments"), exist_ok=True)
            logger.info(f"Workspace '{workspace_name}' created at {workspace_path}")
            
            # Create an empty manifest file
            manifest_data = {"tracks": [], "vst_plugins": [], "chuck_scripts": []}
            with open(os.path.join(workspace_path, "manifest.json"), "w") as f:
                json.dump(manifest_data, f, indent=4)
            
            # Open the workspace window automatically
            workspace_window = WorkspaceWindow(workspace_name, workspace_path)
            workspace_window.show()

        except FileExistsError:
            QMessageBox.warning(None, "Error", f"Workspace '{workspace_name}' already exists.")
        except Exception as e:
            logger.error(f"Failed to create workspace '{workspace_name}': {e}")
            QMessageBox.critical(None, "Error", f"An error occurred while creating the workspace:\n{e}")

def open_workspace():
    workspace_path = QFileDialog.getExistingDirectory(None, "Open Workspace", WORKSPACES_DIR)
    if workspace_path:
        workspace_name = os.path.basename(workspace_path)
        workspace_window = WorkspaceWindow(workspace_name, workspace_path)
        workspace_window.show()

def main():
    app = QApplication([])
    main_window = QWidget()
    main_window.setWindowTitle("PyDAW Main Menu")
    main_window.setGeometry(200, 200, 600, 400)
    
    layout = QVBoxLayout()
    layout.addWidget(QPushButton("Create Workspace", clicked=create_new_workspace))
    layout.addWidget(QPushButton("Open Workspace", clicked=open_workspace))
    
    main_window.setLayout(layout)
    main_window.show()
    
    app.exec()

if __name__ == "__main__":
    main()
