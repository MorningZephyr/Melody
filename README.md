# Piano Learning App MVP

A web application that teaches piano technique by showing finger positions and hand movements for playing pieces.

## Features

- **MIDI File Parsing**: Analyzes MIDI files to extract note data
- **Finger Assignment**: Automatically assigns optimal fingers to each note
- **Hand Visualization**: Shows which fingers to use on which keys
- **Real-time Playback**: Demonstrates finger movements as notes play
- **Hand Separation**: Supports both left and right hand parts

## Project Structure

```
Melody/
├── frontend/           # Web application
│   ├── index.html     # Main HTML page
│   ├── styles.css     # Styling
│   └── script.js      # Frontend logic
├── backend/           # Python Flask API
│   ├── app.py         # API endpoints
│   └── requirements.txt
├── parse_midi.py      # MIDI parsing logic
├── Alla_Turca_Mozart.mid  # Sample MIDI file
└── requirements.txt   # Main dependencies
```

## How to Run

### 1. Install Dependencies

```bash
# Install main requirements
pip install -r requirements.txt

# Install backend requirements
pip install -r backend/requirements.txt
```

### 2. Start the Backend

```bash
cd backend
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Open the Frontend

Open `frontend/index.html` in your web browser, or serve it with a local server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

## How It Works

### 1. MIDI Parsing
- The backend uses `music21` to parse MIDI files
- Extracts note data including pitch, timing, and duration
- Separates left and right hand parts

### 2. Finger Assignment
- Automatically assigns optimal fingers based on note position
- Considers hand ergonomics and reach
- Different algorithms for left vs right hand

### 3. Hand Visualization
- SVG-based hand illustration with 5 fingers
- Highlights which finger should press which key
- Shows hand position and movement

### 4. Real-time Feedback
- Piano keys light up when pressed
- Fingers highlight to show which one to use
- Information panel shows current note and finger assignment

## Current MVP Features

✅ **Basic MIDI parsing**  
✅ **Finger assignment algorithm**  
✅ **Hand visualization**  
✅ **Piano key highlighting**  
✅ **Real-time playback**  
✅ **Backend API integration**  

## Next Steps

- [ ] More sophisticated finger assignment algorithms
- [ ] Hand position optimization
- [ ] Technique pattern recognition (scales, arpeggios)
- [ ] Practice sequence generation
- [ ] Audio playback integration
- [ ] 3D hand models
- [ ] Progress tracking
- [ ] Multiple MIDI file support

## Technical Details

### Finger Assignment Logic
The app uses a simple algorithm based on note position within the octave:
- **Right Hand**: C/C# → thumb, D/D# → index, E/F → middle, F#/G → ring, G#/A/A#/B → pinky
- **Left Hand**: Mirrored assignment for ergonomic playing

### Hand Visualization
- SVG-based hand with 5 finger circles
- Each finger can be highlighted independently
- Labels show finger numbers (T, 1, 2, 3, 4)

### API Endpoints
- `POST /api/parse-midi` - Parse MIDI file and return note data with finger assignments
- `GET /api/health` - Health check endpoint

## Demo

The MVP includes sample data that demonstrates:
1. A C major scale (C4 to C5)
2. Finger assignments for each note
3. Hand visualization showing which finger to use
4. Real-time playback with finger highlighting

Click "Load MIDI File" to load the Mozart piece, or "Play/Pause" to see the demo in action! 