# pydaw

**pydaw** is a Digital Audio Workstation (DAW) built with Pygame. It provides a simple interface to manage projects, tracks, sample packs, and MIDI input. The DAW allows users to create, save, and load projects, add tracks, and manipulate audio samples with various features.

## Features

- Create and manage projects
- Load and manage sample packs (WAV, MP3)
- MIDI input handling (currently limited)
- Simple user interface with a top bar, sidebar, and workspace
- Save and open projects in `.pydaw` format
- Settings and metadata management

## Installation

### Requirements

To run **pydaw**, you need Python 3.8+ and the following dependencies:

- `pygame`
- `pygame.freetype`
- `pygame.midi`
- `tkinter` (for file dialogs)

### Install Dependencies

You can install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Run the Application
Once the dependencies are installed, you can run the DAW using the following command:

```bash
python daw.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/airpioa/pydaw?tab=MIT-1-ov-file#) file for details.

