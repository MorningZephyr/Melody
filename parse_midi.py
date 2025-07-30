from music21 import converter

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