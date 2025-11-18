"""
WARHAMMER AGE OF SIGMAR - BATTLE MANAGEMENT
Battle rounds, turns, and phase management
"""

from data_types import *
from game_state import game_db, MAX_ROUNDS
from utilities import roll_off, print_header, print_subheader, get_yes_no_input
from movement import play_movement_phase, play_charge_phase
from shooting import play_shooting_phase
from combat import play_combat_phase, update_combat_status
from objectives import (determine_objective_control, score_victory_points,
                        display_victory_points, check_victory_conditions,
                        determine_winner)
from battlefield import setup_battlefield


# ============================================================================
# MAIN BATTLE
# ============================================================================

def play_battle():
    """Main battle procedure"""
    print_header("WARHAMMER AGE OF SIGMAR BATTLE")

    game_db.current_game.current_round = 0
    game_db.current_game.player1_points = 0
    game_db.current_game.player2_points = 0
    game_db.current_game.is_first_round = True
    continue_battle = True

    # Setup battlefield
    setup_battlefield()

    # Battle rounds
    while game_db.current_game.current_round < MAX_ROUNDS and continue_battle:
        game_db.current_game.current_round += 1
        play_battle_round()

        # Check victory conditions
        if check_victory_conditions():
            continue_battle = False

        # Ask if players want to continue
        if continue_battle and game_db.current_game.current_round < MAX_ROUNDS:
            if not get_yes_no_input("\nContinue to next round?"):
                continue_battle = False

    # Determine winner
    determine_winner()


def play_battle_round():
    """Play a single battle round"""
    print()
    print("=" * 60)
    print(f"BATTLE ROUND {game_db.current_game.current_round}".center(60))
    print("=" * 60)
    print()

    # Start of battle round
    start_of_battle_round()

    # Determine turn order
    first_player = game_db.current_game.active_player

    # Player turns
    play_player_turn(first_player)

    second_player = 2 if first_player == 1 else 1
    play_player_turn(second_player)

    # End of battle round
    end_of_battle_round()

    # Mark first round as complete
    game_db.current_game.is_first_round = False


# ============================================================================
# START OF BATTLE ROUND
# ============================================================================

def start_of_battle_round():
    """Start of battle round procedures"""
    print_subheader("START OF BATTLE ROUND")

    # Determine priority
    if game_db.current_game.is_first_round:
        print("First round - Player 1 goes first")
        game_db.current_game.active_player = 1
    else:
        print("Rolling for priority...")
        priority_roll = roll_off()

        if priority_roll == 1:
            print("Player 1 wins priority roll")
            game_db.current_game.active_player = 1
        else:
            print("Player 2 wins priority roll")
            game_db.current_game.active_player = 2

    # Determine underdog
    if game_db.current_game.player1_points < game_db.current_game.player2_points:
        game_db.current_game.underdog = 1
        print("Player 1 is the underdog")
    elif game_db.current_game.player2_points < game_db.current_game.player1_points:
        game_db.current_game.underdog = 2
        print("Player 2 is the underdog")
    else:
        game_db.current_game.underdog = 0
        print("No underdog this round")

    # Grant command points
    game_db.current_game.player1_commands = 4
    game_db.current_game.player2_commands = 4

    if game_db.current_game.underdog == 1:
        game_db.current_game.player1_commands += 1
    elif game_db.current_game.underdog == 2:
        game_db.current_game.player2_commands += 1

    print(f"Command points - Player 1: {game_db.current_game.player1_commands}")
    print(f"Command points - Player 2: {game_db.current_game.player2_commands}")


# ============================================================================
# PLAYER TURN
# ============================================================================

def play_player_turn(player: int):
    """Play a single player's turn"""
    print()
    print("=" * 60)
    print(f"PLAYER {player} TURN".center(60))
    print("=" * 60)

    # Reset unit actions
    reset_unit_actions(player)

    # Hero Phase
    game_db.current_game.current_phase = GamePhase.HERO
    play_hero_phase(player)

    # Movement Phase
    game_db.current_game.current_phase = GamePhase.MOVEMENT
    play_movement_phase(player)

    # Shooting Phase
    game_db.current_game.current_phase = GamePhase.SHOOTING
    play_shooting_phase(player)

    # Charge Phase
    game_db.current_game.current_phase = GamePhase.CHARGE
    play_charge_phase(player)

    # Combat Phase
    game_db.current_game.current_phase = GamePhase.COMBAT
    play_combat_phase(player)

    # End of Turn
    game_db.current_game.current_phase = GamePhase.END_OF_TURN
    play_end_of_turn(player)


def reset_unit_actions(player: int):
    """Reset all unit actions at start of turn"""
    for unit in game_db.battlefield_units:
        if unit.owner_player == player:
            unit.has_moved = False
            unit.has_shot = False
            unit.has_fought = False
            unit.has_charged = False
            unit.commands_used = 0


def play_hero_phase(player: int):
    """Execute hero phase"""
    print_subheader("HERO PHASE")
    print("Hero phase abilities not yet implemented")
    # TODO: Implement hero abilities, spells, prayers


def play_end_of_turn(player: int):
    """Execute end of turn procedures"""
    print_subheader("END OF TURN")

    # Determine objective control
    determine_objective_control(player)

    # Score victory points
    score_victory_points(player)

    # Display current scores
    display_victory_points()


# ============================================================================
# END OF BATTLE ROUND
# ============================================================================

def end_of_battle_round():
    """End of battle round procedures"""
    print_subheader("END OF BATTLE ROUND")

    # Update combat status
    update_combat_status()

    # Display battlefield status
    display_battlefield_status()


def display_battlefield_status():
    """Display current battlefield status"""
    print("\n--- Battlefield Status ---")

    print("\nPlayer 1 Units:")
    for unit in game_db.battlefield_units:
        if unit.owner_player == 1 and unit.model_count > 0:
            warscroll = game_db.get_warscroll(unit.warscroll_ref)
            if warscroll:
                status = "IN COMBAT" if unit.is_in_combat else ""
                print(f"  {warscroll.unit_name}: {unit.model_count} models "
                      f"at ({unit.x_position}, {unit.y_position}) {status}")

    print("\nPlayer 2 Units:")
    for unit in game_db.battlefield_units:
        if unit.owner_player == 2 and unit.model_count > 0:
            warscroll = game_db.get_warscroll(unit.warscroll_ref)
            if warscroll:
                status = "IN COMBAT" if unit.is_in_combat else ""
                print(f"  {warscroll.unit_name}: {unit.model_count} models "
                      f"at ({unit.x_position}, {unit.y_position}) {status}")
