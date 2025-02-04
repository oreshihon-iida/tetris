"""Board module for the Tetris game."""
import pygame
from .constants import (
    GRID_WIDTH, GRID_HEIGHT, CELL_SIZE,
    BLACK, WHITE, GRAY
)

class Board:
    """Represents the Tetris game board and handles drawing."""
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game board including grid lines and border."""
        # Fill background
        screen.fill(BLACK)

        # Draw grid
        for y in range(self.height):
            for x in range(self.width):
                # Calculate pixel position with offset for border
                px = (x * CELL_SIZE) + CELL_SIZE
                py = (y * CELL_SIZE) + CELL_SIZE

                # Draw cell border
                pygame.draw.rect(screen, GRAY,
                    (px, py, CELL_SIZE, CELL_SIZE), 1)

        # Draw border around play area
        pygame.draw.rect(screen, WHITE,
            (CELL_SIZE, CELL_SIZE,
             GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 2)
