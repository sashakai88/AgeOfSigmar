// ===========================================================================
// WARHAMMER AGE OF SIGMAR - GameMaker Edition
// Core Game Data Structures and Enums
// ===========================================================================

// ---------------------------------------------------------------------------
// ENUMS
// ---------------------------------------------------------------------------

enum UnitType {
    Infantry,
    Cavalry,
    Monster,
    WarMachine,
    Beast
}

enum FactionType {
    StormcastEternals,
    Skaven,
    Nighthaunt,
    OssiarchBonereapers,
    SonsOfBehemat,
    CitiesOfSigmar,
    LuminethRealmLords,
    Other
}

enum GamePhase {
    Deployment,
    Hero,
    Movement,
    Shooting,
    Charge,
    Combat,
    EndOfTurn
}

enum WeaponType {
    Melee,
    Ranged
}

enum TerrainType {
    Obstacle,
    ObscuringTerrain,
    AreaTerrain,
    PlaceOfPower,
    FactionTerrain
}

// ---------------------------------------------------------------------------
// GLOBAL GAME STATE
// ---------------------------------------------------------------------------

global.current_round = 0;
global.current_phase = GamePhase.Deployment;
global.active_player = 1;
global.is_first_round = true;
global.player1_points = 0;
global.player2_points = 0;
global.player1_commands = 4;
global.player2_commands = 4;
global.underdog = 0;

// Battlefield constants
global.battlefield_width = 44;  // inches
global.battlefield_height = 60; // inches
global.combat_range = 3;        // inches
global.scale = 20;              // pixels per inch

// Lists for game objects
global.battlefield_units = ds_list_create();
global.warscrolls = ds_list_create();
global.objectives = ds_list_create();
global.terrain_features = ds_list_create();

// Selected units
global.selected_units = ds_list_create();

// Camera
global.camera_x = 0;
global.camera_y = 0;
global.camera_zoom = 1.0;

// ---------------------------------------------------------------------------
// CONSTRUCTOR FUNCTIONS
// ---------------------------------------------------------------------------

/// @function UnitWarscroll()
/// @description Creates a unit warscroll data structure
function UnitWarscroll() constructor {
    unit_id = 0;
    unit_name = "";
    faction = FactionType.Other;
    unit_type = UnitType.Infantry;
    keywords = [];

    // Base stats
    move = 0;
    health = 0;
    control = 0;
    save = 0;
    bravery_mod = 0;

    weapons = [];
    abilities = [];
    unit_size = 1;
    points_cost = 0;

    has_fly = false;
    has_ward = false;
    ward_value = 7;
}

/// @function WeaponProfile()
/// @description Creates a weapon profile
function WeaponProfile() constructor {
    weapon_name = "";
    weapon_type = WeaponType.Melee;
    attacks = 0;
    hit = 0;
    wound = 0;
    rend = 0;
    damage = 0;
    range = 0;
    abilities = [];
}

/// @function BattlefieldUnit()
/// @description Creates a battlefield unit instance
function BattlefieldUnit() constructor {
    unit_id = 0;
    warscroll_ref = 0;
    owner_player = 0;

    model_count = 0;
    x_pos = 0;
    y_pos = 0;

    is_in_combat = false;
    has_charged = false;
    has_moved = false;
    has_shot = false;
    has_fought = false;

    damage_pool = 0;
    is_reinforced = false;
    commands_used = 0;

    models = [];
}

/// @function ObjectiveMarker()
/// @description Creates an objective marker
function ObjectiveMarker() constructor {
    objective_id = 0;
    x_pos = 0;
    y_pos = 0;
    controlled_by = 0;
    contesting_units = [];
}

/// @function TerrainFeature()
/// @description Creates a terrain feature
function TerrainFeature() constructor {
    terrain_id = 0;
    terrain_name = "";
    terrain_type = TerrainType.Obstacle;
    x_pos = 0;
    y_pos = 0;
    width = 0;
    height = 0;
    has_cover = false;
    has_obscuring = false;
    is_impassable = false;
}

// ---------------------------------------------------------------------------
// HELPER FUNCTIONS
// ---------------------------------------------------------------------------

/// @function world_to_screen(_wx, _wy)
/// @description Convert world coordinates to screen coordinates
/// @param {real} _wx World X position (inches)
/// @param {real} _wy World Y position (inches)
/// @return {array} [screen_x, screen_y]
function world_to_screen(_wx, _wy) {
    var _screen_x = (_wx * global.scale - global.camera_x) * global.camera_zoom;
    var _screen_y = (_wy * global.scale - global.camera_y) * global.camera_zoom;
    return [_screen_x, _screen_y];
}

/// @function screen_to_world(_sx, _sy)
/// @description Convert screen coordinates to world coordinates
/// @param {real} _sx Screen X position (pixels)
/// @param {real} _sy Screen Y position (pixels)
/// @return {array} [world_x, world_y]
function screen_to_world(_sx, _sy) {
    var _world_x = (_sx / global.camera_zoom + global.camera_x) / global.scale;
    var _world_y = (_sy / global.camera_zoom + global.camera_y) / global.scale;
    return [_world_x, _world_y];
}

/// @function distance_2d(_x1, _y1, _x2, _y2)
/// @description Calculate 2D distance
/// @param {real} _x1 X1
/// @param {real} _y1 Y1
/// @param {real} _x2 X2
/// @param {real} _y2 Y2
/// @return {real} Distance
function distance_2d(_x1, _y1, _x2, _y2) {
    return point_distance(_x1, _y1, _x2, _y2);
}

/// @function roll_d6()
/// @description Roll a D6
/// @return {real} 1-6
function roll_d6() {
    return irandom_range(1, 6);
}

/// @function roll_d3()
/// @description Roll a D3
/// @return {real} 1-3
function roll_d3() {
    return ceil(roll_d6() / 2);
}

/// @function roll_2d6()
/// @description Roll 2D6
/// @return {real} 2-12
function roll_2d6() {
    return roll_d6() + roll_d6();
}

/// @function faction_to_string(_faction)
/// @description Convert faction enum to string
/// @param {enum} _faction FactionType
/// @return {string} Faction name
function faction_to_string(_faction) {
    switch(_faction) {
        case FactionType.StormcastEternals: return "Stormcast Eternals";
        case FactionType.Skaven: return "Skaven";
        case FactionType.Nighthaunt: return "Nighthaunt";
        case FactionType.OssiarchBonereapers: return "Ossiarch Bonereapers";
        case FactionType.SonsOfBehemat: return "Sons of Behemat";
        case FactionType.CitiesOfSigmar: return "Cities of Sigmar";
        case FactionType.LuminethRealmLords: return "Lumineth Realm-lords";
        default: return "Other";
    }
}

/// @function phase_to_string(_phase)
/// @description Convert phase enum to string
/// @param {enum} _phase GamePhase
/// @return {string} Phase name
function phase_to_string(_phase) {
    switch(_phase) {
        case GamePhase.Deployment: return "Deployment";
        case GamePhase.Hero: return "Hero";
        case GamePhase.Movement: return "Movement";
        case GamePhase.Shooting: return "Shooting";
        case GamePhase.Charge: return "Charge";
        case GamePhase.Combat: return "Combat";
        case GamePhase.EndOfTurn: return "End of Turn";
        default: return "Unknown";
    }
}

show_debug_message("Core data structures initialized");
