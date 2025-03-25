#!/bin/bash

# Set the installer and uninstaller scripts
INSTALLER_SCRIPT="installer.py"
UNINSTALLER_SCRIPT="uninstaller.py"

# Set the output directory
OUTPUT_DIR="dist"

# Clean up old build directories
clean() {
    echo "Cleaning up old builds..."
    rm -rf build dist *.spec
}

# Build the app using PyInstaller
build_app() {
    local script_name="$1"
    local output_name="$2"

    echo "Building $output_name..."

    pyinstaller --onefile --windowed --add-data "icon.png:." "$script_name"

    # Move the built app to the desired output directory
    mv "dist/$(basename "$script_name" .py)" "$OUTPUT_DIR/$output_name"
}

# Check if PyInstaller is installed
check_pyinstaller() {
    if ! command -v pyinstaller &> /dev/null; then
        echo "PyInstaller is not installed. Installing it now..."
        pip install pyinstaller
    fi
}

# Main function to build both the installer and uninstaller
main() {
    # Check if PyInstaller is installed
    check_pyinstaller

    # Clean up old build directories
    clean

    # Create the output directory if it doesn't exist
    if [ ! -d "$OUTPUT_DIR" ]; then
        mkdir "$OUTPUT_DIR"
    fi

    # Build the installer app
    if [[ "$OSTYPE" == "darwin"* ]]; then
        build_app "$INSTALLER_SCRIPT" "PyDAW_Installer.app"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        build_app "$INSTALLER_SCRIPT" "PyDAW_Installer"
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        build_app "$INSTALLER_SCRIPT" "PyDAW_Installer.exe"
    fi

    echo "Installer app built at $OUTPUT_DIR"

    # Build the uninstaller app
    if [[ "$OSTYPE" == "darwin"* ]]; then
        build_app "$UNINSTALLER_SCRIPT" "PyDAW_Uninstaller.app"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        build_app "$UNINSTALLER_SCRIPT" "PyDAW_Uninstaller"
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        build_app "$UNINSTALLER_SCRIPT" "PyDAW_Uninstaller.exe"
    fi

    echo "Uninstaller app built at $OUTPUT_DIR"
    echo "Build complete!"
}

# Run the main function
main
