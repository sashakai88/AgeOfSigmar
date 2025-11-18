"""
WARHAMMER AGE OF SIGMAR - SHOOTING PHASE
Shooting attacks and ranged combat
"""

from data_types import *
from game_state import game_db
from utilities import (calculate_distance, print_subheader,
                       get_integer_input)
from combat import (make_hit_roll, make_wound_roll, make_save_roll)
from damage import process_damage_sequence


# ============================================================================
# SHOOTING PHASE
# ============================================================================

def play_shooting_phase(player: int):
    """Execute shooting phase"""
    print_subheader("SHOOTING PHASE")

    while True:
        units = get_units_that_can_shoot(player)

        if not units:
            print(f"Player {player} has no more units that can shoot")
            break

        print(f"\nSelect unit to shoot (0 to end phase):")
        display_shooting_units(units)

        choice = get_integer_input(f"Select unit (0-{len(units)}): ", 0, len(units))

        if choice == 0:
            break

        selected_unit = units[choice - 1]
        execute_shoot(selected_unit)


def get_units_that_can_shoot(player: int) -> List[BattlefieldUnit]:
    """Get units eligible to shoot"""
    units = []

    for unit in game_db.battlefield_units:
        if (unit.owner_player == player and
                unit.model_count > 0 and
                not unit.has_shot and
                unit_has_ranged_weapons(unit)):
            units.append(unit)

    return units


def unit_has_ranged_weapons(unit: BattlefieldUnit) -> bool:
    """Check if unit has ranged weapons"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return False

    for weapon in warscroll.weapons:
        if weapon.weapon_type == WeaponType.RANGED:
            return True

    return False


def display_shooting_units(units: List[BattlefieldUnit]):
    """Display units that can shoot"""
    for i, unit in enumerate(units, 1):
        warscroll = game_db.get_warscroll(unit.warscroll_ref)
        if warscroll:
            status = "IN COMBAT" if unit.is_in_combat else ""
            print(f"{i}. {warscroll.unit_name} at ({unit.x_position}, "
                  f"{unit.y_position}) {status}")


# ============================================================================
# SHOOT EXECUTION
# ============================================================================

def execute_shoot(unit: BattlefieldUnit):
    """Execute shoot ability for a unit"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    print(f"\n=== SHOOT ===")
    print(f"Unit: {warscroll.unit_name}")

    # Check if in combat
    if unit.is_in_combat:
        print("Warning: Unit is in combat. Shooting at -1 to hit (not implemented)")

    # Select target
    targets = get_shootable_targets(unit)

    if not targets:
        print("No valid targets!")
        unit.has_shot = True
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

    # Resolve shooting attacks
    resolve_all_shooting_attacks(unit, target)

    unit.has_shot = True


def get_shootable_targets(unit: BattlefieldUnit) -> List[BattlefieldUnit]:
    """Get valid shooting targets for a unit"""
    targets = []

    for other_unit in game_db.battlefield_units:
        if (other_unit.owner_player != unit.owner_player and
                other_unit.model_count > 0):
            # Simplified - should check visibility
            targets.append(other_unit)

    return targets


# ============================================================================
# SHOOTING ATTACK RESOLUTION
# ============================================================================

def resolve_all_shooting_attacks(attacker: BattlefieldUnit, target: BattlefieldUnit):
    """Resolve all ranged attacks from attacker to target"""
    attacker_ws = game_db.get_warscroll(attacker.warscroll_ref)
    target_ws = game_db.get_warscroll(target.warscroll_ref)

    if not attacker_ws or not target_ws:
        return

    print(f"\nResolving shooting attacks...")
    print(f"Attacker: {attacker_ws.unit_name}")
    print(f"Target: {target_ws.unit_name}")
    print()

    target.damage_pool = 0

    # Attack with each ranged weapon
    for weapon in attacker_ws.weapons:
        if weapon.weapon_type == WeaponType.RANGED:
            if is_target_in_weapon_range(attacker, target, weapon):
                print(f"Shooting with {weapon.weapon_name}")
                resolve_shooting_attacks(attacker, target, weapon)
            else:
                print(f"{weapon.weapon_name} out of range")

    # Process damage
    if target.damage_pool > 0:
        print(f"\nTotal damage pool: {target.damage_pool}")
        process_damage_sequence(target)


def is_target_in_weapon_range(attacker: BattlefieldUnit, target: BattlefieldUnit,
                               weapon: WeaponProfile) -> bool:
    """Check if target is within weapon range"""
    distance = calculate_distance(attacker, target)
    return distance <= weapon.range


def resolve_shooting_attacks(attacker: BattlefieldUnit, target: BattlefieldUnit,
                              weapon: WeaponProfile):
    """Resolve attacks with a ranged weapon"""
    total_attacks = weapon.attacks * attacker.model_count

    print(f"  Attacks: {total_attacks} ({weapon.attacks} x {attacker.model_count} models)")
    print(f"  Range: {weapon.range}\"")
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


# ============================================================================
# SHOOTING REACTIONS
# ============================================================================

def check_shooting_reactions(attacker: BattlefieldUnit, target: BattlefieldUnit):
    """Check for shooting reactions (simplified)"""
    # TODO: Implement shooting reactions
    pass
