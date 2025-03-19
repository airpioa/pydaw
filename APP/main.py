import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from ui import create_new_workspace, open_workspace  # Now it should work
from version import update_version_if_needed  # Import the version management function

# Ensure scripts directory exists
SCRIPTS_DIR = os.path.expanduser("~/pydaw/scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

def main():
    # Check for updates and update the version if needed
    if update_version_if_needed():
        print("Version updated successfully.")

    # Ensure QApplication is created only once
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

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
