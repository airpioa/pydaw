import os
import json

PDAW_DIR = os.path.expanduser("~/pydaw")
WORKSPACES_DIR = os.path.join(PDAW_DIR, "workspaces")
INSTRUMENTS_DIR = os.path.join(PDAW_DIR, "instruments")
SETTINGS_FILE = os.path.join(PDAW_DIR, "pydawsettings.json")

# Ensure necessary directories exist
os.makedirs(PDAW_DIR, exist_ok=True)
os.makedirs(WORKSPACES_DIR, exist_ok=True)
os.makedirs(INSTRUMENTS_DIR, exist_ok=True)

# Load settings
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {"vst_plugins": [], "vst_params": {}, "vst_install_location": ""}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
