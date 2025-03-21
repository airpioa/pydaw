import os
import shutil
import subprocess
import json
import tempfile
from urllib.request import urlopen

# GitHub repository details
GITHUB_REPO = "airpioa/pydaw"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# Paths
PYDAW_DIR = os.path.expanduser("~/pydaw")
MAIN_FILE = os.path.join(PYDAW_DIR, "main.py")
VERSION_FILE = os.path.join(PYDAW_DIR, "version.json")


def log(message):
    """Logs a message to the console."""
    print(f"[UPDATE] {message}")


def get_latest_release():
    """Fetches the latest release tag and repo URL from GitHub."""
    log("Fetching latest release info from GitHub...")
    try:
        with urlopen(GITHUB_API_URL) as response:
            latest_release = json.load(response)

        if "tag_name" not in latest_release:
            raise ValueError("Invalid release data received.")

        tag = latest_release["tag_name"]
        log(f"Latest release found: {tag}")
        return tag
    except Exception as e:
        log(f"Error fetching release info: {e}")
        return None


def update_pydaw():
    """Clones the latest PyDAW release and updates the installation."""
    tag = get_latest_release()
    if not tag:
        log("Failed to get the latest release. Update aborted.")
        return False

    temp_dir = tempfile.mkdtemp()
    clone_url = f"https://github.com/{GITHUB_REPO}.git"

    log(f"Cloning PyDAW {tag} into temporary directory...")
    try:
        subprocess.run(["git", "clone", "--depth", "1", "--branch", tag, clone_url, temp_dir], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        log(f"Git clone failed: {e.stderr}")
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


def update_version():
    """Updates version.json with the latest release tag."""
    tag = get_latest_release()
    if not tag:
        log("Skipping version update due to missing release info.")
        return False

    version_data = {"version": tag}
    with open(VERSION_FILE, "w") as f:
        json.dump(version_data, f, indent=4)

    log(f"Updated version file to {tag}.")
    return True


def restart_pydaw():
    """Restarts PyDAW after updating."""
    log("Restarting PyDAW...")
    if os.path.exists(MAIN_FILE):
        subprocess.run(["python", MAIN_FILE], check=False)
    else:
        log("Error: main.py not found after update!")


if __name__ == "__main__":
    log("Starting update script...")
    try:
        updated = update_pydaw()
        if updated:
            version_updated = update_version()
            if version_updated:
                log("Update successful. Restarting PyDAW...")
                restart_pydaw()
            else:
                log("Version update failed. PyDAW may not be up-to-date.")
        else:
            log("Update failed. Check errors above.")

    except Exception as e:
        log(f"Update failed: {e}")
