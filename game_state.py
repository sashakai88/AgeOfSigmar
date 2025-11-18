"""
WARHAMMER AGE OF SIGMAR - GAME STATE
Global game data structures and state management
"""

from data_types import *
from typing import List


# ============================================================================
# CONSTANTS
# ============================================================================

MAX_UNITS = 100
MAX_WARSCROLLS = 500
MAX_OBJECTIVES = 6
MAX_TERRAIN = 20
MAX_ABILITIES = 200
MAX_ROUNDS = 5
BATTLEFIELD_WIDTH = 44
BATTLEFIELD_HEIGHT = 60
COMBAT_RANGE = 3


# ============================================================================
# GLOBAL GAME STATE
# ============================================================================

class GameDatabase:
    """Central database for all game data"""

    def __init__(self):
        # Warscroll database
        self.all_warscrolls: List[UnitWarscroll] = []
        self.warscroll_count: int = 0

        # Battlefield units
        self.battlefield_units: List[BattlefieldUnit] = []
        self.unit_count: int = 0

        # Abilities database
        self.all_abilities: List[AbilityRecord] = []
        self.ability_count: int = 0

        # Game state
        self.current_game: GameState = GameState()

        # Player armies
        self.player1_army: ArmyRoster = ArmyRoster()
        self.player2_army: ArmyRoster = ArmyRoster()

        # Battlefield elements
        self.objectives: List[ObjectiveMarker] = []
        self.objective_count: int = 0

        self.terrain_features: List[TerrainFeature] = []
        self.terrain_count: int = 0

        # Combat tracking
        self.attack_sequence: List[AttackRoll] = []
        self.attack_sequence_count: int = 0

        # Last dice rolls (for transparency)
        self.last_dice_roll: int = 0
        self.last_charge_roll: int = 0

    def reset_game(self):
        """Reset game state for a new battle"""
        self.battlefield_units = []
        self.unit_count = 0
        self.objectives = []
        self.objective_count = 0
        self.terrain_features = []
        self.terrain_count = 0
        self.attack_sequence = []
        self.attack_sequence_count = 0
        self.current_game = GameState()

    def add_warscroll(self, warscroll: UnitWarscroll) -> int:
        """Add a warscroll to the database and return its index"""
        warscroll.unit_id = self.warscroll_count
        self.all_warscrolls.append(warscroll)
        self.warscroll_count += 1
        return self.warscroll_count - 1

    def add_ability(self, ability: AbilityRecord) -> int:
        """Add an ability to the database and return its index"""
        self.all_abilities.append(ability)
        self.ability_count += 1
        return self.ability_count - 1

    def add_battlefield_unit(self, unit: BattlefieldUnit) -> int:
        """Add a unit to the battlefield and return its index"""
        unit.unit_id = self.unit_count
        self.battlefield_units.append(unit)
        self.unit_count += 1
        return self.unit_count - 1

    def get_warscroll(self, warscroll_id: int) -> Optional[UnitWarscroll]:
        """Get warscroll by ID"""
        if 0 <= warscroll_id < len(self.all_warscrolls):
            return self.all_warscrolls[warscroll_id]
        return None

    def get_battlefield_unit(self, unit_id: int) -> Optional[BattlefieldUnit]:
        """Get battlefield unit by ID"""
        if 0 <= unit_id < len(self.battlefield_units):
            return self.battlefield_units[unit_id]
        return None

    def get_units_by_player(self, player: int) -> List[BattlefieldUnit]:
        """Get all units owned by a player"""
        return [unit for unit in self.battlefield_units if unit.owner_player == player]

    def get_active_units_by_player(self, player: int) -> List[BattlefieldUnit]:
        """Get all active (not destroyed) units owned by a player"""
        return [unit for unit in self.battlefield_units
                if unit.owner_player == player and unit.model_count > 0]

    def find_warscroll_by_name(self, name: str) -> Optional[UnitWarscroll]:
        """Find warscroll by unit name"""
        for warscroll in self.all_warscrolls:
            if warscroll.unit_name.lower() == name.lower():
                return warscroll
        return None

    def get_warscrolls_by_faction(self, faction: FactionType) -> List[UnitWarscroll]:
        """Get all warscrolls for a specific faction"""
        return [ws for ws in self.all_warscrolls if ws.faction == faction]

    def get_hero_warscrolls(self, faction: FactionType) -> List[UnitWarscroll]:
        """Get hero warscrolls for a faction"""
        heroes = []
        for ws in self.all_warscrolls:
            if ws.faction == faction:
                # Check if unit has HERO keyword
                if "HERO" in [kw.upper() for kw in ws.keywords]:
                    heroes.append(ws)
        return heroes

    def get_non_hero_warscrolls(self, faction: FactionType) -> List[UnitWarscroll]:
        """Get non-hero warscrolls for a faction"""
        units = []
        for ws in self.all_warscrolls:
            if ws.faction == faction:
                # Check if unit does NOT have HERO keyword
                if "HERO" not in [kw.upper() for kw in ws.keywords]:
                    units.append(ws)
        return units


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Global game database instance
game_db = GameDatabase()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def initialize_game_database():
    """Initialize the game database with core abilities"""
    from file_operations import load_universal_abilities

    print("Initializing game database...")
    load_universal_abilities()
    print(f"Loaded {game_db.ability_count} core abilities")


def get_player_army(player: int) -> ArmyRoster:
    """Get army roster for a player"""
    if player == 1:
        return game_db.player1_army
    else:
        return game_db.player2_army


def get_player_commands(player: int) -> int:
    """Get command points for a player"""
    if player == 1:
        return game_db.current_game.player1_commands
    else:
        return game_db.current_game.player2_commands


def set_player_commands(player: int, commands: int):
    """Set command points for a player"""
    if player == 1:
        game_db.current_game.player1_commands = commands
    else:
        game_db.current_game.player2_commands = commands


def use_command_point(player: int) -> bool:
    """Use a command point. Returns True if successful."""
    commands = get_player_commands(player)
    if commands > 0:
        set_player_commands(player, commands - 1)
        return True
    return False
