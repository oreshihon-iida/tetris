"""Puyo Puyo game module."""
from typing import List, Tuple, Optional
import random
from .constants import (
    RED, BLUE, GREEN, YELLOW, PURPLE
)

class Puyo:
    """Represents a single Puyo piece with its color and position."""
    COLORS = [RED, BLUE, GREEN, YELLOW, PURPLE]

    def __init__(self, x: int, y: int, color: Optional[Tuple[int, int, int]] = None):
        self.x = x
        self.y = y
        self.color = color if color else random.choice(self.COLORS)

class PuyoPair:
    """Represents a pair of connected Puyos that can be rotated."""
    def __init__(self):
        self.x = 4  # Start from middle
        self.y = 0
        color1 = random.choice(Puyo.COLORS)
        color2 = random.choice(Puyo.COLORS)
        self.main_puyo = Puyo(self.x, self.y, color1)
        self.sub_puyo = Puyo(self.x, self.y - 1, color2)
        self.rotation = 0  # 0: vertical, 1: right, 2: upside down, 3: left

    def rotate_clockwise(self) -> None:
        """Rotate the Puyo pair clockwise."""
        self.rotation = (self.rotation + 1) % 4
        self._update_sub_puyo_position()

    def rotate_counterclockwise(self) -> None:
        """Rotate the Puyo pair counterclockwise."""
        self.rotation = (self.rotation - 1) % 4
        self._update_sub_puyo_position()

    def _update_sub_puyo_position(self) -> None:
        """Update the sub Puyo's position based on rotation state."""
        if self.rotation == 0:  # Vertical
            self.sub_puyo.x = self.main_puyo.x
            self.sub_puyo.y = self.main_puyo.y - 1
        elif self.rotation == 1:  # Right
            self.sub_puyo.x = self.main_puyo.x + 1
            self.sub_puyo.y = self.main_puyo.y
        elif self.rotation == 2:  # Upside down
            self.sub_puyo.x = self.main_puyo.x
            self.sub_puyo.y = self.main_puyo.y + 1
        else:  # Left
            self.sub_puyo.x = self.main_puyo.x - 1
            self.sub_puyo.y = self.main_puyo.y

    def move(self, dx: int, dy: int) -> None:
        """Move the Puyo pair by the given delta."""
        self.x += dx
        self.y += dy
        self.main_puyo.x += dx
        self.main_puyo.y += dy
        self.sub_puyo.x += dx
        self.sub_puyo.y += dy

    def get_positions(self) -> List[Tuple[int, int, Tuple[int, int, int]]]:
        """Get the positions and colors of both Puyos.
        
        Returns:
            List[Tuple[int, int, Tuple[int, int, int]]]: List of (x, y, color) for both Puyos
        """
        return [
            (self.main_puyo.x, self.main_puyo.y, self.main_puyo.color),
            (self.sub_puyo.x, self.sub_puyo.y, self.sub_puyo.color)
        ]

    def get_preview_positions(self, preview_x: int, preview_y: int) -> List[Tuple[int, int, Tuple[int, int, int]]]:
        """Get preview positions and colors for display.
        
        Args:
            preview_x: X coordinate for preview
            preview_y: Y coordinate for preview
            
        Returns:
            List[Tuple[int, int, Tuple[int, int, int]]]: List of (x, y, color) for preview
        """
        return [
            (preview_x, preview_y, self.main_puyo.color),
            (preview_x, preview_y - 1, self.sub_puyo.color)
        ]
