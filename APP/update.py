import requests
import os
import subprocess
import json
from PySide6.QtWidgets import QMessageBox

# Define the repository URL and local directory for PyDAW
REPO_URL = "https://api.github.com/repos/airpioa/pydaw/releases/latest"
LOCAL_DIR = os.path.expanduser('~/pydaw')

def check_for_updates():
    try:
        # Get the latest release from GitHub
        response = requests.get(REPO_URL)
        response.raise_for_status()
        
        latest_release = response.json()
        latest_version = latest_release['tag_name']
        
        # Check current version (assumed to be stored in a JSON file)
        with open(os.path.join(LOCAL_DIR, 'version.json'), 'r') as f:
            current_version = json.load(f)['version']
        
        # Compare versions and update if necessary
        if latest_version != current_version:
            update_code(latest_release['zipball_url'])
        else:
            show_message("You are using the latest version.")
    except Exception as e:
        show_message(f"Error checking for updates: {e}")

def update_code(zipball_url):
    try:
        # Download and unzip the latest release
        response = requests.get(zipball_url, stream=True)
        zip_path = os.path.join(LOCAL_DIR, 'update.zip')
        
        with open(zip_path, 'wb') as f:
            f.write(response.content)

        # Extract and replace the current code
        subprocess.run(["unzip", "-o", zip_path, "-d", LOCAL_DIR])
        os.remove(zip_path)
        show_message("Update complete!")
    except Exception as e:
        show_message(f"Error updating the code: {e}")

def show_message(message):
    # Display a simple message box
    QMessageBox.information(None, "Update", message)
