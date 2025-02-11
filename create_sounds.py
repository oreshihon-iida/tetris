import wave
import numpy as np

# Create a simple beep sound
duration = 0.2  # seconds
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration))
data = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
scaled = np.int16(data * 32767)

# Create rotate.wav
with wave.open('sounds/rotate.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    f.writeframes(scaled.tobytes())

# Create place.wav with lower frequency
t = np.linspace(0, duration, int(sample_rate * duration))
data = np.sin(2 * np.pi * 220 * t)  # 220 Hz sine wave
scaled = np.int16(data * 32767)

with wave.open('sounds/place.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    f.writeframes(scaled.tobytes())

# Create background music (simple repeating pattern)
duration = 2.0  # seconds
t = np.linspace(0, duration, int(sample_rate * duration))
data = np.sin(2 * np.pi * 440 * t) * 0.3 + np.sin(2 * np.pi * 880 * t) * 0.2
scaled = np.int16(data * 32767)

for name in ['menu.wav', 'tetris.wav', 'puyo.wav']:
    with wave.open(f'sounds/{name}', 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(scaled.tobytes())
