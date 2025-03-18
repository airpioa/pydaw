import sys
import os

# Add the full path to the 'scripts' directory in ~/pydaw
sys.path.append(os.path.expanduser("~/pydaw/scripts"))

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from ui import create_new_workspace, open_workspace  # Now it should work
from update import check_for_updates  # Import the update checking function
from version import increment_version  # Import the version management function

# Ensure scripts directory exists
SCRIPTS_DIR = os.path.expanduser("~/pydaw/scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

def main():
    # Increment version automatically at startup
    current_version = increment_version()  # Increment the version on app startup
    print(f"App Version: {current_version}")

    # Check for updates on app start
    check_for_updates()  # Automatically check for updates when the app starts
    
    # Create the QApplication instance before any QWidget
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
