"""Constants used throughout the Tetris game."""

# Grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30  # pixels

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Tetrimino colors
CYAN = (0, 255, 255)    # I piece
YELLOW = (255, 255, 0)  # O piece
PURPLE = (128, 0, 128)  # T piece
GREEN = (0, 255, 0)     # S piece
RED = (255, 0, 0)       # Z piece
BLUE = (0, 0, 255)      # J piece
ORANGE = (255, 165, 0)  # L piece

# Game settings
FALL_SPEED = 1.0  # seconds per grid
FAST_FALL_SPEED = 0.1  # seconds per grid

# Window dimensions
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * CELL_SIZE  # Add padding
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * CELL_SIZE  # Add padding
