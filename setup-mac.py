from setuptools import setup

APP = ['daw.py']  # Replace with the name of your main script (daw.py)
DATA_FILES = [
    ('resources', ['path_to_resources']),  # List additional resource files like images, icons, etc.
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame', 'PyQt6', 'dawdreamer', 'mido', 'pydub', 'PySide2.QtLocation'],  # List of required packages
    'iconfile': 'icon.png',
    'plist': {
        'CFBundleName': 'pydaw',
        'CFBundleDisplayName': 'pydaw',
        'CFBundleIdentifier': 'com.airpioa.pydaw',
        'CFBundleVersion': '1.0',
        'CFBundleShortVersionString': '1.0',
        'NSHighResolutionCapable': True,
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
