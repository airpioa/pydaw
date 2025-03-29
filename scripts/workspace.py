import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QListWidget, QListWidgetItem,
                               QApplication, QMainWindow, QToolBar, QDockWidget, QLineEdit, QMenu, QFileDialog, QInputDialog, QMessageBox)
from chuck_handler import ChucKManager  # Import ChucKManager from chuck_handler.py


class ChucKConsole(QWidget):
    """A separate window for the ChucK console."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ChucK Console")
        self.setGeometry(300, 300, 600, 400)

        self.layout = QVBoxLayout()
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.layout.addWidget(self.console)
        self.setLayout(self.layout)

    def log_message(self, message):
        """Log a message to the console."""
        self.console.append(message)


class InstrumentLibrary(QWidget):
    """Instrument Library to display and load ChucK scripts."""
    def __init__(self, chuck_manager, instruments_dir="instruments", parent=None):
        super().__init__(parent)
        self.chuck_manager = chuck_manager
        self.instruments_dir = instruments_dir  # Directory to search for instruments
        self.setWindowTitle("Instrument Library")
        self.setGeometry(300, 300, 400, 600)

        self.layout = QVBoxLayout()
        self.instrument_list = QListWidget()
        self.load_instruments()
        self.layout.addWidget(self.instrument_list)

        self.load_button = QPushButton("Load Instrument")
        self.load_button.clicked.connect(self.load_selected_instrument)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)
        self.setStyleSheet("QWidget { background-color: #f0f0f0; }")

    def load_instruments(self):
        """Recursively load all .ck files from the instruments directory and its subdirectories."""
        self.instrument_list.clear()  # Clear the list before loading
        if not os.path.exists(self.instruments_dir):
            print(f"Error: Instruments directory '{self.instruments_dir}' does not exist.")
            return

        for root, _, files in os.walk(self.instruments_dir):
            for filename in files:
                if filename.endswith(".ck"):  # Only include .ck files
                    relative_path = os.path.relpath(os.path.join(root, filename), self.instruments_dir)
                    self.instrument_list.addItem(relative_path)

        if self.instrument_list.count() == 0:
            self.instrument_list.addItem("No instruments found.")

    def load_selected_instrument(self):
        """Load the selected instrument and run its ChucK script."""
        selected_item = self.instrument_list.currentItem()
        if selected_item:
            relative_path = selected_item.text()
            script_path = os.path.join(self.instruments_dir, relative_path)
            self.chuck_manager.run_script(script_path)


class Timeline(QWidget):
    """A basic timeline widget for the workspace."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Timeline")
        self.setGeometry(0, 0, 800, 100)
        self.setStyleSheet("QWidget { background-color: #e0e0e0; }")

        layout = QVBoxLayout()
        label = QLabel("Timeline Placeholder")
        layout.addWidget(label)
        self.setLayout(layout)


class WorkspaceWindow(QMainWindow):
    """Main workspace window for managing ChucK scripts and instruments."""
    def __init__(self, workspace_name="New Workspace", workspace_path=""):
        super().__init__()
        self.setWindowTitle(f"{workspace_name} - PyDAW")
        self.workspace_path = workspace_path  # Store the workspace path
        self.setGeometry(200, 200, 1000, 600)
        self.setWindowIcon(QIcon("icon.png"))

        # Initialize ChucKManager
        self.chuck_console_window = ChucKConsole()
        self.chuck_manager = ChucKManager(console=self.chuck_console_window.console)

        # Initialize tempo
        self.tempo = 120  # Default tempo

        # Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Add toolbar actions
        self.add_toolbar_actions()

        # Initialize windows
        self.instrument_library_window = InstrumentLibrary(self.chuck_manager, instruments_dir=os.path.join(self.workspace_path, "instruments"))
        self.timeline = Timeline()

        # Add dockable widgets
        self.add_dockable_widgets()

    def add_toolbar_actions(self):
        """Add actions to the toolbar."""
        # Tempo display and edit
        self.tempo_display = QLineEdit(f"Tempo: {self.tempo} BPM")
        self.tempo_display.setReadOnly(True)
        self.tempo_display.setFixedWidth(120)
        self.tempo_display.setStyleSheet("background-color: #f0f0f0;")
        self.toolbar.addWidget(self.tempo_display)

        # Views dropdown menu
        views_menu = QMenu("Views", self)
        toggle_timeline_action = QAction("Toggle Timeline", self)
        toggle_timeline_action.triggered.connect(self.toggle_timeline)
        views_menu.addAction(toggle_timeline_action)

        toggle_console_action = QAction("Toggle ChucK Console", self)
        toggle_console_action.triggered.connect(self.toggle_console)
        views_menu.addAction(toggle_console_action)

        toggle_instruments_action = QAction("Toggle Instrument Library", self)
        toggle_instruments_action.triggered.connect(self.toggle_instruments)
        views_menu.addAction(toggle_instruments_action)

        views_menu_action = self.toolbar.addAction("Views")
        views_menu_action.setMenu(views_menu)

    def add_dockable_widgets(self):
        """Add dockable widgets to the main window."""
        # Timeline
        self.timeline_dock = QDockWidget("Timeline", self)
        self.timeline_dock.setWidget(self.timeline)
        self.addDockWidget(Qt.TopDockWidgetArea, self.timeline_dock)

        # ChucK Console
        self.console_dock = QDockWidget("ChucK Console", self)
        self.console_dock.setWidget(self.chuck_console_window)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_dock)

        # Instrument Library
        self.instruments_dock = QDockWidget("Instrument Library", self)
        self.instruments_dock.setWidget(self.instrument_library_window)
        self.addDockWidget(Qt.RightDockWidgetArea, self.instruments_dock)

    def toggle_timeline(self):
        """Toggle the visibility of the timeline dock."""
        self.timeline_dock.setVisible(not self.timeline_dock.isVisible())

    def toggle_console(self):
        """Toggle the visibility of the ChucK console dock."""
        self.console_dock.setVisible(not self.console_dock.isVisible())

    def toggle_instruments(self):
        """Toggle the visibility of the instrument library dock."""
        self.instruments_dock.setVisible(not self.instruments_dock.isVisible())

    def closeEvent(self, event):
        """Handle the close event to stop ChucK scripts."""
        self.chuck_manager.stop_all_instruments()
        event.accept()


def open_workspace_window(workspace_name, workspace_path):
    """Open a new workspace window."""
    window = WorkspaceWindow(workspace_name, workspace_path)
    window.show()


def main():
    """Main entry point for the application."""
    # Use the existing QApplication instance if it exists
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # Prompt user to create or open a workspace
    choice, ok = QInputDialog.getItem(
        None,
        "Workspace",
        "Choose an option:",
        ["Create New Workspace", "Open Existing Workspace"],
        editable=False,
    )

    if ok and choice == "Create New Workspace":
        workspace_name, ok = QInputDialog.getText(None, "Create New Workspace", "Workspace Name:")
        if ok and workspace_name:
            workspace_path = os.path.expanduser(f"~/pydaw/workspaces/{workspace_name}")
            os.makedirs(workspace_path, exist_ok=True)
            open_workspace_window(workspace_name, workspace_path)
    elif ok and choice == "Open Existing Workspace":
        workspace_path = QFileDialog.getExistingDirectory(None, "Open Workspace", os.path.expanduser("~/pydaw/workspaces"))
        if workspace_path:
            workspace_name = os.path.basename(workspace_path)
            open_workspace_window(workspace_name, workspace_path)

    # Only call app.exec() if this script is run directly
    if __name__ == "__main__":
        sys.exit(app.exec())