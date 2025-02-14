"""Settings persistence module."""
import json
import os
from pathlib import Path

SETTINGS_FILE = Path.home() / '.tetris_settings.json'

def load_settings() -> dict:
    """Load settings from file."""
    if not SETTINGS_FILE.exists():
        return {}
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}

def save_settings(settings: dict) -> None:
    """Save settings to file."""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f)
    except OSError:
        pass  # Fail silently if we can't save settings
