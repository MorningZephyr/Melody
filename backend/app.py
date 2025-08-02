from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sys
import numpy as np

# Add the parent directory to the path to import parse_midi
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse_midi import parse_midi_file, analyze_difficulty

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/api/parse-midi', methods=['POST'])
def parse_midi():
    """Parse MIDI file and return note data with finger assignments"""
    try:
        # For now, we'll use the existing MIDI file in parent directory
        midi_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Alla_Turca_Mozart.mid")
        
        if not os.path.exists(midi_file):
            return jsonify({'error': f'MIDI file not found at {midi_file}'}), 404
        
        # Parse the MIDI file
        notes_data = parse_midi_file(midi_file)
        
        # Analyze difficulty
        difficulty = analyze_difficulty(notes_data)
        
        # Add finger assignments to the notes
        notes_with_fingers = assign_fingers_to_notes(notes_data)
        
        # Generate hand positions
        hand_positions = generate_hand_positions(notes_with_fingers)
        
        return jsonify({
            'success': True,
            'notes': notes_with_fingers,
            'hand_positions': hand_positions,
            'difficulty': difficulty,
            'total_notes': len(notes_with_fingers)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def assign_fingers_to_notes(notes_data):
    """Assign optimal fingers to notes based on piano technique"""
    notes_with_fingers = []
    
    # Separate notes by hand (part)
    left_hand_notes = [n for n in notes_data if n.get('part') == 1]
    right_hand_notes = [n for n in notes_data if n.get('part') == 0]
    
    # Assign fingers for each hand
    if right_hand_notes:
        right_hand_notes = assign_fingers_to_hand(right_hand_notes, hand='right')
    if left_hand_notes:
        left_hand_notes = assign_fingers_to_hand(left_hand_notes, hand='left')
    
    # Combine and sort by offset
    notes_with_fingers = right_hand_notes + left_hand_notes
    notes_with_fingers.sort(key=lambda x: x['offset'])
    
    return notes_with_fingers

def assign_fingers_to_hand(notes, hand='right'):
    """Assign fingers to notes for a specific hand using piano fingering rules"""
    if not notes:
        return notes
    
    # Sort notes by offset
    notes.sort(key=lambda x: x['offset'])
    
    for i, note in enumerate(notes):
        midi = note.get('midi', 60)
        
        # Basic finger assignment based on position and context
        if hand == 'right':
            finger = assign_right_hand_finger(midi, i, notes)
        else:
            finger = assign_left_hand_finger(midi, i, notes)
        
        note['finger'] = finger
        note['hand'] = hand
        
        # Add finger name for display
        finger_names = {
            1: 'Thumb',
            2: 'Index',
            3: 'Middle',
            4: 'Ring',
            5: 'Pinky'
        }
        note['finger_name'] = finger_names.get(finger, 'Unknown')
    
    return notes

def assign_right_hand_finger(midi, note_index, notes):
    """Assign finger for right hand based on MIDI note and context"""
    # Middle C is MIDI 60
    # Right hand typically plays from middle C upwards
    
    if midi <= 60:  # C4 and below
        return 1  # Thumb
    elif midi <= 62:  # D4
        return 2  # Index
    elif midi <= 64:  # E4
        return 3  # Middle
    elif midi <= 65:  # F4
        return 4  # Ring
    elif midi <= 67:  # G4
        return 5  # Pinky
    elif midi <= 69:  # A4
        return 1  # Back to thumb for higher register
    elif midi <= 71:  # B4
        return 2
    elif midi <= 72:  # C5
        return 3
    elif midi <= 74:  # D5
        return 4
    elif midi <= 76:  # E5
        return 5
    else:  # Higher notes
        # Use pattern: 1,2,3,1,2,3,4,5 for scales
        relative_position = (midi - 77) % 8
        return [1, 2, 3, 1, 2, 3, 4, 5][relative_position]

def assign_left_hand_finger(midi, note_index, notes):
    """Assign finger for left hand based on MIDI note and context"""
    # Left hand typically plays below middle C
    
    if midi >= 60:  # C4 and above
        return 1  # Thumb
    elif midi >= 58:  # A#3
        return 2  # Index
    elif midi >= 56:  # G#3
        return 3  # Middle
    elif midi >= 55:  # G3
        return 4  # Ring
    elif midi >= 53:  # F3
        return 5  # Pinky
    elif midi >= 51:  # D#3
        return 1  # Back to thumb for lower register
    elif midi >= 49:  # C#3
        return 2
    elif midi >= 48:  # C3
        return 3
    elif midi >= 46:  # A#2
        return 4
    elif midi >= 44:  # G#2
        return 5
    else:  # Lower notes
        relative_position = (44 - midi) % 8
        return [5, 4, 3, 2, 1, 5, 4, 3][relative_position]

def generate_hand_positions(notes_with_fingers):
    """Generate hand position data for visualization"""
    positions = []
    
    # Group notes by time offset
    time_groups = {}
    for note in notes_with_fingers:
        offset = round(note['offset'], 2)
        if offset not in time_groups:
            time_groups[offset] = []
        time_groups[offset].append(note)
    
    for offset, notes in sorted(time_groups.items()):
        position = {
            'time': offset,
            'left_hand': {},
            'right_hand': {}
        }
        
        for note in notes:
            hand = note.get('hand', 'right')
            finger = note.get('finger', 1)
            
            hand_key = f"{hand}_hand"
            if hand_key not in position:
                position[hand_key] = {}
            
            position[hand_key][finger] = {
                'note': note['pitch'],
                'midi': note['midi'],
                'active': True
            }
        
        positions.append(position)
    
    return positions

@app.route('/api/hand-analysis', methods=['POST'])
def analyze_hand_position():
    """Analyze hand position and provide technique suggestions"""
    try:
        data = request.get_json()
        notes = data.get('notes', [])
        
        suggestions = []
        
        # Analyze finger independence
        if len(notes) > 1:
            suggestions.append({
                'type': 'technique',
                'message': 'Practice finger independence by playing each note separately first'
            })
        
        # Check for stretches
        midi_notes = [note.get('midi', 60) for note in notes]
        if max(midi_notes) - min(midi_notes) > 12:  # More than an octave
            suggestions.append({
                'type': 'stretch',
                'message': 'This passage requires a wide hand span. Relax your wrist and use arm weight'
            })
        
        # Check for difficult finger combinations
        fingers = [note.get('finger', 1) for note in notes]
        if 4 in fingers and 5 in fingers:  # Ring and pinky together
            suggestions.append({
                'type': 'fingering',
                'message': 'Ring and pinky fingers together - practice slowly and keep other fingers relaxed'
            })
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-midi', methods=['POST'])
def upload_midi():
    """Upload and parse a new MIDI file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.lower().endswith('.mid'):
            # Save the uploaded file
            filename = f"uploaded_{file.filename}"
            filepath = os.path.join(os.path.dirname(__file__), '..', filename)
            file.save(filepath)
            
            # Parse the uploaded file
            notes_data = parse_midi_file(filepath)
            difficulty = analyze_difficulty(notes_data)
            notes_with_fingers = assign_fingers_to_notes(notes_data)
            hand_positions = generate_hand_positions(notes_with_fingers)
            
            return jsonify({
                'success': True,
                'notes': notes_with_fingers,
                'hand_positions': hand_positions,
                'difficulty': difficulty,
                'total_notes': len(notes_with_fingers),
                'filename': filename
            })
        else:
            return jsonify({'error': 'Please upload a MIDI file (.mid)'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Piano Learning API is running'})

if __name__ == '__main__':
    print("Starting Piano Learning Backend...")
    print("Features:")
    print("- MIDI file parsing and analysis")
    print("- Intelligent finger assignment")
    print("- Difficulty assessment")
    print("- Hand position visualization")
    print("\nAccess the web app at: http://localhost:5000")
    print("API Documentation:")
    print("- POST /api/parse-midi - Parse default MIDI file")
    print("- POST /api/hand-analysis - Analyze hand position")
    print("- GET /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 