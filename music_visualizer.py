"""
Sheet Music to Digital Conversion Visualizer
Shows how visual sheet music elements are converted to digital data that apps can process.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon
import numpy as np

class SheetMusicVisualizer:
    """Creates visual representations of how sheet music is digitized"""
    
    def __init__(self):
        self.fig_width = 12
        self.fig_height = 8
    
    def draw_staff_conversion(self):
        """Show how a musical staff is converted to digital coordinates"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(self.fig_width, self.fig_height))
        
        # Left side: Visual staff with notes
        ax1.set_title("Visual Sheet Music", fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        
        # Draw staff lines
        staff_lines = [2, 3, 4, 5, 6]
        for y in staff_lines:
            ax1.plot([1, 9], [y, y], 'k-', linewidth=2)
        
        # Draw clef (simplified treble clef)
        clef_x, clef_y = 1.5, 4
        ax1.text(clef_x, clef_y, '𝄞', fontsize=30, ha='center', va='center')
        
        # Draw notes
        notes_data = [
            (3, 4, '♩'),    # Quarter note on G (4th line)
            (4.5, 5, '♩'),  # Quarter note on A (space above 4th line)
            (6, 6, '♩'),    # Quarter note on B (5th line)
            (7.5, 7, '♩'),  # Quarter note on C (space above 5th line)
        ]
        
        for x, y, symbol in notes_data:
            ax1.text(x, y, symbol, fontsize=20, ha='center', va='center')
        
        # Add measure lines
        ax1.plot([2.5, 2.5], [1.5, 6.5], 'k-', linewidth=3)
        ax1.plot([8.5, 8.5], [1.5, 6.5], 'k-', linewidth=3)
        
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        
        # Right side: Digital representation
        ax2.set_title("Digital Data Representation", fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        
        # Show coordinate system
        ax2.text(5, 9, "Digital Coordinates & Data", fontsize=12, ha='center', fontweight='bold')
        
        # Show note data
        digital_notes = [
            "Note 1: G4, Quarter, Beat 1.0",
            "Note 2: A4, Quarter, Beat 2.0", 
            "Note 3: B4, Quarter, Beat 3.0",
            "Note 4: C5, Quarter, Beat 4.0"
        ]
        
        for i, note_text in enumerate(digital_notes):
            ax2.text(1, 7.5 - i*0.8, note_text, fontsize=10, ha='left',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        
        # Show frequency conversion
        ax2.text(1, 4, "Frequency Conversion:", fontsize=11, fontweight='bold')
        frequencies = [
            "G4 = 392.0 Hz",
            "A4 = 440.0 Hz",
            "B4 = 493.9 Hz", 
            "C5 = 523.3 Hz"
        ]
        
        for i, freq in enumerate(frequencies):
            ax2.text(1.5, 3.5 - i*0.4, freq, fontsize=9, ha='left')
        
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('c:/Users/34789/OneDrive/Desktop/CS/Melody/staff_conversion.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def draw_audio_synthesis_process(self):
        """Visualize how digital notes become audio waves"""
        fig, axes = plt.subplots(2, 2, figsize=(self.fig_width, self.fig_height))
        
        # Top left: Note frequency
        ax1 = axes[0, 0]
        ax1.set_title("1. Note Frequency", fontweight='bold')
        
        # Generate a sine wave for A4 (440 Hz)
        t = np.linspace(0, 0.01, 1000)  # 10ms of audio
        frequency = 440  # A4
        sine_wave = np.sin(2 * np.pi * frequency * t)
        
        ax1.plot(t * 1000, sine_wave, 'b-', linewidth=2)
        ax1.set_xlabel("Time (ms)")
        ax1.set_ylabel("Amplitude")
        ax1.text(0.5, 0.8, f"A4 = {frequency} Hz", transform=ax1.transAxes, 
                bbox=dict(boxstyle="round", facecolor="yellow"))
        ax1.grid(True, alpha=0.3)
        
        # Top right: Envelope shaping
        ax2 = axes[0, 1]
        ax2.set_title("2. Envelope Shaping", fontweight='bold')
        
        # Generate envelope (ADSR - Attack, Decay, Sustain, Release)
        t_envelope = np.linspace(0, 1, 1000)  # 1 second note
        envelope = np.ones_like(t_envelope)
        
        # Attack (0-0.1s)
        attack_mask = t_envelope < 0.1
        envelope[attack_mask] = t_envelope[attack_mask] / 0.1
        
        # Decay (0.1-0.3s)
        decay_mask = (t_envelope >= 0.1) & (t_envelope < 0.3)
        envelope[decay_mask] = 1 - 0.3 * (t_envelope[decay_mask] - 0.1) / 0.2
        
        # Sustain (0.3-0.8s)
        sustain_mask = (t_envelope >= 0.3) & (t_envelope < 0.8)
        envelope[sustain_mask] = 0.7
        
        # Release (0.8-1.0s)
        release_mask = t_envelope >= 0.8
        envelope[release_mask] = 0.7 * (1 - (t_envelope[release_mask] - 0.8) / 0.2)
        
        ax2.plot(t_envelope, envelope, 'r-', linewidth=2)
        ax2.fill_between(t_envelope, 0, envelope, alpha=0.3, color='red')
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Volume")
        
        # Add ADSR labels
        ax2.text(0.05, 0.5, "A", fontsize=12, fontweight='bold')
        ax2.text(0.2, 0.85, "D", fontsize=12, fontweight='bold')
        ax2.text(0.55, 0.75, "S", fontsize=12, fontweight='bold')
        ax2.text(0.9, 0.35, "R", fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Bottom left: Final waveform
        ax3 = axes[1, 0]
        ax3.set_title("3. Final Audio Waveform", fontweight='bold')
        
        # Combine frequency and envelope
        t_final = np.linspace(0, 1, 4400)  # 1 second at 44.1kHz sample rate
        final_wave = np.sin(2 * np.pi * frequency * t_final)
        
        # Apply envelope
        final_envelope = np.ones_like(t_final)
        attack_samples = int(0.1 * len(t_final))
        decay_samples = int(0.3 * len(t_final))
        sustain_samples = int(0.8 * len(t_final))
        
        # Apply simplified envelope
        final_envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        final_envelope[sustain_samples:] = np.linspace(0.7, 0, len(t_final) - sustain_samples)
        final_envelope[decay_samples:sustain_samples] = 0.7
        
        final_audio = final_wave * final_envelope
        
        # Show only first 100ms for clarity
        show_samples = int(0.1 * len(t_final))
        ax3.plot(t_final[:show_samples] * 1000, final_audio[:show_samples], 'g-', linewidth=1)
        ax3.set_xlabel("Time (ms)")
        ax3.set_ylabel("Amplitude")
        ax3.grid(True, alpha=0.3)
        
        # Bottom right: Digital samples
        ax4 = axes[1, 1]
        ax4.set_title("4. Digital Samples", fontweight='bold')
        
        # Show discrete samples
        sample_indices = np.arange(0, 200)  # First 200 samples
        sample_values = final_audio[:200]
        
        ax4.stem(sample_indices, sample_values, basefmt=' ')
        ax4.set_xlabel("Sample Number")
        ax4.set_ylabel("Sample Value")
        ax4.text(0.5, 0.9, "44,100 samples/second", transform=ax4.transAxes,
                bbox=dict(boxstyle="round", facecolor="lightgreen"))
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('c:/Users/34789/OneDrive/Desktop/CS/Melody/audio_synthesis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
    
    def draw_timing_and_rhythm(self):
        """Visualize how timing and rhythm are handled"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(self.fig_width, 6))
        
        # Top: Beat grid
        ax1.set_title("Timing Grid and Note Placement", fontweight='bold')
        ax1.set_xlim(0, 8)
        ax1.set_ylim(-1, 2)
        
        # Draw beat grid
        for beat in range(9):
            ax1.axvline(beat, color='lightgray', linestyle='--', alpha=0.7)
            if beat < 8:
                ax1.text(beat + 0.5, 1.5, f"Beat {beat + 1}", ha='center', fontsize=10)
        
        # Draw notes with different durations
        notes = [
            (0, 1, 1.0, "Quarter"),      # Quarter note
            (1, 1, 1.0, "Quarter"),      # Quarter note  
            (2, 1, 2.0, "Half"),         # Half note
            (4, 1, 0.5, "Eighth"),       # Eighth note
            (4.5, 1, 0.5, "Eighth"),     # Eighth note
            (5, 1, 1.0, "Quarter"),      # Quarter note
            (6, 1, 2.0, "Half"),         # Half note
        ]
        
        colors = ['red', 'red', 'blue', 'green', 'green', 'red', 'blue']
        
        for i, (start, y, duration, name) in enumerate(notes):
            # Draw note block
            rect = Rectangle((start, y-0.2), duration, 0.4, 
                           facecolor=colors[i], alpha=0.7, edgecolor='black')
            ax1.add_patch(rect)
            
            # Add note label
            ax1.text(start + duration/2, y, name[:1], ha='center', va='center', 
                    fontweight='bold', color='white')
        
        ax1.set_xlabel("Time (beats)")
        ax1.set_ylabel("Notes")
        ax1.set_yticks([])
        
        # Add legend
        ax1.text(0, -0.7, "Quarter Note (1 beat)", color='red', fontweight='bold')
        ax1.text(2.5, -0.7, "Half Note (2 beats)", color='blue', fontweight='bold')
        ax1.text(5, -0.7, "Eighth Note (0.5 beats)", color='green', fontweight='bold')
        
        # Bottom: Tempo conversion
        ax2.set_title("Tempo Conversion: Beats to Real Time", fontweight='bold')
        ax2.set_xlim(0, 8)
        ax2.set_ylim(0, 3)
        
        # Show different tempos
        tempos = [60, 120, 180]  # BPM
        tempo_colors = ['red', 'blue', 'green']
        
        for i, (tempo, color) in enumerate(zip(tempos, tempo_colors)):
            y_pos = 2.5 - i * 0.8
            
            # Calculate seconds per beat
            seconds_per_beat = 60 / tempo
            
            # Draw timeline
            ax2.plot([0, 8], [y_pos, y_pos], color=color, linewidth=3, alpha=0.7)
            
            # Mark beats in real time
            for beat in range(9):
                real_time = beat * seconds_per_beat
                ax2.plot(beat, y_pos, 'o', color=color, markersize=8)
                if beat % 2 == 0:  # Label every other beat
                    ax2.text(beat, y_pos + 0.1, f"{real_time:.1f}s", 
                            ha='center', fontsize=8, color=color)
            
            # Tempo label
            ax2.text(-0.5, y_pos, f"{tempo} BPM", ha='right', va='center', 
                    fontweight='bold', color=color, fontsize=12)
        
        ax2.set_xlabel("Beat Number")
        ax2.set_ylabel("Different Tempos")
        ax2.set_yticks([])
        
        plt.tight_layout()
        plt.savefig('c:/Users/34789/OneDrive/Desktop/CS/Melody/timing_rhythm.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()

def create_visualizations():
    """Create all visualizations showing how apps process sheet music"""
    print("Creating visualizations of sheet music processing...")
    
    visualizer = SheetMusicVisualizer()
    
    try:
        print("1. Creating staff conversion diagram...")
        visualizer.draw_staff_conversion()
        
        print("2. Creating audio synthesis process diagram...")
        visualizer.draw_audio_synthesis_process()
        
        print("3. Creating timing and rhythm diagram...")
        visualizer.draw_timing_and_rhythm()
        
        print("\nAll visualizations created successfully!")
        print("Files saved:")
        print("- staff_conversion.png")
        print("- audio_synthesis.png") 
        print("- timing_rhythm.png")
        
    except Exception as e:
        print(f"Error creating visualizations: {e}")
        print("Make sure you have matplotlib installed: pip install matplotlib")

if __name__ == "__main__":
    create_visualizations()
