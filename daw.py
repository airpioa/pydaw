import pygame
import pygame.freetype
import os
import json
import sys
import easygui  # Import easygui for file dialogs
import rtmidi  # Import python-rtmidi to handle MIDI input

# Initialize Pygame
pygame.init()

# Constants for window size and other configurations
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 30
PDAW_DIR = os.path.expanduser("~/pydaw")
WORKSPACE_DIR = os.path.join(PDAW_DIR, "workspaces")
SAMPLES_DIR = os.path.join(PDAW_DIR, "samples")
OUTPUT_DIR = os.path.join(PDAW_DIR, "output")
SETTINGS_FILE = os.path.join(PDAW_DIR, "pydawsettings.json")

# Ensure the necessary directories exist
os.makedirs(WORKSPACE_DIR, exist_ok=True)
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize user settings (if they don't exist)
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

# Colors for the UI
BACKGROUND_COLOR = (36, 36, 36)
BUTTON_COLOR = (80, 80, 80)
BUTTON_HOVER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 165, 0)

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

# MIDI Input Setup (Using python-rtmidi instead of pygame.midi)
midi_in = rtmidi.MidiIn()
available_ports = midi_in.get_ports()

if available_ports:
    midi_in.open_port(0)  # Open the first available MIDI input port
else:
    midi_in.open_virtual_port("My Virtual Input")

# Sample Pack setup (store paths to loaded samples)
sample_pack = []

# Function to handle custom file dialogs using easygui
def custom_file_dialog(folder_path, title="Select File"):
    file_path = easygui.fileopenbox(msg=title, default=folder_path)
    return file_path

def custom_directory_dialog(folder_path, title="Select Directory"):
    dir_path = easygui.diropenbox(msg=title, default=folder_path)
    return dir_path

# Function to save the current project to a .pydaw file
def save_project():
    file_path = custom_file_dialog(WORKSPACE_DIR, "Save Project")
    if file_path:
        with open(file_path, "w") as file:
            json.dump(project_data, file, indent=4)
        print(f"Project saved as {file_path}")

# Function to load a project from a .pydaw file
def load_project():
    file_path = custom_file_dialog(WORKSPACE_DIR, "Load Project")
    if file_path:
        with open(file_path, "r") as file:
            global project_data
            project_data = json.load(file)
        print(f"Project loaded from {file_path}")

# Function to load a sample pack
def load_sample_pack():
    file_paths = easygui.fileopenbox(msg="Load Sample Pack", default=SAMPLES_DIR, filetypes=["*.wav", "*.mp3"], multiple=True)
    if file_paths:
        global sample_pack
        sample_pack = list(file_paths)
        project_data["sample_pack"] = sample_pack
        print(f"Loaded sample pack with {len(sample_pack)} samples.")

# Function to create a new project and ask for the project name
def new_project():
    project_name = easygui.enterbox(msg="Enter a name for your project:")
    if project_name:
        global project_data
        project_data = {
            "name": project_name,
            "tracks": [],
            "settings": {},
            "sample_pack": [],
            "user_metadata": user_metadata
        }
    print("Created a new project!")

# Function to show How-To guide when DAW is opened
def show_how_to():
    easygui.textbox(msg="How-To Guide", text="1. Create a new project or open an existing one.\n2. Add tracks and load sample packs.\n3. Use the EQ, automation, and effects features.\n4. Save and export your project to WAV, MP3, or other formats.")

# Function to draw the GUI components
def draw_gui(screen_width, screen_height):
    screen.fill(BACKGROUND_COLOR)  # Dark background
    
    # Draw top bar (project title and controls)
    pygame.draw.rect(screen, (25, 25, 25), (0, 0, screen_width, 40))  # Top bar background
    font.render_to(screen, (20, 10), f"{project_data['name']}", TEXT_COLOR)
    font.render_to(screen, (screen_width - 150, 10), "New", TEXT_COLOR)
    font.render_to(screen, (screen_width - 100, 10), "Open", TEXT_COLOR)
    font.render_to(screen, (screen_width - 50, 10), "Save", TEXT_COLOR)

    # Draw Sidebar (left side of the screen)
    pygame.draw.rect(screen, BUTTON_COLOR, (0, 40, 200, screen_height - 40))  # Sidebar background
    small_font.render_to(screen, (10, 60), "Tracks", TEXT_COLOR)
    small_font.render_to(screen, (10, 100), "Add Track", TEXT_COLOR)
    small_font.render_to(screen, (10, 140), "Settings", TEXT_COLOR)
    small_font.render_to(screen, (10, 180), "Load Sample Pack", TEXT_COLOR)

    # Main workspace (right side of the screen)
    pygame.draw.rect(screen, (45, 45, 45), (200, 40, screen_width - 200, screen_height - 40))  # Workspace background
    
    # Workspace Title
    small_font.render_to(screen, (210, 50), "Workspace", TEXT_COLOR)

    # Draw buttons with hover effect
    draw_button(screen, "New Project", (250, 100), 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button(screen, "Save Project", (250, 160), 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button(screen, "Open File", (250, 220), 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button(screen, "Load Sample Pack", (250, 280), 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)

    # Display loaded samples (if any)
    if sample_pack:
        small_font.render_to(screen, (250, 350), f"Loaded {len(sample_pack)} Samples", TEXT_COLOR)

    # Update display
    pygame.display.update()

# Function to draw a button with hover effect
def draw_button(surface, text, rect, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(rect[0], rect[1], width, height)

    # Check if the mouse is hovering over the button
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(surface, hover_color, button_rect)  # Hover effect
    else:
        pygame.draw.rect(surface, color, button_rect)  # Default color

    # Render text on the button
    small_font.render_to(surface, (rect[0] + 10, rect[1] + 10), text, TEXT_COLOR)

# Function to handle events (file opening, saving, loading, etc.)
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Top Bar buttons for New, Open, Save
            if screen.get_width() - 150 <= mouse_x <= screen.get_width() and 0 <= mouse_y <= 40:
                new_project()
            
            if screen.get_width() - 100 <= mouse_x <= screen.get_width() and 0 <= mouse_y <= 40:
                load_project()  # Open file dialog
            
            if screen.get_width() - 50 <= mouse_x <= screen.get_width() and 0 <= mouse_y <= 40:
                save_project()  # Save project

            # Sidebar buttons for other actions (e.g., Add Track)
            if 0 <= mouse_x <= 200 and 60 <= mouse_y <= 100:
                print("Tracks clicked")
            if 0 <= mouse_x <= 200 and 100 <= mouse_y <= 140:
                print("Add Track clicked")
            if 0 <= mouse_x <= 200 and 140 <= mouse_y <= 180:
                print("Settings clicked")
            if 0 <= mouse_x <= 200 and 180 <= mouse_y <= 220:
                load_sample_pack()

# Main loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PDAW - Python DAW")
clock = pygame.time.Clock()

# Show the How-To guide for first-time users
show_how_to()

# Run the main loop
while True:
    handle_events()
    draw_gui(SCREEN_WIDTH, SCREEN_HEIGHT)
    clock.tick(FPS)
