"""
Piano Player Application
Demonstrates how apps play piano pieces from sheet music notation.

This example shows the core concepts:
1. Music notation representation
2. Audio synthesis using sine waves
3. Timing and rhythm control
4. Playing a simple melody
"""

import numpy as np
import pygame
import time
from dataclasses import dataclass
from typing import List, Dict
import threading

# Initialize pygame mixer for audio
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()

@dataclass
class Note:
    """Represents a musical note with pitch and duration"""
    name: str          # Note name (C, D, E, F, G, A, B)
    octave: int        # Octave number (4 = middle octave)
    duration: float    # Duration in beats (1.0 = quarter note, 0.5 = eighth note)
    accidental: str = ""  # Sharp (#) or flat (b)

class PianoPlayer:
    """Main class for playing piano music from notation"""
    
    def __init__(self, tempo: int = 120):
        """
        Initialize the piano player
        Args:
            tempo: Beats per minute (BPM)
        """
        self.tempo = tempo
        self.sample_rate = 22050
        self.note_frequencies = self._build_frequency_table()
        
    def _build_frequency_table(self) -> Dict[str, float]:
        """Build a table of note frequencies using equal temperament tuning"""
        # A4 = 440 Hz as reference
        frequencies = {}
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        for octave in range(0, 9):
            for i, note in enumerate(note_names):
                # Calculate frequency using equal temperament formula
                # f = 440 * 2^((n-69)/12) where n is MIDI note number
                midi_note = octave * 12 + i
                frequency = 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
                key = f"{note}{octave}"
                frequencies[key] = frequency
                
        return frequencies
    
    def _generate_tone(self, frequency: float, duration: float, volume: float = 0.3) -> np.ndarray:
        """
        Generate a sine wave tone for a given frequency and duration
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            volume: Volume (0.0 to 1.0)
            
        Returns:
            numpy array of audio samples
        """
        frames = int(duration * self.sample_rate)
        arr = np.zeros(frames)
        
        if frequency > 0:  # Don't generate tone for rests
            # Create sine wave with envelope to avoid clicks
            for i in range(frames):
                # Sine wave
                wave = np.sin(2 * np.pi * frequency * i / self.sample_rate)
                
                # Apply envelope (attack, decay, sustain, release)
                envelope = 1.0
                attack_frames = int(0.01 * self.sample_rate)  # 10ms attack
                release_frames = int(0.1 * self.sample_rate)   # 100ms release
                
                if i < attack_frames:
                    envelope = i / attack_frames
                elif i > frames - release_frames:
                    envelope = (frames - i) / release_frames
                    
                arr[i] = wave * envelope * volume
                
        return arr
    
    def _note_to_frequency(self, note: Note) -> float:
        """Convert a Note object to its frequency in Hz"""
        if note.name == "REST":
            return 0.0
            
        note_key = f"{note.name}{note.accidental}{note.octave}"
        return self.note_frequencies.get(note_key, 0.0)
    
    def _beat_to_seconds(self, beats: float) -> float:
        """Convert beats to seconds based on current tempo"""
        return (beats * 60.0) / self.tempo
    
    def play_note(self, note: Note):
        """Play a single note"""
        frequency = self._note_to_frequency(note)
        duration = self._beat_to_seconds(note.duration)
        
        if frequency > 0:
            print(f"Playing {note.name}{note.accidental}{note.octave} ({frequency:.1f} Hz) for {duration:.2f}s")
        else:
            print(f"Rest for {duration:.2f}s")
            
        # Generate and play the tone
        tone = self._generate_tone(frequency, duration)
        
        # Convert to 16-bit integers for pygame
        tone_int = (tone * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo_tone = np.zeros((len(tone_int), 2), dtype=np.int16)
        stereo_tone[:, 0] = tone_int  # Left channel
        stereo_tone[:, 1] = tone_int  # Right channel
        
        # Play the sound
        sound = pygame.sndarray.make_sound(stereo_tone)
        sound.play()
        
        # Wait for the note to finish
        time.sleep(duration)
    
    def play_melody(self, notes: List[Note]):
        """Play a sequence of notes (melody)"""
        print(f"Playing melody at {self.tempo} BPM...")
        print("-" * 50)
        
        for note in notes:
            self.play_note(note)
        
        print("-" * 50)
        print("Melody finished!")

class SheetMusicParser:
    """Demonstrates how sheet music notation could be parsed"""
    
    @staticmethod
    def parse_simple_notation(notation: str) -> List[Note]:
        """
        Parse a simple text notation into Note objects
        Format: "NOTE_OCTAVE_DURATION" separated by spaces
        Example: "C4_1.0 D4_1.0 E4_1.0" = C-D-E quarter notes in octave 4
        """
        notes = []
        parts = notation.strip().split()
        
        for part in parts:
            if '_' in part:
                components = part.split('_')
                if len(components) >= 3:
                    note_name = components[0]
                    octave = int(components[1])
                    duration = float(components[2])
                    
                    # Handle sharps and flats
                    accidental = ""
                    if '#' in note_name:
                        note_name = note_name.replace('#', '')
                        accidental = "#"
                    elif 'b' in note_name:
                        note_name = note_name.replace('b', '')
                        accidental = "b"
                    
                    notes.append(Note(note_name, octave, duration, accidental))
                    
        return notes

def demo_simple_scale():
    """Demonstrate playing a simple C major scale"""
    print("=== Demo 1: C Major Scale ===")
    
    player = PianoPlayer(tempo=120)
    
    # C major scale: C D E F G A B C
    scale_notation = "C4_1.0 D4_1.0 E4_1.0 F4_1.0 G4_1.0 A4_1.0 B4_1.0 C5_1.0"
    notes = SheetMusicParser.parse_simple_notation(scale_notation)
    
    player.play_melody(notes)

def demo_mary_had_a_little_lamb():
    """Demonstrate playing 'Mary Had a Little Lamb'"""
    print("\n=== Demo 2: Mary Had a Little Lamb ===")
    
    player = PianoPlayer(tempo=120)
    
    # Mary Had a Little Lamb melody
    # E D C D E E E (rest) D D D (rest) E G G (rest)
    # E D C D E E E E D D E D C
    melody_notation = """
    E4_1.0 D4_1.0 C4_1.0 D4_1.0 E4_1.0 E4_1.0 E4_2.0
    D4_1.0 D4_1.0 D4_2.0
    E4_1.0 G4_1.0 G4_2.0
    E4_1.0 D4_1.0 C4_1.0 D4_1.0 E4_1.0 E4_1.0 E4_1.0 E4_1.0 D4_1.0 D4_1.0 E4_1.0 D4_1.0 C4_4.0
    """.replace('\n', ' ').strip()
    
    notes = SheetMusicParser.parse_simple_notation(melody_notation)
    player.play_melody(notes)

def demo_chord_progression():
    """Demonstrate playing multiple notes together (chords)"""
    print("\n=== Demo 3: Simple Chord Progression ===")
    
    player = PianoPlayer(tempo=100)
    
    # Simple chord progression: C major - F major - G major - C major
    # This would normally be played simultaneously, but we'll play them as arpeggios
    chords = [
        "C4_0.5 E4_0.5 G4_0.5 C5_0.5",  # C major arpeggio
        "F4_0.5 A4_0.5 C5_0.5 F5_0.5",  # F major arpeggio  
        "G4_0.5 B4_0.5 D5_0.5 G5_0.5",  # G major arpeggio
        "C4_0.5 E4_0.5 G4_0.5 C5_2.0",  # C major arpeggio with long final note
    ]
    
    for chord_notation in chords:
        notes = SheetMusicParser.parse_simple_notation(chord_notation)
        player.play_melody(notes)

if __name__ == "__main__":
    print("Piano Player Demo - How Apps Play Music from Sheet Music")
    print("=" * 60)
    print("\nThis demonstration shows the key concepts:")
    print("1. Music notation parsing (converting sheet music to data)")
    print("2. Frequency calculation (converting notes to sound frequencies)")
    print("3. Audio synthesis (generating sound waves)")
    print("4. Timing control (playing notes at correct tempo)")
    print("\nPress Ctrl+C to stop at any time.\n")
    
    try:
        demo_simple_scale()
        time.sleep(1)
        
        demo_mary_had_a_little_lamb()
        time.sleep(1)
        
        demo_chord_progression()
        
    except KeyboardInterrupt:
        print("\nDemo stopped by user.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you have the required dependencies installed:")
        print("pip install pygame numpy")
