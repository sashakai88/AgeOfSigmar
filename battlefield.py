"""
WARHAMMER AGE OF SIGMAR - BATTLEFIELD SETUP
Battlefield setup, deployment, and terrain
"""

from data_types import *
from game_state import game_db, COMBAT_RANGE, BATTLEFIELD_WIDTH, BATTLEFIELD_HEIGHT
from utilities import (roll_off, get_integer_input, get_yes_no_input,
                       print_header, print_subheader, is_valid_position)


# ============================================================================
# BATTLEFIELD SETUP
# ============================================================================

def setup_battlefield():
    """Complete battlefield setup"""
    print_header("BATTLEFIELD SETUP")

    place_objectives()
    place_terrain()
    deploy_armies()


def place_objectives():
    """Place objective markers on battlefield"""
    print_subheader("PLACING OBJECTIVES")

    # Standard 4-objective placement
    positions = [
        (12, 12),
        (32, 12),
        (12, 48),
        (32, 48)
    ]

    game_db.objective_count = 4

    for i, (x, y) in enumerate(positions):
        objective = ObjectiveMarker(
            objective_id=i,
            x_position=x,
            y_position=y,
            controlled_by=0,
            contesting_units=[],
            contest_count=0
        )
        game_db.objectives.append(objective)
        print(f"Objective {i + 1} placed at ({x}, {y})")


def place_terrain():
    """Place terrain features"""
    print_subheader("PLACING TERRAIN")

    if not get_yes_no_input("Place terrain features?"):
        return

    terrain_count = get_integer_input("How many terrain features? ", 0, 20)

    for i in range(terrain_count):
        print(f"\nTerrain {i + 1}:")
        place_single_terrain(i)


def place_single_terrain(index: int):
    """Place a single terrain feature"""
    terrain = TerrainFeature()
    terrain.terrain_id = index

    print("Select terrain type:")
    print("1. Obstacle")
    print("2. Obscuring Terrain")
    print("3. Area Terrain")
    print("4. Place of Power")

    type_choice = get_integer_input("Type: ", 1, 4)

    if type_choice == 1:
        terrain.terrain_type = TerrainType.OBSTACLE
        terrain.has_cover = True
        terrain.terrain_name = "Obstacle"
    elif type_choice == 2:
        terrain.terrain_type = TerrainType.OBSCURING_TERRAIN
        terrain.has_cover = True
        terrain.has_obscuring = True
        terrain.terrain_name = "Obscuring Terrain"
    elif type_choice == 3:
        terrain.terrain_type = TerrainType.AREA_TERRAIN
        terrain.has_cover = True
        terrain.terrain_name = "Area Terrain"
    elif type_choice == 4:
        terrain.terrain_type = TerrainType.PLACE_OF_POWER
        terrain.has_cover = True
        terrain.is_place_of_power = True
        terrain.terrain_name = "Place of Power"

    terrain.x_position = get_integer_input(
        f"X position (0-{BATTLEFIELD_WIDTH}): ", 0, BATTLEFIELD_WIDTH)
    terrain.y_position = get_integer_input(
        f"Y position (0-{BATTLEFIELD_HEIGHT}): ", 0, BATTLEFIELD_HEIGHT)

    game_db.terrain_features.append(terrain)
    game_db.terrain_count += 1


# ============================================================================
# DEPLOYMENT
# ============================================================================

def deploy_armies():
    """Deploy both armies"""
    print_subheader("DEPLOYMENT PHASE")

    # Roll off for deployment
    print("\nRolling off for deployment...")
    roll_result = roll_off()

    if roll_result == 1:
        first_deployer = 1
        print("Player 1 chooses who deploys first")
    else:
        first_deployer = 2
        print("Player 2 chooses who deploys first")

    # Spawn units for both players
    spawn_army_units(1, game_db.player1_army)
    spawn_army_units(2, game_db.player2_army)

    # Alternate deployment
    alternate_deployment(first_deployer)


def spawn_army_units(player: int, army: ArmyRoster):
    """Create battlefield units from army roster"""
    print(f"\nSpawning units for Player {player}...")

    # Spawn units from regiments
    for regiment in army.regiments:
        # Spawn hero
        spawn_unit(regiment.hero_unit_id, player)

        # Spawn regiment units
        for unit_id in regiment.units:
            spawn_unit(unit_id, player)

    # Spawn auxiliary units
    for unit_id in army.auxiliary_units:
        spawn_unit(unit_id, player)


def spawn_unit(warscroll_id: int, player: int):
    """Create a battlefield unit from a warscroll"""
    warscroll = game_db.get_warscroll(warscroll_id)
    if not warscroll:
        return

    unit = BattlefieldUnit()
    unit.warscroll_ref = warscroll_id
    unit.owner_player = player
    unit.model_count = warscroll.unit_size

    # Create models
    unit.models = []
    for i in range(warscroll.unit_size):
        model = ModelStats()
        model.model_name = warscroll.unit_name
        model.move = warscroll.base_stats.move
        model.health = warscroll.base_stats.health
        model.control = warscroll.base_stats.control
        model.save = warscroll.base_stats.save
        model.current_health = warscroll.base_stats.health
        model.damage_allocated = 0

        # First model is champion
        if i == 0:
            model.is_champion = True

        unit.models.append(model)

    game_db.add_battlefield_unit(unit)


def alternate_deployment(first_player: int):
    """Alternate deployment between players"""
    print("\n=== ALTERNATING DEPLOYMENT ===")

    current_player = first_player
    units_to_deploy = {1: [], 2: []}

    # Get units for each player
    for unit in game_db.battlefield_units:
        units_to_deploy[unit.owner_player].append(unit)

    while units_to_deploy[1] or units_to_deploy[2]:
        # Check if current player has units to deploy
        if not units_to_deploy[current_player]:
            # Switch to other player
            current_player = 2 if current_player == 1 else 1
            if not units_to_deploy[current_player]:
                break
            continue

        print(f"\n--- Player {current_player}'s turn ---")
        display_undeployed_units(current_player, units_to_deploy[current_player])

        unit_choice = get_integer_input(
            f"Select unit to deploy (1-{len(units_to_deploy[current_player])}): ",
            1, len(units_to_deploy[current_player])
        )

        unit = units_to_deploy[current_player][unit_choice - 1]
        deploy_unit(unit, current_player)

        # Remove from undeployed list
        units_to_deploy[current_player].remove(unit)

        # Switch player
        current_player = 2 if current_player == 1 else 1

    print("\n=== DEPLOYMENT COMPLETE ===")


def display_undeployed_units(player: int, units: List[BattlefieldUnit]):
    """Display units that haven't been deployed yet"""
    print(f"\nPlayer {player} - Units to deploy:")
    for i, unit in enumerate(units, 1):
        warscroll = game_db.get_warscroll(unit.warscroll_ref)
        if warscroll:
            print(f"{i}. {warscroll.unit_name}")


def deploy_unit(unit: BattlefieldUnit, player: int):
    """Deploy a single unit"""
    warscroll = game_db.get_warscroll(unit.warscroll_ref)
    if not warscroll:
        return

    print(f"\nDeploying: {warscroll.unit_name}")

    valid = False
    while not valid:
        x_pos = get_integer_input(
            f"X coordinate (0-{BATTLEFIELD_WIDTH}): ", 0, BATTLEFIELD_WIDTH)
        y_pos = get_integer_input(
            f"Y coordinate (0-{BATTLEFIELD_HEIGHT}): ", 0, BATTLEFIELD_HEIGHT)

        if is_valid_deployment(x_pos, y_pos, player):
            unit.x_position = x_pos
            unit.y_position = y_pos
            valid = True
            print(f"Unit deployed at ({x_pos}, {y_pos})")
        else:
            print("Invalid deployment position. Try again.")


def is_valid_deployment(x: int, y: int, player: int) -> bool:
    """
    Check if deployment position is valid.
    Simplified - assumes player 1 deploys in bottom half, player 2 in top half.
    """
    if not is_valid_position(x, y, BATTLEFIELD_WIDTH, BATTLEFIELD_HEIGHT):
        return False

    # Player 1: bottom half (Y < 30)
    # Player 2: top half (Y > 30)
    if player == 1:
        return y < 30
    else:
        return y > 30
