import os
import json
import sys

sys.path.append(os.path.expanduser("~/pydaw"))
sys.path.append(os.path.expanduser("~/pydaw/scripts"))


from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QApplication
from workspace import open_workspace_window
from config import WORKSPACES_DIR

app = QApplication(sys.argv)


def create_new_workspace():
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
    workspace_path = QFileDialog.getExistingDirectory(None, "Open Workspace", WORKSPACES_DIR)
    if workspace_path:
        workspace_name = os.path.basename(workspace_path)
        open_workspace_window(workspace_name, workspace_path)
