"""
WARHAMMER AGE OF SIGMAR - INPUT HANDLER
Comprehensive mouse and keyboard input system
"""

import pygame
from typing import Tuple, List, Optional
from data_types import *


# ============================================================================
# KEY CODE CONSTANTS
# ============================================================================

# Movement keys
KEY_W = pygame.K_w
KEY_A = pygame.K_a
KEY_S = pygame.K_s
KEY_D = pygame.K_d
KEY_Q = pygame.K_q
KEY_E = pygame.K_e

# Action keys
KEY_R = pygame.K_r  # Retreat
KEY_F = pygame.K_f  # Fight
KEY_SPACE = pygame.K_SPACE
KEY_TAB = pygame.K_TAB
KEY_ESC = pygame.K_ESCAPE

# Number keys for abilities
KEY_1 = pygame.K_1
KEY_2 = pygame.K_2
KEY_3 = pygame.K_3
KEY_4 = pygame.K_4
KEY_5 = pygame.K_5

# Modifier keys
KEY_SHIFT = pygame.K_LSHIFT
KEY_CTRL = pygame.K_LCTRL
KEY_ALT = pygame.K_LALT


# ============================================================================
# INPUT STATE CLASSES
# ============================================================================

class MouseState:
    """Tracks mouse input state"""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.prev_x = 0
        self.prev_y = 0
        self.delta_x = 0
        self.delta_y = 0

        self.left_down = False
        self.right_down = False
        self.middle_down = False

        self.left_just_pressed = False
        self.right_just_pressed = False
        self.middle_just_pressed = False

        self.left_just_released = False
        self.right_just_released = False
        self.middle_just_released = False

        self.scroll_delta = 0

        self.drag_start_x = 0
        self.drag_start_y = 0
        self.is_dragging = False
        self.drag_threshold = 5  # pixels before drag starts

    def update(self):
        """Update mouse state"""
        self.prev_x = self.x
        self.prev_y = self.y
        self.x, self.y = pygame.mouse.get_pos()

        self.delta_x = self.x - self.prev_x
        self.delta_y = self.y - self.prev_y

        # Reset just pressed/released flags
        self.left_just_pressed = False
        self.right_just_pressed = False
        self.middle_just_pressed = False
        self.left_just_released = False
        self.right_just_released = False
        self.middle_just_released = False

        self.scroll_delta = 0

    def handle_button_down(self, button):
        """Handle mouse button press"""
        if button == 1:  # Left
            if not self.left_down:
                self.left_just_pressed = True
                self.drag_start_x = self.x
                self.drag_start_y = self.y
            self.left_down = True
        elif button == 3:  # Right
            if not self.right_down:
                self.right_just_pressed = True
            self.right_down = True
        elif button == 2:  # Middle
            if not self.middle_down:
                self.middle_just_pressed = True
            self.middle_down = True

    def handle_button_up(self, button):
        """Handle mouse button release"""
        if button == 1:  # Left
            if self.left_down:
                self.left_just_released = True
            self.left_down = False
            self.is_dragging = False
        elif button == 3:  # Right
            if self.right_down:
                self.right_just_released = True
            self.right_down = False
        elif button == 2:  # Middle
            if self.middle_down:
                self.middle_just_released = True
            self.middle_down = False

    def update_drag(self):
        """Update drag state"""
        if self.left_down and not self.is_dragging:
            drag_dist = ((self.x - self.drag_start_x) ** 2 +
                        (self.y - self.drag_start_y) ** 2) ** 0.5
            if drag_dist > self.drag_threshold:
                self.is_dragging = True


class KeyboardState:
    """Tracks keyboard input state"""

    def __init__(self):
        self.keys_down = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()

        self.shift = False
        self.ctrl = False
        self.alt = False

    def update(self):
        """Update keyboard state"""
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()

        # Update modifiers
        keys = pygame.key.get_pressed()
        self.shift = keys[KEY_SHIFT] or keys[pygame.K_RSHIFT]
        self.ctrl = keys[KEY_CTRL] or keys[pygame.K_RCTRL]
        self.alt = keys[KEY_ALT] or keys[pygame.K_RALT]

    def handle_key_down(self, key):
        """Handle key press"""
        if key not in self.keys_down:
            self.keys_just_pressed.add(key)
        self.keys_down.add(key)

    def handle_key_up(self, key):
        """Handle key release"""
        if key in self.keys_down:
            self.keys_just_released.add(key)
        self.keys_down.discard(key)

    def is_down(self, key) -> bool:
        """Check if key is currently down"""
        return key in self.keys_down

    def was_just_pressed(self, key) -> bool:
        """Check if key was just pressed this frame"""
        return key in self.keys_just_pressed


# ============================================================================
# SELECTION BOX
# ============================================================================

class SelectionBox:
    """Handles box selection"""

    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.is_active = False

    def start(self, x: int, y: int):
        """Start selection box"""
        self.start_x = x
        self.start_y = y
        self.end_x = x
        self.end_y = y
        self.is_active = True

    def update(self, x: int, y: int):
        """Update selection box"""
        self.end_x = x
        self.end_y = y

    def end(self):
        """End selection box"""
        self.is_active = False

    def get_rect(self) -> Tuple[int, int, int, int]:
        """Get selection rectangle (x, y, width, height)"""
        min_x = min(self.start_x, self.end_x)
        min_y = min(self.start_y, self.end_y)
        max_x = max(self.start_x, self.end_x)
        max_y = max(self.start_y, self.end_y)
        return (min_x, min_y, max_x - min_x, max_y - min_y)


# ============================================================================
# INPUT MANAGER
# ============================================================================

class InputManager:
    """Central input management"""

    def __init__(self):
        self.mouse = MouseState()
        self.keyboard = KeyboardState()
        self.selection_box = SelectionBox()

        # Input mode
        self.is_targeting_ability = False
        self.targeting_ability_name = ""

    def update(self):
        """Update all input states"""
        self.mouse.update()
        self.mouse.update_drag()
        self.keyboard.update()

    def handle_event(self, event):
        """Handle pygame event"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse.handle_button_down(event.button)

            if event.button == 4:  # Scroll up
                self.mouse.scroll_delta = 1
            elif event.button == 5:  # Scroll down
                self.mouse.scroll_delta = -1

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse.handle_button_up(event.button)

        elif event.type == pygame.KEYDOWN:
            self.keyboard.handle_key_down(event.key)

        elif event.type == pygame.KEYUP:
            self.keyboard.handle_key_up(event.key)

    def begin_targeting(self, ability_name: str):
        """Begin ability targeting mode"""
        self.is_targeting_ability = True
        self.targeting_ability_name = ability_name

    def cancel_targeting(self):
        """Cancel ability targeting"""
        self.is_targeting_ability = False
        self.targeting_ability_name = ""
