class PianoLearningApp {
    constructor() {
        this.currentNoteIndex = 0;
        this.notes = [];
        this.isPlaying = false;
        this.animationId = null;
        
        this.init();
    }

    init() {
        this.createPianoKeys();
        this.createHandVisualization();
        this.bindEvents();
        this.loadSampleData(); // For demo purposes
    }

    createPianoKeys() {
        const pianoKeys = document.getElementById('piano-keys');
        const whiteKeys = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
        const blackKeys = ['C#', 'D#', 'F#', 'G#', 'A#'];
        
        // Create white keys
        whiteKeys.forEach((note, index) => {
            const key = document.createElement('div');
            key.className = 'piano-key';
            key.textContent = note;
            key.dataset.note = note;
            key.dataset.midi = 60 + index; // C4 = 60
            pianoKeys.appendChild(key);
        });

        // Create black keys
        const blackKeyPositions = [0, 1, 3, 4, 5]; // Positions between white keys
        blackKeys.forEach((note, index) => {
            const key = document.createElement('div');
            key.className = 'piano-key black';
            key.textContent = note;
            key.dataset.note = note;
            key.dataset.midi = 61 + index; // C#4 = 61
            key.style.left = `${(blackKeyPositions[index] * 40) + 30}px`;
            pianoKeys.appendChild(key);
        });
    }

    createHandVisualization() {
        const handGroup = document.getElementById('hand-group');
        
        // Create 5 fingers (thumb to pinky)
        const fingers = [
            { id: 'thumb', x: 100, y: 200, label: 'T', color: '#ff6b6b' },
            { id: 'index', x: 120, y: 180, label: '1', color: '#ff6b6b' },
            { id: 'middle', x: 140, y: 160, label: '2', color: '#ff6b6b' },
            { id: 'ring', x: 160, y: 180, label: '3', color: '#ff6b6b' },
            { id: 'pinky', x: 180, y: 200, label: '4', color: '#ff6b6b' }
        ];

        fingers.forEach(finger => {
            // Create finger circle
            const fingerElement = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            fingerElement.setAttribute('cx', finger.x);
            fingerElement.setAttribute('cy', finger.y);
            fingerElement.setAttribute('r', '15');
            fingerElement.setAttribute('class', 'finger');
            fingerElement.setAttribute('id', finger.id);
            
            // Create finger label
            const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            label.setAttribute('x', finger.x);
            label.setAttribute('y', finger.y + 4);
            label.setAttribute('class', 'finger-label');
            label.textContent = finger.label;
            
            handGroup.appendChild(fingerElement);
            handGroup.appendChild(label);
        });
    }

    bindEvents() {
        document.getElementById('load-midi').addEventListener('click', () => this.loadMIDI());
        document.getElementById('play-pause').addEventListener('click', () => this.togglePlay());
        document.getElementById('reset').addEventListener('click', () => this.reset());
    }

    loadSampleData() {
        // Sample note data for demo
        this.notes = [
            { pitch: 'C4', midi: 60, duration: 1, finger: 'thumb', hand: 'right' },
            { pitch: 'D4', midi: 62, duration: 1, finger: 'index', hand: 'right' },
            { pitch: 'E4', midi: 64, duration: 1, finger: 'middle', hand: 'right' },
            { pitch: 'F4', midi: 65, duration: 1, finger: 'thumb', hand: 'right' },
            { pitch: 'G4', midi: 67, duration: 1, finger: 'index', hand: 'right' },
            { pitch: 'A4', midi: 69, duration: 1, finger: 'middle', hand: 'right' },
            { pitch: 'B4', midi: 71, duration: 1, finger: 'ring', hand: 'right' },
            { pitch: 'C5', midi: 72, duration: 1, finger: 'pinky', hand: 'right' }
        ];
        
        this.updateInfo();
    }

    assignFingerToNote(note) {
        // Simple finger assignment algorithm
        const midi = note.midi;
        const octave = Math.floor(midi / 12);
        const noteInOctave = midi % 12;
        
        // Basic finger assignment based on note position
        if (noteInOctave <= 1) return 'thumb';      // C, C#
        if (noteInOctave <= 3) return 'index';      // D, D#
        if (noteInOctave <= 5) return 'middle';     // E, F
        if (noteInOctave <= 7) return 'ring';       // F#, G
        if (noteInOctave <= 9) return 'pinky';      // G#, A
        return 'pinky';                              // A#, B
    }

    showHandPosition(note) {
        // Clear previous highlights
        this.clearHighlights();
        
        // Highlight the key
        const keyElement = document.querySelector(`[data-midi="${note.midi}"]`);
        if (keyElement) {
            keyElement.classList.add('active');
        }
        
        // Highlight the finger
        const fingerElement = document.getElementById(note.finger);
        if (fingerElement) {
            fingerElement.classList.add('active');
        }
        
        // Update info panel
        this.updateCurrentNote(note);
    }

    clearHighlights() {
        // Clear piano key highlights
        document.querySelectorAll('.piano-key').forEach(key => {
            key.classList.remove('active');
        });
        
        // Clear finger highlights
        document.querySelectorAll('.finger').forEach(finger => {
            finger.classList.remove('active');
        });
    }

    updateCurrentNote(note) {
        document.getElementById('current-note').textContent = 
            `${note.pitch} (MIDI: ${note.midi})`;
        
        document.getElementById('finger-info').textContent = 
            `Use ${note.finger} finger on ${note.pitch}`;
        
        document.getElementById('hand-position').textContent = 
            `${note.hand} hand, ${note.finger} finger`;
    }

    updateInfo() {
        if (this.notes.length > 0) {
            this.showHandPosition(this.notes[this.currentNoteIndex]);
        }
    }

    togglePlay() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }

    play() {
        if (this.notes.length === 0) return;
        
        this.isPlaying = true;
        document.getElementById('play-pause').textContent = 'Pause';
        
        this.playNextNote();
    }

    pause() {
        this.isPlaying = false;
        document.getElementById('play-pause').textContent = 'Play';
        
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
    }

    playNextNote() {
        if (!this.isPlaying || this.currentNoteIndex >= this.notes.length) {
            this.pause();
            return;
        }
        
        const note = this.notes[this.currentNoteIndex];
        this.showHandPosition(note);
        
        // Move to next note after duration
        setTimeout(() => {
            this.currentNoteIndex++;
            this.playNextNote();
        }, note.duration * 1000); // Convert duration to milliseconds
    }

    reset() {
        this.currentNoteIndex = 0;
        this.pause();
        this.clearHighlights();
        this.updateInfo();
    }

    async loadMIDI() {
        try {
            console.log('Loading MIDI file from backend...');
            
            const response = await fetch('http://localhost:5000/api/parse-midi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.notes = data.notes;
                this.currentNoteIndex = 0;
                this.updateInfo();
                console.log(`Loaded ${data.total_notes} notes from MIDI file`);
            } else {
                console.error('Failed to load MIDI data:', data.error);
            }
            
        } catch (error) {
            console.error('Error loading MIDI file:', error);
            // Fallback to sample data if backend is not available
            this.loadSampleData();
        }
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new PianoLearningApp();
}); 