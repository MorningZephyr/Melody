from music21 import converter, chord
import numpy as np

def parse_midi_file(midi_file_path):
    """Parse MIDI file and return structured note data with enhanced analysis"""
    print(f"Parsing {midi_file_path}")
    score = converter.parse(midi_file_path)
    
    print("Parsed successfully!")
    print("Number of parts:", len(score.parts))
    
    all_notes = []
    
    if score.parts:
        # Process each part (hand)
        for part_index, part in enumerate(score.parts):
            notes = part.flatten().notes
            
            print(f"Notes in part {part_index + 1}:", len(notes))
            
            # Convert notes to structured data
            for note in notes:
                if hasattr(note, 'pitch'):
                    # Single note
                    note_data = {
                        'pitch': note.pitch.nameWithOctave,
                        'midi': note.pitch.midi,
                        'offset': float(note.offset),
                        'duration': float(note.quarterLength),
                        'part': part_index,
                        'type': 'note',
                        'velocity': getattr(note, 'velocity', 64)
                    }
                    all_notes.append(note_data)
                elif hasattr(note, 'pitches'):
                    # Chord - create individual notes for each pitch
                    for pitch in note.pitches:
                        note_data = {
                            'pitch': pitch.nameWithOctave,
                            'midi': pitch.midi,
                            'offset': float(note.offset),
                            'duration': float(note.quarterLength),
                            'part': part_index,
                            'type': 'chord',
                            'velocity': getattr(note, 'velocity', 64)
                        }
                        all_notes.append(note_data)
    
    # Sort notes by offset time
    all_notes.sort(key=lambda x: x['offset'])
    
    return all_notes

def analyze_difficulty(notes_data):
    """Analyze the difficulty level of the piece"""
    if not notes_data:
        return {'level': 'Unknown', 'score': 0, 'factors': []}
    
    factors = []
    score = 0
    
    # Calculate note span
    midi_notes = [note['midi'] for note in notes_data]
    note_span = max(midi_notes) - min(midi_notes)
    if note_span > 36:  # More than 3 octaves
        factors.append("Wide note range")
        score += 2
    elif note_span > 24:  # More than 2 octaves
        score += 1
    
    # Calculate tempo complexity (based on note durations)
    durations = [note['duration'] for note in notes_data]
    min_duration = min(durations)
    if min_duration < 0.25:  # Sixteenth notes or faster
        factors.append("Fast passages")
        score += 2
    elif min_duration < 0.5:
        factors.append("Quick notes")
        score += 1
    
    # Check for chords
    chord_count = sum(1 for note in notes_data if note.get('type') == 'chord')
    if chord_count > len(notes_data) * 0.3:
        factors.append("Many chords")
        score += 1
    
    # Determine level
    if score >= 5:
        level = "Advanced"
    elif score >= 3:
        level = "Intermediate"
    elif score >= 1:
        level = "Beginner+"
    else:
        level = "Beginner"
    
    return {
        'level': level,
        'score': score,
        'factors': factors,
        'note_span': note_span,
        'total_notes': len(notes_data)
    }

if __name__ == "__main__":
    # Original functionality for testing
    print("Parsing Mozart Alla Turca")
    score = converter.parse("Alla_Turca_Mozart.mid")

    print("Parsed successfully!")
    print("Number of parts:", len(score.parts))

    if score.parts:
        first_part = score.parts[0]
        notes = first_part.flatten().notes
        
        print("Notes in first part:", len(notes))
        print("First 5 elements:")
        
        for i, element in enumerate(notes[:5]):
            if hasattr(element, 'pitch'):
                print(f"{i+1}. {element.pitch.nameWithOctave} - MIDI: {element.pitch.midi}")
                print(f"   Offset: {element.offset}, Duration: {element.quarterLength}")