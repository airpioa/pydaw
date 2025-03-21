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
SCRIPTS_DIR = os.path.join(PYDAW_DIR, "scripts")
MAIN_FILE = os.path.join(PYDAW_DIR, "main.py")
VERSION_FILE = os.path.join(PYDAW_DIR, "version.json")


def get_latest_release():
    """Fetches the latest release tag and zipball URL from GitHub."""
    try:
        with urlopen(GITHUB_API_URL) as response:
            latest_release = json.load(response)

        if "tag_name" not in latest_release or "zipball_url" not in latest_release:
            raise ValueError("Invalid release data received.")

        return latest_release["tag_name"], latest_release["zipball_url"]
    except Exception as e:
        print(f"Error fetching release info: {e}")
        return None, None


def update_pydaw():
    """Clones the latest PyDAW release and updates the current installation."""
    tag, _ = get_latest_release()
    if not tag:
        print("Failed to get the latest release. Update aborted.")
        return

    temp_dir = tempfile.mkdtemp()
    clone_url = f"https://github.com/{GITHUB_REPO}.git"

    print(f"Cloning PyDAW {tag} into temporary directory...")
    subprocess.run(["git", "clone", "--depth", "1", "--branch", tag, clone_url, temp_dir], check=True)

    # Copy new files over the existing installation
    for item in os.listdir(temp_dir):
        source_path = os.path.join(temp_dir, item)
        dest_path = os.path.join(PYDAW_DIR, item)

        if os.path.exists(dest_path):
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
            else:
                os.remove(dest_path)

        shutil.move(source_path, dest_path)

    # Clean up
    shutil.rmtree(temp_dir)
    print("PyDAW updated successfully.")


def update_version():
    """Updates version.json with the latest release tag."""
    tag, _ = get_latest_release()
    if not tag:
        print("Skipping version update due to missing release info.")
        return

    version_data = {"version": tag}
    with open(VERSION_FILE, "w") as f:
        json.dump(version_data, f, indent=4)

    print(f"Updated version file to {tag}.")


if __name__ == "__main__":
    print("Running update script...")
    try:
        update_pydaw()
        update_version()
        print("Update completed successfully.")
    except Exception as e:
        print(f"Update failed: {e}")
