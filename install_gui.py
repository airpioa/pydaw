import os
import sys
import subprocess
import shutil
import tkinter as tk
from tkinter import scrolledtext, messagebox
import urllib.request
import json  # To parse the GitHub API response

# GitHub API URL to fetch the latest release
GITHUB_API_URL = "https://api.github.com/repos/airpioa/pydaw/releases/latest"
DAW_INSTALL_PATH = ""
DAW_SCRIPT_PATH = ""

# Determine the correct install path based on OS
if sys.platform == "win32":
    DAW_INSTALL_PATH = "C:\\DAW"
    DAW_SCRIPT_PATH = os.path.join(DAW_INSTALL_PATH, "daw.py")
elif sys.platform == "darwin":
    DAW_INSTALL_PATH = "/Applications/DAW"
    DAW_SCRIPT_PATH = os.path.join(DAW_INSTALL_PATH, "daw.py")
else:
    messagebox.showerror("Unsupported OS", "This installer only supports Windows and macOS.")
    sys.exit(1)

# Function to install missing Python packages
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        update_log(f"⚠️ Failed to install {package}: {e}")
        messagebox.showerror("Installation Failed", f"Failed to install {package}")
        sys.exit(1)

# Function to check and install 'winshell' if it's missing
def check_and_install_winshell():
    try:
        import winshell
    except ImportError:
        answer = messagebox.askyesno("Missing Dependency", "'winshell' module is missing. Would you like to install it?")
        if answer:
            install_package("winshell")
        else:
            update_log("⚠️ 'winshell' not installed. Skipping shortcut creation.")
            messagebox.showinfo("Missing 'winshell'", "You will not be able to create shortcuts without it.")
            
# Function to run system commands and handle errors properly
def run_command(command):
    """Run a system command and return output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr if result.stdout or result.stderr else "No output."
    except Exception as e:
        return str(e) or "Error occurred while running the command."


# Install Homebrew for macOS
def install_homebrew():
    """Install Homebrew on macOS if not installed."""
    if shutil.which("brew") is None:
        update_log("🍺 Homebrew not found. Installing...")
        try:
            result = run_command('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            update_log(result)
        except Exception as e:
            update_log(f"⚠️ Failed to install Homebrew: {e}")
            messagebox.showerror("Homebrew Installation Failed", f"Could not install Homebrew: {e}", f"Please install Homebrew manually from https://brew.sh/ if not already installed.")
    else:
        update_log("✅ Homebrew is already installed.")

# Install Winget for Windows
def install_winget():
    """Install Winget on Windows if not installed."""
    if shutil.which("winget") is None:
        update_log("🖥️ Winget not found. Please install it manually from https://github.com/microsoft/winget-cli/releases")
        messagebox.showerror("Winget Missing", "Please install Winget manually and restart the installer.")
        sys.exit(1)
    else:
        update_log("✅ Winget is already installed.")

# Install FFmpeg based on OS
def install_ffmpeg():
    """Install FFmpeg based on OS."""
    if sys.platform == "win32":
        install_winget()
        update_log("Installing FFmpeg for Windows...")
        result = run_command("winget install --id=Gyan.FFmpeg -e")
        update_log(result)
    elif sys.platform == "darwin":
        install_homebrew()
        update_log("Installing FFmpeg for macOS...")
        result = run_command("brew install ffmpeg")
        update_log(result)
    else:
        update_log("⚠️ FFmpeg installation not automated for this OS.")

# Function to download DAW from GitHub
def download_daw():
    """Download the DAW script from the latest release on GitHub."""
    try:
        update_log(f"⬇️ Fetching latest release from GitHub...")
        # Fetch the latest release information from the GitHub API
        response = urllib.request.urlopen(GITHUB_API_URL)
        release_info = json.load(response)

        # Find the download URL for daw.py (or any specific file)
        assets = release_info.get('assets', [])
        daw_asset_url = None
        for asset in assets:
            if asset['name'] == 'daw.py':  # Change this if the file name is different
                daw_asset_url = asset['browser_download_url']
                break

        if daw_asset_url:
            # Create directory and download the DAW script
            os.makedirs(DAW_INSTALL_PATH, exist_ok=True)
            update_log(f"⬇️ Downloading DAW script to {DAW_SCRIPT_PATH}...")
            urllib.request.urlretrieve(daw_asset_url, DAW_SCRIPT_PATH)
            update_log("✅ DAW script downloaded successfully!")
        else:
            update_log("⚠️ `daw.py` not found in the latest release.")
            messagebox.showerror("Download Failed", "`daw.py` was not found in the latest release.")
            sys.exit(1)

    except Exception as e:
        update_log(f"⚠️ Failed to download DAW script: {e}")
        messagebox.showerror("Download Failed", "Could not download the DAW script.")

# Function to create desktop shortcuts (Windows only)
def create_shortcut():
    """Create a desktop shortcut for the DAW."""
    if sys.platform == "win32":
        try:
            import winshell
            shortcut_path = os.path.join(winshell.desktop(), "DAW.lnk")
            target = DAW_SCRIPT_PATH
            shell = winshell.shell
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = target
            shortcut.save()
            update_log("✅ Shortcut created successfully on desktop.")
        except Exception as e:
            update_log(f"⚠️ Failed to create shortcut: {e}")
            messagebox.showerror("Shortcut Creation Failed", "Failed to create a desktop shortcut.")
    else:
        update_log("⚠️ Shortcut creation is only supported on Windows.")

# Function to run the DAW script after installation
def run_daw():
    """Run the DAW script after installation."""
    if os.path.exists(DAW_SCRIPT_PATH):
        update_log("🎵 Launching DAW...")
        if sys.platform == "win32":
            subprocess.Popen(["python", DAW_SCRIPT_PATH], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["python3", DAW_SCRIPT_PATH], shell=True)
    else:
        update_log("⚠️ DAW script not found. Please check the installation.")

# Function to install all dependencies and DAW
def install_all():
    """Run the full installation process."""
    install_ffmpeg()

    # Install Python packages
    packages = ["pygame", "pydub", "numpy", "sounddevice", "matplotlib"]
    for pkg in packages:
        install_package(pkg)

    # Download and run DAW
    download_daw()
    run_daw()

    # Ask user if they want to create a shortcut
    create_shortcut_answer = messagebox.askyesno("Create Shortcut", "Would you like to create a desktop shortcut?")
    if create_shortcut_answer:
        create_shortcut()

    update_log("\n🎵 ✅ Installation complete! The DAW has been launched.")
    messagebox.showinfo("Installation Complete", "All dependencies have been installed successfully, and the DAW is running!")

# Function to update the log box in the GUI
def update_log(message):
    """Update the GUI log box."""
    log_box.config(state=tk.NORMAL)
    log_box.insert(tk.END, message + "\n")
    log_box.config(state=tk.DISABLED)
    log_box.yview(tk.END)  # Auto-scroll to the bottom
    root.update_idletasks()

# ------------------ GUI Setup ------------------
root = tk.Tk()
root.title("🎵 DAW Auto Installer")
root.geometry("600x400")
root.resizable(False, False)

# Title Label
title_label = tk.Label(root, text="DAW Dependency Installer", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# Log Box
log_box = scrolledtext.ScrolledText(root, width=70, height=15, state=tk.DISABLED)
log_box.pack(pady=10, padx=10)

# Install Button
install_button = tk.Button(root, text="Start Installation", font=("Arial", 12), command=install_all)
install_button.pack(pady=10)

# Quit Button
quit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit)
quit_button.pack(pady=5)

root.mainloop()
