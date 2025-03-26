

# **PyDAW** - Python Digital Audio Workstation

**PyDAW** is a lightweight, feature-rich Digital Audio Workstation built in Python.

This project allows users to create, manipulate, and produce audio in a simple yet powerful DAW environment.

---

## **Features**

- **Workspace Management**: Easily create, open, and manage workspaces with MIDI tracks, instruments, and audio files.
- **MIDI Sequencer**: Record, edit, and play MIDI sequences within the workspace.
- **Virtual Instruments**: Support for virtual instruments and VST plugins.
- **ChucK Integration**: Real-time synthesis and processing capabilities via **ChucK** for sound generation, manipulation, and more.
- **Multi-platform**: Built to run on **Linux**, **macOS**, and **Windows**.

---

## **Running the Installer**

To install **PyDAW**, you'll need to run the installer script. The installer will guide you through the process of setting up **PyDAW** on your system.

1. **Ensure Python is installed**: If Python is not installed on your system, you can download it from [python.org](https://www.python.org/downloads/).

**Step 2: Download installer.py Script**

Access the latest release of the PyDAW project at the following link: https://github.com/airpioa/pydaw/releases/latest

Download the installer.py script.

Navigate to the directory where the installer.py script was downloaded.

run
```bash
pip install PySide6
```

Proceed to Step 3.

3. **Run the Installer Script**:
   
   Once the dependencies are installed, run the following command to start the installer:
   ```bash
   python installer.py
   ```

4. **Follow the Installer Steps**: The installer will ask you for the installation location. After you specify a location, it will automatically download dependencies, configure PyDAW, and set up an application bundle or shortcut based on your platform (macOS, Windows, or Linux).

5. **Complete Installation**: After installation, you can launch PyDAW from the application bundle (macOS) or start menu (Windows).

---

## **Running PyDAW**

Once installed, you can launch **PyDAW** from your installation location or through the application shortcut created by the installer.

---

## **Usage**

1. **Create a New Workspace**: You can create a new workspace where you'll manage your MIDI tracks, instruments, and effects. The workspace is stored as a folder containing all necessary files and a manifest.

2. **Open an Existing Workspace**: Open an existing workspace and start working on your audio and MIDI production.

3. **Add Virtual Instruments and Effects**: PyDAW supports adding virtual instruments and VST plugins directly into your workspace.

4. **MIDI Sequencing**: Sequence and manipulate MIDI tracks. You can edit them, add new notes, and even use external MIDI controllers.

5. **ChucK Integration**: For sound synthesis, you can integrate **ChucK** scripts. This enables powerful real-time audio synthesis and manipulation.

---

## **ChucK Integration** **WIP**

PyDAW integrates **ChucK** for real-time audio synthesis. It allows you to run **ChucK** scripts within your workspace, giving you access to generative sound, music, and real-time audio processing. 

To use **ChucK** in your workspace, simply add a **ChucK** script file in the workspace’s manifest. PyDAW will execute the script through the bundled **ChucK** binary. 

---

## **Uninstalling PyDAW**

If you want to remove **PyDAW** from your system, you can run the uninstaller script.

### Steps to run the uninstaller:

1. **Run the Uninstaller Script**:
   ```bash
   python uninstaller.py
   ```

2. **Follow the Uninstaller Steps**: The uninstaller will remove **PyDAW** from your system and clean up any installation files.

3. **Confirm the Removal**: The uninstaller will prompt you with a warning before proceeding with the deletion. Confirm to proceed.

   > **Warning**: This action will remove all PyDAW files and settings.

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

---
