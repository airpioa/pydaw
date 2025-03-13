import pygame
import pygame.freetype
import os
import json
import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog  # Import PyQt6 for file dialogs
import rtmidi  # Import python-rtmidi to handle MIDI input

# Initialize Pygame
pygame.init()

# Constants for window size and configurations
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 30
PDAW_DIR = os.path.expanduser("~/pydaw")
WORKSPACE_DIR = os.path.join(PDAW_DIR, "workspaces")
SAMPLES_DIR = os.path.join(PDAW_DIR, "samples")
OUTPUT_DIR = os.path.join(PDAW_DIR, "output")
SETTINGS_FILE = os.path.join(PDAW_DIR, "pydawsettings.json")

# Ensure necessary directories exist
os.makedirs(WORKSPACE_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize user settings if they don't exist
if not os.path.exists(SETTINGS_FILE):
    user_settings = {
        "user_metadata": {
            "name": "",
            "email": ""
        }
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(user_settings, f, indent=4)

# Load settings
with open(SETTINGS_FILE, "r") as f:
    settings = json.load(f)
user_metadata = settings["user_metadata"]

# Colors for UI
BACKGROUND_COLOR = (36, 36, 36)
BUTTON_COLOR = (80, 80, 80)
BUTTON_HOVER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)

# Fonts
font = pygame.freetype.SysFont("Arial", 24)
small_font = pygame.freetype.SysFont("Arial", 18)

# Project data structure
project_data = {
    "name": "New Project",
    "tracks": [],
    "settings": {},
    "sample_pack": [],
    "user_metadata": user_metadata
}

# MIDI Input Setup (Using python-rtmidi)
midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()

if available_ports:
    midi_in.open_port(0)  # Open the first available MIDI input port
else:
    midi_in.open_virtual_port("pydaw")  # Set the virtual port name to "pydaw"

# Sample Pack storage
sample_pack = []

# PyQt6 File Dialog Functions
def custom_file_dialog(folder_path, title="Select File"):
    app = QApplication(sys.argv)
    file_dialog = QFileDialog()
    file_dialog.setDirectory(folder_path)
    file_dialog.setWindowTitle(title)
    file_path, _ = file_dialog.getOpenFileName()
    return file_path

def custom_directory_dialog(folder_path, title="Select Directory"):
    app = QApplication(sys.argv)
    file_dialog = QFileDialog()
    file_dialog.setDirectory(folder_path)
    file_dialog.setWindowTitle(title)
    folder_path = file_dialog.getExistingDirectory()
    return folder_path

# Save project function
def save_project():
    file_path = custom_file_dialog(WORKSPACE_DIR, "Save Project")
    if file_path:
        with open(file_path, "w") as file:
            json.dump(project_data, file, indent=4)
        print(f"Project saved as {file_path}")

# Load project function
def load_project():
    file_path = custom_file_dialog(WORKSPACE_DIR, "Load Project")
    if file_path:
        with open(file_path, "r") as file:
            global project_data
            project_data = json.load(file)
        print(f"Project loaded from {file_path}")

# Load sample pack function
def load_sample_pack():
    file_paths = custom_file_dialog(SAMPLES_DIR, "Load Sample Pack")
    if file_paths:
        global sample_pack
        sample_pack = [file_paths]
        project_data["sample_pack"] = sample_pack
        print(f"Loaded sample pack with {len(sample_pack)} samples.")

# Create a new project
def new_project():
    app = QApplication(sys.argv)
    project_name, ok = QInputDialog.getText(None, "New Project", "Enter a name for your project:")
    if ok and project_name:
        global project_data
        project_data = {
            "name": project_name,
            "tracks": [],
            "settings": {},
            "sample_pack": [],
            "user_metadata": user_metadata
        }
    print(f"Created a new project: {project_name}")

# Function to draw GUI
def draw_gui(screen_width, screen_height):
    screen.fill(BACKGROUND_COLOR)  # Dark background
    
    # Top bar (title and controls)
    pygame.draw.rect(screen, (25, 25, 25), (0, 0, screen_width, 40))
    font.render_to(screen, (20, 10), f"{project_data['name']}", TEXT_COLOR)
    font.render_to(screen, (screen_width - 150, 10), "New", TEXT_COLOR)
    font.render_to(screen, (screen_width - 100, 10), "Open", TEXT_COLOR)
    font.render_to(screen, (screen_width - 50, 10), "Save", TEXT_COLOR)

    # Sidebar
    pygame.draw.rect(screen, BUTTON_COLOR, (0, 40, 200, screen_height - 40))
    small_font.render_to(screen, (10, 60), "Tracks", TEXT_COLOR)
    small_font.render_to(screen, (10, 100), "Add Track", TEXT_COLOR)
    small_font.render_to(screen, (10, 140), "Settings", TEXT_COLOR)
    small_font.render_to(screen, (10, 180), "Load Sample Pack", TEXT_COLOR)

    # Main workspace
    pygame.draw.rect(screen, (45, 45, 45), (200, 40, screen_width - 200, screen_height - 40))
    small_font.render_to(screen, (210, 50), "Workspace", TEXT_COLOR)

    # Draw buttons
    draw_button(screen, "New Project", (250, 100), 200, 50)
    draw_button(screen, "Save Project", (250, 160), 200, 50)
    draw_button(screen, "Open File", (250, 220), 200, 50)
    draw_button(screen, "Load Sample Pack", (250, 280), 200, 50)

    pygame.display.update()

# Function to draw buttons
def draw_button(surface, text, rect, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(rect[0], rect[1], width, height)

    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(surface, color, button_rect)
    small_font.render_to(surface, (rect[0] + 10, rect[1] + 10), text, TEXT_COLOR)

# Event handler
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            global SCREEN_WIDTH, SCREEN_HEIGHT
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if SCREEN_WIDTH - 150 <= mouse_x <= SCREEN_WIDTH and 0 <= mouse_y <= 40:
                new_project()
            if SCREEN_WIDTH - 100 <= mouse_x <= SCREEN_WIDTH and 0 <= mouse_y <= 40:
                load_project()
            if SCREEN_WIDTH - 50 <= mouse_x <= SCREEN_WIDTH and 0 <= mouse_y <= 40:
                save_project()

# Main loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("pydaw")
clock = pygame.time.Clock()

while True:
    handle_events()
    draw_gui(SCREEN_WIDTH, SCREEN_HEIGHT)
    clock.tick(FPS)
