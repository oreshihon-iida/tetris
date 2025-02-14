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
BASE_FALL_SPEED = 0.1  # seconds per grid
FAST_FALL_SPEED = 0.004  # seconds per grid

# Level settings
DEFAULT_LINES_PER_LEVEL = 10  # Default number of lines to clear for level up
MIN_LINES_PER_LEVEL = 1  # Minimum lines per level
MAX_LINES_PER_LEVEL = 20  # Maximum lines per level
MAX_LEVEL = 20  # Maximum level (20G)

class GameSettings:
    """Mutable game settings."""
    def __init__(self):
        self.lines_per_level = DEFAULT_LINES_PER_LEVEL

SETTINGS = GameSettings()

# Text settings
LINES_PER_LEVEL_TEXT = "レベルアップまでの行数"
LINES_PER_LEVEL_TEXT_EN = "Lines per Level"

def calculate_fall_speed(level: int) -> float:
    """Calculate fall speed based on level.
    
    Speed increases exponentially with level, maxing out at 20G (0.05/60 seconds per grid)
    """
    if level >= MAX_LEVEL:
        return 0.05/60  # 20G speed
    return BASE_FALL_SPEED * (0.8 ** level)

# UI dimensions
SIDEBAR_WIDTH = 6 * CELL_SIZE  # 6セル分の幅
PREVIEW_OFFSET_Y = 2 * CELL_SIZE  # プレビュー表示の縦位置
LINES_OFFSET_Y = 8 * CELL_SIZE  # 行数表示の縦位置

# Window dimensions
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * CELL_SIZE

# Font settings
FONT_PATHS = [
    # Linux paths
    "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf",
    "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    # Windows paths
    "C:/Windows/Fonts/msgothic.ttc",
    "C:/Windows/Fonts/YuGothM.ttc",
    "C:/Windows/Fonts/meiryo.ttc"
]
JAPANESE_FONT_NAMES = [
    "MS Gothic",
    "Yu Gothic",
    "Meiryo",
    "MS Mincho",
    "Yu Mincho"
]
FONT_SIZE = 48
GAME_OVER_TEXT = "ゲームオーバー"
GAME_OVER_TEXT_EN = "GAME OVER"  # Fallback text for when Japanese fonts are unavailable
GAME_SELECT_TEXT = "ゲームを選択してください"
GAME_SELECT_TEXT_EN = "SELECT GAME"
TETRIS_TEXT = "1: テトリス"
TETRIS_TEXT_EN = "1: TETRIS"
PUYO_TEXT = "2: ぷよぷよ"
PUYO_TEXT_EN = "2: PUYO PUYO"
SETTINGS_TEXT = "3: 設定"
SETTINGS_TEXT_EN = "3: SETTINGS"
VOLUME_TEXT = "音量"
VOLUME_TEXT_EN = "VOLUME"
