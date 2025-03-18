from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QFileDialog, QMessageBox
from PySide6.QtGui import QIcon
import os
import json
from workspace import WorkspaceWindow
from config import WORKSPACES_DIR
from logger import logger

def create_new_workspace():
    workspace_name, ok = QInputDialog.getText(None, "Create New Workspace", "Workspace Name:")
    if ok and workspace_name:
        workspace_path = os.path.join(WORKSPACES_DIR, workspace_name)
        try:
            os.makedirs(workspace_path, exist_ok=False)
            os.makedirs(os.path.join(workspace_path, "instruments"), exist_ok=True)
            logger.info(f"Workspace '{workspace_name}' created at {workspace_path}")
            
            manifest_data = {"tracks": [], "vst_plugins": [], "chuck_scripts": []}
            with open(os.path.join(workspace_path, "manifest.json"), "w") as f:
                json.dump(manifest_data, f, indent=4)
            
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
