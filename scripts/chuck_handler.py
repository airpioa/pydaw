import os
import subprocess
import sys
import shutil
import platform
import urllib.request
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt, QThread, Signal

PYDAW_REPO = "https://github.com/airpioa/pydaw.git"
ICON_URL = "https://raw.githubusercontent.com/airpioa/pydaw/main/icon.png"  # URL for icon

class InstallerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyDAW Installer")
        self.setGeometry(400, 200, 500, 300)
        self.setLayout(QVBoxLayout())

        self.label = QLabel("Welcome to the PyDAW Installer")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label)

        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.layout().addWidget(self.log_window)

        self.install_button = QPushButton("Install PyDAW")
        self.install_button.clicked.connect(self.start_installation)
        self.layout().addWidget(self.install_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.layout().addWidget(self.cancel_button)

    def start_installation(self):
        self.install_button.setEnabled(False)
        self.log_window.append("Starting installation...")
        self.worker = InstallWorker()
        self.worker.log.connect(self.log_message)
        self.worker.done.connect(self.install_done)
        self.worker.start()

    def log_message(self, message):
        self.log_window.append(message)

    def install_done(self, success):
        self.install_button.setEnabled(True)
        self.label.setText("Installation Complete!" if success else "Installation Failed.")

class InstallWorker(QThread):
    log = Signal(str)
    done = Signal(bool)

    def __init__(self):
        super().__init__()
        self.install_location = os.path.expanduser("~/")  # Move installation to home directory

    def run(self):
        try:
            self.log.emit("Starting installation process...")

            # Step 1: Clone the PyDAW repository
            self.clone_pydaw_repo()

            # Step 2: Install necessary dependencies
            self.install_requirements()

            # Step 3: Download the app icon
            self.download_icon()

            # Step 4: Move the app and icon to the correct directory (~/pydaw)
            self.move_files()

            self.log.emit("Installation complete!")
            self.done.emit(True)

        except Exception as e:
            self.log.emit(f"Error during installation: {e}")
            self.done.emit(False)

    def clone_pydaw_repo(self):
        """Clone the PyDAW repository."""
        self.log.emit("Cloning PyDAW repository...")
        subprocess.run(["git", "clone", PYDAW_REPO, self.install_location], check=True)
        self.log.emit("PyDAW repository cloned.")

    def install_requirements(self):
        """Install the required Python dependencies."""
        self.log.emit("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(self.install_location, "requirements.txt")], check=True)
        self.log.emit("Dependencies installed.")

    def download_icon(self):
        """Download the app icon."""
        self.log.emit("Downloading icon...")
        icon_path = os.path.join(self.install_location, "icon.png")
        urllib.request.urlretrieve(ICON_URL, icon_path)
        self.log.emit("Icon downloaded.")

    def move_files(self):
        """Move files to the proper location (user's home directory ~/)."""
        self.log.emit(f"Moving files to {self.install_location}...")
        
        # Move the cloned PyDAW repo into the user's home directory
        home_dir = os.path.expanduser("~")
        if not os.path.exists(self.install_location):
            shutil.move(self.install_location, home_dir)
            self.log.emit(f"Moved PyDAW to {home_dir}")

        self.log.emit("Files moved successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    installer_ui = InstallerUI()
    installer_ui.show()
    sys.exit(app.exec())
