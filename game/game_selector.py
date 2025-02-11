"""Game selector module for choosing between Tetris and Puyo Puyo."""
from typing import Optional
import pygame
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, WHITE,
    GAME_SELECT_TEXT, GAME_SELECT_TEXT_EN,
    TETRIS_TEXT, TETRIS_TEXT_EN,
    PUYO_TEXT, PUYO_TEXT_EN
)

class GameSelector:
    """Handles the game selection screen."""
    def __init__(self, font: pygame.font.Font, has_japanese: bool):
        self.selected_game = None
        self.font = font
        self.has_japanese = has_japanese
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the game selection screen."""
        screen.fill(BLACK)
        
        # Draw title
        title = self.font.render(
            GAME_SELECT_TEXT if self.has_japanese else GAME_SELECT_TEXT_EN,
            True, WHITE
        )
        title_rect = title.get_rect(centerx=WINDOW_WIDTH//2, centery=WINDOW_HEIGHT//3)
        screen.blit(title, title_rect)
        
        # Draw game options
        tetris_text = self.font.render(
            TETRIS_TEXT if self.has_japanese else TETRIS_TEXT_EN,
            True, WHITE
        )
        puyo_text = self.font.render(
            PUYO_TEXT if self.has_japanese else PUYO_TEXT_EN,
            True, WHITE
        )
        
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
