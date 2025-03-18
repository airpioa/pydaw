import sys
import os

# Add the parent directory of 'scripts' (which is '~/pydaw') to the Python path
sys.path.append(os.path.expanduser("~/pydaw"))
sys.path.append(os.path.expanduser("~/pydaw/scripts"))

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from ui import create_new_workspace, open_workspace  # Now it should work
from update import check_for_updates  # Import the update checking function

# Ensure scripts directory exists
SCRIPTS_DIR = os.path.expanduser("~/pydaw/scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

def main():
    # Check for updates on app start
    check_for_updates()  # Automatically check for updates when the app starts
    
    app = QApplication(sys.argv)
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
