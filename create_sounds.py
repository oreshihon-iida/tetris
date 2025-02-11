import wave
import numpy as np

def create_arpeggio(base_freq, duration, pattern, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    data = np.zeros_like(t)
    note_duration = duration / len(pattern)
    
    for i, multiplier in enumerate(pattern):
        start = int(i * sample_rate * note_duration)
        end = int((i + 1) * sample_rate * note_duration)
        note_t = t[start:end]
        freq = base_freq * multiplier
        data[start:end] = np.sin(2 * np.pi * freq * note_t)
    
    return data

def create_bassline(freq, duration, rhythm_pattern, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    data = np.zeros_like(t)
    note_duration = duration / len(rhythm_pattern)
    
    for i, active in enumerate(rhythm_pattern):
        if active:
            start = int(i * sample_rate * note_duration)
            end = int((i + 1) * sample_rate * note_duration)
            note_t = t[start:end]
            data[start:end] = np.sin(2 * np.pi * freq * note_t) * 0.8
    
    return data

def create_noise(duration, sample_rate=44100):
    samples = int(sample_rate * duration)
    return np.random.uniform(-0.1, 0.1, samples)

def create_gradius_style_music(name, base_freq, duration=4.0, sample_rate=44100):
    # Create melodic arpeggio pattern (similar to Gradius)
    arpeggio_pattern = [1, 1.5, 2, 1.5]  # Classic arcade-style arpeggio
    arpeggio = create_arpeggio(base_freq, duration, arpeggio_pattern)
    
    # Create driving bassline
    rhythm = [1, 0, 1, 0, 1, 0, 1, 1]  # Energetic rhythm pattern
    bass = create_bassline(base_freq/2, duration, rhythm)
    
    # Add percussion
    drum_pattern = create_noise(duration)
    
    # Mix melodic components only (removed percussion)
    data = arpeggio * 0.5 + bass * 0.5  # Adjusted mix levels for balance
    scaled = np.int16(data * 32767)
    
    with wave.open(f'sounds/{name}.wav', 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(scaled.tobytes())

# Create sound effects
def create_sound_effect(name, freq, duration=0.2, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    data = np.sin(2 * np.pi * freq * t)
    scaled = np.int16(data * 32767)
    
    with wave.open(f'sounds/{name}.wav', 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(scaled.tobytes())

def create_dragon_quest_music(duration=4.0, sample_rate=44100):
    # Dragon Quest style uses major scales and arpeggiated chords
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Main melody (typical Dragon Quest overworld theme style)
    melody_freq = 440  # A4
    melody = np.sin(2 * np.pi * melody_freq * t) * 0.3
    
    # Harmonics for orchestral feel
    harmony1 = np.sin(2 * np.pi * (melody_freq * 1.25) * t) * 0.2  # Major third
    harmony2 = np.sin(2 * np.pi * (melody_freq * 1.5) * t) * 0.15  # Perfect fifth
    
    # Slow arpeggios for medieval fantasy feel
    arpeggio_pattern = [1, 1.25, 1.5, 2.0]  # Major chord
    arpeggio = create_arpeggio(melody_freq/2, duration, arpeggio_pattern) * 0.25
    
    # Mix all components
    data = melody + harmony1 + harmony2 + arpeggio
    scaled = np.int16(data * 32767)
    
    with wave.open('sounds/menu.wav', 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(scaled.tobytes())

# Create Dragon Quest style menu music
create_dragon_quest_music()

# Create Gradius-style game music
create_gradius_style_music('tetris', 440)  # A4 as base frequency
create_gradius_style_music('puyo', 392)    # G4 as base frequency for variety

# Create sound effects
create_sound_effect('rotate', 440)  # A4
create_sound_effect('place', 220)   # A3
