"""
MIDI File Processor
Demonstrates how apps read and process MIDI files (the most common digital sheet music format).

MIDI (Musical Instrument Digital Interface) files contain:
- Note on/off events with precise timing
- Velocity (how hard a key is pressed)
- Multiple tracks/channels for different instruments
- Tempo changes and other musical events
"""

import struct
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class MidiEventType(Enum):
    """MIDI event types"""
    NOTE_OFF = 0x80
    NOTE_ON = 0x90
    AFTERTOUCH = 0xA0
    CONTROL_CHANGE = 0xB0
    PROGRAM_CHANGE = 0xC0
    CHANNEL_PRESSURE = 0xD0
    PITCH_BEND = 0xE0
    SYSTEM_EXCLUSIVE = 0xF0

@dataclass
class MidiEvent:
    """Represents a MIDI event"""
    delta_time: int      # Time since last event (in ticks)
    event_type: int      # Event type byte
    channel: int         # MIDI channel (0-15)
    data1: int          # First data byte (note number for note events)
    data2: int          # Second data byte (velocity for note events)
    absolute_time: int = 0  # Absolute time from start

@dataclass
class MidiNote:
    """Represents a complete MIDI note (note on + note off)"""
    note_number: int     # MIDI note number (60 = Middle C)
    velocity: int        # Note velocity (0-127)
    start_time: int      # Start time in ticks
    duration: int        # Duration in ticks
    channel: int         # MIDI channel

class SimpleMidiParser:
    """Simplified MIDI file parser for demonstration"""
    
    def __init__(self):
        self.ticks_per_quarter = 480  # Default MIDI resolution
        self.tempo = 500000  # Microseconds per quarter note (120 BPM)
        
    def parse_midi_data(self, midi_bytes: bytes) -> Tuple[List[MidiEvent], Dict]:
        """Parse MIDI file bytes into events and metadata"""
        events = []
        metadata = {
            'format': 0,
            'tracks': 1,
            'ticks_per_quarter': self.ticks_per_quarter,
            'tempo_bpm': 120
        }
        
        # This is a simplified parser - real MIDI parsing is much more complex
        # In practice, you'd use a library like python-midi or mido
        
        # For demonstration, we'll create some sample events
        sample_events = [
            MidiEvent(0, 0x90, 0, 60, 100),    # Note On: Middle C, velocity 100
            MidiEvent(480, 0x80, 0, 60, 0),    # Note Off: Middle C after 1 quarter note
            MidiEvent(0, 0x90, 0, 64, 90),     # Note On: E, velocity 90
            MidiEvent(480, 0x80, 0, 64, 0),    # Note Off: E after 1 quarter note
            MidiEvent(0, 0x90, 0, 67, 80),     # Note On: G, velocity 80
            MidiEvent(960, 0x80, 0, 67, 0),    # Note Off: G after 2 quarter notes
        ]
        
        # Calculate absolute times
        absolute_time = 0
        for event in sample_events:
            absolute_time += event.delta_time
            event.absolute_time = absolute_time
            events.append(event)
            
        return events, metadata
    
    def events_to_notes(self, events: List[MidiEvent]) -> List[MidiNote]:
        """Convert MIDI events to note objects"""
        notes = []
        note_on_events = {}  # Track active notes
        
        for event in events:
            if event.event_type == 0x90 and event.data2 > 0:  # Note On
                note_key = (event.channel, event.data1)
                note_on_events[note_key] = event
                
            elif event.event_type == 0x80 or (event.event_type == 0x90 and event.data2 == 0):  # Note Off
                note_key = (event.channel, event.data1)
                if note_key in note_on_events:
                    note_on = note_on_events[note_key]
                    
                    # Create completed note
                    note = MidiNote(
                        note_number=note_on.data1,
                        velocity=note_on.data2,
                        start_time=note_on.absolute_time,
                        duration=event.absolute_time - note_on.absolute_time,
                        channel=note_on.channel
                    )
                    notes.append(note)
                    
                    # Remove from active notes
                    del note_on_events[note_key]
        
        return notes
    
    def ticks_to_seconds(self, ticks: int) -> float:
        """Convert MIDI ticks to seconds"""
        # seconds = (ticks / ticks_per_quarter) * (tempo_microseconds / 1_000_000)
        seconds_per_tick = (self.tempo / 1_000_000) / self.ticks_per_quarter
        return ticks * seconds_per_tick
    
    def midi_note_to_frequency(self, note_number: int) -> float:
        """Convert MIDI note number to frequency in Hz"""
        # A4 (note 69) = 440 Hz
        return 440.0 * (2.0 ** ((note_number - 69) / 12.0))
    
    def midi_note_to_name(self, note_number: int) -> str:
        """Convert MIDI note number to note name"""
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (note_number // 12) - 1
        note = note_names[note_number % 12]
        return f"{note}{octave}"

class MidiPlayer:
    """Demonstrates how apps play MIDI files"""
    
    def __init__(self, parser: SimpleMidiParser):
        self.parser = parser
        
    def analyze_midi_file(self, midi_data: bytes) -> Dict:
        """Analyze a MIDI file and return information about it"""
        events, metadata = self.parser.parse_midi_data(midi_data)
        notes = self.parser.events_to_notes(events)
        
        analysis = {
            'total_events': len(events),
            'total_notes': len(notes),
            'duration_ticks': max(event.absolute_time for event in events) if events else 0,
            'duration_seconds': 0,
            'note_range': {'lowest': None, 'highest': None},
            'channels_used': set(),
            'tempo_bpm': metadata['tempo_bpm'],
            'time_signature': '4/4',  # Simplified
            'notes_by_channel': {}
        }
        
        # Calculate duration in seconds
        if analysis['duration_ticks'] > 0:
            analysis['duration_seconds'] = self.parser.ticks_to_seconds(analysis['duration_ticks'])
        
        # Analyze notes
        for note in notes:
            # Track note range
            if analysis['note_range']['lowest'] is None or note.note_number < analysis['note_range']['lowest']:
                analysis['note_range']['lowest'] = note.note_number
            if analysis['note_range']['highest'] is None or note.note_number > analysis['note_range']['highest']:
                analysis['note_range']['highest'] = note.note_number
            
            # Track channels
            analysis['channels_used'].add(note.channel)
            
            # Group notes by channel
            if note.channel not in analysis['notes_by_channel']:
                analysis['notes_by_channel'][note.channel] = []
            analysis['notes_by_channel'][note.channel].append(note)
        
        return analysis, notes
    
    def print_note_sequence(self, notes: List[MidiNote]):
        """Print the sequence of notes in the MIDI file"""
        print("\nNote Sequence:")
        print("-" * 80)
        print(f"{'Time (s)':<10} {'Note':<8} {'Frequency':<12} {'Velocity':<10} {'Duration':<10}")
        print("-" * 80)
        
        for note in sorted(notes, key=lambda n: n.start_time):
            start_seconds = self.parser.ticks_to_seconds(note.start_time)
            duration_seconds = self.parser.ticks_to_seconds(note.duration)
            note_name = self.parser.midi_note_to_name(note.note_number)
            frequency = self.parser.midi_note_to_frequency(note.note_number)
            
            print(f"{start_seconds:<10.2f} {note_name:<8} {frequency:<12.1f} {note.velocity:<10} {duration_seconds:<10.2f}")

def demonstrate_midi_processing():
    """Demonstrate how apps process MIDI files"""
    print("=== MIDI File Processing Demo ===")
    print("\nMIDI (Musical Instrument Digital Interface) is the standard format")
    print("for digital sheet music. Here's how apps process MIDI files:\n")
    
    # Create parser and player
    parser = SimpleMidiParser()
    player = MidiPlayer(parser)
    
    # Simulate MIDI file data (normally this would be read from a .mid file)
    print("1. Loading and parsing MIDI data...")
    midi_data = b""  # Placeholder - would contain actual MIDI file bytes
    
    # Analyze the MIDI file
    analysis, notes = player.analyze_midi_file(midi_data)
    
    print(f"\n2. MIDI File Analysis:")
    print(f"   Total events: {analysis['total_events']}")
    print(f"   Total notes: {analysis['total_notes']}")
    print(f"   Duration: {analysis['duration_seconds']:.2f} seconds")
    print(f"   Tempo: {analysis['tempo_bpm']} BPM")
    print(f"   Channels used: {sorted(analysis['channels_used'])}")
    
    if analysis['note_range']['lowest'] is not None:
        lowest_name = parser.midi_note_to_name(analysis['note_range']['lowest'])
        highest_name = parser.midi_note_to_name(analysis['note_range']['highest'])
        print(f"   Note range: {lowest_name} to {highest_name}")
    
    # Show note sequence
    if notes:
        player.print_note_sequence(notes)
    
    print(f"\n3. How MIDI Events Become Audio:")
    print("   Each MIDI note event contains:")
    print("   - Note number (pitch): 0-127 (60 = Middle C)")
    print("   - Velocity (volume): 0-127 (how hard key was pressed)")
    print("   - Timing: Precise start time and duration")
    print("   - Channel: Which instrument/voice (0-15)")
    
    print(f"\n4. Conversion to Audio:")
    if notes:
        sample_note = notes[0]
        frequency = parser.midi_note_to_frequency(sample_note.note_number)
        note_name = parser.midi_note_to_name(sample_note.note_number)
        
        print(f"   Example: Note {sample_note.note_number} ({note_name})")
        print(f"   - Converts to frequency: {frequency:.1f} Hz")
        print(f"   - Volume based on velocity: {sample_note.velocity}/127")
        print(f"   - Duration: {parser.ticks_to_seconds(sample_note.duration):.2f} seconds")
    
    print(f"\n=== Real MIDI File Processing ===")
    print("""
Real MIDI file processing involves:

1. BINARY FILE PARSING:
   - Header chunk: File format, track count, time division
   - Track chunks: Sequence of time-stamped events
   - Variable-length quantities for compact data storage

2. EVENT PROCESSING:
   - Note On/Off events (0x90/0x80)
   - Control changes (volume, pan, pedal)
   - Program changes (instrument selection)
   - Meta events (tempo, time signature, lyrics)

3. TIMING RESOLUTION:
   - Ticks per quarter note (typically 96-960)
   - Tempo changes affect tick-to-time conversion
   - Precise timing for musical expression

4. MULTI-TRACK COORDINATION:
   - Separate tracks for different instruments
   - Synchronized playback across all tracks
   - Individual control over each track's volume/effects

5. REAL-TIME PLAYBACK:
   - Event scheduling based on timestamps
   - Buffer management for smooth audio
   - Low-latency response for interactive playing

Popular libraries for MIDI processing:
- Python: mido, python-midi, pretty_midi
- JavaScript: midi-parser-js, JZZ
- C++: RtMidi, PortMidi
- Java: Java Sound API
""")

if __name__ == "__main__":
    demonstrate_midi_processing()
