"""Settings screen module."""
import pygame
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BLACK, WHITE, GRAY
)

class SettingsScreen:
    """Handles the settings screen UI."""
    def __init__(self, font: pygame.font.Font, has_japanese: bool, audio_manager):
        self.font = font
        self.has_japanese = has_japanese
        self.audio_manager = audio_manager
        self.slider_rect = pygame.Rect(
            WINDOW_WIDTH//4,
            WINDOW_HEIGHT//2,
            WINDOW_WIDTH//2,
            20
        )
        self.handle_rect = pygame.Rect(0, 0, 20, 30)
        self._update_handle_position()

    def _update_handle_position(self) -> None:
        """Update slider handle position based on volume."""
        volume = self.audio_manager.get_volume()
        self.handle_rect.centerx = (
            self.slider_rect.left +
            int(volume * self.slider_rect.width)
        )
        self.handle_rect.centery = self.slider_rect.centery

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
            centery=WINDOW_HEIGHT//3
        )
        screen.blit(title, title_rect)

        # Draw volume label
        volume_text = self.font.render(
            "音量" if self.has_japanese else "Volume",
            True, WHITE
        )
        volume_rect = volume_text.get_rect(
            centerx=WINDOW_WIDTH//2,
            bottom=self.slider_rect.top - 20
        )
        screen.blit(volume_text, volume_rect)

        # Draw slider
        pygame.draw.rect(screen, GRAY, self.slider_rect)
        pygame.draw.rect(screen, WHITE, self.handle_rect)

    def handle_input(self, event) -> bool:
        """Handle input events.

        Returns:
            bool: True if ESC pressed to exit settings
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self._update_volume(event.pos[0])
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left button
                if self.slider_rect.collidepoint(event.pos):
                    self._update_volume(event.pos[0])
        return False

    def _update_volume(self, x_pos: int) -> None:
        """Update volume based on slider position."""
        volume = (x_pos - self.slider_rect.left) / self.slider_rect.width
        volume = max(0.0, min(1.0, volume))
        self.audio_manager.set_volume(volume)
        self._update_handle_position()
