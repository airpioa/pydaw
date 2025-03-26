import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from ui import create_new_workspace, open_workspace  # Import workspace functions

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

def main():
    # Run the version update script as a subprocess
    #run_version_update_script()

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
    layout.addWidget(QPushButton("Create Workspace", clicked=create_new_workspace))
    layout.addWidget(QPushButton("Open Workspace", clicked=open_workspace))

    exit_button = QPushButton("Exit")
    exit_button.clicked.connect(app.quit)
    layout.addWidget(exit_button)

    main_window.setLayout(layout)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
