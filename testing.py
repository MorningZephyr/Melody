from music21 import converter, note, stream

def create_simple_midi():
    """Create a simple MIDI file in memory for testing"""
    
    # Create a simple melody: C-D-E-F-G
    notes_data = [
        (60, 0.0, 1.0),  # C4 at beat 0, duration 1
        (62, 1.0, 1.0),  # D4 at beat 1, duration 1  
        (64, 2.0, 1.0),  # E4 at beat 2, duration 1
        (65, 3.0, 1.0),  # F4 at beat 3, duration 1
        (67, 4.0, 1.0),  # G4 at beat 4, duration 1
    ]
    
    # Create a music21 stream
    melody = stream.Stream()
    
    for pitch, offset, duration in notes_data:
        n = note.Note(pitch)
        n.offset = offset
        n.quarterLength = duration
        melody.append(n)
    
    return melody

def explore_music21_structure():
    """Explore what music21 gives us"""
    
    print("🎵 Exploring Music21 MIDI Structure")
    print("=" * 50)

    # Create our test melody
    melody = create_simple_midi()
    
    print("📊 Whats in a music21 Stream:")
    print(f"Stream type: {type(melody)}")
    print(f"Number of elements: {len(melody)}")
    print()
    
    print("🎼 Individual Notes:")
    for i, element in enumerate(melody.notes):
        print(f"\nNote {i+1}:")
        print(f"  Type: {type(element)}")
        print(f"  Pitch: {element.pitch}")
        print(f"  MIDI Number: {element.pitch.midi}")
        print(f"  Name: {element.pitch.name}")
        print(f"  Offset (start time): {element.offset}")
        print(f"  Duration: {element.quarterLength}")

if __name__ == "__main__":
    explore_music21_structure()