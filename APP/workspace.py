import os
import json
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QTextEdit
from PySide6.QtGui import QIcon
from config import WORKSPACES_DIR
from logger import logger
from daw_engine import load_vst
from chuck_handler import ChucKManager
from midi_handler import load_midi_file

class WorkspaceWindow(QWidget):
    def __init__(self, workspace_name="New Workspace", workspace_path=""):
        super().__init__()
        self.setWindowTitle(f"{workspace_name} - pydaw")
        self.setGeometry(200, 200, 1000, 600)
        self.workspace_path = workspace_path
        self.setWindowIcon(QIcon("icon.png"))
        
        self.layout = QVBoxLayout()

        # Toolbar with Return Button
        self.toolbar = QHBoxLayout()
        self.back_button = QPushButton("Return to Main Menu")
        self.back_button.clicked.connect(self.close)
        self.toolbar.addWidget(self.back_button)
        self.layout.addLayout(self.toolbar)

        # Timeline Placeholder
        self.timeline_label = QLabel("Timeline")
        self.layout.addWidget(self.timeline_label)

        # ChucK Console Window
        self.chuck_console = QTextEdit()
        self.chuck_console.setReadOnly(True)
        self.layout.addWidget(self.chuck_console)

        self.setLayout(self.layout)

        self.chuck_manager = ChucKManager(self.chuck_console)
        
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
                    load_midi_file(track["file"])

    def load_vst_plugins(self, manifest_data):
        if "vst_plugins" in manifest_data:
            for vst_path in manifest_data["vst_plugins"]:
                load_vst(vst_path)

    def load_chuck_instruments(self, manifest_data):
        if "chuck_scripts" in manifest_data:
            for script_path in manifest_data["chuck_scripts"]:
                self.chuck_manager.run_script(script_path)
