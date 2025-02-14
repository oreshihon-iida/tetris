"""Tetris piece module."""
from typing import List, Tuple
import random
from .constants import (
    CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE
)

class Piece:
    """Represents a Tetris piece (tetrimino) with its shape, color, and position."""
    SHAPES = {
        'I': [
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            CYAN
        ],
        'O': [
            [[1, 1],
             [1, 1]],
            YELLOW
        ],
        'T': [
            [[0, 1, 0],
             [1, 1, 1],
             [0, 0, 0]],
            PURPLE
        ],
        'S': [
            [[0, 1, 1],
             [1, 1, 0],
             [0, 0, 0]],
            GREEN
        ],
        'Z': [
            [[1, 1, 0],
             [0, 1, 1],
             [0, 0, 0]],
            RED
        ],
        'J': [
            [[1, 0, 0],
             [1, 1, 1],
             [0, 0, 0]],
            BLUE
        ],
        'L': [
            [[0, 0, 1],
             [1, 1, 1],
             [0, 0, 0]],
            ORANGE
        ]
    }

    def __init__(self):
        shape_name = random.choice(list(self.SHAPES.keys()))
        self.shape = self.SHAPES[shape_name][0]
        self.color = self.SHAPES[shape_name][1]
        self.x = 3
        self.y = 0
        self.rotation = 0

    def rotate(self) -> None:
        """Rotate the piece 90 degrees clockwise."""
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows - 1 - r] = self.shape[r][c]
        self.shape = rotated

    def get_positions(self) -> List[Tuple[int, int]]:
        """Get the grid positions occupied by the piece.

        Returns:
            List[Tuple[int, int]]: List of (x, y) coordinates occupied by the piece
        """
        positions = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    positions.append((self.x + x, self.y + y))
        return positions

    def get_preview_positions(self, preview_x: int, preview_y: int) -> List[Tuple[int, int]]:
        """Get the grid positions for preview display.

        Args:
            preview_x: X coordinate for preview display
            preview_y: Y coordinate for preview display

        Returns:
            List[Tuple[int, int]]: List of (x, y) coordinates for preview display
        """
        positions = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    positions.append((preview_x + x, preview_y + y))
        return positions
