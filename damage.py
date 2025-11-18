"""
WARHAMMER AGE OF SIGMAR - DAMAGE SYSTEM
Damage allocation, ward saves, and model removal
"""

from data_types import *
from game_state import game_db
from utilities import roll_d6, print_subheader


# ============================================================================
# DAMAGE SEQUENCE
# ============================================================================

def process_damage_sequence(unit: BattlefieldUnit):
    """Process the damage sequence for a unit"""
    damage_pool = unit.damage_pool

    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    print_subheader("DAMAGE SEQUENCE")
    print(f"Unit: {warscroll.unit_name}")
    print(f"Damage pool: {damage_pool}")

    # Step 1: Ward saves
    if warscroll.has_ward:
        damage_pool = resolve_ward_saves(unit, damage_pool, warscroll.ward_value)
        print(f"After ward saves: {damage_pool} damage")

    # Step 2: Allocate damage
    if damage_pool > 0:
        allocate_damage(unit, damage_pool)

    # Reset damage pool
    unit.damage_pool = 0


def resolve_ward_saves(unit: BattlefieldUnit, damage_points: int,
                       ward_value: int) -> int:
    """Resolve ward saves against damage"""
    saved_damage = 0

    print(f"Making ward saves ({ward_value}+)...")

    for i in range(damage_points):
        roll = roll_d6()
        if roll >= ward_value:
            saved_damage += 1

    print(f"Ward saves: {saved_damage} / {damage_points}")

    return damage_points - saved_damage


def allocate_damage(unit: BattlefieldUnit, damage_points: int):
    """Allocate damage to models in unit"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    health = warscroll.base_stats.health
    remaining_damage = damage_points
    models_slain = 0

    print("\nAllocating damage...")

    while remaining_damage > 0 and unit.model_count > 0:
        # Allocate 1 damage to first model
        unit.models[0].damage_allocated += 1
        remaining_damage -= 1

        # Check if model is slain
        if unit.models[0].damage_allocated >= health:
            print(f"Model slain!")
            models_slain += 1
            remove_model(unit, 0)

            # Check if unit destroyed
            if unit.model_count == 0:
                destroy_unit(unit)
                return

    print(f"Damage allocated. Models slain: {models_slain}")
    print(f"Models remaining: {unit.model_count}")


def remove_model(unit: BattlefieldUnit, model_index: int):
    """Remove a model from the unit"""
    if model_index < len(unit.models):
        unit.models.pop(model_index)
        unit.model_count -= 1


def destroy_unit(unit: BattlefieldUnit):
    """Mark unit as destroyed"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)

    unit.model_count = 0
    unit.models = []
    unit.is_in_combat = False

    print()
    print("=" * 40)
    print("UNIT DESTROYED!")
    if warscroll:
        print(warscroll.unit_name)
    print("=" * 40)


# ============================================================================
# MORTAL DAMAGE
# ============================================================================

def inflict_mortal_damage(unit: BattlefieldUnit, mortal_damage: int):
    """
    Inflict mortal damage to a unit.
    Mortal damage bypasses saves but can be warded.
    """
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    print(f"\nInflicting {mortal_damage} mortal damage to {warscroll.unit_name}")

    # Ward saves still apply
    if warscroll.has_ward:
        mortal_damage = resolve_ward_saves(unit, mortal_damage, warscroll.ward_value)
        print(f"After ward saves: {mortal_damage} mortal damage")

    if mortal_damage > 0:
        allocate_damage(unit, mortal_damage)


# ============================================================================
# HEALING
# ============================================================================

def heal_unit(unit: BattlefieldUnit, healing_points: int):
    """Heal damage on a unit"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    if unit.model_count == 0:
        print("Unit is destroyed - cannot heal")
        return

    print(f"Healing {healing_points} points of damage")

    # Heal the first damaged model
    if unit.models[0].damage_allocated > 0:
        healed = min(healing_points, unit.models[0].damage_allocated)
        unit.models[0].damage_allocated -= healed
        print(f"Healed {healed} damage from {warscroll.unit_name}")


def return_slain_models(unit: BattlefieldUnit, model_count: int):
    """Return slain models to a unit"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    print(f"Returning {model_count} slain models to {warscroll.unit_name}")

    for i in range(model_count):
        model = ModelStats()
        model.model_name = warscroll.unit_name
        model.move = warscroll.base_stats.move
        model.health = warscroll.base_stats.health
        model.control = warscroll.base_stats.control
        model.save = warscroll.base_stats.save
        model.current_health = warscroll.base_stats.health
        model.damage_allocated = 0

        unit.models.append(model)
        unit.model_count += 1

    print(f"{warscroll.unit_name} now has {unit.model_count} models")
