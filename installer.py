import os
import subprocess
import sys
import shutil
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QDialog, QDialogButtonBox
from PySide6.QtCore import Qt, QThread, Signal

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
        self.install_button.clicked.connect(self.show_install_location_dialog)
        self.layout().addWidget(self.install_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.layout().addWidget(self.cancel_button)

    def show_install_location_dialog(self):
        self.dialog = InstallLocationDialog(self)
        self.dialog.accepted.connect(self.start_installation)
        self.dialog.show()

    def start_installation(self):
        self.install_button.setEnabled(False)
        self.log_window.append("Starting installation...")
        self.worker = InstallWorker(self.dialog.install_location.text())
        self.worker.log.connect(self.log_message)
        self.worker.done.connect(self.install_done)
        self.worker.start()

    def log_message(self, message):
        self.log_window.append(message)

    def install_done(self, success):
        if success:
            self.label.setText("Installation Complete!")
        else:
            self.label.setText("Installation Failed.")
        self.install_button.setEnabled(True)

class InstallLocationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Installation Location")
        self.setGeometry(400, 200, 400, 150)

        layout = QVBoxLayout()

        self.install_location_label = QLabel("Enter installation directory (auto installs to path/pydaw):")
        self.install_location = QLineEdit(self)
        self.install_location.setText(os.path.expanduser("~/"))
        layout.addWidget(self.install_location_label)
        layout.addWidget(self.install_location)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

class InstallWorker(QThread):
    log = Signal(str)
    done = Signal(bool)

    def __init__(self, install_location):
        super().__init__()
        self.install_location = install_location

    def run(self):
        try:
            self.log.emit("Checking dependencies...")

            # Install necessary package managers
            self.install_brew_or_winget()

            # Install dependencies
            self.install_git()
            self.install_python()
            self.clone_pydaw()
            self.install_requirements()

            # Create the .app and move it to Applications folder
            self.create_mac_app_bundle()

            # Cleanup temporary files
            self.cleanup()

            self.log.emit("Installation complete!")
            self.done.emit(True)
        except Exception as e:
            self.log.emit(f"Error: {e}")
            self.done.emit(False)

    def install_brew_or_winget(self):
        """Install Homebrew on macOS or Winget on Windows if missing."""
        if sys.platform == "darwin":
            if not self.is_installed("brew"):
                self.log.emit("Installing Homebrew...")
                subprocess.run(["/bin/bash", "-c", "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"], check=True)
                self.log.emit("Homebrew installed.")
        elif sys.platform == "win32":
            if not self.is_installed("winget"):
                self.log.emit("Winget is not installed. Please install it manually from the Microsoft Store.")
                return

    def install_git(self):
        """Ensure Git is installed."""
        if not self.is_installed("git"):
            self.log.emit("Installing Git...")
            if sys.platform == "darwin":
                subprocess.run(["brew", "install", "git"], check=True)
            elif sys.platform == "linux":
                subprocess.run(["sudo", "apt-get", "install", "-y", "git"], check=True)
            elif sys.platform == "win32":
                subprocess.run(["winget", "install", "--id", "Git.Git", "--silent"], check=True)
            self.log.emit("Git installed.")

    def install_python(self):
        """Ensure Python is installed."""
        if not self.is_installed("python3"):
            self.log.emit("Installing Python...")
            if sys.platform == "darwin":
                subprocess.run(["brew", "install", "python3"], check=True)
            elif sys.platform == "linux":
                subprocess.run(["sudo", "apt-get", "install", "-y", "python3"], check=True)
            elif sys.platform == "win32":
                subprocess.run(["winget", "install", "--id", "Python.Python.3", "--silent"], check=True)
            self.log.emit("Python installed.")

    def clone_pydaw(self):
        """Clone the PyDAW repository into the user-defined path/pydaw folder."""
        self.log.emit("Cloning PyDAW repository...")

        # Ensure the user-defined directory exists
        if not os.path.exists(self.install_location):
            os.makedirs(self.install_location)

        # Define the full path where PyDAW will be cloned
        pydaw_path = os.path.join(self.install_location, "pydaw")

        # Clone the repository into the pydaw directory
        subprocess.run(["git", "clone", "https://github.com/airpioa/pydaw.git", pydaw_path], check=True)
        self.log.emit("PyDAW cloned into path/pydaw.")

    def install_requirements(self):
        """Install the necessary Python requirements."""
        self.log.emit("Installing Python requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(self.install_location, "pydaw", "requirements.txt")], check=True)
        self.log.emit("Python requirements installed.")

    def create_mac_app_bundle(self):
        """Create a macOS .app bundle for easy launching and move it to Applications."""
        app_path = os.path.join(self.install_location, "PyDAW.app")
        if not os.path.exists(app_path):
            subprocess.run(["mkdir", "-p", app_path], check=True)
            # Create a setup.py script to package the .app using py2app
            setup_py = os.path.join(self.install_location, "setup.py")
            with open(setup_py, "w") as f:
                f.write(f"""
from setuptools import setup

APP = ['{os.path.join(self.install_location, 'pydaw', 'main.py')}']
DATA_FILES = []
OPTIONS = {{
    'argv_emulation': True,
    'packages': ['PySide6'],
}}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={{'py2app': OPTIONS}},
    setup_requires=['py2app'],
)
                """)

            # Run py2app to create the .app
            subprocess.run([sys.executable, setup_py, "py2app"], check=True)

            # Move the .app to the Applications folder
            applications_folder = "/Applications"
            if not os.path.exists(applications_folder):
                os.makedirs(applications_folder)

            app_name = "PyDAW.app"
            target_path = os.path.join(applications_folder, app_name)

            # Move the app
            shutil.move(app_path, target_path)
            self.log.emit(f"App successfully moved to {target_path}.")

    def cleanup(self):
        """Clean up temporary files."""
        pass

    def is_installed(self, package_name):
        """Check if a package is installed."""
        try:
            subprocess.run([package_name, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstallerUI()
    window.show()
    sys.exit(app.exec())
