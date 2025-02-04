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
from game.constants import WINDOW_WIDTH, WINDOW_HEIGHT

def main():
    """Initialize and run the Tetris game."""
    pygame.init()  # pylint: disable=no-member
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    board = Board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                pygame.quit()  # pylint: disable=no-member
                sys.exit()

        board.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()
