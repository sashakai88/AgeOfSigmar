"""
WARHAMMER AGE OF SIGMAR - DATA TYPES
All enums and data classes for the game system
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional


# ============================================================================
# ENUMERATED TYPES
# ============================================================================

class UnitType(Enum):
    INFANTRY = "Infantry"
    CAVALRY = "Cavalry"
    MONSTER = "Monster"
    WAR_MACHINE = "WarMachine"
    BEAST = "Beast"


class FactionType(Enum):
    STORMCAST_ETERNALS = "StormcastEternals"
    SKAVEN = "Skaven"
    NIGHTHAUNT = "Nighthaunt"
    OSSIARCH_BONEREAPERS = "OssiarchBonereapers"
    SONS_OF_BEHEMAT = "SonsOfBehemat"
    CITIES_OF_SIGMAR = "CitiesOfSigmar"
    LUMINETH_REALMLORDS = "LuminethRealmLords"
    OTHER = "Other"


class GamePhase(Enum):
    DEPLOYMENT = "Deployment"
    HERO = "Hero"
    MOVEMENT = "Movement"
    SHOOTING = "Shooting"
    CHARGE = "Charge"
    COMBAT = "Combat"
    END_OF_TURN = "EndOfTurn"


class AbilityType(Enum):
    MOVEMENT = "Movement"
    OFFENSIVE = "Offensive"
    DEFENSIVE = "Defensive"
    SHOOTING = "Shooting"
    RALLYING = "Rallying"
    SPECIAL = "Special"
    CONTROL = "Control"
    CORE = "Core"


class WeaponType(Enum):
    MELEE = "Melee"
    RANGED = "Ranged"


class DamageType(Enum):
    NORMAL = "Normal"
    MORTAL = "Mortal"


class TerrainType(Enum):
    OBSTACLE = "Obstacle"
    OBSCURING_TERRAIN = "ObscuringTerrain"
    AREA_TERRAIN = "AreaTerrain"
    PLACE_OF_POWER = "PlaceOfPower"
    FACTION_TERRAIN = "FactionTerrain"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ModelStats:
    """Statistics for a single model"""
    model_name: str = ""
    move: int = 0
    health: int = 0
    control: int = 0
    save: int = 0
    bravery_mod: int = 0
    is_champion: bool = False
    is_musician: bool = False
    is_standard_bearer: bool = False
    current_health: int = 0
    damage_allocated: int = 0


@dataclass
class WeaponProfile:
    """Weapon statistics"""
    weapon_name: str = ""
    weapon_type: WeaponType = WeaponType.MELEE
    attacks: int = 0
    hit: int = 0
    wound: int = 0
    rend: int = 0
    damage: int = 0
    range: int = 0
    abilities: List[str] = field(default_factory=list)
    ability_count: int = 0


@dataclass
class UnitWarscroll:
    """Complete unit warscroll"""
    unit_id: int = 0
    unit_name: str = ""
    faction: FactionType = FactionType.OTHER
    unit_type: UnitType = UnitType.INFANTRY
    keywords: List[str] = field(default_factory=list)
    keyword_count: int = 0
    base_stats: ModelStats = field(default_factory=ModelStats)
    weapons: List[WeaponProfile] = field(default_factory=list)
    weapon_count: int = 0
    unit_size: int = 0
    points_cost: int = 0
    abilities: List[str] = field(default_factory=list)
    ability_count: int = 0
    has_fly: bool = False
    has_ward: bool = False
    ward_value: int = 7


@dataclass
class BattlefieldUnit:
    """Instance of a unit on the battlefield"""
    unit_id: int = 0
    warscroll_ref: int = 0
    owner_player: int = 0
    models: List[ModelStats] = field(default_factory=list)
    model_count: int = 0
    x_position: int = 0
    y_position: int = 0
    is_in_combat: bool = False
    has_charged: bool = False
    has_moved: bool = False
    has_shot: bool = False
    has_fought: bool = False
    damage_pool: int = 0
    is_reinforced: bool = False
    commands_used: int = 0


@dataclass
class Regiment:
    """Regiment structure"""
    regiment_id: int = 0
    hero_unit_id: int = 0
    units: List[int] = field(default_factory=list)
    unit_count: int = 0
    is_generals_regiment: bool = False


@dataclass
class ArmyRoster:
    """Complete army roster"""
    player_name: str = ""
    faction: FactionType = FactionType.OTHER
    points_limit: int = 0
    total_points: int = 0
    regiments: List[Regiment] = field(default_factory=list)
    regiment_count: int = 0
    auxiliary_units: List[int] = field(default_factory=list)
    auxiliary_count: int = 0
    general_unit_id: int = 0
    battle_formation: str = ""
    enhancements: List[str] = field(default_factory=list)
    enhancement_count: int = 0


@dataclass
class ObjectiveMarker:
    """Objective marker on battlefield"""
    objective_id: int = 0
    x_position: int = 0
    y_position: int = 0
    controlled_by: int = 0
    contesting_units: List[int] = field(default_factory=list)
    contest_count: int = 0


@dataclass
class TerrainFeature:
    """Terrain feature"""
    terrain_id: int = 0
    terrain_name: str = ""
    terrain_type: TerrainType = TerrainType.OBSTACLE
    x_position: int = 0
    y_position: int = 0
    width: int = 0
    height: int = 0
    has_cover: bool = False
    has_obscuring: bool = False
    is_impassable: bool = False
    is_place_of_power: bool = False


@dataclass
class AttackRoll:
    """Record of an attack sequence"""
    attacker_unit_id: int = 0
    target_unit_id: int = 0
    weapon_used: Optional[WeaponProfile] = None
    attack_count: int = 0
    hit_rolls: List[int] = field(default_factory=list)
    wound_rolls: List[int] = field(default_factory=list)
    save_rolls: List[int] = field(default_factory=list)
    damage_inflicted: int = 0
    mortal_damage: int = 0
    critical_hits: int = 0


@dataclass
class GameState:
    """Current game state"""
    current_round: int = 0
    current_phase: GamePhase = GamePhase.DEPLOYMENT
    active_player: int = 0
    is_first_round: bool = True
    player1_points: int = 0
    player2_points: int = 0
    underdog: int = 0
    player1_commands: int = 4
    player2_commands: int = 4


@dataclass
class AbilityRecord:
    """Ability definition"""
    ability_name: str = ""
    ability_type: AbilityType = AbilityType.CORE
    timing: str = ""
    command_cost: int = 0
    description: str = ""
    can_be_used_by: str = ""
    is_passive: bool = False
    is_reaction: bool = False
    keywords: List[str] = field(default_factory=list)
    keyword_count: int = 0
