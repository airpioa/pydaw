import os
import shutil
import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt

class UninstallerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyDAW Uninstaller")
        self.setGeometry(400, 200, 400, 200)
        self.setLayout(QVBoxLayout())

        self.label = QLabel("Are you sure you want to uninstall PyDAW? This will remove all files.")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label)

        self.uninstall_button = QPushButton("Uninstall")
        self.uninstall_button.clicked.connect(self.confirm_uninstall)
        self.layout().addWidget(self.uninstall_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.layout().addWidget(self.cancel_button)

    def confirm_uninstall(self):
        """Confirm uninstallation and show warning."""
        reply = QMessageBox.warning(self, "Warning", "This will remove all PyDAW files. Proceed?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.uninstall_pydaw()

    def uninstall_pydaw(self):
        """Remove PyDAW files."""
        install_dir = os.path.expanduser("~/PyDAW")
        if os.path.exists(install_dir):
            shutil.rmtree(install_dir)
            self.label.setText("PyDAW has been uninstalled.")
        else:
            self.label.setText("PyDAW is not installed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UninstallerUI()
    window.show()
    sys.exit(app.exec())
