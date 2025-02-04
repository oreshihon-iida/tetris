"""Constants used throughout the Tetris game."""

# Grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30  # pixels

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Window dimensions
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * CELL_SIZE  # Add padding
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * CELL_SIZE  # Add padding
