

# **PyDAW** - Python Digital Audio Workstation

**PyDAW** is a lightweight, feature-rich Digital Audio Workstation built in Python. It integrates several powerful features, such as:

- **Virtual Instruments** & **VST Plugin** Support
- **MIDI Sequencing** & **MIDI Instrument Integration**
- **ChucK Integration** for real-time audio synthesis and processing
- **PyQt6** for building a modern, customizable user interface

This project allows users to create, manipulate, and produce audio in a simple yet powerful DAW environment.

---

## **Features**

- **Workspace Management**: Easily create, open, and manage workspaces with MIDI tracks, instruments, and audio files.
- **MIDI Sequencer**: Record, edit, and play MIDI sequences within the workspace.
- **Virtual Instruments**: Support for virtual instruments and VST plugins.
- **ChucK Integration**: Real-time synthesis and processing capabilities via **ChucK** for sound generation, manipulation, and more.
- **Multi-platform**: Built to run on **Linux**, **macOS**, and **Windows**.

---

## **Building From Source**

### **1. Clone the Repository**

First, clone the **PyDAW** repository:
```bash
git clone https://github.com/airpioa/pydaw.git
cd pydaw
```

### **2. Install Dependencies**

Install Python dependencies:
```bash
pip install -r requirements.txt
```

For **ChucK** support, make sure **ChucK** is compiled for your platform (Linux/macOS/Windows).

---

## **Building ChucK**

### **Linux**

1. Install dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install build-essential libsndfile1-dev
   ```

2. Compile **ChucK**:
   ```bash
   cd chuck/src
   make mac
   ```

### **macOS**

1. Install dependencies using **Homebrew**:
   ```bash
   brew install libsndfile
   ```

2. Compile **ChucK**:
   ```bash
   cd chuck
   make
   ```

### **Windows**

1. Follow the instructions provided in the [ChucK README](https://github.com/ccrma/chuck/blob/master/README.md) for building on **Windows**. Ensure you have **Visual Studio** and **CMake** installed.

---

## **Building PyDAW with ChucK**

Once **ChucK** is compiled, you can bundle **PyDAW** with **PyInstaller**.

1. Install **PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. Generate the spec file for PyInstaller:
   ```bash
   pyi-makespec --onefile pydaw.py
   ```

3. Modify the spec file to include **ChucK** binary (update the `binaries` section to point to the compiled **ChucK** binary).

4. Build the **PyDAW** application with **ChucK** bundled:
   ```bash
   pyinstaller --onefile pydaw.spec
   ```

5. Distribute your **PyDAW** application for your platform.

---

## **Running PyDAW**

1. **Linux**:
   - After building the application, distribute as a `.tar.gz` or `.deb` package.

2. **macOS**:
   - Build using **py2app** to create a macOS application bundle:
     ```bash
     python setup.py py2app
     ```

3. **Windows**:
   - Use **PyInstaller** to generate a `.exe` file and package it using **Inno Setup** or **NSIS** for distribution.

---

## **Usage**

1. **Create a New Workspace**: You can create a new workspace where you'll manage your MIDI tracks, instruments, and effects. The workspace is stored as a folder containing all necessary files and a manifest.

2. **Open an Existing Workspace**: Open an existing workspace and start working on your audio and MIDI production.

3. **Add Virtual Instruments and Effects**: PyDAW supports adding virtual instruments and VST plugins directly into your workspace.

4. **MIDI Sequencing**: Sequence and manipulate MIDI tracks. You can edit them, add new notes, and even use external MIDI controllers.

5. **ChucK Integration**: For sound synthesis, you can integrate **ChucK** scripts. This enables powerful real-time audio synthesis and manipulation.

---

## **ChucK Integration**

PyDAW integrates **ChucK** for real-time audio synthesis. It allows you to run **ChucK** scripts within your workspace, giving you access to generative sound, music, and real-time audio processing. 

To use **ChucK** in your workspace, simply add a **ChucK** script file in the workspace’s manifest. PyDAW will execute the script through the bundled **ChucK** binary. 

---

## **Contributing**

We welcome contributions to improve **PyDAW**! Feel free to fork the repository, make changes, and submit a pull request.

---

## **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## **Acknowledgments**

- **ChucK**: A powerful and flexible audio programming language for real-time synthesis, by **CCRMA**.
- **PyQt6**: A set of Python bindings for the Qt application framework, used for building the UI.
- **Pygame**: Used for initializing the audio and graphical features in the DAW.
- **mido**: Python library for working with MIDI.
