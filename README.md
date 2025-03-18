

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
---



---

## **Running PyDAW**

```bash/cmd
python daw.py
```

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
