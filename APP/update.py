import os
import requests
import zipfile
import tarfile
import io
import json
import subprocess
from pathlib import Path

# Path to the version file in ~/pydaw
VERSION_FILE_PATH = os.path.expanduser("~/pydaw/version.json")
# Path where the source code should be downloaded and extracted (tmp directory)
TMP_DIR = os.path.expanduser("~/pydaw/tmp")
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
        return version, latest_release
    except requests.RequestException as e:
        print(f"Error fetching the latest release: {e}")
        return None, None

def get_download_url_from_assets(latest_release):
    """Get the download URL for the release assets."""
    assets = latest_release.get("assets", [])
    
    if not assets:
        print("No assets found in the latest release.")
        return None
    
    # Iterate through assets and check for a valid download URL for the release file
    for asset in assets:
        if "browser_download_url" in asset:
            zip_url = asset["browser_download_url"]
            print(f"Found asset with download URL: {zip_url}")
            return zip_url

    # If no valid URL is found
    print("No valid asset download URL found in the latest release.")
    return None

def download_and_extract_release(zip_url, target_directory):
    """Download the release from GitHub and extract it."""
    try:
        print(f"Downloading release from {zip_url}...")
        response = requests.get(zip_url)
        response.raise_for_status()

        # Ensure the target directory exists
        os.makedirs(target_directory, exist_ok=True)

        # Check the file type and extract accordingly
        if zip_url.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                print(f"Extracting files to {target_directory}...")
                zip_ref.extractall(target_directory)
        elif zip_url.endswith('.tar.gz') or zip_url.endswith('.tgz'):
            with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as tar_ref:
                print(f"Extracting files to {target_directory}...")
                tar_ref.extractall(target_directory)
        else:
            print("Unsupported file type for extraction.")
            return False

        print("Extraction completed successfully.")
        return True

    except requests.RequestException as e:
        print(f"Error downloading the release: {e}")
        return False
    except (zipfile.BadZipFile, tarfile.TarError) as e:
        print(f"Error extracting the release: {e}")
        return False

def update_version_file(version):
    """Update the version.json file with the latest version."""
    version_data = {"version": version}
    try:
        with open(VERSION_FILE_PATH, 'w') as version_file:
            json.dump(version_data, version_file, indent=4)
        print(f"Updated version file to {version}.")
    except IOError as e:
        print(f"Error updating the version file: {e}")

def main():
    # Step 1: Get the latest release version from GitHub
    version, latest_release = get_latest_version_from_github()
    
    if version and latest_release:
        # Step 2: Update the version file with the new version
        update_version_file(version)

        # Step 3: Check for release assets and proceed with update
        zip_url = get_download_url_from_assets(latest_release)
        
        if zip_url:
            # Step 4: Download and extract the release to ~/pydaw/tmp
            if download_and_extract_release(zip_url, TMP_DIR):
                print("Update process completed successfully.")
            else:
                print("Failed to download or extract the release.")
        else:
            print("No valid assets found for the update. Skipping download.")
    else:
        print("Failed to fetch the latest version. Update aborted.")

if __name__ == "__main__":
    main()
