#!/usr/bin/env python3
"""
WARHAMMER AGE OF SIGMAR - GAME MANAGEMENT SYSTEM
Main program and menu interface

Based on Cambridge International AS & A Level Computer Science 9618
Warhammer Age of Sigmar 4th Edition Core Rules
"""

import sys
from data_types import *
from game_state import game_db, initialize_game_database
from file_operations import (load_warscroll_database, save_game_state,
                              load_game_state)
from army_builder import create_army_roster, display_army_roster
from battle import play_battle
from utilities import print_header, print_box, get_integer_input, get_yes_no_input

# Try to import graphics module
try:
    from graphical_game import (play_graphical_battle_interactive,
                                view_battlefield_graphically,
                                GRAPHICS_AVAILABLE)
except ImportError:
    GRAPHICS_AVAILABLE = False


# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """Display and handle main menu"""
    print_header("WARHAMMER AGE OF SIGMAR SIMULATOR", 60)
    print()

    while True:
        print("\n" + "=" * 60)
        print("MAIN MENU".center(60))
        print("=" * 60)
        print()
        print("ARMY BUILDING:")
        print("  1. Create Army Roster (Player 1)")
        print("  2. Create Army Roster (Player 2)")
        print("  3. View Army Rosters")
        print()
        print("BATTLE:")
        print("  4. Play Battle (Text Mode)")
        if GRAPHICS_AVAILABLE:
            print("  5. Play Battle (Graphics Mode) 🎨")
            print("  6. View Battlefield (Graphics) 🖼️")
        print()
        print("OTHER:")
        print("  7. View Warscrolls")
        print("  8. Test Combat Sequence")
        print("  9. Save Game")
        print("  10. Load Game")
        print("  11. Exit")
        print()

        if GRAPHICS_AVAILABLE:
            print("  ✓ Graphics mode available")
        else:
            print("  ⚠ Graphics mode unavailable (install pygame)")

        print()
        choice = get_integer_input("Select option: ", 1, 11)

        if choice == 1:
            create_player_army(1)
        elif choice == 2:
            create_player_army(2)
        elif choice == 3:
            view_army_rosters()
        elif choice == 4:
            start_battle()
        elif choice == 5:
            if GRAPHICS_AVAILABLE:
                start_graphical_battle()
            else:
                print("\n❌ Graphics mode not available. Install pygame first.")
        elif choice == 6:
            if GRAPHICS_AVAILABLE:
                view_battlefield_graphically()
            else:
                print("\n❌ Graphics mode not available. Install pygame first.")
        elif choice == 7:
            browse_warscrolls()
        elif choice == 8:
            test_combat_sequence()
        elif choice == 9:
            save_game_state()
        elif choice == 10:
            load_game_menu()
        elif choice == 11:
            print("\nThanks for playing!")
            sys.exit(0)


# ============================================================================
# ARMY CREATION
# ============================================================================

def create_player_army(player: int):
    """Create army for a player"""
    print_header(f"PLAYER {player} ARMY CREATION")

    points_limit = get_integer_input(
        "Enter points limit (default 2000): ", 500, 5000)

    if points_limit == 0:
        points_limit = 2000

    if player == 1:
        create_army_roster(game_db.player1_army, points_limit)
    else:
        create_army_roster(game_db.player2_army, points_limit)


def view_army_rosters():
    """View both army rosters"""
    print_header("ARMY ROSTERS")

    print("\n=== PLAYER 1 ARMY ===")
    if game_db.player1_army.regiment_count > 0:
        display_army_roster(game_db.player1_army)
    else:
        print("No army created yet")

    print("\n=== PLAYER 2 ARMY ===")
    if game_db.player2_army.regiment_count > 0:
        display_army_roster(game_db.player2_army)
    else:
        print("No army created yet")


# ============================================================================
# BATTLE
# ============================================================================

def start_battle():
    """Start a battle"""
    print_header("START BATTLE")

    # Check if both armies are created
    if game_db.player1_army.regiment_count == 0:
        print("\nPlayer 1 has not created an army yet!")
        if get_yes_no_input("Create Player 1 army now?"):
            create_player_army(1)
        else:
            return

    if game_db.player2_army.regiment_count == 0:
        print("\nPlayer 2 has not created an army yet!")
        if get_yes_no_input("Create Player 2 army now?"):
            create_player_army(2)
        else:
            return

    # Reset game state
    game_db.reset_game()

    # Start battle
    play_battle()


def start_graphical_battle():
    """Start a battle in graphics mode"""
    print_header("START GRAPHICAL BATTLE")

    # Check if both armies are created
    if game_db.player1_army.regiment_count == 0:
        print("\nPlayer 1 has not created an army yet!")
        if get_yes_no_input("Create Player 1 army now?"):
            create_player_army(1)
        else:
            return

    if game_db.player2_army.regiment_count == 0:
        print("\nPlayer 2 has not created an army yet!")
        if get_yes_no_input("Create Player 2 army now?"):
            create_player_army(2)
        else:
            return

    # Reset game state
    game_db.reset_game()

    # Start graphical battle
    if GRAPHICS_AVAILABLE:
        play_graphical_battle_interactive()
    else:
        print("\n❌ Graphics mode not available!")
        print("Falling back to text mode...")
        play_battle()


# ============================================================================
# WARSCROLL BROWSER
# ============================================================================

def browse_warscrolls():
    """Browse available warscrolls"""
    print_header("WARSCROLL BROWSER")

    if game_db.warscroll_count == 0:
        print("\nNo warscrolls loaded!")
        return

    while True:
        print("\n1. List all warscrolls")
        print("2. Search by name")
        print("3. Filter by faction")
        print("4. View warscroll details")
        print("5. Back to main menu")

        choice = get_integer_input("Select option: ", 1, 5)

        if choice == 1:
            list_all_warscrolls()
        elif choice == 2:
            search_warscrolls()
        elif choice == 3:
            filter_by_faction()
        elif choice == 4:
            view_warscroll_details()
        elif choice == 5:
            break


def list_all_warscrolls():
    """List all available warscrolls"""
    print("\n=== ALL WARSCROLLS ===")

    for i, warscroll in enumerate(game_db.all_warscrolls, 1):
        from utilities import faction_to_string
        print(f"{i}. {warscroll.unit_name:<30} "
              f"{faction_to_string(warscroll.faction):<25} "
              f"{warscroll.points_cost} pts")


def search_warscrolls():
    """Search for warscrolls by name"""
    search_term = input("\nEnter unit name to search: ").strip().lower()

    results = [ws for ws in game_db.all_warscrolls
               if search_term in ws.unit_name.lower()]

    if results:
        print(f"\nFound {len(results)} results:")
        for ws in results:
            from utilities import faction_to_string
            print(f"  {ws.unit_name} - {faction_to_string(ws.faction)} "
                  f"({ws.points_cost} pts)")
    else:
        print("\nNo results found")


def filter_by_faction():
    """Filter warscrolls by faction"""
    from utilities import faction_to_string

    print("\nSelect faction:")
    factions = list(FactionType)
    for i, faction in enumerate(factions, 1):
        print(f"{i}. {faction_to_string(faction)}")

    choice = get_integer_input(f"Select faction (1-{len(factions)}): ",
                                1, len(factions))

    selected_faction = factions[choice - 1]

    warscrolls = game_db.get_warscrolls_by_faction(selected_faction)

    if warscrolls:
        print(f"\n{faction_to_string(selected_faction)} warscrolls:")
        for ws in warscrolls:
            print(f"  {ws.unit_name} - {ws.points_cost} pts")
    else:
        print(f"\nNo warscrolls found for {faction_to_string(selected_faction)}")


def view_warscroll_details():
    """View detailed warscroll information"""
    unit_name = input("\nEnter unit name: ").strip()

    warscroll = game_db.find_warscroll_by_name(unit_name)

    if warscroll:
        display_warscroll(warscroll)
    else:
        print(f"\nWarscroll not found: {unit_name}")


def display_warscroll(warscroll: UnitWarscroll):
    """Display detailed warscroll information"""
    from utilities import faction_to_string

    print("\n" + "=" * 60)
    print(warscroll.unit_name.center(60))
    print("=" * 60)

    print(f"\nFaction: {faction_to_string(warscroll.faction)}")
    print(f"Unit Size: {warscroll.unit_size}")
    print(f"Points Cost: {warscroll.points_cost}")

    print("\nSTATISTICS:")
    print(f"  Move: {warscroll.base_stats.move}\"")
    print(f"  Health: {warscroll.base_stats.health}")
    print(f"  Control: {warscroll.base_stats.control}")
    print(f"  Save: {warscroll.base_stats.save}+")

    if warscroll.has_ward:
        print(f"  Ward: {warscroll.ward_value}+")

    print("\nKEYWORDS:")
    print(f"  {', '.join(warscroll.keywords)}")

    if warscroll.weapon_count > 0:
        print("\nWEAPONS:")
        for weapon in warscroll.weapons:
            weapon_type = "Melee" if weapon.weapon_type == WeaponType.MELEE else "Ranged"
            print(f"\n  {weapon.weapon_name} ({weapon_type}):")
            print(f"    Attacks: {weapon.attacks}  Hit: {weapon.hit}+  "
                  f"Wound: {weapon.wound}+")
            print(f"    Rend: {weapon.rend}  Damage: {weapon.damage}  "
                  f"Range: {weapon.range}\"")

    if warscroll.ability_count > 0:
        print("\nABILITIES:")
        for ability in warscroll.abilities:
            print(f"  - {ability}")

    print("=" * 60)


# ============================================================================
# TESTING
# ============================================================================

def test_combat_sequence():
    """Test combat mechanics"""
    print_header("COMBAT SEQUENCE TEST")

    print("\nThis feature would allow testing of:")
    print("- Attack rolls (hit, wound, save)")
    print("- Damage allocation")
    print("- Ward saves")
    print("- Model removal")
    print("\nNot yet fully implemented")


# ============================================================================
# SAVE/LOAD
# ============================================================================

def load_game_menu():
    """Load game menu"""
    filename = input("\nEnter save file name: ").strip()

    if not filename.endswith('.sav'):
        filename += '.sav'

    if load_game_state(filename):
        print("Game loaded successfully!")
    else:
        print("Failed to load game")


# ============================================================================
# INITIALIZATION
# ============================================================================

def initialize_game():
    """Initialize the game system"""
    print_box("INITIALIZING GAME SYSTEM")

    # Initialize game database
    initialize_game_database()

    # Load warscrolls
    load_warscroll_database()

    print(f"\n✓ Loaded {game_db.warscroll_count} warscrolls")
    print(f"✓ Loaded {game_db.ability_count} abilities")
    print("\nGame system ready!")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    try:
        # Initialize
        initialize_game()

        # Run main menu
        main_menu()

    except KeyboardInterrupt:
        print("\n\nGame interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
