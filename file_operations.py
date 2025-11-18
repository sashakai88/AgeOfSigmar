"""
WARHAMMER AGE OF SIGMAR - FILE OPERATIONS
Loading and saving game data
"""

import os
from datetime import datetime
from data_types import *
from game_state import game_db
from utilities import parse_tab_delimited_line, parse_comma_delimited


# ============================================================================
# LOADING WARSCROLLS
# ============================================================================

def load_warscroll_database():
    """Load all warscrolls from faction files"""
    print("\nLoading warscroll database...")

    # Load available faction files
    factions = [
        "StormcastEternals",
        "Skaven",
        "Nighthaunt",
        "OssiarchBonereapers"
    ]

    for faction in factions:
        try:
            load_faction_warscrolls(faction)
        except FileNotFoundError:
            print(f"  Warning: {faction} warscroll file not found, skipping...")

    print(f"Loaded {game_db.warscroll_count} unit warscrolls")


def load_faction_warscrolls(faction_name: str):
    """Load warscrolls for a specific faction"""
    filename = f"Warscrolls_{faction_name}.txt"

    if not os.path.exists(filename):
        return

    print(f"  Loading {faction_name}...")

    with open(filename, 'r') as file:
        # Skip header
        file.readline()

        for line in file:
            line = line.strip()
            if line:
                parse_warscroll_line(line, faction_name)


def parse_warscroll_line(line: str, faction_name: str):
    """Parse a warscroll data line"""
    fields = parse_tab_delimited_line(line)

    if len(fields) < 8:
        return

    warscroll = UnitWarscroll()

    # Basic info
    warscroll.unit_name = fields[0] if len(fields) > 0 else ""

    # Stats
    try:
        warscroll.base_stats.move = int(fields[1]) if len(fields) > 1 else 0
        warscroll.base_stats.health = int(fields[2]) if len(fields) > 2 else 0
        warscroll.base_stats.control = int(fields[3]) if len(fields) > 3 else 0
        warscroll.base_stats.save = int(fields[4]) if len(fields) > 4 else 0
        warscroll.unit_size = int(fields[5]) if len(fields) > 5 else 1
        warscroll.points_cost = int(fields[6]) if len(fields) > 6 else 0
    except ValueError:
        pass

    # Faction
    warscroll.faction = string_to_faction(faction_name)

    # Keywords
    if len(fields) > 7:
        keywords = parse_comma_delimited(fields[7])
        warscroll.keywords = keywords
        warscroll.keyword_count = len(keywords)

        # Determine unit type from keywords
        for keyword in keywords:
            kw_upper = keyword.upper()
            if "CAVALRY" in kw_upper:
                warscroll.unit_type = UnitType.CAVALRY
            elif "MONSTER" in kw_upper:
                warscroll.unit_type = UnitType.MONSTER
            elif "WAR MACHINE" in kw_upper or "WARMACHINE" in kw_upper:
                warscroll.unit_type = UnitType.WAR_MACHINE
            elif "BEAST" in kw_upper:
                warscroll.unit_type = UnitType.BEAST
            else:
                warscroll.unit_type = UnitType.INFANTRY

            # Check for special abilities
            if "FLY" in kw_upper:
                warscroll.has_fly = True
            if "WARD" in kw_upper:
                warscroll.has_ward = True
                warscroll.ward_value = 6  # Default ward value

    # Weapons
    if len(fields) > 8:
        parse_weapons(fields[8], warscroll)

    # Abilities
    if len(fields) > 9:
        abilities = parse_comma_delimited(fields[9])
        warscroll.abilities = abilities
        warscroll.ability_count = len(abilities)

    # Add to database
    game_db.add_warscroll(warscroll)


def parse_weapons(weapon_data: str, warscroll: UnitWarscroll):
    """Parse weapon data string"""
    # Format: "WeaponName[Type,Attacks,Hit,Wound,Rend,Damage,Range];..."
    if not weapon_data or weapon_data.strip() == "":
        return

    weapon_entries = weapon_data.split(';')

    for entry in weapon_entries:
        entry = entry.strip()
        if not entry:
            continue

        try:
            # Parse weapon name and stats
            if '[' in entry and ']' in entry:
                name_part = entry[:entry.index('[')]
                stats_part = entry[entry.index('[') + 1:entry.index(']')]

                weapon = WeaponProfile()
                weapon.weapon_name = name_part.strip()

                stats = stats_part.split(',')
                if len(stats) >= 7:
                    weapon.weapon_type = WeaponType.MELEE if stats[0].strip(
                    ).upper() == 'MELEE' else WeaponType.RANGED
                    weapon.attacks = int(stats[1].strip())
                    weapon.hit = int(stats[2].strip())
                    weapon.wound = int(stats[3].strip())
                    weapon.rend = int(stats[4].strip())
                    weapon.damage = int(stats[5].strip())
                    weapon.range = int(stats[6].strip())

                    warscroll.weapons.append(weapon)
                    warscroll.weapon_count += 1
        except (ValueError, IndexError):
            continue


def string_to_faction(faction_name: str) -> FactionType:
    """Convert faction string to enum"""
    faction_map = {
        "StormcastEternals": FactionType.STORMCAST_ETERNALS,
        "Skaven": FactionType.SKAVEN,
        "Nighthaunt": FactionType.NIGHTHAUNT,
        "OssiarchBonereapers": FactionType.OSSIARCH_BONEREAPERS,
        "SonsOfBehemat": FactionType.SONS_OF_BEHEMAT,
        "CitiesOfSigmar": FactionType.CITIES_OF_SIGMAR,
        "LuminethRealmLords": FactionType.LUMINETH_REALMLORDS
    }
    return faction_map.get(faction_name, FactionType.OTHER)


# ============================================================================
# LOADING ABILITIES
# ============================================================================

def load_universal_abilities():
    """Load core universal abilities"""
    # Normal Move
    ability = AbilityRecord(
        ability_name="Normal Move",
        ability_type=AbilityType.MOVEMENT,
        timing="Your Movement Phase",
        command_cost=0,
        description="Move each model up to its Move characteristic",
        is_passive=False,
        is_reaction=False,
        keywords=["CORE", "MOVE"]
    )
    ability.keyword_count = len(ability.keywords)
    game_db.add_ability(ability)

    # Run
    ability = AbilityRecord(
        ability_name="Run",
        ability_type=AbilityType.MOVEMENT,
        timing="Your Movement Phase",
        command_cost=0,
        description="Move + D6, but cannot charge this turn",
        is_passive=False,
        is_reaction=False,
        keywords=["CORE", "MOVE", "RUN"]
    )
    ability.keyword_count = len(ability.keywords)
    game_db.add_ability(ability)

    # Charge
    ability = AbilityRecord(
        ability_name="Charge",
        ability_type=AbilityType.MOVEMENT,
        timing="Your Charge Phase",
        command_cost=0,
        description="Roll 2D6 and move that distance towards enemy",
        is_passive=False,
        is_reaction=False,
        keywords=["CORE", "MOVE", "CHARGE"]
    )
    ability.keyword_count = len(ability.keywords)
    game_db.add_ability(ability)

    # Shoot
    ability = AbilityRecord(
        ability_name="Shoot",
        ability_type=AbilityType.SHOOTING,
        timing="Your Shooting Phase",
        command_cost=0,
        description="Make ranged attacks with unit's weapons",
        is_passive=False,
        is_reaction=False,
        keywords=["CORE", "ATTACK", "SHOOT"]
    )
    ability.keyword_count = len(ability.keywords)
    game_db.add_ability(ability)

    # Fight
    ability = AbilityRecord(
        ability_name="Fight",
        ability_type=AbilityType.OFFENSIVE,
        timing="Any Combat Phase",
        command_cost=0,
        description="Pile in and make melee attacks",
        is_passive=False,
        is_reaction=False,
        keywords=["CORE", "ATTACK", "FIGHT"]
    )
    ability.keyword_count = len(ability.keywords)
    game_db.add_ability(ability)


# ============================================================================
# SAVING GAME STATE
# ============================================================================

def save_game_state():
    """Save current game state to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"GameState_{timestamp}.sav"

    try:
        with open(filename, 'w') as file:
            # Write game state
            file.write(f"ROUND:{game_db.current_game.current_round}\n")
            file.write(f"PHASE:{game_db.current_game.current_phase.value}\n")
            file.write(f"ACTIVE:{game_db.current_game.active_player}\n")
            file.write(f"P1_POINTS:{game_db.current_game.player1_points}\n")
            file.write(f"P2_POINTS:{game_db.current_game.player2_points}\n")

            # Write unit count and positions
            file.write(f"UNITS:{game_db.unit_count}\n")

            for unit in game_db.battlefield_units:
                file.write(f"UNIT:{unit.unit_id},{unit.warscroll_ref},"
                           f"{unit.owner_player},{unit.x_position},"
                           f"{unit.y_position},{unit.model_count}\n")

        print(f"Game saved successfully to {filename}")
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False


def load_game_state(filename: str):
    """Load game state from file"""
    if not os.path.exists(filename):
        print(f"Save file {filename} not found")
        return False

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)

                    if key == "ROUND":
                        game_db.current_game.current_round = int(value)
                    elif key == "ACTIVE":
                        game_db.current_game.active_player = int(value)
                    elif key == "P1_POINTS":
                        game_db.current_game.player1_points = int(value)
                    elif key == "P2_POINTS":
                        game_db.current_game.player2_points = int(value)
                    # TODO: Load unit positions

        print(f"Game loaded successfully from {filename}")
        return True
    except Exception as e:
        print(f"Error loading game: {e}")
        return False
