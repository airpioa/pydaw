#!/bin/bash

echo "[BUILD] Building PyDAW Installer..."

# Install PyInstaller if not present
pip show pyinstaller >/dev/null || pip install pyinstaller

# Remove previous builds
rm -rf dist build PyDAW_Installer.spec

# Detect OS
OS="$(uname)"
if [[ "$OS" == "Darwin" ]]; then
    TARGET="macOS"
elif [[ "$OS" == "Linux" ]]; then
    TARGET="Linux"
else
    TARGET="Windows"
fi

echo "[BUILD] Detected OS: $TARGET"

# Build standalone installer
pyinstaller --onefile --noconsole --name=PyDAW_Installer installer.py

# Move output to release directory
mkdir -p release
mv dist/PyDAW_Installer release/PyDAW_Installer-"$TARGET"

echo "[BUILD] Build complete! Output: release/PyDAW_Installer-$TARGET"
