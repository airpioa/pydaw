import sys
import os
import subprocess
import time
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from ui import create_new_workspace, open_workspace  # Import UI functions from ui.py

def run_version_update_script():
    """Run the version.py script to check for updates and update the version."""
    try:
        print("Running version update script...")
        subprocess.run(["python", os.path.expanduser("~/pydaw/version.py")], check=True)
        print("Version update completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running the version update script: {e}")

def relaunch_app():
    """Relaunch the application after updates."""
    try:
        print("Relaunching the application...")
        # Delay for a short moment to ensure all update operations finish
        time.sleep(2)

        # Relaunch the app using the same Python interpreter
        subprocess.Popen([sys.executable, os.path.abspath(__file__)])
        sys.exit()  # Exit the current instance of the app

    except Exception as e:
        print(f"Error during relaunch: {e}")

def main():
    # Step 1: Run the version update script to update the version if needed
    run_version_update_script()

    # Step 2: Relaunch the application after updating
    relaunch_app()

    # Step 3: Initialize QApplication and UI elements using ui.py
    app = QApplication(sys.argv)

    # Create the main window or show the main menu
    main_window = QWidget()
    main_window.setWindowTitle("PyDAW Main Menu")
    main_window.setGeometry(200, 200, 600, 400)
    main_window.setWindowIcon(QIcon("icon.png"))

    # Use the UI buttons for creating and opening workspaces
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
