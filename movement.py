"""
WARHAMMER AGE OF SIGMAR - MOVEMENT PHASE
Movement, running, retreating, and charging
"""

from data_types import *
from game_state import game_db, COMBAT_RANGE, BATTLEFIELD_WIDTH, BATTLEFIELD_HEIGHT
from utilities import (roll_d6, roll_2d6, roll_d3, calculate_distance,
                       calculate_distance_2d, print_subheader, get_integer_input,
                       is_valid_position)
from damage import inflict_mortal_damage
from combat import update_combat_status


# ============================================================================
# MOVEMENT PHASE
# ============================================================================

def play_movement_phase(player: int):
    """Execute movement phase"""
    print_subheader("MOVEMENT PHASE")

    while True:
        units = get_units_that_can_move(player)

        if not units:
            print(f"Player {player} has no more units that can move")
            break

        print(f"\nSelect unit to move (0 to end phase):")
        display_moveable_units(units)

        choice = get_integer_input(f"Select unit (0-{len(units)}): ", 0, len(units))

        if choice == 0:
            break

        selected_unit = units[choice - 1]
        select_movement_type(selected_unit)

    # Update combat status after movement
    update_combat_status()


def get_units_that_can_move(player: int) -> List[BattlefieldUnit]:
    """Get units eligible to move"""
    units = []

    for unit in game_db.battlefield_units:
        if (unit.owner_player == player and
                unit.model_count > 0 and
                not unit.has_moved):
            units.append(unit)

    return units


def display_moveable_units(units: List[BattlefieldUnit]):
    """Display units that can move"""
    for i, unit in enumerate(units, 1):
        warscroll = game_db.get_warscroll(unit.warscroll_ref)
        if warscroll:
            status = "IN COMBAT" if unit.is_in_combat else ""
            print(f"{i}. {warscroll.unit_name} at ({unit.x_position}, "
                  f"{unit.y_position}) Move: {warscroll.base_stats.move}\" {status}")


def select_movement_type(unit: BattlefieldUnit):
    """Select type of movement"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    print(f"\nMovement options for {warscroll.unit_name}:")
    print("1. Normal Move")
    print("2. Run")

    if unit.is_in_combat:
        print("3. Retreat")
        max_choice = 3
    else:
        max_choice = 2

    choice = get_integer_input(f"Select movement type (1-{max_choice}): ", 1, max_choice)

    if choice == 1:
        normal_move(unit)
    elif choice == 2:
        run_move(unit)
    elif choice == 3 and unit.is_in_combat:
        retreat_move(unit)


# ============================================================================
# NORMAL MOVE
# ============================================================================

def normal_move(unit: BattlefieldUnit):
    """Execute normal move"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    move_distance = warscroll.base_stats.move

    print(f"\nNormal Move: {move_distance}\" movement")
    print(f"Current position: ({unit.x_position}, {unit.y_position})")

    new_x = get_integer_input(
        f"New X position (0-{BATTLEFIELD_WIDTH}): ", 0, BATTLEFIELD_WIDTH)
    new_y = get_integer_input(
        f"New Y position (0-{BATTLEFIELD_HEIGHT}): ", 0, BATTLEFIELD_HEIGHT)

    # Validate move
    if is_valid_move(unit, new_x, new_y, move_distance):
        unit.x_position = new_x
        unit.y_position = new_y
        unit.has_moved = True

        print("Unit moved successfully")
    else:
        print("Invalid move distance or position")


def is_valid_move(unit: BattlefieldUnit, new_x: int, new_y: int,
                  max_distance: int) -> bool:
    """Check if move is valid"""
    if not is_valid_position(new_x, new_y, BATTLEFIELD_WIDTH, BATTLEFIELD_HEIGHT):
        return False

    distance = calculate_distance_2d(
        unit.x_position, unit.y_position, new_x, new_y)

    return distance <= max_distance


# ============================================================================
# RUN MOVE
# ============================================================================

def run_move(unit: BattlefieldUnit):
    """Execute run move"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    if unit.is_in_combat:
        print("Cannot run while in combat!")
        return

    move_characteristic = warscroll.base_stats.move
    run_roll = roll_d6()
    total_move = move_characteristic + run_roll

    print(f"\nRun Move: {move_characteristic}\" + D6")
    print(f"Run roll: {run_roll}")
    print(f"Total movement: {total_move}\"")
    print(f"Current position: ({unit.x_position}, {unit.y_position})")

    new_x = get_integer_input(
        f"New X position (0-{BATTLEFIELD_WIDTH}): ", 0, BATTLEFIELD_WIDTH)
    new_y = get_integer_input(
        f"New Y position (0-{BATTLEFIELD_HEIGHT}): ", 0, BATTLEFIELD_HEIGHT)

    if is_valid_move(unit, new_x, new_y, total_move):
        unit.x_position = new_x
        unit.y_position = new_y
        unit.has_moved = True

        print("Unit ran successfully")
    else:
        print("Invalid run move")


# ============================================================================
# RETREAT MOVE
# ============================================================================

def retreat_move(unit: BattlefieldUnit):
    """Execute retreat move"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    if not unit.is_in_combat:
        print("Unit is not in combat - cannot retreat")
        return

    # Inflict D3 mortal damage
    mortal_damage = roll_d3()
    print(f"\nRetreating inflicts {mortal_damage} mortal damage")

    inflict_mortal_damage(unit, mortal_damage)

    if unit.model_count == 0:
        print("Unit destroyed during retreat!")
        return

    move_distance = warscroll.base_stats.move

    print(f"Retreat Move: {move_distance}\"")
    print(f"Current position: ({unit.x_position}, {unit.y_position})")

    new_x = get_integer_input(
        f"New X position (0-{BATTLEFIELD_WIDTH}): ", 0, BATTLEFIELD_WIDTH)
    new_y = get_integer_input(
        f"New Y position (0-{BATTLEFIELD_HEIGHT}): ", 0, BATTLEFIELD_HEIGHT)

    if is_valid_retreat(unit, new_x, new_y, move_distance):
        unit.x_position = new_x
        unit.y_position = new_y
        unit.has_moved = True
        unit.is_in_combat = False

        print("Unit retreated successfully")
    else:
        print("Invalid retreat move")


def is_valid_retreat(unit: BattlefieldUnit, new_x: int, new_y: int,
                     max_distance: int) -> bool:
    """Check if retreat move is valid"""
    # Simplified - should ensure unit moves away from enemy
    return is_valid_move(unit, new_x, new_y, max_distance)


# ============================================================================
# CHARGE PHASE
# ============================================================================

def play_charge_phase(player: int):
    """Execute charge phase"""
    print_subheader("CHARGE PHASE")

    while True:
        units = get_units_that_can_charge(player)

        if not units:
            print(f"Player {player} has no more units that can charge")
            break

        print(f"\nSelect unit to charge (0 to end phase):")
        display_chargeable_units(units)

        choice = get_integer_input(f"Select unit (0-{len(units)}): ", 0, len(units))

        if choice == 0:
            break

        selected_unit = units[choice - 1]
        execute_charge(selected_unit)

    # Update combat status after charges
    update_combat_status()


def get_units_that_can_charge(player: int) -> List[BattlefieldUnit]:
    """Get units eligible to charge"""
    units = []

    for unit in game_db.battlefield_units:
        if (unit.owner_player == player and
                unit.model_count > 0 and
                not unit.has_charged and
                not unit.is_in_combat):
            units.append(unit)

    return units


def display_chargeable_units(units: List[BattlefieldUnit]):
    """Display units that can charge"""
    for i, unit in enumerate(units, 1):
        warscroll = game_db.get_warscroll(unit.warscroll_ref)
        if warscroll:
            print(f"{i}. {warscroll.unit_name} at ({unit.x_position}, {unit.y_position})")


def execute_charge(unit: BattlefieldUnit):
    """Execute a charge"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    print(f"\nCharging with: {warscroll.unit_name}")

    # Select target
    targets = get_visible_enemy_units(unit)

    if not targets:
        print("No valid targets to charge!")
        return

    print("\nSelect target unit:")
    for i, target in enumerate(targets, 1):
        target_ws = game_db.get_warscroll(target.warscroll_ref)
        if target_ws:
            distance = calculate_distance(unit, target)
            print(f"{i}. {target_ws.unit_name} (Distance: {distance:.1f}\")")

    target_choice = get_integer_input(
        f"Select target (1-{len(targets)}): ", 1, len(targets))

    target = targets[target_choice - 1]
    initial_distance = calculate_distance(unit, target)

    print(f"Distance to target: {initial_distance:.1f}\"")

    # Make charge roll
    charge_roll = roll_2d6()
    print(f"Charge roll: {charge_roll}")

    game_db.last_charge_roll = charge_roll

    if charge_roll >= int(initial_distance):
        print("Charge successful!")

        new_x = get_integer_input(
            f"New X position (0-{BATTLEFIELD_WIDTH}): ", 0, BATTLEFIELD_WIDTH)
        new_y = get_integer_input(
            f"New Y position (0-{BATTLEFIELD_HEIGHT}): ", 0, BATTLEFIELD_HEIGHT)

        if is_valid_charge_position(unit, target, new_x, new_y, charge_roll):
            unit.x_position = new_x
            unit.y_position = new_y
            unit.has_charged = True
            unit.is_in_combat = True

            print("Charge completed!")
        else:
            print("Invalid charge position")
    else:
        print("Charge failed - insufficient distance")


def is_valid_charge_position(unit: BattlefieldUnit, target: BattlefieldUnit,
                              new_x: int, new_y: int, charge_roll: int) -> bool:
    """Check if charge position is valid"""
    # Must be within charge distance of starting position
    if not is_valid_move(unit, new_x, new_y, charge_roll):
        return False

    # Must end within 3" of target
    final_distance = calculate_distance_2d(
        new_x, new_y, target.x_position, target.y_position)

    return final_distance <= COMBAT_RANGE


def get_visible_enemy_units(unit: BattlefieldUnit) -> List[BattlefieldUnit]:
    """Get visible enemy units"""
    enemies = []

    for other_unit in game_db.battlefield_units:
        if (other_unit.owner_player != unit.owner_player and
                other_unit.model_count > 0):
            # Simplified visibility check
            enemies.append(other_unit)

    return enemies
