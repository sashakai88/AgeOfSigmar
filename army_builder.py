"""
WARHAMMER AGE OF SIGMAR - ARMY BUILDER
Army roster creation and management
"""

from data_types import *
from game_state import game_db
from utilities import (faction_to_string, get_integer_input, get_yes_no_input,
                       get_choice_input, print_header, print_subheader)


# ============================================================================
# ARMY ROSTER CREATION
# ============================================================================

def create_army_roster(army: ArmyRoster, points_limit: int):
    """Create a complete army roster"""
    print_header("ARMY ROSTER CREATION")
    print(f"Points Limit: {points_limit}")
    print()

    army.points_limit = points_limit
    army.total_points = 0
    army.regiment_count = 0
    army.auxiliary_count = 0

    # Select faction
    select_faction(army)

    # Build army
    while True:
        print()
        print("1. Add Regiment")
        print("2. Add Auxiliary Unit")
        print("3. Finish Roster")

        choice = get_integer_input("Select option: ", 1, 3)

        if choice == 1:
            add_regiment(army)
        elif choice == 2:
            add_auxiliary_unit(army)
        elif choice == 3:
            break

    # Pick general
    if army.regiment_count > 0:
        pick_general(army)

    # Display final roster
    display_army_roster(army)


def select_faction(army: ArmyRoster):
    """Select faction for army"""
    print_subheader("SELECT FACTION")

    factions = [
        ("Stormcast Eternals", FactionType.STORMCAST_ETERNALS),
        ("Skaven", FactionType.SKAVEN),
        ("Nighthaunt", FactionType.NIGHTHAUNT),
        ("Ossiarch Bonereapers", FactionType.OSSIARCH_BONEREAPERS),
        ("Sons of Behemat", FactionType.SONS_OF_BEHEMAT),
        ("Cities of Sigmar", FactionType.CITIES_OF_SIGMAR),
        ("Lumineth Realm-lords", FactionType.LUMINETH_REALMLORDS),
        ("Other", FactionType.OTHER)
    ]

    faction_names = [f[0] for f in factions]
    choice = get_choice_input("Select Faction:", faction_names)

    army.faction = factions[choice][1]
    print(f"\nFaction selected: {faction_to_string(army.faction)}")


def add_regiment(army: ArmyRoster):
    """Add a regiment to the army"""
    if army.total_points >= army.points_limit:
        print("\nPoints limit reached!")
        return

    if army.regiment_count >= 5:
        print("\nMaximum regiments reached!")
        return

    print_subheader(f"CREATING REGIMENT {army.regiment_count + 1}")

    regiment = Regiment()
    regiment.regiment_id = army.regiment_count

    # Select hero
    print("\nSelect Hero for this regiment:")
    heroes = game_db.get_hero_warscrolls(army.faction)

    if not heroes:
        print("No heroes available for this faction!")
        return

    display_unit_list(heroes)
    hero_choice = get_integer_input(
        f"Select hero (1-{len(heroes)}): ", 1, len(heroes))

    selected_hero = heroes[hero_choice - 1]

    if army.total_points + selected_hero.points_cost > army.points_limit:
        print(f"\nNot enough points! Need {selected_hero.points_cost}, "
              f"have {army.points_limit - army.total_points}")
        return

    regiment.hero_unit_id = selected_hero.unit_id
    army.total_points += selected_hero.points_cost

    print(f"\nAdded: {selected_hero.unit_name} ({selected_hero.points_cost} pts)")
    print(f"Points remaining: {army.points_limit - army.total_points}")

    # Add units to regiment (up to 3)
    regiment.units = []
    regiment.unit_count = 0

    while regiment.unit_count < 3:
        if not get_yes_no_input("\nAdd unit to regiment?"):
            break

        print("\nSelect unit:")
        units = game_db.get_non_hero_warscrolls(army.faction)

        if not units:
            print("No units available!")
            break

        display_unit_list(units)
        unit_choice = get_integer_input(
            f"Select unit (1-{len(units)}): ", 1, len(units))

        selected_unit = units[unit_choice - 1]

        if army.total_points + selected_unit.points_cost > army.points_limit:
            print(f"\nNot enough points! Need {selected_unit.points_cost}, "
                  f"have {army.points_limit - army.total_points}")
            continue

        regiment.units.append(selected_unit.unit_id)
        regiment.unit_count += 1
        army.total_points += selected_unit.points_cost

        print(f"\nAdded: {selected_unit.unit_name} ({selected_unit.points_cost} pts)")
        print(f"Points remaining: {army.points_limit - army.total_points}")

    # Add regiment to army
    army.regiments.append(regiment)
    army.regiment_count += 1


def add_auxiliary_unit(army: ArmyRoster):
    """Add an auxiliary unit to the army"""
    if army.total_points >= army.points_limit:
        print("\nPoints limit reached!")
        return

    print_subheader("ADD AUXILIARY UNIT")

    units = game_db.get_non_hero_warscrolls(army.faction)

    if not units:
        print("No units available!")
        return

    display_unit_list(units)
    unit_choice = get_integer_input(
        f"Select unit (1-{len(units)}): ", 1, len(units))

    selected_unit = units[unit_choice - 1]

    if army.total_points + selected_unit.points_cost > army.points_limit:
        print(f"\nNot enough points! Need {selected_unit.points_cost}, "
              f"have {army.points_limit - army.total_points}")
        return

    army.auxiliary_units.append(selected_unit.unit_id)
    army.auxiliary_count += 1
    army.total_points += selected_unit.points_cost

    print(f"\nAdded: {selected_unit.unit_name} ({selected_unit.points_cost} pts)")
    print(f"Points remaining: {army.points_limit - army.total_points}")


def pick_general(army: ArmyRoster):
    """Pick the army general from heroes"""
    print_subheader("SELECT GENERAL")
    print("Pick a hero to be your general:")

    for i, regiment in enumerate(army.regiments):
        hero = game_db.get_warscroll(regiment.hero_unit_id)
        if hero:
            print(f"{i + 1}. {hero.unit_name}")

    if army.regiment_count > 0:
        choice = get_integer_input(
            f"Select general (1-{army.regiment_count}): ", 1, army.regiment_count)

        army.general_unit_id = army.regiments[choice - 1].hero_unit_id
        army.regiments[choice - 1].is_generals_regiment = True

        general = game_db.get_warscroll(army.general_unit_id)
        if general:
            print(f"\nGeneral selected: {general.unit_name}")


def display_unit_list(units: List[UnitWarscroll]):
    """Display a list of units with stats"""
    print()
    for i, unit in enumerate(units, 1):
        print(f"{i}. {unit.unit_name:<30} "
              f"Move:{unit.base_stats.move}\" "
              f"Health:{unit.base_stats.health} "
              f"Save:{unit.base_stats.save}+ "
              f"Points:{unit.points_cost}")


def display_army_roster(army: ArmyRoster):
    """Display complete army roster"""
    print()
    print("╔" + "=" * 42 + "╗")
    print("║" + "ARMY ROSTER".center(42) + "║")
    print("╚" + "=" * 42 + "╝")
    print()
    print(f"Faction: {faction_to_string(army.faction)}")
    print(f"Points: {army.total_points} / {army.points_limit}")

    if army.general_unit_id > 0:
        general = game_db.get_warscroll(army.general_unit_id)
        if general:
            print(f"General: {general.unit_name}")

    print("\nREGIMENTS:")
    for i, regiment in enumerate(army.regiments):
        print(f"\nRegiment {i + 1}", end="")
        if regiment.is_generals_regiment:
            print(" (General's Regiment)", end="")
        print()

        hero = game_db.get_warscroll(regiment.hero_unit_id)
        if hero:
            print(f"  Hero: {hero.unit_name}")

        for unit_id in regiment.units:
            unit = game_db.get_warscroll(unit_id)
            if unit:
                print(f"  - {unit.unit_name}")

    if army.auxiliary_count > 0:
        print("\nAUXILIARY UNITS:")
        for unit_id in army.auxiliary_units:
            unit = game_db.get_warscroll(unit_id)
            if unit:
                print(f"  - {unit.unit_name}")


def select_enhancements(army: ArmyRoster):
    """Select enhancements for army (simplified)"""
    print_subheader("SELECT ENHANCEMENTS")
    print("Enhancement selection not yet implemented")
    # TODO: Implement enhancement selection
