# 🎨 CUSTOMIZATION GUIDE - GameMaker Edition

Complete guide to customizing units, factions, and gameplay in the Warhammer Age of Sigmar GameMaker implementation.

## 📍 Where to Customize What

### 1. Spawn Units on Battlefield
**File**: `/AgeOfSigmarGM/objects/obj_game_controller/Create_0.gml`
**Lines**: 37-51

```gml
// SPAWN STARTING UNITS - CUSTOMIZE HERE!
// Usage: spawn_unit(warscroll_id, x_inches, y_inches, player, model_count)

// Player 1 (Blue)
spawn_unit(0, 10, 54, 1, 5);  // Spawn 5 Liberators at position (10", 54")
spawn_unit(0, 20, 54, 1, 5);  // Spawn 5 more Liberators at (20", 54")

// Player 2 (Red)
spawn_unit(1, 15, 6, 2, 20);  // Spawn 20 Clanrats at (15", 6")
```

**To add more units**: Just add more `spawn_unit()` calls!

---

### 2. Create New Warscrolls (Unit Types)
**File**: `/AgeOfSigmarGM/scripts/scr_helpers/scr_helpers.gml`
**Function**: `load_sample_warscrolls()` (starts at line 224)

**Current Warscrolls**:
- **ID 0**: Liberators (Stormcast Eternals)
- **ID 1**: Clanrats (Skaven)

**To add a new warscroll**, add this code BEFORE line 278:

```gml
// Blood Warriors (Khorne) - Warscroll ID will be 2
var _blood_warriors = new UnitWarscroll();
_blood_warriors.unit_id = 2;
_blood_warriors.unit_name = "Blood Warriors";
_blood_warriors.faction = FactionType.Khorne;  // Must exist in enum
_blood_warriors.unit_type = UnitType.Infantry;
_blood_warriors.move = 4;              // Movement in inches
_blood_warriors.health = 2;            // Wounds per model
_blood_warriors.control = 1;           // Objective control value
_blood_warriors.save = 4;              // Save characteristic (4+ = 4)
_blood_warriors.unit_size = 10;        // Standard unit size
_blood_warriors.points_cost = 180;     // Points value

// Create weapon
var _goreaxe = new WeaponProfile();
_goreaxe.weapon_name = "Goreaxe";
_goreaxe.weapon_type = WeaponType.Melee;
_goreaxe.attacks = 2;                  // Attacks per model
_goreaxe.hit = 3;                      // Hit on 3+
_goreaxe.wound = 3;                    // Wound on 3+
_goreaxe.rend = 1;                     // -1 rend
_goreaxe.damage = 1;                   // 1 damage per hit
_goreaxe.range = 1;                    // Melee (1")

_blood_warriors.weapons = [_goreaxe];
ds_list_add(global.warscrolls, _blood_warriors);
```

Then spawn them with: `spawn_unit(2, x, y, player, 10);`

---

### 3. Add New Factions
**File**: `/AgeOfSigmarGM/scripts/scr_core_data/scr_core_data.gml`
**Line**: ~15

**Current Enum**:
```gml
enum FactionType {
    StormcastEternals,
    Skaven,
    Nighthaunt,
    Khorne,
    Sylvaneth,
    LuminethRealmLords,
    Other
}
```

**To add a faction**:
1. Add it to the enum (e.g., `IronJawz,`)
2. Use it in warscrolls: `_unit.faction = FactionType.IronJawz;`
3. Optional: Add faction-specific colors in renderer (see below)

---

### 4. Change Unit Colors/Appearance
**File**: `/AgeOfSigmarGM/objects/obj_battlefield_renderer/Draw_0.gml`
**Function**: `draw_all_units()` (line ~164)

**Current Code** (line ~178):
```gml
// Determine color
var _unit_color = c_blue;
if (_unit.owner_player == 2) {
    _unit_color = c_red;
}
```

**To add faction-specific colors**:
```gml
// Determine color by faction
var _warscroll = global.warscrolls[| _unit.warscroll_ref];
var _unit_color = c_blue;  // Default

switch(_warscroll.faction) {
    case FactionType.StormcastEternals:
        _unit_color = (_unit.owner_player == 1) ? c_blue : c_navy;
        break;
    case FactionType.Skaven:
        _unit_color = (_unit.owner_player == 1) ? c_olive : make_color_rgb(139, 69, 19);
        break;
    case FactionType.Khorne:
        _unit_color = make_color_rgb(180, 0, 0);  // Dark red
        break;
    case FactionType.Nighthaunt:
        _unit_color = make_color_rgb(100, 255, 100);  // Ghostly green
        break;
    default:
        _unit_color = (_unit.owner_player == 1) ? c_blue : c_red;
}
```

**To change unit sizes** (line ~171):
```gml
var _radius = 15;  // Default infantry
if (_warscroll.unit_type == UnitType.Monster) {
    _radius = 35;  // Make monsters BIGGER
} else if (_warscroll.unit_type == UnitType.Cavalry) {
    _radius = 20;  // Make cavalry bigger
}
```

---

### 5. Add Ranged Weapons
**In warscroll definition** (scr_helpers.gml):

```gml
// Judicators (Stormcast with bows)
var _judicators = new UnitWarscroll();
_judicators.unit_id = 3;
_judicators.unit_name = "Judicators";
_judicators.faction = FactionType.StormcastEternals;
_judicators.unit_type = UnitType.Infantry;
_judicators.move = 5;
_judicators.health = 2;
_judicators.control = 1;
_judicators.save = 4;
_judicators.unit_size = 5;
_judicators.points_cost = 180;

// Ranged weapon
var _skybolt_bow = new WeaponProfile();
_skybolt_bow.weapon_name = "Skybolt Bow";
_skybolt_bow.weapon_type = WeaponType.Ranged;  // Important!
_skybolt_bow.attacks = 2;
_skybolt_bow.hit = 3;
_skybolt_bow.wound = 3;
_skybolt_bow.rend = 1;
_skybolt_bow.damage = 1;
_skybolt_bow.range = 24;  // 24" range

// Melee weapon for close combat
var _storm_gladius = new WeaponProfile();
_storm_gladius.weapon_name = "Storm Gladius";
_storm_gladius.weapon_type = WeaponType.Melee;
_storm_gladius.attacks = 1;
_storm_gladius.hit = 3;
_storm_gladius.wound = 4;
_storm_gladius.rend = 0;
_storm_gladius.damage = 1;
_storm_gladius.range = 1;

_judicators.weapons = [_skybolt_bow, _storm_gladius];  // Both weapons
ds_list_add(global.warscrolls, _judicators);
```

The shooting system will automatically use ranged weapons during the Shooting Phase!

---

### 6. Create Monster Units

```gml
// Stardrake (Monster)
var _stardrake = new UnitWarscroll();
_stardrake.unit_id = 4;
_stardrake.unit_name = "Stardrake";
_stardrake.faction = FactionType.StormcastEternals;
_stardrake.unit_type = UnitType.Monster;  // Important!
_stardrake.move = 10;
_stardrake.health = 18;  // Lots of wounds!
_stardrake.control = 5;  // High control value
_stardrake.save = 3;     // Strong armor
_stardrake.unit_size = 1;  // Single model
_stardrake.points_cost = 450;

var _great_claws = new WeaponProfile();
_great_claws.weapon_name = "Great Claws";
_great_claws.weapon_type = WeaponType.Melee;
_great_claws.attacks = 6;
_great_claws.hit = 3;
_great_claws.wound = 2;
_great_claws.rend = 2;
_great_claws.damage = 3;  // High damage per attack
_great_claws.range = 2;   // 2" reach

_stardrake.weapons = [_great_claws];
ds_list_add(global.warscrolls, _stardrake);
```

Spawn it: `spawn_unit(4, 22, 30, 1, 1);  // Single model`

---

### 7. Modify Battlefield Setup

**Change battlefield size** - `scr_core_data.gml` line ~40:
```gml
global.battlefield_width = 44;   // Change width (inches)
global.battlefield_height = 60;  // Change height (inches)
```

**Change objective positions** - `scr_helpers.gml` line ~283:
```gml
function place_objectives() {
    // Custom positions [x, y] in inches
    var _positions = [
        [10, 15],   // Objective 1
        [34, 15],   // Objective 2
        [10, 45],   // Objective 3
        [34, 45],   // Objective 4
        [22, 30]    // Objective 5 (center)
    ];

    for (var i = 0; i < array_length(_positions); i++) {
        var _obj = new ObjectiveMarker();
        _obj.objective_id = i;
        _obj.x_pos = _positions[i][0];
        _obj.y_pos = _positions[i][1];
        _obj.controlled_by = 0;
        ds_list_add(global.objectives, _obj);
    }
}
```

**Add terrain** - Add to `Create_0.gml` after objectives:
```gml
// Add terrain features
var _forest = new TerrainFeature();
_forest.terrain_name = "Haunted Woods";
_forest.x_pos = 22;
_forest.y_pos = 30;
_forest.radius = 6;  // 6" radius
_forest.blocks_line_of_sight = true;
_forest.is_impassable = false;
ds_list_add(global.terrain_features, _forest);

var _ruins = new TerrainFeature();
_ruins.terrain_name = "Ancient Ruins";
_ruins.x_pos = 35;
_ruins.y_pos = 20;
_ruins.radius = 4;
_ruins.blocks_line_of_sight = true;
_ruins.is_impassable = false;
ds_list_add(global.terrain_features, _ruins);
```

---

### 8. Customize Camera Settings

**File**: `/AgeOfSigmarGM/objects/obj_game_controller/Step_0.gml`

**Camera speed** (line ~15):
```gml
var _camera_speed = 8;  // Increase for faster camera (default: 8)
```

**Zoom limits** (line ~25):
```gml
global.camera_zoom = clamp(global.camera_zoom * 1.1, 0.5, 3.0);
//                                                    ^^^  ^^^
//                                                    min  max
// Change to (0.3, 5.0) for wider zoom range
```

**Starting zoom** - `Create_0.gml` line 18:
```gml
global.camera_zoom = 0.8;  // Start zoomed out (default: 1.0)
```

---

### 9. Add Unit Abilities

**In warscroll** (scr_helpers.gml):
```gml
_liberators.abilities = [
    "Shield Wall - +1 to save rolls",
    "Sigmar's Blessing - 6+ ward save"
];
```

**Create ability function** (at end of scr_helpers.gml):
```gml
/// @function activate_shield_wall(_unit)
function activate_shield_wall(_unit) {
    var _warscroll = global.warscrolls[| _unit.warscroll_ref];

    show_debug_message(_warscroll.unit_name + " activates Shield Wall!");

    // Buff save by 1 for this phase
    _warscroll.save -= 1;  // Lower number = better save

    // You can add temporary buffs here
}
```

**Hook up to hotkeys** - `obj_game_controller/Step_0.gml`:
```gml
// Ability hotkeys (add around line 80)
if (keyboard_check_pressed(ord("1"))) {
    if (ds_list_size(global.selected_units) > 0) {
        var _unit = global.selected_units[| 0];
        activate_shield_wall(_unit);
    }
}
```

---

### 10. Change Deployment Zones

**File**: `obj_battlefield_renderer/Draw_0.gml`
**Function**: `draw_deployment_zones()` (line ~56)

```gml
function draw_deployment_zones() {
    draw_set_color(deployment_zone_color);
    draw_set_alpha(deployment_zone_alpha);

    // Player 1 deployment zone - CUSTOMIZE SIZE
    var _p1_depth = 12;  // Change from 9" to 12"
    var _p1_top_left = world_to_screen(0, global.battlefield_height - _p1_depth);
    var _p1_bottom_right = world_to_screen(global.battlefield_width, global.battlefield_height);
    draw_rectangle(_p1_top_left[0], _p1_top_left[1],
                   _p1_bottom_right[0], _p1_bottom_right[1], false);

    // Player 2 deployment zone
    var _p2_depth = 12;  // Change from 9" to 12"
    var _p2_top_left = world_to_screen(0, 0);
    var _p2_bottom_right = world_to_screen(global.battlefield_width, _p2_depth);
    draw_rectangle(_p2_top_left[0], _p2_top_left[1],
                   _p2_bottom_right[0], _p2_bottom_right[1], false);

    draw_set_alpha(1.0);
}
```

---

## 🎯 Quick Reference

### Spawn Units
```gml
// obj_game_controller/Create_0.gml (line 43+)
spawn_unit(warscroll_id, x, y, player, model_count);
```

### Add Warscrolls
```gml
// scr_helpers.gml load_sample_warscrolls() (line 224+)
var _unit = new UnitWarscroll();
_unit.unit_name = "Your Unit";
_unit.faction = FactionType.YourFaction;
// ... set stats ...
ds_list_add(global.warscrolls, _unit);
```

### Add Factions
```gml
// scr_core_data.gml enum FactionType (line 15+)
enum FactionType {
    // ... existing ...
    YourNewFaction,
}
```

### Change Colors
```gml
// obj_battlefield_renderer/Draw_0.gml draw_all_units() (line 178+)
_unit_color = make_color_rgb(R, G, B);
```

### Add Terrain
```gml
// obj_game_controller/Create_0.gml (after place_objectives)
var _terrain = new TerrainFeature();
_terrain.x_pos = 22; _terrain.y_pos = 30;
ds_list_add(global.terrain_features, _terrain);
```

---

## 📋 Complete Example: Adding a New Army

Let's add **Ironjawz Orruks** to the game:

### Step 1: Add Faction (scr_core_data.gml)
```gml
enum FactionType {
    StormcastEternals,
    Skaven,
    Nighthaunt,
    Khorne,
    Sylvaneth,
    LuminethRealmLords,
    Ironjawz,  // NEW!
    Other
}
```

### Step 2: Create Warscroll (scr_helpers.gml, in load_sample_warscrolls)
```gml
// Ardboyz - Warscroll ID 2
var _ardboyz = new UnitWarscroll();
_ardboyz.unit_id = 2;
_ardboyz.unit_name = "Ardboyz";
_ardboyz.faction = FactionType.Ironjawz;
_ardboyz.unit_type = UnitType.Infantry;
_ardboyz.move = 4;
_ardboyz.health = 2;
_ardboyz.control = 1;
_ardboyz.save = 4;
_ardboyz.unit_size = 10;
_ardboyz.points_cost = 160;

var _choppa = new WeaponProfile();
_choppa.weapon_name = "Big Choppa";
_choppa.weapon_type = WeaponType.Melee;
_choppa.attacks = 2;
_choppa.hit = 4;
_choppa.wound = 3;
_choppa.rend = 1;
_choppa.damage = 1;
_choppa.range = 1;

_ardboyz.weapons = [_choppa];
ds_list_add(global.warscrolls, _ardboyz);
```

### Step 3: Add Custom Color (obj_battlefield_renderer/Draw_0.gml)
```gml
// In draw_all_units(), replace color section:
var _warscroll = global.warscrolls[| _unit.warscroll_ref];
var _unit_color = c_blue;

if (_warscroll.faction == FactionType.Ironjawz) {
    _unit_color = make_color_rgb(50, 100, 50);  // Dark green
} else if (_unit.owner_player == 2) {
    _unit_color = c_red;
} else {
    _unit_color = c_blue;
}
```

### Step 4: Spawn Units (obj_game_controller/Create_0.gml)
```gml
// Add to spawn section:
spawn_unit(2, 12, 50, 1, 10);  // 10 Ardboyz for Player 1
spawn_unit(2, 28, 52, 1, 10);  // 10 more Ardboyz
```

### Done! Your Ironjawz are ready to WAAAGH!

---

## 🔍 Finding Things Quickly

| What | Where | Line |
|------|-------|------|
| Spawn units | `obj_game_controller/Create_0.gml` | 43+ |
| Create warscrolls | `scr_helpers.gml` `load_sample_warscrolls()` | 224+ |
| Add factions | `scr_core_data.gml` enum | 15 |
| Unit colors | `obj_battlefield_renderer/Draw_0.gml` | 178 |
| Camera speed | `obj_game_controller/Step_0.gml` | 15 |
| Battlefield size | `scr_core_data.gml` | 40 |
| Objective positions | `scr_helpers.gml` `place_objectives()` | 283 |
| Deployment zones | `obj_battlefield_renderer/Draw_0.gml` | 56 |
| Unit sizes | `obj_battlefield_renderer/Draw_0.gml` | 171 |
| Combat rules | `scr_combat.gml` | entire file |

---

**Now you can fully customize your game!** 🎨⚔️

For more details, see:
- `README_GAMEMAKER.md` - Complete documentation
- `QUICKSTART_GAMEMAKER.md` - Tutorial
- `GAMEMAKER_IMPLEMENTATION_SUMMARY.md` - Technical details
