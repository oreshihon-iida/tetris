"""Audio management module for game sounds and music."""
from typing import Dict, Optional
import os
import logging
import pygame
from pygame import mixer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioManager:
    """Manages game audio including sound effects and background music."""
    def __init__(self):
        self._sounds: Dict[str, Optional[mixer.Sound]] = {}
        self._current_music: Optional[str] = None
        self._has_audio = False
        self._volume = 1.0  # Add volume property
        self.initialize()

    def initialize(self) -> None:
        """Initialize audio system with fallback options."""
        # Disable audio for testing
        self._has_audio = False
        logger.warning("Audio disabled for testing")

    def _load_sounds(self) -> None:
        """Load sound effects with verification."""
        sound_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
        if not os.path.exists(sound_dir):
            logger.error(f"Sound directory not found: {sound_dir}")
            return

        sound_files = {
            'rotate': 'rotate.wav',
            'place': 'place.wav'
        }

        for key, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            if not os.path.exists(path):
                logger.error(f"Sound file not found: {path}")
                self._sounds[key] = None
                continue

            try:
                self._sounds[key] = mixer.Sound(path)
            except pygame.error as e:
                logger.error(f"Failed to load sound {filename}: {e}")
                self._sounds[key] = None

    def play_sound(self, sound_name: str) -> None:
        if not self._has_audio:
            return
        if sound := self._sounds.get(sound_name):
            sound.play()

    def play_music(self, music_name: str) -> None:
        """Play background music with verification."""
        if not self._has_audio:
            return

        if self._current_music == music_name:
            return

        music_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
        music_file = os.path.join(music_dir, f"{music_name}.wav")
        
        if not os.path.exists(music_file):
            logger.error(f"Music file not found: {music_file}")
            self._current_music = None
            return

        try:
            mixer.music.load(music_file)
            mixer.music.play(-1)  # -1 for infinite loop
            self._current_music = music_name
            logger.info(f"Playing music: {music_name}")
        except pygame.error as e:
            logger.error(f"Failed to load music {music_name}: {e}")
            self._current_music = None

    def stop_music(self) -> None:
        mixer.music.stop()
        self._current_music = None

    def set_volume(self, volume: float) -> None:
        """Set volume for both music and sound effects.

        Args:
            volume: Float between 0.0 and 1.0
        """
        if not self._has_audio:
            return
        self._volume = max(0.0, min(1.0, volume))
        mixer.music.set_volume(self._volume)
        for sound in self._sounds.values():
            if sound:
                sound.set_volume(self._volume)

    def get_volume(self) -> float:
        """Get current volume level."""
        return self._volume
