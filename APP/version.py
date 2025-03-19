import os
import json
import requests

VERSION_FILE = os.path.expanduser('~/pydaw/version.json')

def read_version():
    """Reads the current version from the version.json file."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            data = json.load(f)
            return data.get("version", None)
    else:
        return None

def write_version(version):
    """Writes the current version to version.json."""
    data = {"version": version}
    with open(VERSION_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def increment_version(version):
    """Increments the patch version and writes it to version.json."""
    major, minor, patch = map(int, version.split('.'))
    patch += 1  # Increment the patch version
    new_version = f"{major}.{minor}.{patch}"

    write_version(new_version)
    return new_version

def get_latest_version_from_repo():
    """Fetch the latest version from the repository (GitHub API in this case)."""
    try:
        # Example using GitHub's API for latest release information
        response = requests.get("https://api.github.com/repos/airpioa/pydaw/releases/latest")
        response.raise_for_status()  # Raise an exception for HTTP errors
        latest_version = response.json()['tag_name']
        return latest_version
    except requests.RequestException as e:
        print(f"Error fetching latest version: {e}")
        return None

def check_for_update():
    """Compares the current version with the latest version and updates if needed."""
    current_version = read_version()
    latest_version = get_latest_version_from_repo()

    if current_version and latest_version:
        if current_version != latest_version:
            print(f"Update found! Current version: {current_version}, Latest version: {latest_version}")
            return True
    return False

def update_version_if_needed():
    """Check for updates and increment the version if necessary."""
    if check_for_update():
        print("Updating to the latest version...")
        current_version = read_version() or "1.0.0"  # If no version exists, assume it's version 1.0.0
        increment_version(current_version)
        return True
    return False
