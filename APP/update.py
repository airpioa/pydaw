import os
import requests
import zipfile
import io
import json
from pathlib import Path

# Path to the target directory where scripts are stored
SCRIPTS_DIR = os.path.expanduser("~/pydaw/scripts")
APP_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current directory of the script

# Path to the version.json file
VERSION_FILE_PATH = os.path.join(APP_DIR, "version.json")

# GitHub repository details
REPO_OWNER = "airpioa"
REPO_NAME = "pydaw"

def get_latest_release_url():
    """Fetch the latest release zip file URL from GitHub."""
    try:
        # GitHub API to get latest release details
        api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()  # Check if the request was successful
        latest_release = response.json()
        zip_url = latest_release["assets"][0]["browser_download_url"]
        version = latest_release["tag_name"]  # Get the version from the release
        return zip_url, version
    except requests.RequestException as e:
        print(f"Error fetching the latest release: {e}")
        return None, None

def download_and_extract_zip(zip_url, extract_to_dir):
    """Download the .zip file and extract its contents."""
    try:
        # Download the .zip file
        print("Downloading the latest release...")
        response = requests.get(zip_url)
        response.raise_for_status()  # Check if the request was successful

        # Extract the content of the zip file in-memory
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            print(f"Extracting files to {extract_to_dir}...")
            zip_ref.extractall(extract_to_dir)
        print("Extraction complete.")
    except requests.RequestException as e:
        print(f"Error downloading or extracting the zip file: {e}")

def update_version_file(version):
    """Update the version file with the latest version."""
    version_data = {"version": version}
    try:
        with open(VERSION_FILE_PATH, 'w') as version_file:
            json.dump(version_data, version_file, indent=4)
        print(f"Updated version file to {version}.")
    except IOError as e:
        print(f"Error updating the version file: {e}")

def update_scripts():
    """Update scripts by downloading and extracting the latest release."""
    # Step 1: Get the URL of the latest release zip file and version
    zip_url, version = get_latest_release_url()

    if zip_url and version:
        # Step 2: Download and extract the zip file to the scripts directory
        download_and_extract_zip(zip_url, SCRIPTS_DIR)
        
        # Step 3: Update the version file with the new version
        update_version_file(version)
    else:
        print("Failed to retrieve the latest release URL. Update aborted.")

def clean_up_previous_versions():
    """Optionally clean up previous versions if necessary."""
    # You could add logic here to remove old or conflicting files if required
    pass

if __name__ == "__main__":
    update_scripts()  # Run the update process
