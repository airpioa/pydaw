import os
import subprocess
import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                               QLineEdit, QTextEdit, QDialog, QDialogButtonBox, QMessageBox)
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
        if self.dialog.exec() == QDialog.Accepted:
            install_location = self.dialog.install_location.text()
            self.check_existing_install(install_location)

    def check_existing_install(self, install_location):
        """Check if PyDAW is already installed and prompt for update."""
        pydaw_path = os.path.join(install_location, "pydaw")

        if os.path.exists(pydaw_path):
            reply = QMessageBox.question(
                self, "Update PyDAW",
                "PyDAW is already installed. Do you want to update it?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                self.log_window.append("Installation canceled.")
                return

            self.log_window.append("Updating PyDAW...")

        self.start_installation(install_location)

    def start_installation(self, install_location):
        self.install_button.setEnabled(False)
        self.log_window.append("Starting installation...")
        self.worker = InstallWorker(install_location)
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
            self.install_git()
            self.install_python()
            self.clone_or_update_pydaw()
            self.install_requirements()
            self.cleanup()
            self.log.emit("Installation complete!")
            self.done.emit(True)
        except Exception as e:
            self.log.emit(f"Error: {e}")
            self.done.emit(False)

    def install_git(self):
        if not self.is_installed("git"):
            self.log.emit("Installing Git...")
            subprocess.run(["brew", "install", "git"], check=True)
            self.log.emit("Git installed.")

    def install_python(self):
        if not self.is_installed("python3"):
            self.log.emit("Installing Python...")
            subprocess.run(["brew", "install", "python3"], check=True)
            self.log.emit("Python installed.")

    def clone_or_update_pydaw(self):
        pydaw_path = os.path.join(self.install_location, "pydaw")

        if os.path.exists(pydaw_path):
            self.log.emit("Updating PyDAW...")
            subprocess.run(["git", "-C", pydaw_path, "pull"], check=True)
            self.log.emit("PyDAW has been updated.")
            return

        self.log.emit("Cloning PyDAW repository...")
        subprocess.run(["git", "clone", "https://github.com/airpioa/pydaw.git", pydaw_path], check=True)
        self.log.emit("PyDAW cloned into path/pydaw.")

    def install_requirements(self):
        self.log.emit("Installing Python requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r",
                        os.path.join(self.install_location, "pydaw", "requirements.txt")], check=True)
        self.log.emit("Python requirements installed.")

    def cleanup(self):
        pass

    def is_installed(self, package_name):
        try:
            subprocess.run([package_name, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InstallerUI()
    window.show()
    sys.exit(app.exec())
