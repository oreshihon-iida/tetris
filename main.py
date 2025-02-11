"""
Game Implementation

A PyGame-based game collection with:
1. Tetris
   - Left/Right arrows: Move piece
   - Down arrow: Increase falling speed
   - Up arrow: Rotate piece
2. Puyo Puyo
   - Left/Right arrows: Move Puyo pair
   - Down arrow: Increase falling speed
   - Up arrow: Rotate piece
"""
import sys
import pygame
from game.board import Board
from game.pieces import Piece
from game.puyo_board import PuyoBoard
from game.puyo import PuyoPair
from game.game_selector import GameSelector
from game.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    FALL_SPEED, FAST_FALL_SPEED,
    WHITE, GRAY, CELL_SIZE,
    FONT_PATHS, FONT_SIZE,
    GAME_OVER_TEXT, GAME_OVER_TEXT_EN,
    JAPANESE_FONT_NAMES
)

def init_font():
    """Initialize game font with Japanese support."""
    # Try loading fonts from file paths first
    for font_path in FONT_PATHS:
        try:
            font = pygame.font.Font(font_path, FONT_SIZE)
            test_surface = font.render("テスト", True, WHITE)
            if test_surface.get_width() > 0:
                print(f"Successfully loaded font: {font_path}")
                return font, True
        except (FileNotFoundError, OSError) as e:
            print(f"Failed to load font {font_path}: {e}")
    
    # Try system fonts as fallback
    for font_name in JAPANESE_FONT_NAMES:
        try:
            font = pygame.font.SysFont(font_name, FONT_SIZE)
            test_surface = font.render("テスト", True, WHITE)
            if test_surface.get_width() > 0:
                print(f"Successfully loaded system font: {font_name}")
                return font, True
        except Exception as e:
            print(f"Failed to load system font {font_name}: {e}")
    
    print("Falling back to default font")
    return pygame.font.Font(None, FONT_SIZE), False

def run_tetris():
    """Initialize and run the Tetris game."""
    pygame.init()  # pylint: disable=no-member
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    board = Board()
    current_piece = None
    next_piece = Piece()
    fall_time = 0
    fall_speed = FALL_SPEED
    game_over = False
    font, has_japanese = init_font()

    while True:
        if current_piece is None and not game_over:
            current_piece = next_piece
            next_piece = Piece()
            if not board.is_valid_move(current_piece):
                game_over = True

        fall_time += clock.get_rawtime()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                pygame.quit()  # pylint: disable=no-member
                sys.exit()
            if not game_over and current_piece:
                if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                    if event.key == pygame.K_LEFT:  # pylint: disable=no-member
                        current_piece.x -= 1
                        if not board.is_valid_move(current_piece):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:  # pylint: disable=no-member
                        current_piece.x += 1
                        if not board.is_valid_move(current_piece):
                            current_piece.x -= 1
                    elif event.key == pygame.K_UP:  # pylint: disable=no-member
                        current_piece.rotate()
                        if not board.is_valid_move(current_piece):
                            for _ in range(3):  # 元の向きに戻す
                                current_piece.rotate()
                    elif event.key == pygame.K_DOWN:  # pylint: disable=no-member
                        fall_speed = FAST_FALL_SPEED
                elif event.type == pygame.KEYUP:  # pylint: disable=no-member
                    if event.key == pygame.K_DOWN:  # pylint: disable=no-member
                        fall_speed = FALL_SPEED
            elif game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # pylint: disable=no-member
                    board = Board()
                    current_piece = None
                    game_over = False
                    fall_speed = FALL_SPEED
                    fall_time = 0

        if not game_over and current_piece and fall_time >= fall_speed * 1000:
            current_piece.y += 1
            if not board.is_valid_move(current_piece):
                current_piece.y -= 1
                board.merge_piece(current_piece)
                board.clear_lines()
                current_piece = None
            fall_time = 0

        board.draw(screen)
        board.draw_sidebar(screen, next_piece)
        if current_piece:
            for x, y in current_piece.get_positions():
                px = (x * CELL_SIZE) + CELL_SIZE
                py = (y * CELL_SIZE) + CELL_SIZE
                pygame.draw.rect(screen, current_piece.color,
                    (px, py, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GRAY,
                    (px, py, CELL_SIZE, CELL_SIZE), 1)

        if game_over:
            text = font.render(GAME_OVER_TEXT if has_japanese else GAME_OVER_TEXT_EN, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()

def run_puyo():
    """Initialize and run the Puyo Puyo game."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Puyo Puyo")
    clock = pygame.time.Clock()
    board = PuyoBoard()
    current_pair = None
    next_pair = PuyoPair()
    fall_time = 0
    fall_speed = FALL_SPEED
    game_over = False
    font, has_japanese = init_font()

    while True:
        if current_pair is None and not game_over:
            current_pair = next_pair
            next_pair = PuyoPair()
            if not board.is_valid_move(current_pair):
                game_over = True

        fall_time += clock.get_rawtime()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over and current_pair:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_pair.move(-1, 0)
                        if not board.is_valid_move(current_pair):
                            current_pair.move(1, 0)
                    elif event.key == pygame.K_RIGHT:
                        current_pair.move(1, 0)
                        if not board.is_valid_move(current_pair):
                            current_pair.move(-1, 0)
                    elif event.key == pygame.K_UP:
                        current_pair.rotate_clockwise()
                        if not board.is_valid_move(current_pair):
                            current_pair.rotate_counterclockwise()
                    elif event.key == pygame.K_DOWN:
                        fall_speed = FAST_FALL_SPEED
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        fall_speed = FALL_SPEED
            elif game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    board = PuyoBoard()
                    current_pair = None
                    game_over = False
                    fall_speed = FALL_SPEED
                    fall_time = 0

        if not game_over and current_pair and fall_time >= fall_speed * 1000:
            current_pair.move(0, 1)
            if not board.is_valid_move(current_pair):
                current_pair.move(0, -1)
                board.merge_pair(current_pair)
                while board.apply_gravity():
                    pass
                while board.clear_groups():
                    while board.apply_gravity():
                        pass
                current_pair = None
            fall_time = 0

        board.draw(screen)
        board.draw_sidebar(screen, next_pair)
        if current_pair:
            for x, y, color in current_pair.get_positions():
                if y >= 0:  # Only draw if within visible area
                    px = (x * CELL_SIZE) + CELL_SIZE
                    py = (y * CELL_SIZE) + CELL_SIZE
                    pygame.draw.rect(screen, color,
                        (px, py, CELL_SIZE, CELL_SIZE))
                    pygame.draw.circle(screen, color,
                        (px + CELL_SIZE//2, py + CELL_SIZE//2),
                        CELL_SIZE//2 - 2)
                    pygame.draw.rect(screen, GRAY,
                        (px, py, CELL_SIZE, CELL_SIZE), 1)

        if game_over:
            text = font.render(GAME_OVER_TEXT if has_japanese else GAME_OVER_TEXT_EN, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()

def main():
    """Initialize and run the game selector."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game Selection")
    font, has_japanese = init_font()
    selector = GameSelector(font, has_japanese)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            selected_game = selector.handle_input(event)
            if selected_game == 'tetris':
                run_tetris()
            elif selected_game == 'puyo':
                run_puyo()
        
        selector.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
