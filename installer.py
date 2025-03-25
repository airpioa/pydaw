import os
import subprocess
import sys

def install_pyside6():
    """Ensure PySide6 is installed before running the UI."""
    try:
        import PySide6  # Try to import PySide6
    except ImportError:
        print("[INSTALLER] PySide6 not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PySide6"], check=True)
        print("[INSTALLER] PySide6 installed.")

# Install PySide6 first
install_pyside6()

# Now import PySide6 and launch UI
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QProgressBar
from PySide6.QtCore import Qt, QThread, Signal

# Define the UI after ensuring PySide6 is installed
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
        if success:
            self.label.setText("Installation Complete!")
        else:
            self.label.setText("Installation Failed.")
        self.install_button.setEnabled(True)

class InstallWorker(QThread):
    log = Signal(str)
    done = Signal(bool)

    def run(self):
        try:
            self.log.emit("Checking dependencies...")

            # Install Python, Git, and requirements
            self.install_python()
            self.install_git()
            self.clone_pydaw()
            self.install_requirements()

            self.log.emit("Installation complete!")
            self.done.emit(True)
        except Exception as e:
            self.log.emit(f"Error: {e}")
            self.done.emit(False)

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
        temp_dir = "/tmp/pydaw" if sys.platform != "win32" else os.path.join(os.environ["TEMP"], "pydaw")
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/airpioa/pydaw.git", temp_dir], check=True)
        if os.path.exists(temp_dir):
            self.log.emit("PyDAW installed.")

    def install_requirements(self):
        """Install dependencies from requirements.txt."""
        self.log.emit("Installing dependencies...")
        temp_dir = "/tmp/pydaw" if sys.platform != "win32" else os.path.join(os.environ["TEMP"], "pydaw")
        requirements_file = os.path.join(temp_dir, "requirements.txt")

        if os.path.exists(requirements_file):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)
            self.log.emit("Dependencies installed.")
        else:
            self.log.emit("No requirements.txt found. Skipping dependencies.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstallerUI()
    window.show()
    sys.exit(app.exec())
