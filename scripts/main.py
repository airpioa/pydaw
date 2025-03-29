import sys
import os
import subprocess
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from wsui import main as start_wsui  # Import the main function from wsui.py
from config import SETTINGS_FILE

# Ensure scripts directory exists
SCRIPTS_DIR = os.path.expanduser("~/pydaw/scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)


def run_version_update_script():
    """Run the version.py script to update the version if needed."""
    try:
        print("Running version update script...")
        subprocess.run(["python", os.path.expanduser("~/pydaw/scripts/version.py")], check=True)
        print("Version update script completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running version update script: {e}")


def setup_auto_updates():
    """Prompt the user to enable auto-updates on the first start."""
    if not os.path.exists(SETTINGS_FILE):
        config = {}
    else:
        with open(SETTINGS_FILE, "r") as f:
            config = json.load(f)

    # Check if auto-update is already enabled
    if not config.get("auto_update_enabled", False):
        # Prompt the user to enable auto-updates
        app = QApplication.instance() or QApplication(sys.argv)
        response = QMessageBox.question(
            None,
            "Enable Auto-Updates",
            "Would you like to enable automatic updates for PyDAW?",
            QMessageBox.Yes | QMessageBox.No
        )

        if response == QMessageBox.Yes:
            config["auto_update_enabled"] = True
            with open(SETTINGS_FILE, "w") as f:
                json.dump(config, f, indent=4)
            QMessageBox.information(None, "Auto-Updates Enabled", "Automatic updates have been enabled.")
        else:
            config["auto_update_enabled"] = False
            with open(SETTINGS_FILE, "w") as f:
                json.dump(config, f, indent=4)
            QMessageBox.information(None, "Auto-Updates Disabled", "Automatic updates have been disabled.")

    return config.get("auto_update_enabled", False)


def main():
    # Prompt the user to set up auto-updates on the first start
    auto_updates_enabled = setup_auto_updates()

    # Run the version update script if auto-updates are enabled
    if auto_updates_enabled:
        run_version_update_script()

    # Ensure QApplication is created only once
    app = QApplication.instance()
    if not app:  # If QApplication instance doesn't exist, create one
        app = QApplication(sys.argv)

    # Now it's safe to create the main window
    main_window = QWidget()
    main_window.setWindowTitle("PyDAW Main Menu")
    main_window.setGeometry(200, 200, 600, 400)
    main_window.setWindowIcon(QIcon("icon.png"))

    layout = QVBoxLayout()

    # Add a button to start PyDAW workspaces
    start_button = QPushButton("Start PyDAW Workspace")
    start_button.clicked.connect(start_wsui)  # Call the main function from wsui.py
    layout.addWidget(start_button)

    # Add an exit button
    exit_button = QPushButton("Exit")
    exit_button.clicked.connect(app.quit)
    layout.addWidget(exit_button)

    main_window.setLayout(layout)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()