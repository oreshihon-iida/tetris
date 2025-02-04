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
FALL_SPEED = 0.5  # seconds per grid
FAST_FALL_SPEED = 0.02  # seconds per grid

# UI dimensions
SIDEBAR_WIDTH = 6 * CELL_SIZE  # 6セル分の幅
PREVIEW_OFFSET_Y = 2 * CELL_SIZE  # プレビュー表示の縦位置
LINES_OFFSET_Y = 8 * CELL_SIZE  # 行数表示の縦位置

# Window dimensions
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * CELL_SIZE

# Font settings
FONT_PATHS = [
    "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",  # Primary
    "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf", # Fallback 1
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",       # Fallback 2
]
FONT_SIZE = 48
GAME_OVER_TEXT = "ゲームオーバー"
