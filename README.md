# 🎹 Piano Technique Master

An advanced web application that teaches piano technique through AI-powered finger positioning, hand visualization, and interactive learning experiences.

## ✨ Features

### 🎵 **MIDI Analysis & Processing**
- **Advanced MIDI Parsing**: Analyzes complex piano pieces with multi-hand support
- **Intelligent Finger Assignment**: AI-driven fingering suggestions based on classical piano technique
- **Difficulty Assessment**: Automatic evaluation of piece complexity with detailed analysis
- **Hand Separation**: Independent analysis and visualization for left and right hands

### 🎯 **Interactive Learning**
- **Real-time Hand Visualization**: SVG-based finger positioning with visual feedback
- **Piano Key Mapping**: Interactive 3-octave piano with finger indicators
- **Playback Control**: Variable tempo playback with note-by-note progression
- **Technique Suggestions**: Personalized tips based on current hand position

### 🚀 **Advanced Features**
- **Modern UI/UX**: Responsive design with glassmorphism effects
- **Keyboard Navigation**: Full keyboard shortcuts for hands-free learning
- **Progress Tracking**: Visual progress indicators and learning statistics
- **Multiple View Modes**: Focus on individual hands or combined visualization

### 🤖 **Future AI Integration**
- **Computer Vision Ready**: Architecture prepared for hand tracking integration
- **Machine Learning Pipeline**: Foundation for training on pianist hand positions
- **Adaptive Learning**: Personalized technique recommendations

## 🏗️ Project Architecture

```
Melody/
├── frontend/                 # Modern React-style Web Application
│   ├── index.html           # Main application interface
│   ├── styles.css           # Modern CSS with animations
│   └── script.js            # Advanced JavaScript application logic
├── backend/                 # Python Flask API Server
│   ├── app.py              # REST API with ML-ready endpoints
│   └── requirements.txt    # Backend dependencies
├── parse_midi.py           # Enhanced MIDI analysis engine
├── Alla_Turca_Mozart.mid  # Sample classical piece
└── requirements.txt        # Main project dependencies
```

## 🚀 Quick Start

### 1. **Environment Setup**

```bash
# Clone or navigate to the project directory
cd Melody

# Activate your virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install main dependencies
pip install -r requirements.txt

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

### 2. **Start the Backend Server**

```bash
cd backend
python app.py
```

The backend will start on `http://localhost:5000` with the following endpoints:
- `POST /api/parse-midi` - Analyze the default MIDI file
- `POST /api/upload-midi` - Upload and analyze custom MIDI files  
- `POST /api/hand-analysis` - Get technique suggestions
- `GET /api/health` - Server health check

### 3. **Launch the Web Application**

Open `frontend/index.html` in a modern web browser. The application will automatically connect to the backend API.

## 🎮 How to Use

### **Basic Operation**
1. **Load a Piece**: Click "🎵 Load Piano Piece" to analyze the default Mozart piece
2. **Start Learning**: Use "▶️ Play" to begin the interactive tutorial
3. **Control Tempo**: Adjust playback speed with the tempo slider (10% - 200%)
4. **Focus Practice**: Use the hand selector to practice individual hands

### **Keyboard Shortcuts**
- `Space` - Play/Pause playback
- `→` - Step forward one note
- `←` - Step backward one note  
- `R` - Reset to beginning

### **Visual Learning**
- **Piano Keys**: Light up with finger numbers during playback
- **Hand Diagrams**: SVG visualizations show which fingers to use
- **Progress Tracking**: Real-time statistics and completion percentage
- **Technique Tips**: Contextual suggestions for difficult passages

## 🎯 Learning Methodology

### **Finger Assignment Algorithm**
The application uses advanced algorithms based on classical piano pedagogy:

- **Right Hand**: Thumb-based positioning with optimal finger crossings
- **Left Hand**: Mirrored technique with emphasis on bass note stability
- **Chord Recognition**: Intelligent fingering for multi-note combinations
- **Scale Patterns**: Automatic detection and standard fingerings

### **Difficulty Analysis**
Pieces are automatically assessed across multiple dimensions:

- **Note Range**: Span and register analysis
- **Rhythmic Complexity**: Duration patterns and timing challenges
- **Harmonic Content**: Chord density and complexity
- **Technical Demands**: Stretches, finger independence, and speed requirements

## 🔧 Technical Details

### **Backend Technologies**
- **Flask**: RESTful API framework
- **Music21**: Professional music analysis library
- **NumPy**: Numerical computing for audio analysis
- **CORS**: Cross-origin resource sharing for web integration

### **Frontend Technologies**
- **Modern JavaScript**: ES6+ with async/await patterns
- **SVG Graphics**: Scalable hand visualizations
- **CSS Grid/Flexbox**: Responsive layout system
- **CSS Animations**: Smooth transitions and visual feedback

### **API Endpoints**

#### `POST /api/parse-midi`
Analyzes the default MIDI file and returns structured note data with finger assignments.

**Response:**
```json
{
  "success": true,
  "notes": [...],
  "hand_positions": [...],
  "difficulty": {
    "level": "Intermediate",
    "score": 3,
    "factors": ["Quick notes", "Wide note range"]
  },
  "total_notes": 245
}
```

#### `POST /api/upload-midi`
Accepts file uploads for custom MIDI analysis.

#### `POST /api/hand-analysis`
Provides technique suggestions based on current hand position.

## 🔮 Future Development

### **Planned Features**
- **Real-time Hand Tracking**: Computer vision integration using MediaPipe
- **Audio Analysis**: Microphone input for performance evaluation
- **Machine Learning**: Training models on professional pianist techniques
- **Social Features**: Share progress and compete with other learners
- **Mobile App**: Native iOS/Android applications

### **AI/ML Integration Roadmap**
1. **Data Collection**: Record hand positions from expert pianists
2. **Model Training**: Develop neural networks for optimal fingering
3. **Real-time Analysis**: Live hand tracking and correction
4. **Personalization**: Adaptive learning based on individual progress

## 🛠️ Development

### **Adding New Features**
The codebase is designed for extensibility:

- **Backend**: Add new endpoints in `backend/app.py`
- **Frontend**: Extend the `PianoLearningApp` class in `script.js`
- **Analysis**: Enhance MIDI processing in `parse_midi.py`

### **Testing**
```bash
# Test backend API
curl http://localhost:5000/api/health

# Load the frontend in browser developer tools
# Check console for any JavaScript errors
```

## 📊 Performance Features

- **Optimized Rendering**: Efficient SVG updates and DOM manipulation
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Memory Management**: Proper cleanup of timers and event listeners
- **Progressive Loading**: Lazy loading of large MIDI files

## 🎨 Design Philosophy

The application follows modern web design principles:

- **Glassmorphism UI**: Translucent elements with backdrop blur
- **Smooth Animations**: CSS transitions for professional feel
- **Intuitive Navigation**: Clear visual hierarchy and user flow
- **Accessibility**: Keyboard navigation and screen reader support

## 📚 Educational Impact

This tool addresses key challenges in piano education:

- **Visual Learning**: Makes abstract finger techniques visible
- **Self-Paced Practice**: Learn at your own speed with instant feedback
- **Technique Foundation**: Builds proper habits from the beginning
- **Piece Analysis**: Understand the structure of classical works

## 🤝 Contributing

We welcome contributions to enhance the piano learning experience:

1. **Bug Reports**: Use GitHub issues for bug tracking
2. **Feature Requests**: Suggest new educational features
3. **Code Contributions**: Submit pull requests with improvements
4. **Educational Content**: Help create learning materials

## 📄 License

This project is designed for educational purposes and piano technique development.

---

**Piano Technique Master** - Revolutionizing piano education through technology and intelligent analysis.

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