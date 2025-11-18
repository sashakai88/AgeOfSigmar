"""
WARHAMMER AGE OF SIGMAR - GRAPHICS ENGINE
2D Graphics rendering using Pygame
"""

try:
    import pygame
    import pygame.gfxdraw
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not installed. Graphics mode unavailable.")
    print("Install with: pip install pygame")

import math
from typing import Tuple, List, Optional
from data_types import *
from game_state import game_db, BATTLEFIELD_WIDTH, BATTLEFIELD_HEIGHT, COMBAT_RANGE


# ============================================================================
# CONSTANTS AND COLORS
# ============================================================================

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
BATTLEFIELD_OFFSET_X = 50
BATTLEFIELD_OFFSET_Y = 50
BATTLEFIELD_PIXEL_WIDTH = 880
BATTLEFIELD_PIXEL_HEIGHT = 800

# Scale factor (pixels per inch)
SCALE = BATTLEFIELD_PIXEL_WIDTH / BATTLEFIELD_WIDTH

# Colors (R, G, B)
COLOR_BACKGROUND = (20, 25, 35)
COLOR_BATTLEFIELD = (45, 52, 54)
COLOR_GRID = (60, 70, 80)
COLOR_PLAYER1 = (52, 152, 219)  # Blue
COLOR_PLAYER2 = (231, 76, 60)   # Red
COLOR_OBJECTIVE = (241, 196, 15)  # Gold
COLOR_TERRAIN = (46, 134, 64)   # Green
COLOR_TEXT = (236, 240, 241)
COLOR_HIGHLIGHT = (255, 255, 255)
COLOR_COMBAT_RANGE = (255, 100, 100, 50)
COLOR_MOVEMENT_RANGE = (100, 255, 100, 50)
COLOR_CHARGE_RANGE = (255, 255, 100, 50)
COLOR_SELECTED = (255, 215, 0)  # Gold
COLOR_PANEL = (30, 35, 45)
COLOR_BUTTON = (70, 80, 90)
COLOR_BUTTON_HOVER = (90, 100, 110)
COLOR_HP_BAR = (46, 204, 113)
COLOR_HP_BAR_BG = (100, 100, 100)


# ============================================================================
# GRAPHICS ENGINE CLASS
# ============================================================================

class GraphicsEngine:
    """Main graphics engine for rendering the game"""

    def __init__(self):
        if not PYGAME_AVAILABLE:
            raise ImportError("Pygame is required for graphics mode")

        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Warhammer Age of Sigmar")

        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)

        # Selected unit
        self.selected_unit = None
        self.hover_unit = None

        # Mouse state
        self.mouse_pos = (0, 0)

        # UI panels
        self.info_panel_rect = pygame.Rect(950, 50, 400, 800)

    def world_to_screen(self, x: float, y: float) -> Tuple[int, int]:
        """Convert world coordinates (inches) to screen pixels"""
        screen_x = int(BATTLEFIELD_OFFSET_X + x * SCALE)
        screen_y = int(BATTLEFIELD_OFFSET_Y + y * SCALE)
        return (screen_x, screen_y)

    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[float, float]:
        """Convert screen pixels to world coordinates (inches)"""
        world_x = (screen_x - BATTLEFIELD_OFFSET_X) / SCALE
        world_y = (screen_y - BATTLEFIELD_OFFSET_Y) / SCALE
        return (world_x, world_y)

    def draw_battlefield(self):
        """Draw the battlefield with grid"""
        # Background
        self.screen.fill(COLOR_BACKGROUND)

        # Battlefield area
        bf_rect = pygame.Rect(
            BATTLEFIELD_OFFSET_X,
            BATTLEFIELD_OFFSET_Y,
            BATTLEFIELD_PIXEL_WIDTH,
            BATTLEFIELD_PIXEL_HEIGHT
        )
        pygame.draw.rect(self.screen, COLOR_BATTLEFIELD, bf_rect)

        # Grid lines (every 6 inches)
        grid_spacing = 6 * SCALE

        # Vertical lines
        for i in range(int(BATTLEFIELD_WIDTH / 6) + 1):
            x = BATTLEFIELD_OFFSET_X + i * grid_spacing
            pygame.draw.line(
                self.screen,
                COLOR_GRID,
                (x, BATTLEFIELD_OFFSET_Y),
                (x, BATTLEFIELD_OFFSET_Y + BATTLEFIELD_PIXEL_HEIGHT),
                1
            )

        # Horizontal lines
        for i in range(int(BATTLEFIELD_HEIGHT / 6) + 1):
            y = BATTLEFIELD_OFFSET_Y + i * grid_spacing
            pygame.draw.line(
                self.screen,
                COLOR_GRID,
                (BATTLEFIELD_OFFSET_X, y),
                (BATTLEFIELD_OFFSET_X + BATTLEFIELD_PIXEL_WIDTH, y),
                1
            )

        # Border
        pygame.draw.rect(self.screen, COLOR_HIGHLIGHT, bf_rect, 2)

        # Deployment zones (simplified - horizontal split)
        deployment_y = BATTLEFIELD_OFFSET_Y + BATTLEFIELD_PIXEL_HEIGHT / 2
        pygame.draw.line(
            self.screen,
            (100, 100, 200),
            (BATTLEFIELD_OFFSET_X, deployment_y),
            (BATTLEFIELD_OFFSET_X + BATTLEFIELD_PIXEL_WIDTH, deployment_y),
            2
        )

        # Labels
        text_p1 = self.font_small.render("Player 1 Deployment", True, COLOR_PLAYER1)
        text_p2 = self.font_small.render("Player 2 Deployment", True, COLOR_PLAYER2)
        self.screen.blit(text_p1, (BATTLEFIELD_OFFSET_X + 10, BATTLEFIELD_OFFSET_Y + 10))
        self.screen.blit(text_p2, (BATTLEFIELD_OFFSET_X + 10,
                                   BATTLEFIELD_OFFSET_Y + BATTLEFIELD_PIXEL_HEIGHT - 30))

    def draw_objectives(self):
        """Draw objective markers"""
        for objective in game_db.objectives:
            screen_pos = self.world_to_screen(objective.x_position, objective.y_position)

            # Control radius (3")
            radius = int(COMBAT_RANGE * SCALE)

            # Draw control circle
            pygame.draw.circle(
                self.screen,
                (*COLOR_OBJECTIVE, 30),
                screen_pos,
                radius,
                0
            )

            # Draw objective marker
            pygame.draw.circle(
                self.screen,
                COLOR_OBJECTIVE,
                screen_pos,
                12,
                0
            )
            pygame.draw.circle(
                self.screen,
                COLOR_HIGHLIGHT,
                screen_pos,
                12,
                2
            )

            # Draw objective number
            text = self.font_small.render(str(objective.objective_id + 1), True, COLOR_BACKGROUND)
            text_rect = text.get_rect(center=screen_pos)
            self.screen.blit(text, text_rect)

            # Show controller
            if objective.controlled_by > 0:
                controller_color = COLOR_PLAYER1 if objective.controlled_by == 1 else COLOR_PLAYER2
                pygame.draw.circle(
                    self.screen,
                    controller_color,
                    screen_pos,
                    15,
                    3
                )

    def draw_terrain(self):
        """Draw terrain features"""
        for terrain in game_db.terrain_features:
            screen_pos = self.world_to_screen(terrain.x_position, terrain.y_position)

            # Draw terrain as a square/rectangle
            size = 40
            rect = pygame.Rect(
                screen_pos[0] - size // 2,
                screen_pos[1] - size // 2,
                size,
                size
            )

            pygame.draw.rect(self.screen, COLOR_TERRAIN, rect)
            pygame.draw.rect(self.screen, COLOR_HIGHLIGHT, rect, 2)

            # Draw type indicator
            text = self.font_tiny.render(terrain.terrain_type.value[:3], True, COLOR_TEXT)
            text_rect = text.get_rect(center=screen_pos)
            self.screen.blit(text, text_rect)

    def draw_unit(self, unit: BattlefieldUnit):
        """Draw a single unit"""
        if unit.model_count == 0:
            return

        warscroll = game_db.get_warscroll(unit.warscroll_ref)
        if not warscroll:
            return

        screen_pos = self.world_to_screen(unit.x_position, unit.y_position)

        # Determine color
        color = COLOR_PLAYER1 if unit.owner_player == 1 else COLOR_PLAYER2

        # Draw unit circle (size based on unit type)
        if warscroll.unit_type == UnitType.MONSTER:
            radius = 25
        elif warscroll.unit_type == UnitType.CAVALRY:
            radius = 18
        else:
            radius = 15

        # Highlight if selected
        if self.selected_unit == unit:
            pygame.draw.circle(self.screen, COLOR_SELECTED, screen_pos, radius + 5, 3)

        # Highlight if hovering
        if self.hover_unit == unit:
            pygame.draw.circle(self.screen, COLOR_HIGHLIGHT, screen_pos, radius + 3, 2)

        # Draw unit body
        pygame.draw.circle(self.screen, color, screen_pos, radius)
        pygame.draw.circle(self.screen, COLOR_HIGHLIGHT, screen_pos, radius, 2)

        # Draw model count
        count_text = self.font_small.render(str(unit.model_count), True, COLOR_TEXT)
        count_rect = count_text.get_rect(center=screen_pos)
        self.screen.blit(count_text, count_rect)

        # Draw health bar
        health_percentage = unit.model_count / warscroll.unit_size
        bar_width = radius * 2
        bar_height = 4
        bar_x = screen_pos[0] - radius
        bar_y = screen_pos[1] + radius + 5

        # Background
        pygame.draw.rect(
            self.screen,
            COLOR_HP_BAR_BG,
            (bar_x, bar_y, bar_width, bar_height)
        )

        # Health
        pygame.draw.rect(
            self.screen,
            COLOR_HP_BAR,
            (bar_x, bar_y, int(bar_width * health_percentage), bar_height)
        )

        # Combat indicator
        if unit.is_in_combat:
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (screen_pos[0] + radius - 5, screen_pos[1] - radius + 5),
                5
            )

        # Unit name (small text below)
        name_text = self.font_tiny.render(warscroll.unit_name[:15], True, COLOR_TEXT)
        name_rect = name_text.get_rect(center=(screen_pos[0], screen_pos[1] + radius + 15))
        self.screen.blit(name_text, name_rect)

    def draw_all_units(self):
        """Draw all units on the battlefield"""
        for unit in game_db.battlefield_units:
            self.draw_unit(unit)

    def draw_range_indicator(self, unit: BattlefieldUnit, range_inches: float, color: Tuple):
        """Draw a range circle around a unit"""
        screen_pos = self.world_to_screen(unit.x_position, unit.y_position)
        radius = int(range_inches * SCALE)

        # Create surface with alpha
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (radius, radius), radius)

        self.screen.blit(
            surface,
            (screen_pos[0] - radius, screen_pos[1] - radius)
        )

    def draw_info_panel(self):
        """Draw the information panel on the right"""
        # Panel background
        pygame.draw.rect(self.screen, COLOR_PANEL, self.info_panel_rect)
        pygame.draw.rect(self.screen, COLOR_HIGHLIGHT, self.info_panel_rect, 2)

        y_offset = self.info_panel_rect.y + 20
        x = self.info_panel_rect.x + 20

        # Title
        title = self.font_large.render("Game Info", True, COLOR_HIGHLIGHT)
        self.screen.blit(title, (x, y_offset))
        y_offset += 60

        # Current round
        round_text = self.font_medium.render(
            f"Round: {game_db.current_game.current_round}/5",
            True,
            COLOR_TEXT
        )
        self.screen.blit(round_text, (x, y_offset))
        y_offset += 40

        # Current phase
        phase_text = self.font_medium.render(
            f"Phase: {game_db.current_game.current_phase.value}",
            True,
            COLOR_TEXT
        )
        self.screen.blit(phase_text, (x, y_offset))
        y_offset += 40

        # Active player
        player_text = self.font_medium.render(
            f"Active: Player {game_db.current_game.active_player}",
            True,
            COLOR_PLAYER1 if game_db.current_game.active_player == 1 else COLOR_PLAYER2
        )
        self.screen.blit(player_text, (x, y_offset))
        y_offset += 60

        # Victory points
        vp_title = self.font_medium.render("Victory Points:", True, COLOR_HIGHLIGHT)
        self.screen.blit(vp_title, (x, y_offset))
        y_offset += 35

        p1_vp = self.font_small.render(
            f"Player 1: {game_db.current_game.player1_points}",
            True,
            COLOR_PLAYER1
        )
        self.screen.blit(p1_vp, (x + 20, y_offset))
        y_offset += 30

        p2_vp = self.font_small.render(
            f"Player 2: {game_db.current_game.player2_points}",
            True,
            COLOR_PLAYER2
        )
        self.screen.blit(p2_vp, (x + 20, y_offset))
        y_offset += 50

        # Command points
        cmd_title = self.font_medium.render("Command Points:", True, COLOR_HIGHLIGHT)
        self.screen.blit(cmd_title, (x, y_offset))
        y_offset += 35

        p1_cmd = self.font_small.render(
            f"Player 1: {game_db.current_game.player1_commands}",
            True,
            COLOR_PLAYER1
        )
        self.screen.blit(p1_cmd, (x + 20, y_offset))
        y_offset += 30

        p2_cmd = self.font_small.render(
            f"Player 2: {game_db.current_game.player2_commands}",
            True,
            COLOR_PLAYER2
        )
        self.screen.blit(p2_cmd, (x + 20, y_offset))
        y_offset += 50

        # Selected unit info
        if self.selected_unit:
            self.draw_selected_unit_info(x, y_offset)

    def draw_selected_unit_info(self, x: int, y_offset: int):
        """Draw detailed info for selected unit"""
        warscroll = game_db.get_warscroll(self.selected_unit.warscroll_ref)
        if not warscroll:
            return

        # Separator
        pygame.draw.line(
            self.screen,
            COLOR_HIGHLIGHT,
            (x, y_offset),
            (self.info_panel_rect.right - 20, y_offset),
            2
        )
        y_offset += 20

        # Unit name
        name = self.font_medium.render(warscroll.unit_name[:20], True, COLOR_HIGHLIGHT)
        self.screen.blit(name, (x, y_offset))
        y_offset += 35

        # Stats
        stats = [
            f"Move: {warscroll.base_stats.move}\"",
            f"Health: {warscroll.base_stats.health}",
            f"Save: {warscroll.base_stats.save}+",
            f"Control: {warscroll.base_stats.control}",
            f"Models: {self.selected_unit.model_count}/{warscroll.unit_size}"
        ]

        for stat in stats:
            text = self.font_small.render(stat, True, COLOR_TEXT)
            self.screen.blit(text, (x, y_offset))
            y_offset += 25

        # Status
        y_offset += 10
        status_title = self.font_small.render("Status:", True, COLOR_HIGHLIGHT)
        self.screen.blit(status_title, (x, y_offset))
        y_offset += 25

        statuses = []
        if self.selected_unit.has_moved:
            statuses.append("Moved")
        if self.selected_unit.has_shot:
            statuses.append("Shot")
        if self.selected_unit.has_charged:
            statuses.append("Charged")
        if self.selected_unit.has_fought:
            statuses.append("Fought")
        if self.selected_unit.is_in_combat:
            statuses.append("In Combat")

        if not statuses:
            statuses = ["Ready"]

        for status in statuses:
            text = self.font_tiny.render(f"• {status}", True, COLOR_TEXT)
            self.screen.blit(text, (x + 10, y_offset))
            y_offset += 20

    def get_unit_at_position(self, screen_x: int, screen_y: int) -> Optional[BattlefieldUnit]:
        """Get unit at screen position"""
        world_pos = self.screen_to_world(screen_x, screen_y)

        for unit in game_db.battlefield_units:
            if unit.model_count == 0:
                continue

            dx = unit.x_position - world_pos[0]
            dy = unit.y_position - world_pos[1]
            distance = math.sqrt(dx * dx + dy * dy)

            # Check if within click radius (about 1.5")
            if distance <= 1.5:
                return unit

        return None

    def handle_click(self, screen_x: int, screen_y: int):
        """Handle mouse click"""
        unit = self.get_unit_at_position(screen_x, screen_y)

        if unit:
            self.selected_unit = unit
            print(f"Selected: {game_db.get_warscroll(unit.warscroll_ref).unit_name}")
        else:
            self.selected_unit = None

    def update(self):
        """Update graphics state"""
        self.mouse_pos = pygame.mouse.get_pos()

        # Update hover unit
        if BATTLEFIELD_OFFSET_X <= self.mouse_pos[0] <= BATTLEFIELD_OFFSET_X + BATTLEFIELD_PIXEL_WIDTH:
            if BATTLEFIELD_OFFSET_Y <= self.mouse_pos[1] <= BATTLEFIELD_OFFSET_Y + BATTLEFIELD_PIXEL_HEIGHT:
                self.hover_unit = self.get_unit_at_position(self.mouse_pos[0], self.mouse_pos[1])
            else:
                self.hover_unit = None
        else:
            self.hover_unit = None

    def render(self):
        """Render the complete scene"""
        self.draw_battlefield()
        self.draw_terrain()
        self.draw_objectives()
        self.draw_all_units()

        # Draw range indicators for selected unit
        if self.selected_unit and self.selected_unit.model_count > 0:
            warscroll = game_db.get_warscroll(self.selected_unit.warscroll_ref)
            if warscroll:
                # Movement range
                if not self.selected_unit.has_moved:
                    self.draw_range_indicator(
                        self.selected_unit,
                        warscroll.base_stats.move,
                        COLOR_MOVEMENT_RANGE
                    )

                # Combat range
                if self.selected_unit.is_in_combat:
                    self.draw_range_indicator(
                        self.selected_unit,
                        COMBAT_RANGE,
                        COLOR_COMBAT_RANGE
                    )

        self.draw_info_panel()

        pygame.display.flip()
        self.clock.tick(60)

    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos[0], event.pos[1])

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    # Deselect
                    self.selected_unit = None

        return True

    def quit(self):
        """Clean up and quit pygame"""
        pygame.quit()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_pygame_available() -> bool:
    """Check if pygame is available"""
    return PYGAME_AVAILABLE
