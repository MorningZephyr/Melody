from music21 import converter

def parse_midi_file(midi_file_path):
    """Parse MIDI file and return structured note data"""
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
                    note_data = {
                        'pitch': note.pitch.nameWithOctave,
                        'midi': note.pitch.midi,
                        'offset': float(note.offset),
                        'duration': float(note.quarterLength),
                        'part': part_index
                    }
                    all_notes.append(note_data)
    
    return all_notes

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