"""Board module for the Tetris game."""
import pygame
from .constants import (
    GRID_WIDTH, GRID_HEIGHT, CELL_SIZE,
    BLACK, WHITE, GRAY,
    WINDOW_WIDTH, SIDEBAR_WIDTH,
    PREVIEW_OFFSET_Y, LINES_OFFSET_Y
)

class Board:
    """Represents the Tetris game board and handles drawing."""
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.lines_cleared = 0  # 消した行数のカウンター

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
        self.lines_cleared += lines_cleared
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

    def draw_sidebar(self, screen: pygame.Surface, next_piece: 'Piece') -> None:
        """Draw sidebar with next piece preview and lines cleared."""
        # Draw next piece preview
        if next_piece:
            # サイドバーの左端に配置（1セル分のマージン）
            sidebar_left = GRID_WIDTH * CELL_SIZE + 2 * CELL_SIZE
            preview_x = (sidebar_left + CELL_SIZE) // CELL_SIZE
            preview_y = PREVIEW_OFFSET_Y // CELL_SIZE
            
            # プレビュー用の位置を使用して描画
            for x, y in next_piece.get_preview_positions(preview_x, preview_y):
                px = x * CELL_SIZE
                py = y * CELL_SIZE
                pygame.draw.rect(screen, next_piece.color,
                    (px, py, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GRAY,
                    (px, py, CELL_SIZE, CELL_SIZE), 1)

        # Draw lines cleared
        font = pygame.font.Font(None, 36)
        text = f"Lines: {self.lines_cleared}"
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(
            centerx=WINDOW_WIDTH - SIDEBAR_WIDTH // 2,
            centery=LINES_OFFSET_Y
        )
        screen.blit(text_surface, text_rect)
