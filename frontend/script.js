// Piano Learning App - Enhanced JavaScript
class PianoLearningApp {
    constructor() {
        this.notes = [];
        this.handPositions = [];
        this.currentNoteIndex = 0;
        this.isPlaying = false;
        this.playbackSpeed = 1.0;
        this.visibleHands = 'both';
        this.playbackTimer = null;
        
        this.initializeApp();
    }

    initializeApp() {
        this.createPianoKeys();
        this.setupEventListeners();
        this.createHandVisualization();
    }

    setupEventListeners() {
        // Main controls
        document.getElementById('load-midi').addEventListener('click', () => this.loadMIDI());
        document.getElementById('play-pause').addEventListener('click', () => this.togglePlayback());
        document.getElementById('reset').addEventListener('click', () => this.resetPlayback());
        
        // Playback controls
        document.getElementById('tempo-slider').addEventListener('input', (e) => this.setTempo(e.target.value));
        document.getElementById('hand-selector').addEventListener('change', (e) => this.setVisibleHands(e.target.value));
        
        // Window resize handler to recreate piano keys with correct sizing
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.createPianoKeys();
            }, 250);
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
    }

    createPianoKeys() {
        const pianoKeys = document.getElementById('piano-keys');
        pianoKeys.innerHTML = '';
        
        // Create container for proper layering
        const whiteKeysContainer = document.createElement('div');
        whiteKeysContainer.className = 'white-keys-container';
        
        const blackKeysContainer = document.createElement('div');
        blackKeysContainer.className = 'black-keys-container';
        
        // Piano keyboard pattern for each octave
        const keyPattern = [
            { note: 'C', type: 'white', hasSharp: true },
            { note: 'D', type: 'white', hasSharp: true },
            { note: 'E', type: 'white', hasSharp: false },
            { note: 'F', type: 'white', hasSharp: true },
            { note: 'G', type: 'white', hasSharp: true },
            { note: 'A', type: 'white', hasSharp: true },
            { note: 'B', type: 'white', hasSharp: false }
        ];
        
        let whiteKeyIndex = 0;
        
        // Calculate key dimensions based on screen size
        const isMobile = window.innerWidth <= 768;
        const whiteKeyWidth = isMobile ? 30 : 40;
        const whiteKeySpacing = isMobile ? 32 : 42;
        const blackKeyOffset = isMobile ? 21 : 28;
        
        for (let octave = 3; octave <= 5; octave++) {
            keyPattern.forEach((keyInfo, patternIndex) => {
                const noteName = keyInfo.note + octave;
                const midi = this.noteToMidi(noteName);
                
                // Create white key
                const whiteKey = this.createKey(noteName, midi, 'white-key');
                whiteKey.style.left = `${whiteKeyIndex * whiteKeySpacing}px`;
                whiteKeysContainer.appendChild(whiteKey);
                
                // Create black key if this white key has a sharp
                if (keyInfo.hasSharp) {
                    const sharpName = keyInfo.note + '#' + octave;
                    const sharpMidi = this.noteToMidi(sharpName);
                    const blackKey = this.createKey(sharpName, sharpMidi, 'black-key');
                    
                    // Position black key between white keys
                    blackKey.style.left = `${whiteKeyIndex * whiteKeySpacing + blackKeyOffset}px`;
                    blackKeysContainer.appendChild(blackKey);
                }
                
                whiteKeyIndex++;
            });
        }
        
        pianoKeys.appendChild(whiteKeysContainer);
        pianoKeys.appendChild(blackKeysContainer);
    }

    createKey(noteName, midi, className) {
        const key = document.createElement('div');
        key.className = `piano-key ${className}`;
        key.dataset.note = noteName;
        key.dataset.midi = midi;
        
        // Add key label
        const label = document.createElement('div');
        label.className = 'key-label';
        label.textContent = noteName;
        key.appendChild(label);
        
        // Add finger indicator
        const fingerIndicator = document.createElement('div');
        fingerIndicator.className = 'finger-indicator';
        key.appendChild(fingerIndicator);
        
        // Add click handler
        key.addEventListener('click', () => this.playKey(midi, noteName));
        
        return key;
    }

    createHandVisualization() {
        this.createHandSVG('right-hand-svg', 'right');
        this.createHandSVG('left-hand-svg', 'left');
    }

    createHandSVG(svgId, hand) {
        const svg = document.getElementById(svgId);
        const group = svg.querySelector('g');
        
        // Hand position and finger coordinates
        const fingerPositions = {
            right: [
                { x: 50, y: 150, width: 25, height: 80, finger: 1 },  // Thumb
                { x: 85, y: 120, width: 20, height: 110, finger: 2 }, // Index
                { x: 115, y: 110, width: 20, height: 120, finger: 3 }, // Middle
                { x: 145, y: 115, width: 20, height: 115, finger: 4 }, // Ring
                { x: 175, y: 125, width: 18, height: 105, finger: 5 }  // Pinky
            ],
            left: [
                { x: 175, y: 150, width: 25, height: 80, finger: 1 },  // Thumb
                { x: 145, y: 120, width: 20, height: 110, finger: 2 }, // Index
                { x: 115, y: 110, width: 20, height: 120, finger: 3 }, // Middle
                { x: 85, y: 115, width: 20, height: 115, finger: 4 },  // Ring
                { x: 55, y: 125, width: 18, height: 105, finger: 5 }   // Pinky
            ]
        };

        fingerPositions[hand].forEach(finger => {
            // Create finger shape
            const fingerElement = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
            fingerElement.setAttribute('cx', finger.x + finger.width / 2);
            fingerElement.setAttribute('cy', finger.y + finger.height / 2);
            fingerElement.setAttribute('rx', finger.width / 2);
            fingerElement.setAttribute('ry', finger.height / 2);
            fingerElement.setAttribute('class', 'finger finger-base');
            fingerElement.setAttribute('data-finger', finger.finger);
            
            // Add finger number
            const fingerNumber = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            fingerNumber.setAttribute('x', finger.x + finger.width / 2);
            fingerNumber.setAttribute('y', finger.y + finger.height / 2);
            fingerNumber.setAttribute('class', 'finger-number');
            fingerNumber.textContent = finger.finger;
            
            group.appendChild(fingerElement);
            group.appendChild(fingerNumber);
        });
    }

    async loadMIDI() {
        try {
            const response = await fetch('http://localhost:5000/api/parse-midi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error('Failed to load MIDI file');
            }

            const data = await response.json();
            
            this.notes = data.notes;
            this.handPositions = data.hand_positions;
            this.displayDifficultyInfo(data.difficulty);
            
            document.getElementById('play-pause').disabled = false;
            document.getElementById('total-notes').textContent = data.total_notes;
            
            this.showNotification('MIDI file loaded successfully!', 'success');
            
        } catch (error) {
            console.error('Error loading MIDI:', error);
            this.showNotification('Error loading MIDI file. Make sure the backend is running.', 'error');
        }
    }

    displayDifficultyInfo(difficulty) {
        const badge = document.getElementById('difficulty-badge');
        const details = document.getElementById('difficulty-details');
        
        badge.textContent = difficulty.level;
        badge.className = `difficulty-badge difficulty-${difficulty.level.toLowerCase()}`;
        
        details.innerHTML = `
            <p><strong>Complexity Score:</strong> ${difficulty.score}/5</p>
            <p><strong>Total Notes:</strong> ${difficulty.total_notes}</p>
            <p><strong>Note Range:</strong> ${difficulty.note_span} semitones</p>
            ${difficulty.factors.length > 0 ? 
                `<p><strong>Challenges:</strong> ${difficulty.factors.join(', ')}</p>` : ''}
        `;
    }

    togglePlayback() {
        if (this.isPlaying) {
            this.pausePlayback();
        } else {
            this.startPlayback();
        }
    }

    startPlayback() {
        if (this.notes.length === 0) {
            this.showNotification('Please load a MIDI file first', 'warning');
            return;
        }

        this.isPlaying = true;
        document.getElementById('play-pause').innerHTML = '<span>⏸️</span> Pause';
        
        this.playNextNote();
    }

    pausePlayback() {
        this.isPlaying = false;
        document.getElementById('play-pause').innerHTML = '<span>▶️</span> Play';
        
        if (this.playbackTimer) {
            clearTimeout(this.playbackTimer);
        }
    }

    resetPlayback() {
        this.pausePlayback();
        this.currentNoteIndex = 0;
        this.clearAllHighlights();
        this.updateProgress();
        document.getElementById('current-note').textContent = 'None';
        document.getElementById('finger-info').textContent = 'None';
        document.getElementById('hand-position').textContent = 'None';
        document.getElementById('current-time').textContent = '0.0s';
    }

    playNextNote() {
        if (!this.isPlaying || this.currentNoteIndex >= this.notes.length) {
            this.pausePlayback();
            this.showNotification('Playback completed!', 'success');
            return;
        }

        const note = this.notes[this.currentNoteIndex];
        this.displayCurrentNote(note);
        this.highlightKey(note);
        this.highlightFinger(note);
        this.updateProgress();
        
        // Calculate delay to next note
        const nextNote = this.notes[this.currentNoteIndex + 1];
        const delay = nextNote ? 
            (nextNote.offset - note.offset) * 1000 / this.playbackSpeed : 
            note.duration * 1000 / this.playbackSpeed;

        this.currentNoteIndex++;
        
        this.playbackTimer = setTimeout(() => {
            this.playNextNote();
        }, Math.max(delay, 100)); // Minimum 100ms delay
    }

    displayCurrentNote(note) {
        document.getElementById('current-note').textContent = note.pitch;
        document.getElementById('finger-info').textContent = `${note.finger} (${note.finger_name})`;
        document.getElementById('hand-position').textContent = note.hand === 'right' ? 'Right Hand' : 'Left Hand';
        document.getElementById('current-time').textContent = `${note.offset.toFixed(1)}s`;
    }

    highlightKey(note) {
        // Clear previous highlights
        this.clearKeyHighlights();
        
        // Highlight current key
        const key = document.querySelector(`[data-midi="${note.midi}"]`);
        if (key) {
            key.classList.add('active');
            
            // Show finger indicator
            const fingerIndicator = key.querySelector('.finger-indicator');
            if (fingerIndicator) {
                fingerIndicator.textContent = note.finger;
                fingerIndicator.classList.add('show');
            }
        }
    }

    highlightFinger(note) {
        // Clear previous finger highlights
        this.clearFingerHighlights();
        
        // Highlight current finger
        const handSvg = note.hand === 'right' ? 'right-hand-svg' : 'left-hand-svg';
        const finger = document.querySelector(`#${handSvg} [data-finger="${note.finger}"]`);
        
        if (finger) {
            finger.classList.remove('finger-base');
            finger.classList.add('finger-active');
        }
    }

    clearAllHighlights() {
        this.clearKeyHighlights();
        this.clearFingerHighlights();
    }

    clearKeyHighlights() {
        document.querySelectorAll('.piano-key.active').forEach(key => {
            key.classList.remove('active');
        });
        
        document.querySelectorAll('.finger-indicator.show').forEach(indicator => {
            indicator.classList.remove('show');
        });
    }

    clearFingerHighlights() {
        document.querySelectorAll('.finger-active').forEach(finger => {
            finger.classList.remove('finger-active');
            finger.classList.add('finger-base');
        });
    }

    updateProgress() {
        const progress = this.notes.length > 0 ? (this.currentNoteIndex / this.notes.length) * 100 : 0;
        document.getElementById('progress-fill').style.width = `${progress}%`;
        document.getElementById('progress-text').textContent = `${Math.round(progress)}%`;
        document.getElementById('notes-played').textContent = this.currentNoteIndex;
    }

    setTempo(speed) {
        this.playbackSpeed = parseFloat(speed);
        document.getElementById('tempo-display').textContent = `${Math.round(speed * 100)}%`;
    }

    setVisibleHands(hands) {
        this.visibleHands = hands;
        
        const leftHand = document.getElementById('left-hand-container');
        const rightHand = document.getElementById('right-hand-container');
        
        switch (hands) {
            case 'right':
                leftHand.style.display = 'none';
                rightHand.style.display = 'block';
                break;
            case 'left':
                leftHand.style.display = 'block';
                rightHand.style.display = 'none';
                break;
            case 'both':
            default:
                leftHand.style.display = 'block';
                rightHand.style.display = 'block';
                break;
        }
    }

    handleKeyboard(event) {
        switch (event.code) {
            case 'Space':
                event.preventDefault();
                this.togglePlayback();
                break;
            case 'ArrowRight':
                event.preventDefault();
                if (!this.isPlaying && this.currentNoteIndex < this.notes.length) {
                    this.currentNoteIndex++;
                    this.displayCurrentNote(this.notes[this.currentNoteIndex - 1]);
                    this.updateProgress();
                }
                break;
            case 'ArrowLeft':
                event.preventDefault();
                if (!this.isPlaying && this.currentNoteIndex > 0) {
                    this.currentNoteIndex--;
                    this.displayCurrentNote(this.notes[this.currentNoteIndex]);
                    this.updateProgress();
                }
                break;
            case 'KeyR':
                event.preventDefault();
                this.resetPlayback();
                break;
        }
    }

    playKey(midi, noteName) {
        // Visual feedback for manual key press
        const key = document.querySelector(`[data-midi="${midi}"]`);
        if (key) {
            key.classList.add('pulse');
            setTimeout(() => key.classList.remove('pulse'), 600);
        }
        
        console.log(`Playing note: ${noteName} (MIDI: ${midi})`);
    }

    noteToMidi(noteName) {
        const noteMap = {
            'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
            'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
        };
        
        const match = noteName.match(/([A-G]#?)(\d+)/);
        if (!match) return 60; // Default to middle C
        
        const note = match[1];
        const octave = parseInt(match[2]);
        
        return (octave + 1) * 12 + noteMap[note];
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '15px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '10000',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });
        
        // Set background color based on type
        const colors = {
            success: '#4CAF50',
            error: '#f44336',
            warning: '#ff9800',
            info: '#2196F3'
        };
        notification.style.background = colors[type] || colors.info;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.pianoApp = new PianoLearningApp();
});