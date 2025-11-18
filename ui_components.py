"""
WARHAMMER AGE OF SIGMAR - UI COMPONENTS
UI buttons, panels, menus, and tooltips
"""

import pygame
from typing import Tuple, List, Optional, Callable
from data_types import *


# ============================================================================
# COLORS
# ============================================================================

UI_BACKGROUND = (30, 35, 45)
UI_PANEL = (40, 45, 55)
UI_BUTTON = (70, 80, 90)
UI_BUTTON_HOVER = (90, 100, 110)
UI_BUTTON_ACTIVE = (110, 120, 130)
UI_BUTTON_DISABLED = (50, 55, 60)
UI_TEXT = (236, 240, 241)
UI_TEXT_DISABLED = (120, 120, 120)
UI_BORDER = (100, 110, 120)
UI_HIGHLIGHT = (255, 215, 0)


# ============================================================================
# UI BUTTON
# ============================================================================

class UIButton:
    """Clickable UI button"""

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 callback: Optional[Callable] = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

        self.is_enabled = True
        self.is_visible = True
        self.is_hovered = False
        self.is_pressed = False

        self.tooltip = ""
        self.icon = None

    def update(self, mouse_pos: Tuple[int, int], mouse_down: bool):
        """Update button state"""
        if not self.is_enabled or not self.is_visible:
            self.is_hovered = False
            self.is_pressed = False
            return

        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.is_pressed = self.is_hovered and mouse_down

    def handle_click(self) -> bool:
        """Handle button click. Returns True if clicked."""
        if self.is_enabled and self.is_visible and self.is_hovered:
            if self.callback:
                self.callback()
            return True
        return False

    def draw(self, screen, font):
        """Draw button"""
        if not self.is_visible:
            return

        # Determine color
        if not self.is_enabled:
            color = UI_BUTTON_DISABLED
            text_color = UI_TEXT_DISABLED
        elif self.is_pressed:
            color = UI_BUTTON_ACTIVE
            text_color = UI_TEXT
        elif self.is_hovered:
            color = UI_BUTTON_HOVER
            text_color = UI_TEXT
        else:
            color = UI_BUTTON
            text_color = UI_TEXT

        # Draw button background
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, UI_BORDER, self.rect, 2)

        # Draw text
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


# ============================================================================
# UI PANEL
# ============================================================================

class UIPanel:
    """UI panel container"""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title

        self.is_visible = True
        self.is_draggable = False
        self.is_dragging = False

        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.buttons: List[UIButton] = []
        self.text_lines: List[str] = []

        self.background_color = UI_PANEL
        self.border_color = UI_BORDER

    def add_button(self, button: UIButton):
        """Add button to panel"""
        self.buttons.append(button)

    def add_text(self, text: str):
        """Add text line to panel"""
        self.text_lines.append(text)

    def clear_text(self):
        """Clear all text lines"""
        self.text_lines.clear()

    def update(self, mouse_pos: Tuple[int, int], mouse_down: bool):
        """Update panel and buttons"""
        if not self.is_visible:
            return

        # Update buttons
        for button in self.buttons:
            button.update(mouse_pos, mouse_down)

    def handle_drag_start(self, mouse_pos: Tuple[int, int]):
        """Start dragging panel"""
        if self.is_draggable and self.rect.collidepoint(mouse_pos):
            self.is_dragging = True
            self.drag_offset_x = mouse_pos[0] - self.rect.x
            self.drag_offset_y = mouse_pos[1] - self.rect.y

    def handle_drag(self, mouse_pos: Tuple[int, int]):
        """Update drag position"""
        if self.is_dragging:
            self.rect.x = mouse_pos[0] - self.drag_offset_x
            self.rect.y = mouse_pos[1] - self.drag_offset_y

            # Update button positions
            # (Buttons have absolute positions, so need to move them too)

    def handle_drag_end(self):
        """End dragging"""
        self.is_dragging = False

    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Handle click on panel or buttons. Returns True if handled."""
        if not self.is_visible:
            return False

        # Check buttons
        for button in self.buttons:
            if button.handle_click():
                return True

        # Check if clicked on panel
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen, font):
        """Draw panel"""
        if not self.is_visible:
            return

        # Draw background
        pygame.draw.rect(screen, self.background_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        # Draw title
        if self.title:
            title_surface = font.render(self.title, True, UI_TEXT)
            screen.blit(title_surface, (self.rect.x + 10, self.rect.y + 10))

        # Draw text lines
        y_offset = 40 if self.title else 10
        for line in self.text_lines:
            text_surface = font.render(line, True, UI_TEXT)
            screen.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
            y_offset += 25

        # Draw buttons
        for button in self.buttons:
            button.draw(screen, font)


# ============================================================================
# CONTEXT MENU
# ============================================================================

class ContextMenu:
    """Right-click context menu"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 200
        self.is_visible = False

        self.options: List[str] = []
        self.callbacks: List[Optional[Callable]] = []

        self.hovered_index = -1
        self.option_height = 30

    def show(self, x: int, y: int, options: List[Tuple[str, Optional[Callable]]]):
        """Show context menu at position"""
        self.x = x
        self.y = y
        self.options = [opt[0] for opt in options]
        self.callbacks = [opt[1] for opt in options]
        self.is_visible = True

        # Adjust position if off-screen
        height = len(self.options) * self.option_height
        if self.y + height > 800:  # Assuming screen height
            self.y = 800 - height

    def hide(self):
        """Hide context menu"""
        self.is_visible = False
        self.hovered_index = -1

    def update(self, mouse_pos: Tuple[int, int]):
        """Update hover state"""
        if not self.is_visible:
            return

        self.hovered_index = -1

        # Check which option is hovered
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(
                self.x,
                self.y + i * self.option_height,
                self.width,
                self.option_height
            )
            if option_rect.collidepoint(mouse_pos):
                self.hovered_index = i
                break

    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Handle click on menu. Returns True if handled."""
        if not self.is_visible:
            return False

        # Check if clicked on menu
        menu_rect = pygame.Rect(
            self.x, self.y,
            self.width,
            len(self.options) * self.option_height
        )

        if menu_rect.collidepoint(mouse_pos):
            # Execute callback for hovered option
            if 0 <= self.hovered_index < len(self.callbacks):
                callback = self.callbacks[self.hovered_index]
                if callback:
                    callback()

            self.hide()
            return True
        else:
            # Clicked outside menu
            self.hide()
            return False

    def draw(self, screen, font):
        """Draw context menu"""
        if not self.is_visible:
            return

        # Draw background
        menu_rect = pygame.Rect(
            self.x, self.y,
            self.width,
            len(self.options) * self.option_height
        )
        pygame.draw.rect(screen, UI_PANEL, menu_rect)
        pygame.draw.rect(screen, UI_BORDER, menu_rect, 2)

        # Draw options
        for i, option in enumerate(self.options):
            y = self.y + i * self.option_height

            # Highlight if hovered
            if i == self.hovered_index:
                hover_rect = pygame.Rect(self.x, y, self.width, self.option_height)
                pygame.draw.rect(screen, UI_BUTTON_HOVER, hover_rect)

            # Draw text
            text_surface = font.render(option, True, UI_TEXT)
            screen.blit(text_surface, (self.x + 10, y + 5))


# ============================================================================
# TOOLTIP
# ============================================================================

class Tooltip:
    """Tooltip display"""

    def __init__(self):
        self.text = ""
        self.x = 0
        self.y = 0
        self.is_visible = False
        self.delay = 0.5  # seconds
        self.timer = 0.0

        self.padding = 5
        self.background_color = (50, 50, 50, 200)
        self.text_color = (255, 255, 255)

    def show(self, text: str, x: int, y: int):
        """Show tooltip"""
        self.text = text
        self.x = x + 15
        self.y = y + 15
        self.timer = 0.0
        self.is_visible = True

    def hide(self):
        """Hide tooltip"""
        self.is_visible = False
        self.text = ""
        self.timer = 0.0

    def update(self, dt: float):
        """Update tooltip timer"""
        if self.is_visible and self.timer < self.delay:
            self.timer += dt

    def draw(self, screen, font):
        """Draw tooltip"""
        if not self.is_visible or self.timer < self.delay or not self.text:
            return

        # Render text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()

        # Create background rect
        bg_rect = pygame.Rect(
            self.x,
            self.y,
            text_rect.width + self.padding * 2,
            text_rect.height + self.padding * 2
        )

        # Adjust if off-screen
        if bg_rect.right > screen.get_width():
            bg_rect.x = screen.get_width() - bg_rect.width
        if bg_rect.bottom > screen.get_height():
            bg_rect.y = screen.get_height() - bg_rect.height

        # Draw background
        surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.background_color, surface.get_rect())
        pygame.draw.rect(surface, UI_BORDER, surface.get_rect(), 1)
        screen.blit(surface, (bg_rect.x, bg_rect.y))

        # Draw text
        screen.blit(text_surface, (bg_rect.x + self.padding, bg_rect.y + self.padding))


# ============================================================================
# UI MANAGER
# ============================================================================

class UIManager:
    """Manages all UI elements"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.panels: List[UIPanel] = []
        self.context_menu = ContextMenu()
        self.tooltip = Tooltip()

        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def add_panel(self, panel: UIPanel):
        """Add panel to UI"""
        self.panels.append(panel)

    def update(self, mouse_pos: Tuple[int, int], mouse_down: bool, dt: float):
        """Update all UI elements"""
        # Update panels
        for panel in self.panels:
            panel.update(mouse_pos, mouse_down)

        # Update context menu
        self.context_menu.update(mouse_pos)

        # Update tooltip
        self.tooltip.update(dt)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Handle click on UI. Returns True if UI consumed the click."""
        # Check context menu first
        if self.context_menu.handle_click(mouse_pos):
            return True

        # Check panels
        for panel in reversed(self.panels):  # Top to bottom
            if panel.handle_click(mouse_pos):
                return True

        return False

    def is_mouse_over_ui(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if mouse is over any UI element"""
        # Check context menu
        if self.context_menu.is_visible:
            menu_rect = pygame.Rect(
                self.context_menu.x, self.context_menu.y,
                self.context_menu.width,
                len(self.context_menu.options) * self.context_menu.option_height
            )
            if menu_rect.collidepoint(mouse_pos):
                return True

        # Check panels
        for panel in self.panels:
            if panel.is_visible and panel.rect.collidepoint(mouse_pos):
                return True

        return False

    def show_context_menu(self, x: int, y: int, options: List[Tuple[str, Optional[Callable]]]):
        """Show context menu"""
        self.context_menu.show(x, y, options)

    def show_tooltip(self, text: str, x: int, y: int):
        """Show tooltip"""
        self.tooltip.show(text, x, y)

    def hide_tooltip(self):
        """Hide tooltip"""
        self.tooltip.hide()

    def draw(self, screen):
        """Draw all UI elements"""
        # Draw panels
        for panel in self.panels:
            panel.draw(screen, self.font_small)

        # Draw context menu
        self.context_menu.draw(screen, self.font_small)

        # Draw tooltip
        self.tooltip.draw(screen, self.font_small)
