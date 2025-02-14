"""Settings screen module."""
import pygame
import sys
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, WHITE, GRAY,
    LINES_PER_LEVEL_TEXT, LINES_PER_LEVEL_TEXT_EN,
    MIN_LINES_PER_LEVEL, MAX_LINES_PER_LEVEL,
    DEFAULT_LINES_PER_LEVEL
)
from .settings_store import load_settings, save_settings

class SettingsScreen:
    """Handles the settings screen UI."""
    def __init__(self, font: pygame.font.Font, has_japanese: bool, audio_manager):
        self.font = font
        self.has_japanese = has_japanese
        self.audio_manager = audio_manager
        
        # Load saved settings
        self.settings = load_settings()
        volume = self.settings.get('volume', 1.0)
        lines_per_level = self.settings.get('lines_per_level', DEFAULT_LINES_PER_LEVEL)
        
        # Apply loaded settings
        self.audio_manager.set_volume(volume)
        from .constants import SETTINGS
        SETTINGS.lines_per_level = lines_per_level
        
        # Volume slider
        self.volume_slider_rect = pygame.Rect(
            WINDOW_WIDTH//4,
            WINDOW_HEIGHT//2 - 50,
            WINDOW_WIDTH//2,
            20
        )
        self.volume_handle_rect = pygame.Rect(0, 0, 20, 30)
        
        # Lines per level slider
        self.lines_slider_rect = pygame.Rect(
            WINDOW_WIDTH//4,
            WINDOW_HEIGHT//2 + 50,
            WINDOW_WIDTH//2,
            20
        )
        self.lines_handle_rect = pygame.Rect(0, 0, 20, 30)
        
        self._update_volume_handle()
        self._update_lines_handle()

    def _update_volume_handle(self) -> None:
        """Update volume slider handle position."""
        volume = self.audio_manager.get_volume()
        self.volume_handle_rect.centerx = (
            self.volume_slider_rect.left +
            int(volume * self.volume_slider_rect.width)
        )
        self.volume_handle_rect.centery = self.volume_slider_rect.centery
        
    def _update_lines_handle(self) -> None:
        """Update lines per level slider handle position."""
        from .constants import SETTINGS, MIN_LINES_PER_LEVEL, MAX_LINES_PER_LEVEL
        normalized_pos = (SETTINGS.lines_per_level - MIN_LINES_PER_LEVEL) / (MAX_LINES_PER_LEVEL - MIN_LINES_PER_LEVEL)
        self.lines_handle_rect.centerx = (
            self.lines_slider_rect.left +
            int(normalized_pos * self.lines_slider_rect.width)
        )
        self.lines_handle_rect.centery = self.lines_slider_rect.centery

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the settings screen."""
        screen.fill(BLACK)

        # Draw title
        title = self.font.render(
            "設定" if self.has_japanese else "Settings",
            True, WHITE
        )
        title_rect = title.get_rect(
            centerx=WINDOW_WIDTH//2,
            centery=WINDOW_HEIGHT//4
        )
        screen.blit(title, title_rect)

        # Draw volume section
        volume_text = self.font.render(
            "音量" if self.has_japanese else "Volume",
            True, WHITE
        )
        volume_rect = volume_text.get_rect(
            centerx=WINDOW_WIDTH//2,
            bottom=self.volume_slider_rect.top - 20
        )
        screen.blit(volume_text, volume_rect)
        pygame.draw.rect(screen, GRAY, self.volume_slider_rect)
        pygame.draw.rect(screen, WHITE, self.volume_handle_rect)

        # Draw lines per level section
        lines_text = self.font.render(
            LINES_PER_LEVEL_TEXT if self.has_japanese else LINES_PER_LEVEL_TEXT_EN,
            True, WHITE
        )
        lines_rect = lines_text.get_rect(
            centerx=WINDOW_WIDTH//2,
            bottom=self.lines_slider_rect.top - 20
        )
        screen.blit(lines_text, lines_rect)
        pygame.draw.rect(screen, GRAY, self.lines_slider_rect)
        pygame.draw.rect(screen, WHITE, self.lines_handle_rect)

        # Draw current value for lines per level
        from .constants import SETTINGS
        value_text = self.font.render(str(SETTINGS.lines_per_level), True, WHITE)
        value_rect = value_text.get_rect(
            centerx=WINDOW_WIDTH//2,
            top=self.lines_slider_rect.bottom + 20
        )
        screen.blit(value_text, value_rect)

    def handle_input(self, event) -> bool:
        """Handle input events.

        Returns:
            bool: True if ESC pressed to exit settings
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.volume_slider_rect.collidepoint(event.pos):
                self._update_volume(event.pos[0])
            elif self.lines_slider_rect.collidepoint(event.pos):
                self._update_lines_per_level(event.pos[0])
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left button
                if self.volume_slider_rect.collidepoint(event.pos):
                    self._update_volume(event.pos[0])
                elif self.lines_slider_rect.collidepoint(event.pos):
                    self._update_lines_per_level(event.pos[0])
        return False

    def _update_volume(self, x_pos: int) -> None:
        """Update volume based on slider position."""
        volume = (x_pos - self.volume_slider_rect.left) / self.volume_slider_rect.width
        volume = max(0.0, min(1.0, volume))
        self.audio_manager.set_volume(volume)
        self.settings['volume'] = volume
        save_settings(self.settings)
        self._update_volume_handle()

    def _update_lines_per_level(self, x_pos: int) -> None:
        """Update lines per level based on slider position."""
        normalized_pos = (x_pos - self.lines_slider_rect.left) / self.lines_slider_rect.width
        normalized_pos = max(0.0, min(1.0, normalized_pos))
        
        # Calculate lines per level (1-20)
        from .constants import MIN_LINES_PER_LEVEL, MAX_LINES_PER_LEVEL
        import builtins
        lines = builtins.round(MIN_LINES_PER_LEVEL + normalized_pos * (MAX_LINES_PER_LEVEL - MIN_LINES_PER_LEVEL))
        
        # Update the global setting and save
        from .constants import SETTINGS
        SETTINGS.lines_per_level = lines
        self.settings['lines_per_level'] = lines
        save_settings(self.settings)
        self._update_lines_handle()
