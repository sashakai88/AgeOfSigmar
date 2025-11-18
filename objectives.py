"""
WARHAMMER AGE OF SIGMAR - OBJECTIVE CONTROL
Objective control and victory point scoring
"""

from data_types import *
from game_state import game_db, COMBAT_RANGE
from utilities import calculate_distance_to_objective, print_subheader


# ============================================================================
# OBJECTIVE CONTROL
# ============================================================================

def determine_objective_control(active_player: int):
    """Determine control of all objectives"""
    print_subheader("DETERMINING OBJECTIVE CONTROL")

    for objective in game_db.objectives:
        check_objective_control(objective, active_player)


def check_objective_control(objective: ObjectiveMarker, active_player: int):
    """Check control of a single objective"""
    player1_score = 0
    player2_score = 0

    print(f"\nObjective {objective.objective_id + 1}:")

    # Calculate control scores
    for unit in game_db.battlefield_units:
        if unit.model_count > 0:
            distance = calculate_distance_to_objective(unit, objective)

            if distance <= COMBAT_RANGE:
                # Unit is contesting
                control_score = calculate_unit_control_score(unit)

                warscroll = game_db.get_warscroll(unit.warscroll_ref)
                unit_name = warscroll.unit_name if warscroll else "Unknown"

                if unit.owner_player == 1:
                    player1_score += control_score
                    print(f"  Player 1 - {unit_name} contesting "
                          f"(Control: {control_score})")
                else:
                    player2_score += control_score
                    print(f"  Player 2 - {unit_name} contesting "
                          f"(Control: {control_score})")

    print(f"  Control scores - P1: {player1_score}  P2: {player2_score}")

    # Determine control
    if player1_score > player2_score:
        if objective.controlled_by != 1:
            print("  Player 1 gains control!")
            objective.controlled_by = 1
        else:
            print("  Player 1 maintains control")
    elif player2_score > player1_score:
        if objective.controlled_by != 2:
            print("  Player 2 gains control!")
            objective.controlled_by = 2
        else:
            print("  Player 2 maintains control")
    else:
        print("  Contested - no change in control")


def calculate_unit_control_score(unit: BattlefieldUnit) -> int:
    """Calculate the control score of a unit"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return 0

    base_control = warscroll.base_stats.control
    model_count = unit.model_count

    total_control = base_control * model_count

    # Check for standard bearer
    if unit_has_standard_bearer(unit):
        total_control += 1

    return total_control


def unit_has_standard_bearer(unit: BattlefieldUnit) -> bool:
    """Check if unit has a standard bearer"""
    for model in unit.models:
        if model.is_standard_bearer:
            return True
    return False


# ============================================================================
# VICTORY POINT SCORING
# ============================================================================

def score_victory_points(player: int):
    """Score victory points for a player"""
    objectives_controlled = 0

    for objective in game_db.objectives:
        if objective.controlled_by == player:
            objectives_controlled += 1

    # Award points (typically 2 VP per objective)
    points = objectives_controlled * 2

    if player == 1:
        game_db.current_game.player1_points += points
        print(f"\nPlayer 1 scores {points} victory points")
        print(f"Total: {game_db.current_game.player1_points} VP")
    else:
        game_db.current_game.player2_points += points
        print(f"\nPlayer 2 scores {points} victory points")
        print(f"Total: {game_db.current_game.player2_points} VP")


def display_victory_points():
    """Display current victory point totals"""
    print("\n" + "=" * 40)
    print("VICTORY POINTS")
    print("=" * 40)
    print(f"Player 1: {game_db.current_game.player1_points} VP")
    print(f"Player 2: {game_db.current_game.player2_points} VP")
    print("=" * 40)


def display_objective_status():
    """Display status of all objectives"""
    print_subheader("OBJECTIVE STATUS")

    for objective in game_db.objectives:
        controller = "Uncontrolled"
        if objective.controlled_by == 1:
            controller = "Player 1"
        elif objective.controlled_by == 2:
            controller = "Player 2"

        print(f"Objective {objective.objective_id + 1} at "
              f"({objective.x_position}, {objective.y_position}): {controller}")


# ============================================================================
# VICTORY CONDITIONS
# ============================================================================

def check_victory_conditions() -> bool:
    """
    Check if victory conditions are met.
    Returns True if game should end.
    """
    # Check if one player has no units left
    player1_units = sum(
        1 for unit in game_db.battlefield_units
        if unit.owner_player == 1 and unit.model_count > 0
    )

    player2_units = sum(
        1 for unit in game_db.battlefield_units
        if unit.owner_player == 2 and unit.model_count > 0
    )

    if player1_units == 0:
        print("\nPlayer 1 has no units remaining!")
        return True

    if player2_units == 0:
        print("\nPlayer 2 has no units remaining!")
        return True

    # Could add other victory conditions here
    return False


def determine_winner():
    """Determine and announce the winner"""
    print("\n" + "=" * 50)
    print("BATTLE CONCLUDED")
    print("=" * 50)

    display_victory_points()

    print()
    if game_db.current_game.player1_points > game_db.current_game.player2_points:
        print("🏆 PLAYER 1 WINS! 🏆")
        margin = game_db.current_game.player1_points - game_db.current_game.player2_points
        print(f"Victory by {margin} points")
    elif game_db.current_game.player2_points > game_db.current_game.player1_points:
        print("🏆 PLAYER 2 WINS! 🏆")
        margin = game_db.current_game.player2_points - game_db.current_game.player1_points
        print(f"Victory by {margin} points")
    else:
        print("⚔️ DRAW ⚔️")
        print("Both players have equal victory points")

    print("=" * 50)
