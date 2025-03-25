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

        self.install_location_label = QLabel("Enter installation directory (auto installes to path/pydaw):")
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
            
            # Create shortcuts (macOS - .app package, Windows - start menu shortcut)
            self.create_shortcut()

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
                subprocess.run(["sudo", "apt-get", "install", "-y", "python3", "python3-pip"], check=True)
            elif sys.platform == "win32":
                subprocess.run(["winget", "install", "--id", "Python.Python.3", "--silent"], check=True)
            self.log.emit("Python installed.")

    def is_installed(self, command):
        """Check if a command is installed."""
        try:
            subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except Exception:
            return False

    def clone_pydaw(self):
        """Clone PyDAW repository."""
        self.log.emit("Cloning PyDAW...")
        self.temp_dir = "/tmp/pydaw" if sys.platform != "win32" else os.path.join(os.environ["TEMP"], "pydaw")
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/airpioa/pydaw.git", self.temp_dir], check=True)
        if os.path.exists(self.temp_dir):
            self.log.emit("PyDAW installed.")

    def install_requirements(self):
        """Install dependencies from requirements.txt."""
        self.log.emit("Installing dependencies...")
        requirements_file = os.path.join(self.temp_dir, "requirements.txt")

        if os.path.exists(requirements_file):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)
            self.log.emit("Dependencies installed.")
        else:
            self.log.emit("No requirements.txt found. Skipping dependencies.")

    def create_shortcut(self):
        """Create shortcuts in Start Menu (Windows) or Applications (macOS)."""
        self.log.emit("Creating application shortcut...")

        os.makedirs(self.install_location, exist_ok=True)
        shutil.move(self.temp_dir, self.install_location)

        if sys.platform == "win32":
            shortcut_path = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\PyDAW.lnk")
            command = f'powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut(\'{shortcut_path}\');$s.TargetPath=\'{self.install_location}\\main.py\';$s.Save()"'
            subprocess.run(command, shell=True, check=True)
            self.log.emit("Shortcut created in Start Menu.")
             
        else:
            shortcut_path = os.path.expanduser("~/Desktop/PyDAW.desktop")
            with open(shortcut_path, "w") as f:
                f.write(f"[Desktop Entry]\nName=PyDAW\nExec=python3 {self.install_location}/main.py\nType=Application\nIcon={self.install_location}/icon.png\n")
            subprocess.run(["chmod", "+x", shortcut_path])
            self.log.emit("Shortcut created on Desktop.")

    def cleanup(self):
        """Remove temporary installation files."""
        if os.path.exists(self.temp_dir):
            self.log.emit("Cleaning up temporary files...")
            try:
                shutil.rmtree(self.temp_dir)
                self.log.emit("Temporary files removed.")
            except Exception as e:
                self.log.emit(f"Failed to remove temp files: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstallerUI()
    window.show()
    sys.exit(app.exec())
