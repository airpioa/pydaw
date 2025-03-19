import os
import sys
import subprocess
import json

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

def increment_version():
    """Increments the version (patch version)."""
    version = read_version()
    if version is None:
        version = "1.0.0"  # Set the default version if the file doesn't exist

    major, minor, patch = map(int, version.split('.'))
    patch += 1  # Increment the patch version
    new_version = f"{major}.{minor}.{patch}"
    
    write_version(new_version)
    return new_version

def check_for_updates():
    """Checks for updates and restarts the app if needed."""
    # Simulate update check (you can replace with real update check logic)
    print("Checking for updates...")

    # For now, let's assume we always need to update
    updated = True

    if updated:
        print("Update found. Restarting the app...")

        # Close the current app instance
        sys.exit(0)  # Close the current application

        # Restart the app by invoking the main script
        subprocess.Popen([sys.executable, os.path.abspath(__file__)])  # Restart the app
        sys.exit(0)

