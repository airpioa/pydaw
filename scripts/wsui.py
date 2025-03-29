import os
import json
import sys
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox, QApplication
from workspace import open_workspace_window  # Import the function from workspace.py

# Detect custom installation paths
DEFAULT_WORKSPACES_DIR = os.path.expanduser("~/pydaw/")
CUSTOM_INSTALL_PATH = os.getenv("PYDAW_CUSTOM_PATH", DEFAULT_WORKSPACES_DIR)
WORKSPACES_DIR = os.path.join(CUSTOM_INSTALL_PATH, "workspaces")
os.makedirs(WORKSPACES_DIR, exist_ok=True)  # Ensure the workspaces directory exists


def create_new_workspace():
    """Create a new workspace."""
    workspace_name, ok = QInputDialog.getText(None, "Create New Workspace", "Workspace Name:")
    if ok and workspace_name:
        workspace_path = os.path.join(WORKSPACES_DIR, workspace_name)
        try:
            # Create the workspace directory and subdirectories
            os.makedirs(workspace_path, exist_ok=False)
            os.makedirs(os.path.join(workspace_path, "instruments"), exist_ok=True)

            # Create an empty manifest file
            manifest_data = {"tracks": [], "vst_plugins": [], "chuck_scripts": []}
            with open(os.path.join(workspace_path, "manifest.json"), "w") as f:
                json.dump(manifest_data, f, indent=4)

            # Open the newly created workspace
            open_workspace_window(workspace_name, workspace_path)
        except FileExistsError:
            QMessageBox.warning(None, "Error", f"Workspace '{workspace_name}' already exists.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"An error occurred while creating the workspace:\n{e}")


def open_existing_workspace():
    """Open an existing workspace."""
    workspace_path = QFileDialog.getExistingDirectory(None, "Open Workspace", WORKSPACES_DIR)
    if workspace_path:
        workspace_name = os.path.basename(workspace_path)
        open_workspace_window(workspace_name, workspace_path)


def main():
    """Main entry point for the UI."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # Prompt the user to create or open a workspace
    choice, ok = QInputDialog.getItem(
        None,
        "Workspace",
        "Choose an option:",
        ["Create New Workspace", "Open Existing Workspace"],
        editable=False,
    )

    if ok and choice == "Create New Workspace":
        create_new_workspace()
    elif ok and choice == "Open Existing Workspace":
        open_existing_workspace()

    # Only call app.exec() if this script is run directly
    if __name__ == "__main__":
        sys.exit(app.exec())