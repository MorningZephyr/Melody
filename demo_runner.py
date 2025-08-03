"""
Demo Runner - Demonstrates how apps play piano pieces from sheet music
Run this script to see all the demonstrations in sequence.
"""

import sys
import time
import subprocess

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n--- {title} ---")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['pygame', 'numpy', 'matplotlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nPlease install them with:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def run_basic_demo():
    """Run the basic piano player demo"""
    print_header("BASIC PIANO PLAYING DEMO")
    print("This demo shows how apps convert sheet music notes to audio...")
    
    try:
        # Import and run basic demo
        from piano_player import demo_simple_scale, demo_mary_had_a_little_lamb, demo_chord_progression
        
        print_section("C Major Scale")
        demo_simple_scale()
        
        print_section("Mary Had a Little Lamb")
        demo_mary_had_a_little_lamb()
        
        print_section("Chord Progression")
        demo_chord_progression()
        
    except Exception as e:
        print(f"Error running basic demo: {e}")

def run_advanced_demo():
    """Run the advanced sheet music analysis demo"""
    print_header("ADVANCED SHEET MUSIC ANALYSIS")
    print("This shows how real music apps parse and analyze sheet music...")
    
    try:
        from advanced_sheet_reader import demonstrate_sheet_music_reading
        demonstrate_sheet_music_reading()
        
    except Exception as e:
        print(f"Error running advanced demo: {e}")

def run_midi_demo():
    """Run the MIDI processing demo"""
    print_header("MIDI FILE PROCESSING")
    print("This demonstrates how apps handle the industry standard MIDI format...")
    
    try:
        from midi_processor import demonstrate_midi_processing
        demonstrate_midi_processing()
        
    except Exception as e:
        print(f"Error running MIDI demo: {e}")

def run_visualization_demo():
    """Run the visualization demo"""
    print_header("MUSIC PROCESSING VISUALIZATIONS")
    print("Creating visual diagrams showing how sheet music becomes audio...")
    
    try:
        from music_visualizer import create_visualizations
        create_visualizations()
        
    except Exception as e:
        print(f"Error running visualization demo: {e}")
        print("Note: This requires matplotlib and may not work in all environments")

def main():
    """Main demo runner"""
    print_header("HOW APPS PLAY PIANO PIECES FROM SHEET MUSIC")
    print("""
This comprehensive demonstration shows the complete process of how 
applications convert sheet music notation into audio that you can hear.

The process involves four main steps:
1. Reading music notation (visual symbols or digital formats)
2. Converting notes to precise frequencies and timing
3. Generating audio waveforms through synthesis
4. Playing the audio with proper timing and expression

Let's explore each step with interactive demonstrations!
""")
    
    # Check if we have required packages
    if not check_dependencies():
        return
    
    try:
        input("\nPress Enter to start the basic piano demo...")
        run_basic_demo()
        
        input("\nPress Enter to continue to advanced sheet music analysis...")
        run_advanced_demo()
        
        input("\nPress Enter to continue to MIDI processing demo...")
        run_midi_demo()
        
        print("\nWould you like to generate visualization diagrams?")
        response = input("This will create PNG files showing the process (y/n): ").lower()
        if response.startswith('y'):
            run_visualization_demo()
        
        print_header("DEMONSTRATION COMPLETE")
        print("""
Summary of what we've demonstrated:

1. BASIC AUDIO SYNTHESIS
   - Converting note names (C, D, E) to frequencies (Hz)
   - Generating sine wave audio for each note
   - Playing melodies with proper timing

2. ADVANCED MUSIC NOTATION
   - Parsing different sheet music formats (ABC, custom notation)
   - Handling complex musical elements (time signatures, key signatures)
   - Analyzing musical structure and content

3. MIDI FILE PROCESSING  
   - Industry standard digital music format
   - Precise timing and multi-track coordination
   - Professional-grade music data handling

4. VISUAL REPRESENTATION
   - How visual sheet music maps to digital coordinates
   - Audio synthesis pipeline visualization
   - Timing and rhythm conversion diagrams

This is the foundation of how all music applications work:
- Digital Audio Workstations (Logic, Pro Tools)
- Music learning apps (Simply Piano, Flowkey)
- Notation software (Sibelius, MuseScore)
- Virtual instruments and synthesizers
- Game audio systems

For more advanced features, explore the individual demo files
and extend them with additional music theory and audio processing!
""")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please check that all required packages are installed.")

if __name__ == "__main__":
    main()
