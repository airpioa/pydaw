import os
import json
import tempfile
import shutil
import subprocess
import requests

# Constants
GITHUB_API_URL = "https://api.github.com/repos/airpioa/pydaw/releases/latest"
GIT_CLONE_URL = "https://github.com/airpioa/pydaw.git"
PYDAW_DIR = os.path.expanduser("~/pydaw")


def log(message):
    """Logs messages with an [UPDATE] prefix."""
    print(f"[UPDATE] {message}")


def get_latest_release_tag():
    """Fetches the latest release tag from GitHub."""
    log("Fetching latest release tag from GitHub...")
    try:
        response = requests.get(GITHUB_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("tag_name")
    except (requests.RequestException, json.JSONDecodeError) as e:
        log(f"Failed to fetch release tag: {e}")
        return None


def update_pydaw():
    """Clones the latest PyDAW release into a temporary directory and updates the installation."""
    latest_tag = get_latest_release_tag()
    if not latest_tag:
        log("Failed to get the latest release. Update aborted.")
        return False

    temp_dir = tempfile.mkdtemp()
    
    log(f"Cloning PyDAW {latest_tag} into temporary directory...")
    try:
        subprocess.run(["git", "clone", "--depth", "1", GIT_CLONE_URL, temp_dir], check=True)
        subprocess.run(["git", "fetch", "--tags"], cwd=temp_dir, check=True)
        subprocess.run(["git", "checkout", latest_tag], cwd=temp_dir, check=True)
    except subprocess.CalledProcessError as e:
        log(f"Git clone failed: {e}")
        return False

    log("Replacing existing PyDAW files...")
    for item in os.listdir(temp_dir):
        source_path = os.path.join(temp_dir, item)
        dest_path = os.path.join(PYDAW_DIR, item)

        if os.path.exists(dest_path):
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
            else:
                os.remove(dest_path)

        shutil.move(source_path, dest_path)

    shutil.rmtree(temp_dir)
    log("PyDAW update completed successfully.")
    return True


if __name__ == "__main__":
    log("Starting update script...")
    if update_pydaw():
        log("Update completed successfully.")
    else:
        log("Update failed. Check errors above.")
