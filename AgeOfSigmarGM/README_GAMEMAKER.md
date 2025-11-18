# 🎮 WARHAMMER AGE OF SIGMAR - GameMaker Edition

Complete GameMaker Studio 2 implementation of the Warhammer Age of Sigmar tabletop game system.

## 📋 Overview

This is a fully functional digital recreation of the Warhammer Age of Sigmar 4th Edition rules, built entirely in GameMaker Studio 2 using GML (GameMaker Language). It features complete combat resolution, movement mechanics, objective control, and victory point scoring.

## 🎯 Features

### Core Game Systems
- ✅ **Complete Combat Resolution** - Hit/Wound/Save sequences with critical hits
- ✅ **Movement System** - Normal movement, running, retreating, and charging
- ✅ **Objective Control** - Capture objectives with Control characteristic
- ✅ **Victory Points** - Automatic scoring based on objective control
- ✅ **Turn Structure** - 7 phases per turn (Hero, Movement, Shooting, Charge, Combat, End of Turn)
- ✅ **Battle Rounds** - Standard 5-round games with automatic winner determination

### Visual Features
- ✅ **2D Battlefield** - 44" × 60" game area with 6" grid
- ✅ **Unit Rendering** - Color-coded units with health bars and model counts
- ✅ **Objective Markers** - Visual objective markers with 3" control zones
- ✅ **Deployment Zones** - Marked 9" deployment zones for both players
- ✅ **Range Indicators** - Movement and combat range visualization
- ✅ **Terrain Features** - Destructible and impassable terrain support

### Interactive Controls
- ✅ **WASD Camera** - Smooth camera movement across battlefield
- ✅ **Mouse Selection** - Left-click to select units
- ✅ **Box Selection** - Click and drag to select multiple units
- ✅ **Right-Click Commands** - Move or attack based on target
- ✅ **Hotkeys** - Quick access to all game functions
- ✅ **Zoom** - Mouse wheel zoom (0.5x - 3.0x)

### UI System
- ✅ **Top Bar** - Round counter, phase, victory points, command points
- ✅ **Bottom Panel** - Selected unit stats and ability buttons
- ✅ **Right Panel** - Controls reference and game info
- ✅ **Selection Feedback** - Visual indicators for selected/hovered units

## 🎮 Controls

### Camera
| Key | Action |
|-----|--------|
| W | Move camera up |
| A | Move camera left |
| S | Move camera down |
| D | Move camera right |
| Q | Rotate camera left (reserved) |
| E | Rotate camera right (reserved) |
| Mouse Wheel | Zoom in/out |

### Unit Selection
| Input | Action |
|-------|--------|
| Left Click | Select single unit |
| Click + Drag | Box select multiple units |
| Shift + Click | Add unit to selection |
| Tab | Cycle through friendly units |
| Space | Deselect all |

### Unit Commands
| Input | Action |
|-------|--------|
| Right Click Ground | Move selected units |
| Right Click Enemy | Attack with selected units |
| R | Retreat selected units |
| F | Fight with selected units |

### Abilities
| Key | Action |
|-----|--------|
| 1 | Use ability 1 |
| 2 | Use ability 2 |
| 3 | Use ability 3 |
| 4 | Use ability 4 |
| 5 | Use ability 5 |

### Game Flow
| Key | Action |
|-----|--------|
| N | Next phase |
| ESC | Pause/Menu |

## 📁 Project Structure

```
AgeOfSigmarGM/
├── scripts/
│   ├── scr_core_data/           # Enums, data structures, coordinate functions
│   │   └── scr_core_data.gml
│   ├── scr_combat/              # Complete combat resolution system
│   │   └── scr_combat.gml
│   ├── scr_movement/            # Movement, retreat, charge mechanics
│   │   └── scr_movement.gml
│   └── scr_helpers/             # Utility functions, warscrolls, objectives
│       └── scr_helpers.gml
├── objects/
│   ├── obj_game_controller/     # Main game loop and input handling
│   │   ├── Create_0.gml         # Initialize game state
│   │   ├── Step_0.gml           # Process input and update game
│   │   └── Draw_64.gml          # Render GUI overlay
│   └── obj_battlefield_renderer/# Battlefield visualization
│       ├── Create_0.gml         # Initialize renderer
│       └── Draw_0.gml           # Render battlefield, units, objectives
├── rooms/
│   └── rm_battlefield/          # Main battlefield room (1600×900)
│       └── rm_battlefield.yy
└── AgeOfSigmarGM.yyp            # GameMaker project file
```

## 🔧 Installation

### Requirements
- **GameMaker Studio 2** (version 2023.8 or later)
- **Windows/Mac/Linux** - Cross-platform compatible

### Setup
1. Open GameMaker Studio 2
2. Select `File → Open Project`
3. Navigate to `/AgeOfSigmarGM/AgeOfSigmarGM.yyp`
4. Click `Run` (F5) to start the game

## 🎲 Game Mechanics

### Combat Resolution
```gml
1. Hit Roll:  Roll ≥ Hit characteristic (1 always fails, 6 always hits)
2. Wound Roll: Roll ≥ Wound characteristic
3. Save Roll:  Defender rolls ≥ Save - Rend
4. Damage:     Allocate damage to models
```

### Movement
- **Normal Move**: Up to Move characteristic in inches
- **Run**: Move + D6 inches (cannot charge/shoot)
- **Retreat**: Move + D6 inches away from combat (cannot charge/shoot)
- **Charge**: Roll 2D6, move up to that distance toward enemy

### Objective Control
- Units within 3" of objective contribute Control characteristic
- Player with highest total Control captures the objective
- Captured objectives award 2 VP at end of each turn

### Victory Conditions
- **5 Battle Rounds**: Game ends after round 5
- **Victory Points**: Player with most VP wins
- **Automatic Victory**: If one player has 3× opponent's VP (minimum 20 VP difference)

## 🗂️ Data Structures

### UnitWarscroll (Constructor)
```gml
function UnitWarscroll() constructor {
    unit_id = 0;
    unit_name = "";
    faction = FactionType.Other;
    unit_type = UnitType.Infantry;

    // Characteristics
    move = 0;          // Movement in inches
    health = 0;        // Wounds per model
    control = 0;       // Objective control value
    save = 0;          // Save characteristic (3+ = 3)

    // Weapons array
    weapons = [];

    // Abilities array
    abilities = [];

    // Regiment options
    unit_size = 1;     // Models per unit
    points_cost = 0;   // Points value
}
```

### BattlefieldUnit (Constructor)
```gml
function BattlefieldUnit() constructor {
    warscroll_ref = 0;     // Index into global.warscrolls
    x_pos = 0.0;           // X position (inches)
    y_pos = 0.0;           // Y position (inches)

    owner_player = 1;      // 1 or 2
    model_count = 0;       // Current models alive

    // Status flags
    has_moved = false;
    has_run = false;
    has_retreated = false;
    has_charged = false;
    has_fought = false;
    is_in_combat = false;

    // Model array for damage tracking
    models = [];
}
```

## 🎨 Visual System

### Coordinate Conversion
The game uses a dual coordinate system:
- **World Coordinates**: Game positions in inches (0-60" × 0-44")
- **Screen Coordinates**: Pixel positions for rendering

```gml
function world_to_screen(_world_x, _world_y) {
    var _screen_x = (_world_x * global.scale - global.camera_x) * global.camera_zoom;
    var _screen_y = (_world_y * global.scale - global.camera_y) * global.camera_zoom;
    return [_screen_x, _screen_y];
}

function screen_to_world(_screen_x, _screen_y) {
    var _world_x = (_screen_x / global.camera_zoom + global.camera_x) / global.scale;
    var _world_y = (_screen_y / global.camera_zoom + global.camera_y) / global.scale;
    return [_world_x, _world_y];
}
```

### Unit Rendering
- **Infantry**: 15px radius circles
- **Cavalry**: 18px radius circles
- **Monsters**: 25px radius circles
- **Player 1**: Blue units
- **Player 2**: Red units
- **Selected**: Gold ring highlight
- **Health Bar**: Green bar above unit
- **Model Count**: White number in center

## 📜 Sample Warscrolls

### Liberators (Stormcast Eternals)
```
Move: 5"    Health: 2    Save: 4+    Control: 1
Unit Size: 5    Points: 110

Weapons:
- Warhammer (Melee): 2 attacks, 4+ hit, 3+ wound, -1 rend, 1 damage, 1" range
```

### Clanrats (Skaven)
```
Move: 6"    Health: 1    Save: 5+    Control: 1
Unit Size: 20    Points: 120

Weapons:
- Rusty Blade (Melee): 1 attack, 4+ hit, 4+ wound, 0 rend, 1 damage, 1" range
```

## 🚀 Extending the Game

### Adding New Warscrolls
Edit `scr_helpers.gml` and add to `load_sample_warscrolls()`:

```gml
var _new_unit = new UnitWarscroll();
_new_unit.unit_id = 2;
_new_unit.unit_name = "Your Unit Name";
_new_unit.faction = FactionType.YourFaction;
_new_unit.move = 6;
_new_unit.health = 2;
_new_unit.control = 1;
_new_unit.save = 4;

var _weapon = new WeaponProfile();
_weapon.weapon_name = "Weapon Name";
_weapon.attacks = 2;
_weapon.hit = 3;
_weapon.wound = 3;
_weapon.rend = 1;
_weapon.damage = 1;
_weapon.range = 1;

_new_unit.weapons = [_weapon];
ds_list_add(global.warscrolls, _new_unit);
```

### Adding Abilities
Create ability functions in `scr_helpers.gml`:

```gml
function ability_lightning_strike(_caster_unit) {
    show_debug_message("Lightning Strike activated!");
    // Ability logic here
}
```

### Custom Terrain
Add terrain in `Create_0.gml`:

```gml
var _forest = new TerrainFeature();
_forest.terrain_name = "Haunted Forest";
_forest.x_pos = 22;
_forest.y_pos = 22;
_forest.radius = 6;
_forest.blocks_line_of_sight = true;
ds_list_add(global.terrain_features, _forest);
```

## 🐛 Debugging

### Debug Messages
All major game events output to the console:
```
Helper functions loaded
Loaded 2 warscrolls
Placed 4 objectives
Selected next unit
=== END OF TURN ===
```

### Debug Overlay
Press F3 in GameMaker to show:
- FPS counter
- Instance count
- Memory usage
- Mouse coordinates

### Common Issues

**Units not appearing:**
- Check `global.battlefield_units` list
- Verify warscroll_ref is valid index
- Ensure model_count > 0

**Camera not moving:**
- Check camera bounds in Step event
- Verify global.camera_x/y are updating
- Test with debug overlay enabled

**Combat not resolving:**
- Check is_in_combat flags
- Verify target is within 3"
- Ensure has_fought is false

## 📚 GML Reference

### Global Variables
```gml
global.battlefield_width = 44      // Battlefield width (inches)
global.battlefield_height = 60     // Battlefield height (inches)
global.scale = 20                  // Pixels per inch
global.combat_range = 3            // Combat engagement range (inches)

global.camera_x                    // Camera X position
global.camera_y                    // Camera Y position
global.camera_zoom = 1.0           // Zoom level (0.5 - 3.0)

global.current_round               // Current battle round (1-5)
global.current_phase               // Current game phase (enum)
global.active_player               // Active player (1 or 2)

global.player1_points              // Player 1 victory points
global.player2_points              // Player 2 victory points
global.player1_command_points      // Player 1 command points
global.player2_command_points      // Player 2 command points

global.warscrolls                  // ds_list of UnitWarscroll
global.battlefield_units           // ds_list of BattlefieldUnit
global.selected_units              // ds_list of selected units
global.objectives                  // ds_list of ObjectiveMarker
global.terrain_features            // ds_list of TerrainFeature
```

### Key Functions
```gml
// Distance calculation
distance_2d(_x1, _y1, _x2, _y2)

// Dice rolling
roll_d6()
roll_2d6()
roll_d3()

// Combat
make_hit_roll(_hit_characteristic)
make_wound_roll(_wound_characteristic)
make_save_roll(_save_characteristic, _rend)
resolve_weapon_attacks(_attacker, _target, _weapon)
allocate_damage(_unit, _damage_points)

// Movement
execute_normal_move(_unit, _target_x, _target_y)
execute_run(_unit, _target_x, _target_y)
execute_retreat(_unit, _target_x, _target_y)
execute_charge(_unit, _target_x, _target_y)

// Game flow
advance_to_next_phase()
end_current_turn()
determine_objective_control()
score_victory_points()
determine_winner()
```

## 🎓 Learning Resources

### GML Basics
- [GameMaker Manual](https://manual.yoyogames.com/)
- [GML Reference](https://manual.yoyogames.com/GameMaker_Language/GameMaker_Language_Index.htm)
- [Constructors Guide](https://manual.yoyogames.com/GameMaker_Language/GML_Overview/Structs.htm)

### Warhammer Age of Sigmar Rules
- [Core Rules (PDF)](https://www.warhammer-community.com/aos-core-rules/)
- [Warscroll Builder](https://www.warhammer.com/en-GB/aos)

## 🔮 Future Enhancements

Potential additions:
- [ ] Army builder UI
- [ ] Save/load game state
- [ ] Multiplayer support (local/online)
- [ ] Animation effects for attacks
- [ ] Sound effects and music
- [ ] Custom unit sprites
- [ ] Faction-specific abilities
- [ ] Battle reports and statistics
- [ ] Tournament mode
- [ ] AI opponents
- [ ] Minimap
- [ ] Replay system
- [ ] Custom scenarios
- [ ] Spell effects visualization
- [ ] Unit facing/rotation
- [ ] Morale system

## 📄 License

This is a fan-made project for educational purposes. Warhammer Age of Sigmar is a trademark of Games Workshop Ltd.

## 🙏 Credits

- **Game Design**: Games Workshop
- **Implementation**: GameMaker Studio 2 (GML)
- **Based on**: Warhammer Age of Sigmar 4th Edition rules

---

**Version**: 1.0.0
**Last Updated**: 2025-11-18
**GameMaker Version**: 2023.8+

*For the glory of Sigmar!* ⚔️
