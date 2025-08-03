"""
Advanced Music Sheet Reader
Demonstrates how real apps parse standard music notation formats.

This shows how professional music apps handle:
1. Standard music notation formats (MIDI, MusicXML)
2. Complex timing with different note values
3. Key signatures and time signatures
4. Multiple voices/parts
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import json

class NoteValue(Enum):
    """Standard musical note durations"""
    WHOLE = 4.0
    HALF = 2.0
    QUARTER = 1.0
    EIGHTH = 0.5
    SIXTEENTH = 0.25
    THIRTY_SECOND = 0.125

class Accidental(Enum):
    """Musical accidentals"""
    NATURAL = ""
    SHARP = "#"
    FLAT = "b"
    DOUBLE_SHARP = "##"
    DOUBLE_FLAT = "bb"

@dataclass
class TimeSignature:
    """Represents time signature (e.g., 4/4, 3/4, 6/8)"""
    numerator: int    # Beats per measure
    denominator: int  # Note value that gets the beat

@dataclass
class KeySignature:
    """Represents key signature"""
    key: str          # Key name (C, G, D, etc.)
    mode: str = "major"  # major or minor
    sharps: int = 0   # Number of sharps (positive) or flats (negative)

@dataclass
class MusicalNote:
    """Advanced note representation matching real sheet music"""
    pitch: str                    # Note name (C, D, E, etc.)
    octave: int                  # Octave number
    duration: NoteValue          # Note duration
    accidental: Accidental = Accidental.NATURAL
    dots: int = 0               # Number of dots (extend duration)
    tied: bool = False          # Whether note is tied to next
    measure: int = 1            # Measure number
    beat: float = 1.0          # Beat position within measure
    voice: int = 1             # Voice/part number (for multiple parts)
    dynamics: str = "mf"       # Dynamic marking (pp, p, mp, mf, f, ff)

@dataclass
class Measure:
    """Represents a musical measure/bar"""
    number: int
    notes: List[MusicalNote]
    time_signature: TimeSignature
    key_signature: KeySignature

class MusicSheet:
    """Represents a complete piece of sheet music"""
    
    def __init__(self, title: str = "Untitled"):
        self.title = title
        self.composer = ""
        self.tempo = 120  # BPM
        self.measures: List[Measure] = []
        self.default_time_sig = TimeSignature(4, 4)
        self.default_key_sig = KeySignature("C")
    
    def add_measure(self, measure: Measure):
        """Add a measure to the sheet"""
        self.measures.append(measure)
    
    def get_total_duration(self) -> float:
        """Calculate total duration in beats"""
        total = 0.0
        for measure in self.measures:
            for note in measure.notes:
                duration = note.duration.value
                # Apply dots (each dot adds half the value of the previous duration)
                dot_multiplier = 1.0
                for _ in range(note.dots):
                    dot_multiplier += 0.5 ** (_ + 1)
                total += duration * dot_multiplier
        return total

class SheetMusicReader:
    """Demonstrates how apps parse different music notation formats"""
    
    @staticmethod
    def parse_abc_notation(abc_text: str) -> MusicSheet:
        """
        Parse ABC notation (a simple text format for music)
        Example ABC: "C D E F | G A B c |"
        """
        sheet = MusicSheet()
        lines = abc_text.strip().split('\n')
        
        current_measure = 1
        current_beat = 1.0
        
        for line in lines:
            if line.startswith('T:'):  # Title
                sheet.title = line[2:].strip()
            elif line.startswith('C:'):  # Composer
                sheet.composer = line[2:].strip()
            elif line.startswith('Q:'):  # Tempo
                tempo_str = line[2:].strip()
                if tempo_str.isdigit():
                    sheet.tempo = int(tempo_str)
            elif not line.startswith(('X:', 'T:', 'C:', 'M:', 'L:', 'K:')):
                # Parse notes
                notes = SheetMusicReader._parse_abc_notes(line, current_measure, current_beat)
                if notes:
                    measure = Measure(
                        current_measure,
                        notes,
                        sheet.default_time_sig,
                        sheet.default_key_sig
                    )
                    sheet.add_measure(measure)
                    current_measure += 1
        
        return sheet
    
    @staticmethod
    def _parse_abc_notes(note_line: str, measure_num: int, start_beat: float) -> List[MusicalNote]:
        """Parse ABC notation notes from a line"""
        notes = []
        tokens = note_line.replace('|', '').strip().split()
        beat = start_beat
        
        for token in tokens:
            if token:
                # Simple parsing - in real ABC, this would be much more complex
                note_char = token[0].upper()
                octave = 4
                
                # Handle octave indicators
                if token[0].islower():
                    octave = 5  # Lowercase = higher octave
                
                # Handle accidentals
                accidental = Accidental.NATURAL
                if '^' in token:
                    accidental = Accidental.SHARP
                elif '_' in token:
                    accidental = Accidental.FLAT
                
                # Default to quarter notes for simplicity
                duration = NoteValue.QUARTER
                
                note = MusicalNote(
                    pitch=note_char,
                    octave=octave,
                    duration=duration,
                    accidental=accidental,
                    measure=measure_num,
                    beat=beat
                )
                notes.append(note)
                beat += duration.value
        
        return notes
    
    @staticmethod
    def create_sample_sheet() -> MusicSheet:
        """Create a sample sheet music for demonstration"""
        sheet = MusicSheet("Twinkle Twinkle Little Star")
        sheet.composer = "Traditional"
        sheet.tempo = 120
        
        # Measure 1: Twinkle twinkle (C C G G)
        measure1_notes = [
            MusicalNote("C", 4, NoteValue.QUARTER, measure=1, beat=1.0),
            MusicalNote("C", 4, NoteValue.QUARTER, measure=1, beat=2.0),
            MusicalNote("G", 4, NoteValue.QUARTER, measure=1, beat=3.0),
            MusicalNote("G", 4, NoteValue.QUARTER, measure=1, beat=4.0),
        ]
        measure1 = Measure(1, measure1_notes, sheet.default_time_sig, sheet.default_key_sig)
        
        # Measure 2: little star (A A G)
        measure2_notes = [
            MusicalNote("A", 4, NoteValue.QUARTER, measure=2, beat=1.0),
            MusicalNote("A", 4, NoteValue.QUARTER, measure=2, beat=2.0),
            MusicalNote("G", 4, NoteValue.HALF, measure=2, beat=3.0),
        ]
        measure2 = Measure(2, measure2_notes, sheet.default_time_sig, sheet.default_key_sig)
        
        # Measure 3: How I wonder (F F E E)
        measure3_notes = [
            MusicalNote("F", 4, NoteValue.QUARTER, measure=3, beat=1.0),
            MusicalNote("F", 4, NoteValue.QUARTER, measure=3, beat=2.0),
            MusicalNote("E", 4, NoteValue.QUARTER, measure=3, beat=3.0),
            MusicalNote("E", 4, NoteValue.QUARTER, measure=3, beat=4.0),
        ]
        measure3 = Measure(3, measure3_notes, sheet.default_time_sig, sheet.default_key_sig)
        
        # Measure 4: what you are (D D C)
        measure4_notes = [
            MusicalNote("D", 4, NoteValue.QUARTER, measure=4, beat=1.0),
            MusicalNote("D", 4, NoteValue.QUARTER, measure=4, beat=2.0),
            MusicalNote("C", 4, NoteValue.HALF, measure=4, beat=3.0),
        ]
        measure4 = Measure(4, measure4_notes, sheet.default_time_sig, sheet.default_key_sig)
        
        sheet.add_measure(measure1)
        sheet.add_measure(measure2)
        sheet.add_measure(measure3)
        sheet.add_measure(measure4)
        
        return sheet

class MusicAnalyzer:
    """Analyzes sheet music for various properties"""
    
    @staticmethod
    def analyze_sheet(sheet: MusicSheet) -> Dict:
        """Analyze a music sheet and return statistics"""
        analysis = {
            'title': sheet.title,
            'composer': sheet.composer,
            'tempo': sheet.tempo,
            'total_measures': len(sheet.measures),
            'total_notes': 0,
            'note_distribution': {},
            'rhythm_complexity': 0.0,
            'range': {'lowest': None, 'highest': None},
            'key_signature': sheet.default_key_sig.key,
            'time_signature': f"{sheet.default_time_sig.numerator}/{sheet.default_time_sig.denominator}"
        }
        
        all_notes = []
        note_counts = {}
        
        for measure in sheet.measures:
            for note in measure.notes:
                all_notes.append(note)
                analysis['total_notes'] += 1
                
                # Count note occurrences
                note_name = f"{note.pitch}{note.accidental.value}"
                note_counts[note_name] = note_counts.get(note_name, 0) + 1
                
                # Track range
                note_value = MusicAnalyzer._note_to_midi(note)
                if analysis['range']['lowest'] is None or note_value < analysis['range']['lowest']:
                    analysis['range']['lowest'] = note_value
                if analysis['range']['highest'] is None or note_value > analysis['range']['highest']:
                    analysis['range']['highest'] = note_value
        
        analysis['note_distribution'] = note_counts
        
        # Calculate rhythm complexity (variety of note durations)
        durations = [note.duration.value for note in all_notes]
        unique_durations = len(set(durations))
        analysis['rhythm_complexity'] = unique_durations / len(durations) if durations else 0
        
        return analysis
    
    @staticmethod
    def _note_to_midi(note: MusicalNote) -> int:
        """Convert a musical note to MIDI note number"""
        note_values = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        base_value = note_values.get(note.pitch, 0)
        
        # Apply accidental
        if note.accidental == Accidental.SHARP:
            base_value += 1
        elif note.accidental == Accidental.FLAT:
            base_value -= 1
        
        # MIDI note number = (octave + 1) * 12 + note_value
        return (note.octave + 1) * 12 + base_value

def demonstrate_sheet_music_reading():
    """Demonstrate how apps read and analyze sheet music"""
    print("=== Sheet Music Reading Demo ===")
    print("\n1. Creating sample sheet music...")
    
    # Create sample sheet
    sheet = SheetMusicReader.create_sample_sheet()
    
    print(f"Created: '{sheet.title}' by {sheet.composer}")
    print(f"Tempo: {sheet.tempo} BPM")
    print(f"Measures: {len(sheet.measures)}")
    
    print("\n2. Sheet music content:")
    for measure in sheet.measures:
        print(f"\nMeasure {measure.number}:")
        for note in measure.notes:
            duration_name = note.duration.name.lower().replace('_', ' ')
            accidental = note.accidental.value
            print(f"  Beat {note.beat}: {note.pitch}{accidental}{note.octave} ({duration_name} note)")
    
    print("\n3. Music analysis:")
    analysis = MusicAnalyzer.analyze_sheet(sheet)
    
    print(f"Total notes: {analysis['total_notes']}")
    print(f"Key signature: {analysis['key_signature']}")
    print(f"Time signature: {analysis['time_signature']}")
    print(f"Note range: MIDI {analysis['range']['lowest']} to {analysis['range']['highest']}")
    print(f"Rhythm complexity: {analysis['rhythm_complexity']:.2f}")
    
    print("\nNote distribution:")
    for note, count in analysis['note_distribution'].items():
        print(f"  {note}: {count} times")
    
    print("\n4. Demonstrating ABC notation parsing:")
    abc_sample = """T:Simple Scale
C:Demo Composer
Q:120
C D E F | G A B c |"""
    
    print("ABC notation input:")
    print(abc_sample)
    
    abc_sheet = SheetMusicReader.parse_abc_notation(abc_sample)
    print(f"\nParsed: '{abc_sheet.title}' by {abc_sheet.composer}")
    
    print("\n=== How Real Apps Process Sheet Music ===")
    print("""
Real music applications process sheet music through several steps:

1. FILE FORMAT PARSING:
   - MIDI files: Binary format with precise timing and note data
   - MusicXML: XML format preserving visual layout and notation
   - ABC notation: Text format for simple melodies
   - Proprietary formats: Sibelius, Finale, MuseScore files

2. MUSIC THEORY PROCESSING:
   - Parse time signatures, key signatures, clefs
   - Handle complex rhythms (tuplets, syncopation)
   - Process articulations (staccato, legato, accents)
   - Interpret expression markings (dynamics, tempo changes)

3. AUDIO SYNTHESIS:
   - Convert notes to frequencies using equal temperament
   - Apply instrument samples or synthesis algorithms
   - Handle effects (reverb, velocity, pedaling)
   - Mix multiple voices/instruments

4. TIMING ENGINE:
   - Precise timing based on tempo and note values
   - Handle tempo changes and ritardando/accelerando
   - Coordinate multiple parts in ensemble pieces
   - Account for human-like timing variations

5. USER INTERFACE:
   - Display sheet music visually
   - Highlight currently playing notes
   - Allow tempo, volume, and playback controls
   - Enable editing and annotation
""")

if __name__ == "__main__":
    demonstrate_sheet_music_reading()
