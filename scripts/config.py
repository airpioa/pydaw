import os
import json

# Define the base directory for PyDAW
PYDAW_DIR = os.path.expanduser("~/pydaw")
WORKSPACES_DIR = os.path.join(PYDAW_DIR, "workspaces")
INSTRUMENTS_DIR = os.path.join(PYDAW_DIR, "instruments")
SETTINGS_FILE = os.path.join(PYDAW_DIR, "pydawsettings.json")

# Ensure necessary directories exist
os.makedirs(PYDAW_DIR, exist_ok=True)
os.makedirs(WORKSPACES_DIR, exist_ok=True)
os.makedirs(INSTRUMENTS_DIR, exist_ok=True)

# Load or initialize settings
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {
        "vst_plugins": [],
        "vst_params": {},
        "vst_install_location": "",
        "auto_update_enabled": False  # Default to auto-updates disabled
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)