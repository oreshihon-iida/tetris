from typing import Dict, Optional
import os
import pygame
from pygame import mixer

class AudioManager:
    def __init__(self):
        self._sounds: Dict[str, Optional[mixer.Sound]] = {}
        self._current_music: Optional[str] = None
        self._has_audio = False
        self.initialize()

    def initialize(self) -> None:
        try:
            pygame.mixer.init(44100, -16, 2, 512)
            self._has_audio = True
        except pygame.error:
            print("Warning: Audio initialization failed. Running without sound.")
            self._has_audio = False
        self._load_sounds()

    def _load_sounds(self) -> None:
        sound_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
        os.makedirs(sound_dir, exist_ok=True)
        
        sound_files = {
            'rotate': 'rotate.wav',
            'place': 'place.wav'
        }
        
        for key, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            try:
                self._sounds[key] = mixer.Sound(path)
            except (FileNotFoundError, pygame.error):
                print(f"Failed to load sound: {filename}")
                self._sounds[key] = None

    def play_sound(self, sound_name: str) -> None:
        if not self._has_audio:
            return
        if sound := self._sounds.get(sound_name):
            sound.play()

    def play_music(self, music_name: str) -> None:
        if not self._has_audio or self._current_music == music_name:
            return
            
        music_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
        music_file = os.path.join(music_dir, f"{music_name}.wav")
        
        try:
            mixer.music.load(music_file)
            mixer.music.play(-1)  # -1 for infinite loop
            self._current_music = music_name
        except (FileNotFoundError, pygame.error):
            print(f"Failed to load music: {music_name}")
            self._current_music = None

    def stop_music(self) -> None:
        mixer.music.stop()
        self._current_music = None
