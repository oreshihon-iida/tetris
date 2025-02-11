"""Game selector module for choosing between Tetris and Puyo Puyo."""
from typing import Optional
import pygame
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, WHITE
)

class GameSelector:
    """Handles the game selection screen."""
    def __init__(self):
        self.selected_game = None
        self.font = pygame.font.Font(None, 48)
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game selection screen."""
        screen.fill(BLACK)
        
        # Draw title
        title = self.font.render("ゲームを選択してください", True, WHITE)
        title_rect = title.get_rect(centerx=WINDOW_WIDTH//2, centery=WINDOW_HEIGHT//3)
        screen.blit(title, title_rect)
        
        # Draw game options
        tetris_text = self.font.render("1: テトリス", True, WHITE)
        puyo_text = self.font.render("2: ぷよぷよ", True, WHITE)
        
        tetris_rect = tetris_text.get_rect(centerx=WINDOW_WIDTH//2, centery=WINDOW_HEIGHT//2)
        puyo_rect = puyo_text.get_rect(centerx=WINDOW_WIDTH//2, centery=WINDOW_HEIGHT//2 + 60)
        
        screen.blit(tetris_text, tetris_rect)
        screen.blit(puyo_text, puyo_rect)
        
    def handle_input(self, event) -> Optional[str]:
        """Handle keyboard input for game selection.
        
        Returns:
            str: Selected game ('tetris', 'puyo', or None)
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return 'tetris'
            elif event.key == pygame.K_2:
                return 'puyo'
        return None
