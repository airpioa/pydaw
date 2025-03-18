import os
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

# Automatically update the version when starting the app
if __name__ == "__main__":
    current_version = increment_version()  # This increments the version by 1 (patch version)
    print(f"Current version: {current_version}")
