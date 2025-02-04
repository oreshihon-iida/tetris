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

    def is_valid_move(self, piece) -> bool:
        """Check if the piece can move to its current position.
        
        Args:
            piece: The piece to check

        Returns:
            bool: True if the move is valid, False otherwise
        """
        for x, y in piece.get_positions():
            if (x < 0 or x >= self.width or
                y < 0 or y >= self.height or
                self.grid[y][x] != 0):
                return False
        return True

    def merge_piece(self, piece) -> None:
        """Fix the piece in its current position on the board.
        
        Args:
            piece: The piece to merge into the board
        """
        for x, y in piece.get_positions():
            self.grid[y][x] = piece.color

    def clear_lines(self) -> int:
        """Clear completed lines and return the number of lines cleared.
        
        Returns:
            int: Number of lines cleared
        """
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            if all(cell != 0 for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0] * self.width)
                lines_cleared += 1
            else:
                y -= 1
        return lines_cleared

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game board including grid lines and border."""
        # Fill background
        screen.fill(BLACK)

        # Draw grid and pieces
        for y in range(self.height):
            for x in range(self.width):
                px = (x * CELL_SIZE) + CELL_SIZE
                py = (y * CELL_SIZE) + CELL_SIZE

                # Draw filled cells
                if self.grid[y][x] != 0:
                    pygame.draw.rect(screen, self.grid[y][x],
                        (px, py, CELL_SIZE, CELL_SIZE))

                # Draw cell border
                pygame.draw.rect(screen, GRAY,
                    (px, py, CELL_SIZE, CELL_SIZE), 1)

        # Draw border around play area
        pygame.draw.rect(screen, WHITE,
            (CELL_SIZE, CELL_SIZE,
             GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 2)
