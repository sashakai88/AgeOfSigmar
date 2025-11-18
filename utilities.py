"""
WARHAMMER AGE OF SIGMAR - UTILITY FUNCTIONS
Distance calculations, dice rolling, and helper functions
"""

import random
import math
from data_types import FactionType, GamePhase


# ============================================================================
# DICE ROLLING FUNCTIONS
# ============================================================================

def roll_d6() -> int:
    """Roll a single D6"""
    return random.randint(1, 6)


def roll_d3() -> int:
    """Roll a D3 (D6 / 2 rounded up)"""
    roll = roll_d6()
    return (roll + 1) // 2


def roll_2d6() -> int:
    """Roll 2D6"""
    return roll_d6() + roll_d6()


def roll_off() -> int:
    """
    Perform a roll-off between two players.
    Returns 1 if player 1 wins, 2 if player 2 wins.
    """
    roll1 = roll_d6()
    roll2 = roll_d6()

    print(f"Roll-off: Player 1 rolls {roll1}, Player 2 rolls {roll2}")

    while roll1 == roll2:
        print("Tie! Rolling again...")
        roll1 = roll_d6()
        roll2 = roll_d6()
        print(f"Player 1 rolls {roll1}, Player 2 rolls {roll2}")

    if roll1 > roll2:
        return 1
    else:
        return 2


# ============================================================================
# DISTANCE CALCULATIONS
# ============================================================================

def calculate_distance_2d(x1: int, y1: int, x2: int, y2: int) -> float:
    """Calculate Euclidean distance between two points"""
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def calculate_distance(unit1, unit2) -> float:
    """Calculate distance between two battlefield units"""
    return calculate_distance_2d(
        unit1.x_position, unit1.y_position,
        unit2.x_position, unit2.y_position
    )


def calculate_distance_to_objective(unit, objective) -> float:
    """Calculate distance from unit to objective marker"""
    return calculate_distance_2d(
        unit.x_position, unit.y_position,
        objective.x_position, objective.y_position
    )


# ============================================================================
# CONVERSION FUNCTIONS
# ============================================================================

def faction_to_string(faction: FactionType) -> str:
    """Convert faction enum to display string"""
    faction_names = {
        FactionType.STORMCAST_ETERNALS: "Stormcast Eternals",
        FactionType.SKAVEN: "Skaven",
        FactionType.NIGHTHAUNT: "Nighthaunt",
        FactionType.OSSIARCH_BONEREAPERS: "Ossiarch Bonereapers",
        FactionType.SONS_OF_BEHEMAT: "Sons of Behemat",
        FactionType.CITIES_OF_SIGMAR: "Cities of Sigmar",
        FactionType.LUMINETH_REALMLORDS: "Lumineth Realm-lords",
        FactionType.OTHER: "Other"
    }
    return faction_names.get(faction, "Unknown")


def phase_to_string(phase: GamePhase) -> str:
    """Convert phase enum to display string"""
    phase_names = {
        GamePhase.DEPLOYMENT: "Deployment",
        GamePhase.HERO: "Hero",
        GamePhase.MOVEMENT: "Movement",
        GamePhase.SHOOTING: "Shooting",
        GamePhase.CHARGE: "Charge",
        GamePhase.COMBAT: "Combat",
        GamePhase.END_OF_TURN: "End of Turn"
    }
    return phase_names.get(phase, "Unknown")


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def is_visible(observer_id: int, target_id: int) -> bool:
    """
    Check if target is visible to observer.
    Simplified version - full implementation would check line of sight,
    terrain, obscuring, etc.
    """
    # TODO: Implement full line of sight rules with terrain
    return True


def is_valid_position(x: int, y: int, battlefield_width: int = 44,
                      battlefield_height: int = 60) -> bool:
    """Check if position is within battlefield bounds"""
    return 0 <= x <= battlefield_width and 0 <= y <= battlefield_height


# ============================================================================
# STRING PARSING
# ============================================================================

def parse_tab_delimited_line(line: str) -> list:
    """Parse a tab-delimited line into fields"""
    return line.strip().split('\t')


def parse_comma_delimited(text: str) -> list:
    """Parse comma-delimited text into list"""
    if not text or text.strip() == "":
        return []
    return [item.strip() for item in text.split(',')]


# ============================================================================
# DISPLAY HELPERS
# ============================================================================

def print_header(text: str, width: int = 50):
    """Print a formatted header"""
    print()
    print("=" * width)
    print(text.center(width))
    print("=" * width)


def print_subheader(text: str):
    """Print a formatted subheader"""
    print()
    print(f"=== {text} ===")


def print_box(text: str, width: int = 44):
    """Print text in a box"""
    print()
    print("╔" + "═" * width + "╗")
    print("║ " + text.ljust(width - 2) + " ║")
    print("╚" + "═" * width + "╝")


def format_stat_line(label: str, value, width: int = 30):
    """Format a stat line for display"""
    return f"{label.ljust(width)}: {value}"


# ============================================================================
# INPUT HELPERS
# ============================================================================

def get_integer_input(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Get validated integer input from user"""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")


def get_yes_no_input(prompt: str) -> bool:
    """Get yes/no input from user"""
    while True:
        response = input(f"{prompt} (Y/N): ").strip().upper()
        if response in ['Y', 'YES']:
            return True
        elif response in ['N', 'NO']:
            return False
        else:
            print("Please enter Y or N")


def get_choice_input(prompt: str, options: list) -> int:
    """
    Display numbered options and get user choice.
    Returns the index (0-based) of the selected option.
    """
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Select option: "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")
