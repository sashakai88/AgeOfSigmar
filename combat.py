"""
WARHAMMER AGE OF SIGMAR - COMBAT SYSTEM
Combat phase, attack resolution, and damage
"""

from data_types import *
from game_state import game_db, COMBAT_RANGE
from utilities import (roll_d6, calculate_distance, print_subheader,
                       get_integer_input, get_yes_no_input)


# ============================================================================
# COMBAT PHASE
# ============================================================================

def play_combat_phase(player: int):
    """Execute combat phase"""
    print_subheader("COMBAT PHASE")

    # Get units eligible to fight
    eligible_units = get_units_eligible_to_fight(player)

    if not eligible_units:
        print(f"Player {player} has no units eligible to fight")
        return

    current_player = player
    all_fought = False

    while not all_fought:
        # Get eligible units for current player
        if current_player == player:
            units = get_units_eligible_to_fight(player)
        else:
            opponent = 2 if player == 1 else 1
            units = get_units_eligible_to_fight(opponent)

        if not units:
            # Switch to other player
            current_player = 2 if current_player == 1 else 1
            units = get_units_eligible_to_fight(current_player)

            if not units:
                all_fought = True
                break

        # Display eligible units
        print(f"\n--- Player {current_player}'s turn to fight ---")
        display_units_to_fight(units)

        if not units:
            print("No units eligible to fight")
            break

        unit_choice = get_integer_input(
            f"Select unit to fight (1-{len(units)}, 0 to skip): ", 0, len(units))

        if unit_choice == 0:
            current_player = 2 if current_player == 1 else 1
            continue

        selected_unit = units[unit_choice - 1]
        execute_fight(selected_unit)

        # Switch player
        current_player = 2 if current_player == 1 else 1

        # Check if all have fought
        all_fought = have_all_eligible_units_fought()


def get_units_eligible_to_fight(player: int) -> List[BattlefieldUnit]:
    """Get units that can fight"""
    eligible = []

    for unit in game_db.battlefield_units:
        if (unit.owner_player == player and
                unit.model_count > 0 and
                not unit.has_fought and
                unit.is_in_combat):
            eligible.append(unit)

    return eligible


def display_units_to_fight(units: List[BattlefieldUnit]):
    """Display units eligible to fight"""
    print("\nUnits eligible to fight:")
    for i, unit in enumerate(units, 1):
        warscroll = game_db.get_warscroll(unit.warscroll_ref)
        if warscroll:
            print(f"{i}. {warscroll.unit_name} at ({unit.x_position}, {unit.y_position})")


def have_all_eligible_units_fought() -> bool:
    """Check if all eligible units have fought"""
    for unit in game_db.battlefield_units:
        if unit.is_in_combat and not unit.has_fought and unit.model_count > 0:
            return False
    return True


# ============================================================================
# FIGHT SEQUENCE
# ============================================================================

def execute_fight(unit: BattlefieldUnit):
    """Execute fight ability for a unit"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    print(f"\n=== FIGHT ===")
    print(f"Unit: {warscroll.unit_name}")

    # Pile in
    print("\nMake pile-in move (up to 3\")")
    pile_in_move(unit)

    # Select target
    if unit.is_in_combat:
        targets = get_units_in_combat_with(unit)

        if not targets:
            print("No valid targets!")
            unit.has_fought = True
            return

        print("\nSelect target unit:")
        for i, target in enumerate(targets, 1):
            target_ws = game_db.get_warscroll(target.warscroll_ref)
            if target_ws:
                print(f"{i}. {target_ws.unit_name}")

        target_choice = get_integer_input(
            f"Select target (1-{len(targets)}): ", 1, len(targets))

        target = targets[target_choice - 1]

        # Resolve attacks
        resolve_all_combat_attacks(unit, target)

        unit.has_fought = True
    else:
        print("Unit is not in combat")
        unit.has_fought = True


def pile_in_move(unit: BattlefieldUnit):
    """Execute pile-in move"""
    if get_yes_no_input("Make pile-in move?"):
        new_x = get_integer_input("New X position: ")
        new_y = get_integer_input("New Y position: ")

        # Simplified - should validate move is <= 3" and towards enemy
        from utilities import calculate_distance_2d
        distance = calculate_distance_2d(
            unit.x_position, unit.y_position, new_x, new_y)

        if distance <= 3.0:
            unit.x_position = new_x
            unit.y_position = new_y
            print("Pile-in complete")
        else:
            print("Move too far (max 3\")")


def get_units_in_combat_with(unit: BattlefieldUnit) -> List[BattlefieldUnit]:
    """Get enemy units in combat with this unit"""
    targets = []

    for other_unit in game_db.battlefield_units:
        if (other_unit.owner_player != unit.owner_player and
                other_unit.model_count > 0):

            distance = calculate_distance(unit, other_unit)
            if distance <= COMBAT_RANGE:
                targets.append(other_unit)

    return targets


# ============================================================================
# ATTACK RESOLUTION
# ============================================================================

def resolve_all_combat_attacks(attacker: BattlefieldUnit, target: BattlefieldUnit):
    """Resolve all melee attacks from attacker to target"""
    attacker_ws = game_db.get_warscroll(attacker.warscroll_ref)
    target_ws = game_db.get_warscroll(target.warscroll_ref)

    if not attacker_ws or not target_ws:
        return

    print(f"\nResolving combat attacks...")
    print(f"Attacker: {attacker_ws.unit_name}")
    print(f"Target: {target_ws.unit_name}")
    print()

    target.damage_pool = 0

    # Attack with each melee weapon
    for weapon in attacker_ws.weapons:
        if weapon.weapon_type == WeaponType.MELEE:
            print(f"Attacking with {weapon.weapon_name}")
            resolve_weapon_attacks(attacker, target, weapon)

    # Process damage
    if target.damage_pool > 0:
        print(f"\nTotal damage pool: {target.damage_pool}")
        from damage import process_damage_sequence
        process_damage_sequence(target)


def resolve_weapon_attacks(attacker: BattlefieldUnit, target: BattlefieldUnit,
                            weapon: WeaponProfile):
    """Resolve attacks with a specific weapon"""
    total_attacks = weapon.attacks * attacker.model_count

    print(f"  Attacks: {total_attacks} ({weapon.attacks} x {attacker.model_count} models)")
    print(f"  Hit: {weapon.hit}+  Wound: {weapon.wound}+")
    print(f"  Rend: {weapon.rend}  Damage: {weapon.damage}")
    print()

    # Hit rolls
    hit_count = 0
    print("  Rolling to hit...")
    for i in range(total_attacks):
        if make_hit_roll(weapon.hit):
            hit_count += 1

    print(f"  Hits: {hit_count} / {total_attacks}")

    if hit_count == 0:
        return

    # Wound rolls
    wound_count = 0
    print("  Rolling to wound...")
    for i in range(hit_count):
        if make_wound_roll(weapon.wound):
            wound_count += 1

    print(f"  Wounds: {wound_count} / {hit_count}")

    if wound_count == 0:
        return

    # Save rolls
    unsaved_count = 0
    print("  Making save rolls...")
    for i in range(wound_count):
        if not make_save_roll(target, weapon.rend):
            unsaved_count += 1

    print(f"  Failed saves: {unsaved_count} / {wound_count}")

    # Calculate damage
    damage_dealt = unsaved_count * weapon.damage
    target.damage_pool += damage_dealt

    print(f"  Damage inflicted: {damage_dealt}")
    print()


def make_hit_roll(hit_characteristic: int) -> bool:
    """Make a hit roll"""
    roll = roll_d6()

    # Unmodified 1 always fails
    if roll == 1:
        return False

    # Unmodified 6 is critical hit
    if roll == 6:
        # Could track critical hits here
        pass

    return roll >= hit_characteristic


def make_wound_roll(wound_characteristic: int) -> bool:
    """Make a wound roll"""
    roll = roll_d6()

    # Unmodified 1 always fails
    if roll == 1:
        return False

    return roll >= wound_characteristic


def make_save_roll(defender: BattlefieldUnit, rend: int) -> bool:
    """Make a save roll"""
    roll = roll_d6()

    defender_ws = game_db.get_warscroll(defender.warscroll_ref)
    if not defender_ws:
        return False

    # Unmodified 1 always fails
    if roll == 1:
        return False

    # Subtract rend from roll
    modified_roll = roll - rend

    return modified_roll >= defender_ws.base_stats.save


# ============================================================================
# COMBAT STATE MANAGEMENT
# ============================================================================

def update_combat_status():
    """Update which units are in combat"""
    for unit in game_db.battlefield_units:
        if unit.model_count == 0:
            unit.is_in_combat = False
            continue

        in_combat = False
        for other_unit in game_db.battlefield_units:
            if (other_unit.owner_player != unit.owner_player and
                    other_unit.model_count > 0):

                distance = calculate_distance(unit, other_unit)
                if distance <= COMBAT_RANGE:
                    in_combat = True
                    break

        unit.is_in_combat = in_combat


def check_combat_reactions(attacker: BattlefieldUnit, target: BattlefieldUnit):
    """Check for combat reactions (simplified)"""
    # TODO: Implement All-out Attack, All-out Defence reactions
    print("  (Combat reactions not yet implemented)")
