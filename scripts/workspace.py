import os
import json
import sys
from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                               QPushButton, QTextEdit, QListWidget, QListWidgetItem, QSplitter, QApplication)
from PySide6.QtGui import QIcon
from chuck_handler import ChucKManager

workspace_instances = []  # Keep track of open workspaces

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
            # Run the ChucK script using the ChucKManager instance
            self.chuck_manager.run_script(self.script_path)
            self.script_finished.emit(f"Finished running {self.script_path}")
        except Exception as e:
            self.script_finished.emit(f"Error running {self.script_path}: {e}")

class InstrumentLibrary(QWidget):
    def __init__(self, chuck_manager):
        super().__init__()
        self.chuck_manager = chuck_manager
        self.setWindowTitle("Instrument Library")
        self.setGeometry(300, 300, 300, 600)
        
        self.layout = QVBoxLayout()
        self.instrument_list = QListWidget()
        self.load_instruments()  # Dynamically load instruments
        self.layout.addWidget(self.instrument_list)

        self.load_button = QPushButton("Load Instrument")
        self.load_button.clicked.connect(self.load_selected_instrument)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)
    
    def load_instruments(self):
        instruments_folder = "~/pydaw/instruments"  # Define path to instruments folder
        instruments_folder = os.path.expanduser(instruments_folder)  # Expand ~ to user home directory

        # List all .ck files in the instruments folder (excluding config.status or any other irrelevant files)
        try:
            for filename in os.listdir(instruments_folder):
                if filename.endswith(".ck") and filename != "config.status":  # Filter out config.status
                    instrument_name = filename[:-3]  # Remove the .ck extension
                    item = QListWidgetItem(instrument_name)
                    self.instrument_list.addItem(item)
        except FileNotFoundError:
            print(f"Error: The instruments folder '{instruments_folder}' does not exist.")
    
    def load_selected_instrument(self):
        selected_item = self.instrument_list.currentItem()
        if selected_item:
            instrument_name = selected_item.text()
            chuck_script = os.path.expanduser(f"~/pydaw/instruments/{instrument_name}.ck")  # Correct path

            # Run the script in the background using a new thread
            self.chuck_thread = ChucKThread(self.chuck_manager, chuck_script)
            self.chuck_thread.start()

            # Optionally, connect a signal to display when the script finishes
            self.chuck_thread.script_finished.connect(self.handle_script_finished)

    def handle_script_finished(self, message):
        print(message)  # You can display this in the UI, log it, or perform other actions


class WorkspaceWindow(QWidget):
    def __init__(self, workspace_name="New Workspace", workspace_path=""):
        super().__init__()
        self.setWindowTitle(f"{workspace_name} - pydaw")
        self.setGeometry(200, 200, 1000, 600)
        self.workspace_path = workspace_path
        self.setWindowIcon(QIcon("icon.png"))

        self.layout = QVBoxLayout()
        
        # Toolbar with Return Button
        self.toolbar = QHBoxLayout()
        self.back_button = QPushButton("Return to Main Menu")
        self.back_button.clicked.connect(self.close)
        self.toolbar.addWidget(self.back_button)
        
        self.open_instrument_library_button = QPushButton("Open Instrument Library")
        self.open_instrument_library_button.clicked.connect(self.open_instrument_library)
        self.toolbar.addWidget(self.open_instrument_library_button)
        
        # Stop ChucK VM Button
        self.stop_chuck_button = QPushButton("Stop ChucK VM")
        self.stop_chuck_button.clicked.connect(self.stop_chuck_vm)
        self.toolbar.addWidget(self.stop_chuck_button)
        
        self.layout.addLayout(self.toolbar)
        
        # Splitter to separate timeline and console
        self.splitter = QSplitter()
        
        # Timeline Placeholder
        self.timeline_label = QLabel("Timeline")
        self.splitter.addWidget(self.timeline_label)
        
        # ChucK Console Window
        self.chuck_console = QTextEdit()
        self.chuck_console.setReadOnly(True)
        self.splitter.addWidget(self.chuck_console)
        
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)
        
        self.chuck_manager = ChucKManager(self.chuck_console)
        self.instrument_library = None
        
        # Load workspace contents
        self.load_workspace()
    
    def open_instrument_library(self):
        if not self.instrument_library:
            self.instrument_library = InstrumentLibrary(self.chuck_manager)
        self.instrument_library.show()

    def stop_chuck_vm(self):
        """Stop all running instruments (ChucK scripts)"""
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
    global workspace_instances
    window = WorkspaceWindow(workspace_name, workspace_path)
    workspace_instances.append(window)
    window.show()


# Main function to start the application
def main():
    app = QApplication(sys.argv)
    # Example workspace name and path, this can be dynamically chosen
    open_workspace_window("Sample Workspace", "~/pydaw/workspaces/sample_workspace")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
