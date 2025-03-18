#!/bin/bash

# Step 1: Clone ChucK Repository and Compile

# Clone ChucK source code
if [ ! -d "chuck" ]; then
  git clone https://github.com/ccrma/chuck.git
fi

cd chuck

# Linux Compilation
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  sudo apt-get update
  sudo apt-get install build-essential libsndfile1-dev
  make
fi

# macOS Compilation
if [[ "$OSTYPE" == "darwin"* ]]; then
  brew install libsndfile
  make
fi

# Windows Compilation (requires Visual Studio and CMake)
if [[ "$OSTYPE" == "msys"* ]]; then
  echo "Please manually compile ChucK on Windows using Visual Studio and CMake"
  exit 1
fi

cd ..

# Step 2: Install PyInstaller and Bundle PyDAW

pip install -r requirements.txt  # Install PyDAW dependencies
pip install pyinstaller          # Install PyInstaller
pip install py2app               # Install py2app for macOS

# Create a spec file for PyInstaller
pyi-makespec --onefile pydaw.py

# Modify pydaw.spec to include ChucK binary (done manually in the spec file)

# Step 3: Build the PyDAW app with ChucK bundled
pyinstaller --onefile pydaw.spec

# Step 4: Distribute the Application

# For Linux (create .tar.gz)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  tar -czvf pydaw-linux.tar.gz ./dist/pydaw
fi

# For macOS (create app bundle)
if [[ "$OSTYPE" == "darwin"* ]]; then
  python setup-mac.py py2app --qt-plugins pyqt6
  tar -czvf pydaw-macos.tar.gz ./dist/pydaw.app
fi

# For Windows (PyInstaller generates .exe, use an installer like Inno Setup)
if [[ "$OSTYPE" == "msys"* ]]; then
  echo "Please distribute the .exe file using Inno Setup or NSIS."
fi

echo "Build maybe complete! The app is ready for distribution."
