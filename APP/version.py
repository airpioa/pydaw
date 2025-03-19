import os
import requests
import json
import subprocess
from pathlib import Path

# Path to the version file in ~/pydaw
VERSION_FILE_PATH = os.path.expanduser("~/pydaw/version.json")

# GitHub repository details
REPO_OWNER = "airpioa"
REPO_NAME = "pydaw"

def get_latest_version_from_github():
    """Fetch the latest release version from GitHub."""
    try:
        # GitHub API to get latest release details
        api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()  # Check if the request was successful
        latest_release = response.json()
        version = latest_release["tag_name"]  # Get the version from the release
        return version
    except requests.RequestException as e:
        print(f"Error fetching the latest release: {e}")
        return None

def update_version_file(version):
    """Update the version.json file with the latest version."""
    version_data = {"version": version}
    try:
        with open(VERSION_FILE_PATH, 'w') as version_file:
            json.dump(version_data, version_file, indent=4)
        print(f"Updated version file to {version}.")
    except IOError as e:
        print(f"Error updating the version file: {e}")

def run_update_script():
    """Run the update.py script to download and extract the release."""
    try:
        print("Running update.py script...")
        subprocess.run(["python", "update.py"], check=True)
        print("Update completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during the update process: {e}")

def main():
    # Step 1: Get the latest release version from GitHub
    version = get_latest_version_from_github()
    
    if version:
        # Step 2: Update the version file with the new version
        update_version_file(version)

        # Step 3: Run the update.py script to download the new release
        run_update_script()
    else:
        print("Failed to fetch the latest version. Update aborted.")

if __name__ == "__main__":
    main()
