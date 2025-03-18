import mido
from mido import MidiFile
from logger import logger

def load_midi_file(midi_file_path):
    try:
        midi = MidiFile(midi_file_path)
        for msg in midi.play():
            print(msg)
    except Exception as e:
        logger.error(f"Failed to load MIDI file: {e}")
