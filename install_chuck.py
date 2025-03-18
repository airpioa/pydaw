import os
import subprocess
import sys
import platform

def install_chuck():
    system = platform.system()

    if system == "Darwin":  # macOS
        print("Installing ChucK on macOS using Homebrew...")
        subprocess.run(["brew", "install", "chuck"], check=True)
    
    elif system == "Linux":
        print("Installing ChucK on Linux using APT...")
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "chuck"], check=True)

    elif system == "Windows":
        print("Downloading and installing ChucK on Windows...")
        chuck_url = "https://chuck.cs.princeton.edu/release/files/chuck-1.4.1.1-win64.zip"
        subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {chuck_url} -OutFile chuck.zip"], check=True)
        subprocess.run(["powershell", "-Command", "Expand-Archive -Path chuck.zip -DestinationPath C:\\ChucK -Force"], check=True)
        chuck_path = "C:\\ChucK"
        os.environ["PATH"] += os.pathsep + chuck_path
        print(f"ChucK installed in {chuck_path}")

    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        install_chuck()
        print("ChucK installation completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing ChucK: {e}")
        sys.exit(1)
