import os
import json
import sys

# Ensure the scripts directory is in the Python path
sys.path.append(os.path.expanduser("~/pydaw"))
sys.path.append(os.path.expanduser("~/pydaw/scripts"))

from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QApplication, QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton
from workspace import open_workspace_window  # Import the function from workspace.py
from config import WORKSPACES_DIR

app = QApplication(sys.argv)


def create_new_workspace():
    """Create a new workspace."""
    workspace_name, ok = QInputDialog.getText(None, "Create New Workspace", "Workspace Name:")
    if ok and workspace_name:
        workspace_path = os.path.join(WORKSPACES_DIR, workspace_name)
        try:
            os.makedirs(workspace_path, exist_ok=False)
            os.makedirs(os.path.join(workspace_path, "instruments"), exist_ok=True)

            # Create an empty manifest file
            manifest_data = {"tracks": [], "vst_plugins": [], "chuck_scripts": []}
            with open(os.path.join(workspace_path, "manifest.json"), "w") as f:
                json.dump(manifest_data, f, indent=4)

            open_workspace_window(workspace_name, workspace_path)
        except FileExistsError:
            QMessageBox.warning(None, "Error", f"Workspace '{workspace_name}' already exists.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"An error occurred while creating the workspace:\n{e}")


def open_workspace():
    """Open an existing workspace."""
    workspace_path = QFileDialog.getExistingDirectory(None, "Open Workspace", WORKSPACES_DIR)
    if workspace_path:
        workspace_name = os.path.basename(workspace_path)
        open_workspace_window(workspace_name, workspace_path)


class InstrumentManagementUI(QWidget):
    """Logic Pro-style instrument management UI."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instrument Management")
        self.setGeometry(300, 300, 800, 600)
        self.layout = QVBoxLayout()

        # Track list
        self.track_list = QListWidget()
        self.layout.addWidget(QLabel("Tracks"))
        self.layout.addWidget(self.track_list)

        # Add track button
        self.add_track_button = QPushButton("Add Track")
        self.add_track_button.clicked.connect(self.add_track)
        self.layout.addWidget(self.add_track_button)

        # MIDI keyboard input
        self.midi_input_label = QLabel("MIDI Keyboard Input")
        self.layout.addWidget(self.midi_input_label)

        # Music typing mode
        self.music_typing_button = QPushButton("Enable Music Typing")
        self.music_typing_button.clicked.connect(self.enable_music_typing)
        self.layout.addWidget(self.music_typing_button)

        self.setLayout(self.layout)

    def add_track(self):
        """Add a new track to the track list."""
        track_name, ok = QInputDialog.getText(self, "Add Track", "Track Name:")
        if ok and track_name:
            self.track_list.addItem(track_name)

    def enable_music_typing(self):
        """Enable music typing mode for note input."""
        QMessageBox.information(self, "Music Typing", "Music typing mode enabled.")