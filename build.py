import os
import sys
import platform
import subprocess

def run_command(command):
    """Run a command in the terminal."""
    subprocess.run(command, shell=True, check=True)

def build_windows():
    """Build the Windows executable."""
    print("🖥️ Building Windows executable...")
    run_command("pyinstaller --onefile --windowed --distpath dist/win install_gui.py")
    print("✅ Windows build complete! Find it in dist/win/")

def build_macos():
    """Build the macOS app."""
    print("🍏 Building macOS app...")
    run_command('pyinstaller --onefile --windowed --name "DAW Installer" --distpath dist/mac install_gui.py')
    print("✅ macOS build complete! Find it in dist/mac/")

def main():
    """Run the appropriate build based on OS."""
    current_os = platform.system()

    if current_os == "Windows":
        build_windows()
    elif current_os == "Darwin":  # macOS
        build_macos()
    else:
        print("⚠️ Unsupported OS for building.")

if __name__ == "__main__":
    main()
