"""Board module for Puyo Puyo game."""
from typing import List, Set, Tuple, Optional, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from .puyo import PuyoPair
from .constants import (
    GRID_WIDTH, GRID_HEIGHT, CELL_SIZE,
    BLACK, WHITE, GRAY,
    WINDOW_WIDTH, SIDEBAR_WIDTH,
    PREVIEW_OFFSET_Y, LINES_OFFSET_Y
)

class PuyoBoard:
    """Represents the Puyo Puyo game board and handles game logic."""
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.chain_count = 0

    def is_valid_move(self, puyo_pair) -> bool:
        """Check if the Puyo pair can move to its current position."""
        for x, y, _ in puyo_pair.get_positions():
            if (x < 0 or x >= self.width or
                y < 0 or y >= self.height or
                (y >= 0 and self.grid[y][x] is not None)):
                return False
        return True

    def merge_pair(self, puyo_pair) -> None:
        """Fix the Puyo pair in its current position on the board."""
        for x, y, color in puyo_pair.get_positions():
            if y >= 0:  # Only merge if within the grid
                self.grid[y][x] = color

    def apply_gravity(self) -> bool:
        """Apply gravity to make Puyos fall into empty spaces.
        
        Returns:
            bool: True if any Puyo moved
        """
        moved = False
        for x in range(self.width):
            for y in range(self.height - 2, -1, -1):
                if self.grid[y][x] is not None and self.grid[y + 1][x] is None:
                    self.grid[y + 1][x] = self.grid[y][x]
                    self.grid[y][x] = None
                    moved = True
        return moved

    def find_connected(self, x: int, y: int, color: Optional[Tuple[int, int, int]], visited: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Find all connected Puyos of the same color using DFS."""
        if (x < 0 or x >= self.width or y < 0 or y >= self.height or
            self.grid[y][x] != color or (x, y) in visited):
            return []
        
        visited.add((x, y))
        connected = [(x, y)]
        
        # Check all four directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            connected.extend(self.find_connected(x + dx, y + dy, color, visited))
        
        return connected

    def clear_groups(self) -> bool:
        """Clear groups of 4 or more connected Puyos.
        
        Returns:
            bool: True if any groups were cleared
        """
        visited = set()
        cleared = False
        
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is not None and (x, y) not in visited:
                    color = self.grid[y][x]
                    group = self.find_connected(x, y, color, visited)
                    if len(group) >= 4:
                        for gx, gy in group:
                            self.grid[gy][gx] = None
                        self.score += len(group) * 10 * (self.chain_count + 1)
                        cleared = True

        if cleared:
            self.chain_count += 1
        else:
            self.chain_count = 0
            
        return cleared

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game board including grid lines and Puyos."""
        # Fill background
        screen.fill(BLACK)

        # Draw grid and Puyos
        for y in range(self.height):
            for x in range(self.width):
                px = (x * CELL_SIZE) + CELL_SIZE
                py = (y * CELL_SIZE) + CELL_SIZE

                # Draw filled cells
                if self.grid[y][x] is not None:
                    pygame.draw.rect(screen, self.grid[y][x],
                        (px, py, CELL_SIZE, CELL_SIZE))
                    pygame.draw.circle(screen, self.grid[y][x],
                        (px + CELL_SIZE//2, py + CELL_SIZE//2),
                        CELL_SIZE//2 - 2)

                # Draw cell border
                pygame.draw.rect(screen, GRAY,
                    (px, py, CELL_SIZE, CELL_SIZE), 1)

        # Draw border around play area
        pygame.draw.rect(screen, WHITE,
            (CELL_SIZE, CELL_SIZE,
             GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 2)

    def draw_sidebar(self, screen: pygame.Surface, next_pair: Optional['PuyoPair']) -> None:
        """Draw sidebar with next Puyo pair preview and score."""
        if next_pair:
            sidebar_left = GRID_WIDTH * CELL_SIZE + 2 * CELL_SIZE
            preview_x = (sidebar_left + CELL_SIZE) // CELL_SIZE
            preview_y = PREVIEW_OFFSET_Y // CELL_SIZE
            
            for x, y, color in next_pair.get_preview_positions(preview_x, preview_y):
                px = x * CELL_SIZE
                py = y * CELL_SIZE
                pygame.draw.rect(screen, color,
                    (px, py, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, color,
                    (px + CELL_SIZE//2, py + CELL_SIZE//2),
                    CELL_SIZE//2 - 2)
                pygame.draw.rect(screen, GRAY,
                    (px, py, CELL_SIZE, CELL_SIZE), 1)

        # Draw score
        font = pygame.font.Font(None, 36)
        text = f"Score: {self.score}"
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(
            centerx=WINDOW_WIDTH - SIDEBAR_WIDTH // 2,
            centery=LINES_OFFSET_Y
        )
        screen.blit(text_surface, text_rect)
