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
    
    # Mix all components
    data = arpeggio * 0.4 + bass * 0.4 + drum_pattern
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

# Create menu music (simpler theme)
t = np.linspace(0, 2.0, int(44100 * 2.0))
menu_data = np.sin(2 * np.pi * 440 * t) * 0.3 + np.sin(2 * np.pi * 880 * t) * 0.2
menu_scaled = np.int16(menu_data * 32767)

with wave.open('sounds/menu.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    f.writeframes(menu_scaled.tobytes())

# Create Gradius-style game music
create_gradius_style_music('tetris', 440)  # A4 as base frequency
create_gradius_style_music('puyo', 392)    # G4 as base frequency for variety

# Create sound effects
create_sound_effect('rotate', 440)  # A4
create_sound_effect('place', 220)   # A3
