import os
import subprocess
import wave
import threading
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QToolBar, QLineEdit, QMenu, QListWidget,
    QVBoxLayout, QLabel, QWidget, QPushButton, QDialog, QSpinBox, QTextEdit, QSizePolicy, QSlider
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction, QMouseEvent
from chuck_handler import ChucKManager


class ChucKConsole(QTextEdit):
    """A dedicated console widget for displaying ChucK output."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas; font-size: 12px;")
        self.setPlaceholderText("ChucK Console Output...")

    def log(self, message):
        """Log a message to the console."""
        self.append(message)

    def log_error(self, error_message):
        """Log an error message to the console."""
        sanitized_error_message = html.escape(error_message)
        self.append(f"<span style='color: red;'>ERROR: {sanitized_error_message}</span>")

class InstrumentLibrary(QWidget):
    """Instrument Library to display and load ChucK scripts and play audio files."""
    def __init__(self, chuck_manager, workspace_instruments_dir, global_instruments_dir, console, parent=None):
        super().__init__(parent)
        self.chuck_manager = chuck_manager
        self.workspace_instruments_dir = os.path.expanduser(workspace_instruments_dir)
        self.global_instruments_dir = os.path.expanduser(global_instruments_dir)
        self.console = console  # Reference to the ChucK console
        self.setWindowTitle("Instrument Library")

        # Dictionary to track audio playback subprocesses
        self.audio_processes = {}

        self.layout = QVBoxLayout()
        self.instrument_list = QListWidget()
        self.load_instruments()
        self.layout.addWidget(self.instrument_list)

        self.load_button = QPushButton("Load Instrument")
        self.load_button.clicked.connect(self.load_selected_item)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)

    def load_instruments(self):
        """Load all .ck and audio files from both the workspace and global instruments directories."""
        self.instrument_list.clear()

        # Load instruments from the workspace directory
        if os.path.exists(self.workspace_instruments_dir):
            self._load_items_from_directory(self.workspace_instruments_dir, "Workspace")

        # Load instruments from the global directory
        if os.path.exists(self.global_instruments_dir):
            self._load_items_from_directory(self.global_instruments_dir, "Global")

        if self.instrument_list.count() == 0:
            self.instrument_list.addItem("No instruments or audio files found.")

    def _load_items_from_directory(self, directory, source_label):
        """Helper function to load .ck and audio files from a specific directory."""
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".ck") or filename.endswith((".wav", ".mp3", ".ogg")):
                    relative_path = os.path.relpath(os.path.join(root, filename), directory)
                    self.instrument_list.addItem(f"[{source_label}] {relative_path}")

    def load_selected_item(self):
        """Load the selected item and either run its ChucK script or play its audio file."""
        selected_item = self.instrument_list.currentItem()
        if selected_item:
            item_text = selected_item.text()
            if item_text.startswith("[Workspace]"):
                base_dir = self.workspace_instruments_dir
                relative_path = item_text.replace("[Workspace] ", "")
            elif item_text.startswith("[Global]"):
                base_dir = self.global_instruments_dir
                relative_path = item_text.replace("[Global] ", "")
            else:
                return

            file_path = os.path.join(base_dir, relative_path)

            if file_path.endswith(".ck"):
                # Run the ChucK script
                self.chuck_manager.run_script(file_path)
                self.console.log(f"Running ChucK script: {file_path}")
            elif file_path.endswith((".wav", ".mp3", ".ogg")):
                # Play the audio file
                self.play_audio(file_path)
                self.console.log(f"Playing audio file: {file_path}")

    def play_audio(self, file_path):
        """Play an audio file in a separate subprocess."""
        try:
            # Start a new subprocess to play the audio file using ffplay
            process = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", file_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Store the process in the dictionary
            self.audio_processes[file_path] = process
        except Exception as e:
            self.console.log_error(f"Error playing audio file {file_path}: {e}")


class ViewsWindow(QDialog):
    """Window to manage views."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Views")
        self.setGeometry(300, 300, 200, 150)

        self.layout = QVBoxLayout()
        self.console_button = QPushButton("Toggle Console")
        self.instrument_library_button = QPushButton("Toggle Instrument Library")
        self.timeline_button = QPushButton("Toggle Timeline")

        self.layout.addWidget(self.console_button)
        self.layout.addWidget(self.instrument_library_button)
        self.layout.addWidget(self.timeline_button)

        self.setLayout(self.layout)


class Timeline(QWidget):
    """A timeline widget for recording and mixing audio from ChucK scripts."""
    def __init__(self, chuck_manager, workspace_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Timeline")
        self.chuck_manager = chuck_manager
        self.workspace_path = workspace_path
        self.layout = QVBoxLayout()

        # Add a placeholder label
        self.label = QLabel("Timeline - Record and Mix Audio")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)


class TempoDialog(QDialog):
    """Dialog to change the tempo."""
    def __init__(self, current_tempo, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Tempo")
        self.setGeometry(300, 300, 200, 150)

        self.layout = QVBoxLayout()
        self.tempo_spinbox = QSpinBox()
        self.tempo_spinbox.setRange(20, 300)
        self.tempo_spinbox.setValue(current_tempo)
        self.layout.addWidget(QLabel("Set Tempo (BPM):"))
        self.layout.addWidget(self.tempo_spinbox)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_tempo)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def save_tempo(self):
        """Save the tempo and close the dialog."""
        self.accept()  # Close the dialog and mark it as accepted

    def get_tempo(self):
        """Return the selected tempo."""
        return self.tempo_spinbox.value()


class WorkspaceWindow(QMainWindow):
    """Main workspace window for managing ChucK scripts and instruments."""
    def __init__(self, workspace_name="New Workspace", workspace_path=""):
        super().__init__()
        self.setWindowTitle(f"{workspace_name} - PyDAW")
        self.workspace_path = workspace_path
        self.setGeometry(200, 200, 1000, 600)
        self.setWindowIcon(QIcon("icon.png"))

        # Initialize ChucKManager
        self.chuck_console = ChucKConsole()  # Separate ChucK console widget
        self.chuck_manager = ChucKManager(console=self.chuck_console)

        # Default tempo
        self.tempo = 120

        # Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Add toolbar actions
        self.add_toolbar_actions()

        # Dockable widgets
        self.add_dockable_widgets()

        # Last opened ChucK script
        self.last_opened_script = None

        # Set the main layout
        self.setCentralWidget(self.chuck_console)

    def add_toolbar_actions(self):
        """Add actions to the toolbar."""
        # Tempo display
        self.tempo_display = QLineEdit(f"Tempo: {self.tempo} BPM")
        self.tempo_display.setReadOnly(True)
        self.tempo_display.setFixedWidth(150)
        self.tempo_display.setStyleSheet("background-color: #f0f0f0;")

        # Ensure the tempo dialog opens when clicked
        self.tempo_display.mousePressEvent = self.open_tempo_dialog_event
        self.toolbar.addWidget(self.tempo_display)

        # Stop All Scripts button
        stop_all_action = QAction("Stop All Scripts", self)
        stop_all_action.triggered.connect(self.chuck_manager.stop_all_scripts)
        self.toolbar.addAction(stop_all_action)

        # Stop ChucK VM button
        stop_vm_action = QAction("Stop ChucK VM", self)
        stop_vm_action.triggered.connect(self.stop_chuck_vm)
        self.toolbar.addAction(stop_vm_action)

        # Stop Last Script button
        stop_script_action = QAction("Stop Last Script", self)
        stop_script_action.triggered.connect(self.stop_last_script)
        self.toolbar.addAction(stop_script_action)

        # Views button
        views_action = QAction("Views", self)
        views_action.triggered.connect(self.open_views_window)
        self.toolbar.addAction(views_action)

    def open_tempo_dialog_event(self, event: QMouseEvent):
        """Open the tempo dialog when the tempo display is clicked."""
        self.open_tempo_dialog()

    def open_tempo_dialog(self):
        """Open the tempo dialog to change the tempo."""
        dialog = TempoDialog(self.tempo, self)
        if dialog.exec():
            self.tempo = dialog.get_tempo()
            self.tempo_display.setText(f"Tempo: {self.tempo} BPM")

    def open_views_window(self):
        """Open the views window."""
        views_window = ViewsWindow(self)
        views_window.console_button.clicked.connect(self.toggle_console)
        views_window.instrument_library_button.clicked.connect(self.toggle_instruments)
        views_window.timeline_button.clicked.connect(self.toggle_timeline)
        views_window.exec()

    def stop_chuck_vm(self):
        """Stop the ChucK virtual machine."""
        self.chuck_manager.stop_vm()
        self.chuck_console.log("ChucK VM stopped.")

    def stop_last_script(self):
        """Stop the last opened ChucK script."""
        if self.last_opened_script:
            self.chuck_manager.stop_script(self.last_opened_script)

    def add_dockable_widgets(self):
        """Add dockable widgets to the main window."""
        # Console
        self.console_dock = QDockWidget("Console", self)
        self.console_dock.setWidget(self.chuck_console)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_dock)

        # Instrument Library
        self.instrument_library = InstrumentLibrary(
            self.chuck_manager,
            workspace_instruments_dir=os.path.join(self.workspace_path, "instruments"),
            global_instruments_dir="~/pydaw/instruments",
            console=self.chuck_console
        )
        self.instrument_library_dock = QDockWidget("Instrument Library", self)
        self.instrument_library_dock.setWidget(self.instrument_library)
        self.addDockWidget(Qt.RightDockWidgetArea, self.instrument_library_dock)

        # Timeline
        self.timeline = Timeline(self.chuck_manager, self.workspace_path)
        self.timeline_dock = QDockWidget("Timeline", self)
        self.timeline_dock.setWidget(self.timeline)
        self.addDockWidget(Qt.TopDockWidgetArea, self.timeline_dock)

    def toggle_console(self):
        """Toggle the visibility of the console dock."""
        self.console_dock.setVisible(not self.console_dock.isVisible())

    def toggle_instruments(self):
        """Toggle the visibility of the instrument library dock."""
        self.instrument_library_dock.setVisible(not self.instrument_library_dock.isVisible())

    def toggle_timeline(self):
        """Toggle the visibility of the timeline dock."""
        self.timeline_dock.setVisible(not self.timeline_dock.isVisible())


# Global variable to keep the WorkspaceWindow instance in scope
workspace_window = None


def open_workspace_window(workspace_name, workspace_path):
    """Open a new workspace window."""
    global workspace_window
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    workspace_window = WorkspaceWindow(workspace_name, workspace_path)
    workspace_window.show()