"""
Tetris Game Implementation

A PyGame-based Tetris game with standard controls:
- Left/Right arrows: Move piece
- Down arrow: Increase falling speed
- Up arrow: Rotate piece
"""
import sys
import pygame
from game.board import Board
from game.pieces import Piece
from game.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    FALL_SPEED, FAST_FALL_SPEED,
    WHITE, GRAY, CELL_SIZE
)

def main():
    """Initialize and run the Tetris game."""
    pygame.init()  # pylint: disable=no-member
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    board = Board()
    current_piece = None
    fall_time = 0
    fall_speed = FALL_SPEED
    game_over = False
    font = pygame.font.Font(None, 48)

    while True:
        if current_piece is None and not game_over:
            current_piece = Piece()
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
        if current_piece:
            for x, y in current_piece.get_positions():
                px = (x * CELL_SIZE) + CELL_SIZE
                py = (y * CELL_SIZE) + CELL_SIZE
                pygame.draw.rect(screen, current_piece.color,
                    (px, py, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GRAY,
                    (px, py, CELL_SIZE, CELL_SIZE), 1)

        if game_over:
            text = font.render("ゲームオーバー", True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)

        pygame.display.flip()

if __name__ == "__main__":
    main()
