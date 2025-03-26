import os
import json
import sys
import subprocess
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                               QPushButton, QTextEdit, QListWidget, QListWidgetItem, QSplitter, QApplication)
from PySide6.QtGui import QIcon


class ChucKManager:
    """Handles execution of ChucK scripts and stopping them."""
    
    def __init__(self, console: QTextEdit = None):
        self.console = console
        self.processes = []  # Store running ChucK processes

    def log_output(self, message):
        """Log messages to the console (if available)."""
        if self.console:
            self.console.append(message)

    def run_script(self, script_path):
        """Run a ChucK script and track the process."""
        try:
            self.log_output(f"Starting ChucK script: {script_path}")
            
            process = subprocess.Popen(
                ["chuck", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(process)

            while True:
                output = process.stdout.readline()
                if not output:
                    break
                self.log_output(output.strip())

            self.log_output(f"ChucK script finished: {script_path}")

        except Exception as e:
            self.log_output(f"Error running ChucK script: {e}")

    def stop_all_instruments(self):
        """Stops all running ChucK scripts."""
        if self.processes:
            self.log_output("Stopping all ChucK instruments...")
            for process in self.processes:
                process.terminate()
            self.processes.clear()
        else:
            self.log_output("No ChucK instruments running.")


class ChucKThread(QThread):
    """Thread to run ChucK scripts in the background."""
    script_finished = Signal(str)

    def __init__(self, chuck_manager, script_path):
        super().__init__()
        self.chuck_manager = chuck_manager
        self.script_path = script_path

    def run(self):
        """Run the ChucK script in the background."""
        try:
            self.chuck_manager.run_script(self.script_path)
            self.script_finished.emit(f"Finished running {self.script_path}")
        except Exception as e:
            self.script_finished.emit(f"Error running {self.script_path}: {e}")


class InstrumentLibrary(QWidget):
    """Loads and manages instrument selection from ~/pydaw/instruments."""

    def __init__(self, chuck_manager):
        super().__init__()
        self.chuck_manager = chuck_manager
        self.setWindowTitle("Instrument Library")
        self.setGeometry(300, 300, 300, 600)

        self.layout = QVBoxLayout()
        self.instrument_list = QListWidget()
        self.layout.addWidget(self.instrument_list)

        self.load_button = QPushButton("Load Instrument")
        self.load_button.clicked.connect(self.load_selected_instrument)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)
        self.load_instruments()

    def load_instruments(self):
        """Recursively scan ~/pydaw/instruments for .ck files and list them."""
        instruments_dir = os.path.expanduser("~/pydaw/instruments")
        self.instrument_list.clear()

        for root, _, files in os.walk(instruments_dir):
            for file in files:
                if file.endswith(".ck") and file != "config.status":
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, instruments_dir)
                    item = QListWidgetItem(relative_path)
                    item.setData(32, full_path)  # Store full path in UI
                    self.instrument_list.addItem(item)

    def load_selected_instrument(self):
        """Run the selected instrument."""
        selected_item = self.instrument_list.currentItem()
        if selected_item:
            instrument_path = selected_item.data(32)
            self.chuck_manager.run_script(instrument_path)


class WorkspaceWindow(QWidget):
    """Main workspace window for arranging audio and handling instruments."""

    def __init__(self, workspace_name="New Workspace", workspace_path=""):
        super().__init__()
        self.setWindowTitle(f"{workspace_name} - pydaw")
        self.setGeometry(200, 200, 1000, 600)
        self.workspace_path = workspace_path
        self.setWindowIcon(QIcon("icon.png"))

        self.layout = QVBoxLayout()

        # Toolbar
        self.toolbar = QHBoxLayout()
        self.back_button = QPushButton("Return to Main Menu")
        self.back_button.clicked.connect(self.close)
        self.toolbar.addWidget(self.back_button)

        self.open_instrument_library_button = QPushButton("Open Instrument Library")
        self.open_instrument_library_button.clicked.connect(self.open_instrument_library)
        self.toolbar.addWidget(self.open_instrument_library_button)

        self.stop_chuck_button = QPushButton("Stop ChucK VM")
        self.stop_chuck_button.clicked.connect(self.stop_chuck_vm)
        self.toolbar.addWidget(self.stop_chuck_button)

        self.layout.addLayout(self.toolbar)

        # Splitter
        self.splitter = QSplitter()
        self.timeline_label = QLabel("Timeline")
        self.splitter.addWidget(self.timeline_label)

        self.chuck_console = QTextEdit()
        self.chuck_console.setReadOnly(True)
        self.splitter.addWidget(self.chuck_console)

        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)

        self.chuck_manager = ChucKManager(self.chuck_console)
        self.instrument_library = None

        self.load_workspace()

    def open_instrument_library(self):
        """Opens the instrument library window."""
        if not self.instrument_library:
            self.instrument_library = InstrumentLibrary(self.chuck_manager)
        self.instrument_library.show()

    def stop_chuck_vm(self):
        """Stop all running ChucK scripts."""
        self.chuck_manager.stop_all_instruments()

    def load_workspace(self):
        manifest_path = os.path.join(self.workspace_path, "manifest.json")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                manifest_data = json.load(f)
            self.load_chuck_scripts(manifest_data)

    def load_chuck_scripts(self, manifest_data):
        if "chuck_scripts" in manifest_data:
            for script_path in manifest_data["chuck_scripts"]:
                self.chuck_manager.run_script(script_path)


def open_workspace_window(workspace_name, workspace_path):
    """Opens a new workspace window."""
    window = WorkspaceWindow(workspace_name, workspace_path)
    window.show()


# Main function to start the application
def main():
    app = QApplication(sys.argv)
    open_workspace_window("Sample Workspace", "~/pydaw/workspaces/sample_workspace")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
