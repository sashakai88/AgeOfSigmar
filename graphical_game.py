"""
WARHAMMER AGE OF SIGMAR - GRAPHICAL GAME MODE
Interactive 2D graphical game interface
"""

try:
    import pygame
    from graphics_engine import GraphicsEngine, is_pygame_available
    GRAPHICS_AVAILABLE = True
except ImportError:
    GRAPHICS_AVAILABLE = False
    # Create a dummy type for type hints when pygame is not available
    class GraphicsEngine:
        pass

from data_types import *
from game_state import game_db
from utilities import print_header, get_yes_no_input
from battle import (start_of_battle_round, end_of_battle_round,
                    reset_unit_actions, play_hero_phase, play_end_of_turn)
from movement import (play_movement_phase, play_charge_phase)
from shooting import play_shooting_phase
from combat import play_combat_phase, update_combat_status
from objectives import check_victory_conditions, determine_winner
from battlefield import setup_battlefield


# ============================================================================
# GRAPHICAL BATTLE MODE
# ============================================================================

def play_graphical_battle():
    """Play battle in graphical mode"""
    if not GRAPHICS_AVAILABLE:
        print("\n❌ Graphics mode not available!")
        print("Install pygame with: pip install pygame")
        return

    print_header("GRAPHICAL BATTLE MODE")
    print("\nStarting graphical battle...")
    print("\nControls:")
    print("  • Click units to select them")
    print("  • ESC or close window to exit")
    print("  • SPACE to deselect")
    print()
    input("Press Enter to start...")

    # Initialize graphics engine
    engine = GraphicsEngine()

    # Setup battlefield (this should already be done, but ensure it)
    if game_db.objective_count == 0:
        print("Setting up battlefield...")
        setup_battlefield()

    # Reset game state
    game_db.current_game.current_round = 0
    game_db.current_game.player1_points = 0
    game_db.current_game.player2_points = 0
    game_db.current_game.is_first_round = True

    print("Graphics initialized. Starting battle...")

    # Main game loop
    try:
        running = True
        game_active = True

        while running and game_active:
            # Handle events
            running = engine.handle_events()

            # Update
            engine.update()

            # Render
            engine.render()

            # Check for end of game
            if game_db.current_game.current_round >= 5:
                game_active = False

            # Allow some interaction
            pygame.time.wait(16)  # ~60 FPS

    except KeyboardInterrupt:
        print("\nBattle interrupted!")
    finally:
        engine.quit()

    # Show final results
    determine_winner()


def play_graphical_battle_interactive():
    """
    Play battle in graphical mode with interactive turn-by-turn controls.
    Graphics display with text-based phase controls.
    """
    if not GRAPHICS_AVAILABLE:
        print("\n❌ Graphics mode not available!")
        print("Install pygame with: pip install pygame")
        return

    print_header("INTERACTIVE GRAPHICAL BATTLE")
    print("\nThis mode combines:")
    print("  • Visual battlefield display")
    print("  • Interactive unit selection")
    print("  • Text-based phase controls")
    print()

    # Initialize graphics engine
    engine = GraphicsEngine()

    # Setup battlefield
    if game_db.objective_count == 0:
        print("Setting up battlefield...")
        setup_battlefield()

    # Reset game state
    game_db.current_game.current_round = 0
    game_db.current_game.player1_points = 0
    game_db.current_game.player2_points = 0
    game_db.current_game.is_first_round = True

    try:
        # Main battle loop
        continue_battle = True

        while continue_battle and game_db.current_game.current_round < 5:
            game_db.current_game.current_round += 1

            # Start of round
            print_header(f"BATTLE ROUND {game_db.current_game.current_round}")
            start_of_battle_round()

            # Update graphics
            for _ in range(30):  # Show for about 0.5 seconds
                if not engine.handle_events():
                    continue_battle = False
                    break
                engine.update()
                engine.render()

            if not continue_battle:
                break

            # Player turns
            for player in [game_db.current_game.active_player,
                          2 if game_db.current_game.active_player == 1 else 1]:

                print(f"\n{'='*60}")
                print(f"PLAYER {player} TURN".center(60))
                print('='*60)

                reset_unit_actions(player)

                # Show graphics during turn
                if not run_graphical_turn(engine, player):
                    continue_battle = False
                    break

            # End of round
            end_of_battle_round()
            update_combat_status()

            # Update graphics
            for _ in range(60):  # Show for about 1 second
                if not engine.handle_events():
                    continue_battle = False
                    break
                engine.update()
                engine.render()

            # Check victory
            if check_victory_conditions():
                break

            # Ask to continue
            if game_db.current_game.current_round < 5:
                if not get_yes_no_input("\nContinue to next round?"):
                    break

        # Keep window open for final results
        print("\n" + "="*60)
        print("Battle Complete! Window will stay open.")
        print("Close window or press ESC to exit.")
        print("="*60)

        while True:
            if not engine.handle_events():
                break
            engine.update()
            engine.render()

    except KeyboardInterrupt:
        print("\nBattle interrupted!")
    finally:
        engine.quit()

    determine_winner()


def run_graphical_turn(engine: GraphicsEngine, player: int) -> bool:
    """
    Run a player's turn with graphical display.
    Returns False if should quit.
    """
    phases = [
        ("Hero Phase", lambda: play_hero_phase_graphical(engine, player)),
        ("Movement Phase", lambda: play_movement_phase_graphical(engine, player)),
        ("Shooting Phase", lambda: play_shooting_phase_graphical(engine, player)),
        ("Charge Phase", lambda: play_charge_phase_graphical(engine, player)),
        ("Combat Phase", lambda: play_combat_phase_graphical(engine, player)),
        ("End of Turn", lambda: play_end_of_turn_graphical(engine, player))
    ]

    for phase_name, phase_func in phases:
        print(f"\n=== {phase_name} ===")

        # Update graphics during phase
        for _ in range(20):
            if not engine.handle_events():
                return False
            engine.update()
            engine.render()

        # Execute phase
        if not phase_func():
            return False

        # Update graphics after phase
        for _ in range(20):
            if not engine.handle_events():
                return False
            engine.update()
            engine.render()

    return True


# ============================================================================
# GRAPHICAL PHASE IMPLEMENTATIONS
# ============================================================================

def play_hero_phase_graphical(engine: GraphicsEngine, player: int) -> bool:
    """Hero phase with graphics"""
    game_db.current_game.current_phase = GamePhase.HERO

    # Update graphics while showing phase
    for _ in range(30):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    print("Hero phase (simplified)")
    return True


def play_movement_phase_graphical(engine: GraphicsEngine, player: int) -> bool:
    """Movement phase with graphics"""
    from movement import play_movement_phase

    game_db.current_game.current_phase = GamePhase.MOVEMENT

    # Show graphics
    for _ in range(30):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    play_movement_phase(player)

    # Update graphics after movement
    for _ in range(30):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    return True


def play_shooting_phase_graphical(engine: GraphicsEngine, player: int) -> bool:
    """Shooting phase with graphics"""
    from shooting import play_shooting_phase

    game_db.current_game.current_phase = GamePhase.SHOOTING

    for _ in range(30):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    play_shooting_phase(player)

    for _ in range(30):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    return True


def play_charge_phase_graphical(engine: GraphicsEngine, player: int) -> bool:
    """Charge phase with graphics"""
    from movement import play_charge_phase

    game_db.current_game.current_phase = GamePhase.CHARGE

    for _ in range(30):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    play_charge_phase(player)

    for _ in range(30):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    return True


def play_combat_phase_graphical(engine: GraphicsEngine, player: int) -> bool:
    """Combat phase with graphics"""
    from combat import play_combat_phase

    game_db.current_game.current_phase = GamePhase.COMBAT

    for _ in range(30):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    play_combat_phase(player)

    # Show combat results
    for _ in range(60):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    return True


def play_end_of_turn_graphical(engine: GraphicsEngine, player: int) -> bool:
    """End of turn with graphics"""
    game_db.current_game.current_phase = GamePhase.END_OF_TURN

    play_end_of_turn(player)

    # Show updated scores
    for _ in range(60):
        if not engine.handle_events():
            return False
        engine.update()
        engine.render()

    return True


# ============================================================================
# BATTLEFIELD VIEWER
# ============================================================================

def view_battlefield_graphically():
    """View the current battlefield state in graphics mode"""
    if not GRAPHICS_AVAILABLE:
        print("\n❌ Graphics mode not available!")
        return

    print("Opening battlefield viewer...")
    print("Controls:")
    print("  • Click units to see their stats")
    print("  • ESC to exit")

    engine = GraphicsEngine()

    try:
        running = True
        while running:
            running = engine.handle_events()
            engine.update()
            engine.render()
    except KeyboardInterrupt:
        pass
    finally:
        engine.quit()
