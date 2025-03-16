import pygame
import os
import json
import shutil
import logging
import dawdreamer  # VST plugin hosting
import mido  # MIDI handling
from mido import MidiFile
from PyQt6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtGui import QIcon
from pydub import AudioSegment

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
SETTINGS_FILE = os.path.join(PDAW_DIR, "pydawsettings.json")

# Ensure necessary directories exist
os.makedirs(PDAW_DIR, exist_ok=True)
os.makedirs(WORKSPACES_DIR, exist_ok=True)

# Load settings or initialize new settings
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {"vst_plugins": [], "vst_params": {}, "vst_install_location": ""}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

# UI Colors
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)

# Fonts (Fix Pygame Font Issue)
try:
    font = pygame.font.Font(None, 24)  # Fallback font
except Exception:
    font = pygame.font.SysFont("Arial", 24)

# Initialize Pygame Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("pydaw - Python DAW")
clock = pygame.time.Clock()

# DawDreamer Engine for VSTs (Fix incorrect kwargs)
try:
    engine = dawdreamer.RenderEngine(44100, 512)
    engine.set_bpm(120)
except Exception as e:
    logger.error(f"Error initializing DAW Dreamer: {e}")

# Workspace Management
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
        self.setLayout(self.layout)
        self.load_workspace()

    def load_workspace(self):
        manifest_path = os.path.join(self.workspace_path, "manifest.json")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                manifest_data = json.load(f)
            self.load_midi_tracks(manifest_data)
            self.load_vst_plugins(manifest_data)

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

# Functions
def open_workspace():
    workspace_path = QFileDialog.getExistingDirectory(None, "Open Workspace", WORKSPACES_DIR)
    if workspace_path:
        workspace_name = os.path.basename(workspace_path)
        workspace_window = WorkspaceWindow(workspace_name, workspace_path)
        workspace_window.show()

def create_new_workspace():
    workspace_name, ok = QFileDialog.getText(None, "Create New Workspace", "Workspace Name:")
    if ok and workspace_name:
        workspace_path = os.path.join(WORKSPACES_DIR, workspace_name)
        os.makedirs(workspace_path, exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "midi"), exist_ok=True)
        os.makedirs(os.path.join(workspace_path, "vst"), exist_ok=True)
        create_workspace_manifest(workspace_path)
        workspace_window = WorkspaceWindow(workspace_name, workspace_path)
        workspace_window.show()

def create_workspace_manifest(workspace_path):
    manifest = {
        "name": os.path.basename(workspace_path),
        "tracks": [],
        "vst_plugins": [],
        "settings": {"bpm": 120, "sample_rate": 44100},
        "version": "1.0.0"
    }
    manifest_path = os.path.join(workspace_path, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)

def import_midi_to_workspace(workspace_path):
    midi_file, _ = QFileDialog.getOpenFileName(None, "Select MIDI File", "", "MIDI Files (*.mid)")
    if midi_file:
        shutil.copy(midi_file, os.path.join(workspace_path, "midi", os.path.basename(midi_file)))

def import_vst_to_workspace(workspace_path):
    vst_file, _ = QFileDialog.getOpenFileName(None, "Select VST Plugin", "", "VST Plugins (*.dll *.vst3 *.so *.dylib)")
    if vst_file:
        shutil.copy(vst_file, os.path.join(workspace_path, "vst", os.path.basename(vst_file)))

# Main Menu
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
