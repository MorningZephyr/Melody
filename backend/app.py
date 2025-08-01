from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys

# Add the parent directory to the path to import parse_midi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse_midi import parse_midi_file

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/api/parse-midi', methods=['POST'])
def parse_midi():
    """Parse MIDI file and return note data with finger assignments"""
    try:
        # For now, we'll use the existing MIDI file
        midi_file = "Alla_Turca_Mozart.mid"
        
        if not os.path.exists(midi_file):
            return jsonify({'error': 'MIDI file not found'}), 404
        
        # Parse the MIDI file
        notes_data = parse_midi_file(midi_file)
        
        # Add finger assignments to the notes
        notes_with_fingers = assign_fingers_to_notes(notes_data)
        
        return jsonify({
            'success': True,
            'notes': notes_with_fingers,
            'total_notes': len(notes_with_fingers)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def assign_fingers_to_notes(notes_data):
    """Assign optimal fingers to notes based on piano technique"""
    notes_with_fingers = []
    
    for note in notes_data:
        # Extract note information
        pitch = note.get('pitch', '')
        midi = note.get('midi', 60)
        duration = note.get('duration', 1.0)
        offset = note.get('offset', 0.0)
        
        # Determine which hand to use (simplified logic)
        hand = 'right' if midi >= 60 else 'left'
        
        # Assign finger based on MIDI note number
        finger = assign_finger(midi, hand)
        
        notes_with_fingers.append({
            'pitch': pitch,
            'midi': midi,
            'duration': duration,
            'offset': offset,
            'finger': finger,
            'hand': hand
        })
    
    return notes_with_fingers

def assign_finger(midi, hand):
    """Simple finger assignment algorithm"""
    # Basic finger assignment based on note position in octave
    note_in_octave = midi % 12
    
    if hand == 'right':
        # Right hand finger assignment
        if note_in_octave in [0, 1]:  # C, C#
            return 'thumb'
        elif note_in_octave in [2, 3]:  # D, D#
            return 'index'
        elif note_in_octave in [4, 5]:  # E, F
            return 'middle'
        elif note_in_octave in [6, 7]:  # F#, G
            return 'ring'
        else:  # G#, A, A#, B
            return 'pinky'
    else:
        # Left hand finger assignment (mirrored)
        if note_in_octave in [0, 1]:  # C, C#
            return 'pinky'
        elif note_in_octave in [2, 3]:  # D, D#
            return 'ring'
        elif note_in_octave in [4, 5]:  # E, F
            return 'middle'
        elif note_in_octave in [6, 7]:  # F#, G
            return 'index'
        else:  # G#, A, A#, B
            return 'thumb'

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 