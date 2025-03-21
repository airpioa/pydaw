import os
import shutil
import subprocess
import json
import tempfile
import re

# GitHub repository details
GITHUB_REPO = "airpioa/pydaw"
GIT_CLONE_URL = f"https://github.com/{GITHUB_REPO}.git"

# Paths
PYDAW_DIR = os.path.expanduser("~/pydaw")
MAIN_FILE = os.path.join(PYDAW_DIR, "main.py")
VERSION_FILE = os.path.join(PYDAW_DIR, "version.json")


def log(message):
    """Logs a message to the console."""
    print(f"[UPDATE] {message}")


def get_latest_release_tag():
    """Gets the latest release tag from GitHub using git ls-remote."""
    log("Fetching latest release tag from GitHub...")
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", GIT_CLONE_URL],
            capture_output=True, text=True, check=True
        )
        
        # Extract only valid numeric version tags
        tags = re.findall(r"refs/tags/v?(\d+\.\d+\.\d+)", result.stdout)

        if tags:
            latest_tag = sorted(tags, key=lambda v: [int(x) for x in v.split(".")])[-1]
            log(f"Latest release tag found: v{latest_tag}")
            return f"v{latest_tag}"
        else:
            log("No valid numeric release tags found.")
            return None
    except subprocess.CalledProcessError as e:
        log(f"Error fetching release tags: {e.stderr}")
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
        subprocess.run(["git", "clone", "--depth", "1", "--single-branch", "--branch", latest_tag, GIT_CLONE_URL, temp_dir], check=True)
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
    latest_tag = get_latest_release_tag()
    if not latest_tag:
        log("Skipping version update due to missing release info.")
        return False

    version_data = {"version": latest_tag}
    with open(VERSION_FILE, "w") as f:
        json.dump(version_data, f, indent=4)

    log(f"Updated version file to {latest_tag}.")
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
        if update_pydaw():
            if update_version():
                log("Update successful. Restarting PyDAW...")
                restart_pydaw()
            else:
                log("Version update failed. PyDAW may not be up-to-date.")
        else:
            log("Update failed. Check errors above.")
    except Exception as e:
        log(f"Update failed: {e}")
