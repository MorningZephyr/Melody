# Piano Music Player Project

This project demonstrates how applications play piano pieces from sheet music notation. It covers the complete process from visual sheet music to digital audio output.

## How Apps Play Piano Pieces

### 1. **Music Notation Input**
Apps accept sheet music in various formats:
- **MIDI files**: Binary format with precise timing and note data
- **MusicXML**: XML format preserving visual layout and musical notation
- **ABC notation**: Simple text format for melodies
- **Scanned sheet music**: Using Optical Music Recognition (OMR)

### 2. **Digital Representation**
Sheet music is converted to digital data containing:
- **Note information**: Pitch, duration, dynamics, articulation
- **Timing data**: Precise start times and note lengths
- **Musical context**: Key signature, time signature, tempo
- **Structure**: Measures, repeats, multiple voices

### 3. **Audio Synthesis**
Digital notes are converted to sound through:
- **Frequency calculation**: Converting note names to frequencies (A4 = 440 Hz)
- **Waveform generation**: Creating sine waves, samples, or synthesis
- **Envelope shaping**: Adding attack, decay, sustain, release (ADSR)
- **Effects processing**: Reverb, dynamics, pedaling simulation

### 4. **Timing Engine**
Precise playback timing is managed by:
- **Tempo conversion**: Converting beats to real-time seconds
- **Rhythm coordination**: Handling different note values accurately
- **Synchronization**: Coordinating multiple voices or instruments
- **Expression**: Adding human-like timing variations

## Project Files

### Core Demonstrations
- `piano_player.py` - Basic piano synthesis and note playing
- `advanced_sheet_reader.py` - Advanced music notation parsing
- `midi_processor.py` - MIDI file processing (industry standard)
- `music_visualizer.py` - Visual diagrams of the process

### Installation
```bash
pip install -r requirements.txt
```

### Running the Demos
```bash
# Basic piano playing with simple melodies
python piano_player.py

# Advanced sheet music analysis
python advanced_sheet_reader.py

# MIDI file processing demonstration
python midi_processor.py

# Create visual diagrams
python music_visualizer.py
```

## Key Concepts Explained

### Music Theory to Digital Conversion
1. **Note Names → MIDI Numbers**: C4 = 60, A4 = 69, etc.
2. **MIDI Numbers → Frequencies**: f = 440 × 2^((n-69)/12)
3. **Durations → Time**: Quarter note = 60/BPM seconds
4. **Dynamics → Volume**: pp, p, mp, mf, f, ff → 0.0 to 1.0

### Audio Processing Pipeline
```
Sheet Music → Parser → Note Events → Frequency Generator → Envelope → Audio Output
```

### Real-World Applications
This technology is used in:
- **Digital Audio Workstations** (Logic Pro, Pro Tools, Cubase)
- **Music Learning Apps** (Simply Piano, Flowkey, Yousician)
- **Notation Software** (Sibelius, Finale, MuseScore)
- **Virtual Instruments** (Piano VSTs, sample libraries)
- **Game Audio** (Dynamic music systems)

### Technical Architecture
Modern music apps typically use:
- **Audio engines**: JUCE, FMOD, Wwise, Web Audio API
- **MIDI libraries**: RtMidi, PortMidi, mido (Python)
- **DSP frameworks**: FFTW, Accelerate, Web Audio
- **Notation libraries**: music21, VexFlow, OpenSheetMusicDisplay

## Advanced Features

Real applications also handle:
- **Multiple instruments**: Orchestra, band, ensemble pieces
- **Complex rhythms**: Tuplets, syncopation, polyrhythms
- **Expression**: Crescendo, ritardando, articulations
- **Interactive features**: Following along, practice modes
- **Audio analysis**: Pitch detection for instrument input

## Getting Started

1. Run `piano_player.py` to hear basic note synthesis
2. Explore `advanced_sheet_reader.py` for music analysis
3. Check `midi_processor.py` to understand industry standards
4. Use `music_visualizer.py` to see visual representations

This project provides a foundation for understanding digital music processing and can be extended for more complex musical applications.
