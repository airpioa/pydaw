import os
import json
import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                               QPushButton, QTextEdit, QListWidget, QListWidgetItem, QSplitter)
from PySide6.QtGui import QIcon
from chuck_handler import ChucKManager

workspace_instances = []  # Keep track of open workspaces

class InstrumentLibrary(QWidget):
    def __init__(self, chuck_manager):
        super().__init__()
        self.chuck_manager = chuck_manager
        self.setWindowTitle("Instrument Library")
        self.setGeometry(300, 300, 300, 600)
        
        self.layout = QVBoxLayout()
        self.instrument_list = QListWidget()
        self.load_instruments()
        self.layout.addWidget(self.instrument_list)

        self.load_button = QPushButton("Load Instrument")
        self.load_button.clicked.connect(self.load_selected_instrument)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)
    
    def load_instruments(self):
        instruments = [
            
        ]
        for instrument in instruments:
            item = QListWidgetItem(instrument)
            self.instrument_list.addItem(item)
    
    def load_selected_instrument(self):
        selected_item = self.instrument_list.currentItem()
        if selected_item:
            instrument_name = selected_item.text()
            chuck_script = f"~/pydaw/instruments{instrument_name}.ck"  # Replace with actual path
            self.chuck_manager.run_script(chuck_script)


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
