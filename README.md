# Warhammer Age of Sigmar - Game Management System

A comprehensive implementation of the Warhammer Age of Sigmar tabletop wargame system, based on the 4th Edition Core Rules.

## 🎮 Available in Two Versions! 🎨

### Python + Pygame Version
Play in **graphical mode** with a full visual battlefield, interactive unit selection, and real-time battle display!

### GameMaker Studio 2 Version (NEW!)
Complete **GameMaker implementation** with professional 2D graphics, WASD camera controls, and mouse-driven gameplay!

![Graphics Mode Available](https://img.shields.io/badge/Graphics-Pygame-blue)
![GameMaker](https://img.shields.io/badge/GameMaker-GML-orange)
![Python 3.7+](https://img.shields.io/badge/Python-3.7+-green)

## Overview

This project implements a fully functional digital version of Warhammer Age of Sigmar, including:

### Core Features
- **Army Building**: Create army rosters with regiments and heroes
- **Battle Management**: Complete battle sequence with all 7 phases
- **Combat Resolution**: Full attack sequence (hit, wound, save, damage)
- **Movement System**: Normal moves, running, retreating, and charging
- **Shooting Phase**: Ranged combat with weapon profiles
- **Objective Control**: Victory point scoring and objective control
- **Damage System**: Damage allocation, ward saves, and model removal

### Graphics Mode (Python + Pygame)
- **2D Visual Battlefield**: 44" × 60" battlefield with grid
- **Interactive Units**: Click to select, view stats in real-time
- **Range Indicators**: Visual movement and combat ranges
- **Objective Markers**: Animated control zones
- **Info Panel**: Live game state and unit details
- **60 FPS Rendering**: Smooth, responsive graphics

### GameMaker Version Features
- **Professional 2D Graphics**: Polished visual presentation
- **WASD Camera Controls**: Smooth camera movement and zoom
- **Mouse-Driven Gameplay**: Left-click select, right-click command
- **Box Selection**: Click and drag to select multiple units
- **Real-Time Combat**: Automatic combat resolution with visual feedback
- **Complete UI System**: Top bar, bottom panel, right controls
- **Hotkey System**: Quick access to all game functions
- **See**: `/AgeOfSigmarGM/` folder for complete GameMaker project

## System Requirements

### Python Version
- Python 3.7 or higher
- **Optional**: Pygame 2.5+ for graphics mode
  ```bash
  pip install pygame
  ```

### GameMaker Version
- GameMaker Studio 2 (version 2023.8 or later)
- Windows, Mac, or Linux
- **No additional dependencies!**
- Open `/AgeOfSigmarGM/AgeOfSigmarGM.yyp` in GameMaker and press F5 to play!

## File Structure

```
AgeOfSigmar/
├── PYTHON VERSION
│   ├── main.py                  # Main program and menu system
│   ├── data_types.py            # All data classes and enums
│   ├── game_state.py            # Global game state management
│   ├── utilities.py             # Utility functions (dice, distance, etc.)
│   ├── file_operations.py       # Loading/saving game data
│   ├── army_builder.py          # Army roster creation
│   ├── battlefield.py           # Battlefield setup and deployment
│   ├── movement.py              # Movement phase mechanics
│   ├── shooting.py              # Shooting phase
│   ├── combat.py                # Combat phase and attack resolution
│   ├── damage.py                # Damage allocation and model removal
│   ├── objectives.py            # Objective control and scoring
│   ├── battle.py                # Battle rounds and turn management
│   ├── graphics_engine.py       # 2D graphics rendering engine
│   ├── graphical_game.py        # Graphical game mode
│   ├── input_handler.py         # Mouse & keyboard input system
│   ├── ui_components.py         # UI buttons, panels, tooltips
│   ├── Warscrolls_StormcastEternals.txt  # Stormcast warscroll data
│   ├── Warscrolls_Skaven.txt    # Skaven warscroll data
│   ├── requirements.txt         # Python package dependencies
│   ├── README.md                # This file
│   ├── QUICKSTART.md            # Quick start guide
│   └── GRAPHICS_GUIDE.md        # Graphics mode guide
│
└── GAMEMAKER VERSION
    └── AgeOfSigmarGM/           # Complete GameMaker Studio 2 project
        ├── AgeOfSigmarGM.yyp    # GameMaker project file (OPEN THIS!)
        ├── scripts/             # GML scripts (4 core systems)
        │   ├── scr_core_data/   # Data structures & enums
        │   ├── scr_combat/      # Combat resolution
        │   ├── scr_movement/    # Movement mechanics
        │   └── scr_helpers/     # Utilities & setup
        ├── objects/             # GameMaker objects
        │   ├── obj_game_controller/      # Main game loop
        │   └── obj_battlefield_renderer/ # Visual rendering
        ├── rooms/               # Game rooms
        │   └── rm_battlefield/  # Main battlefield (1600×900)
        ├── README_GAMEMAKER.md  # Complete GameMaker documentation
        ├── QUICKSTART_GAMEMAKER.md       # Quick start tutorial
        └── GAMEMAKER_IMPLEMENTATION_SUMMARY.md  # Full summary
```

## How to Run

### Quick Start (Text Mode)

1. **Start the game:**
   ```bash
   python3 main.py
   ```

2. **Create armies for both players:**
   - Select option 1 or 2 from the main menu
   - Choose a faction
   - Add regiments (hero + up to 3 units each)
   - Pick your general

3. **Start a battle:**
   - Select option 4 for text mode
   - OR option 5 for graphics mode (requires pygame)
   - Follow the deployment process
   - Play through battle rounds

### Graphics Mode Setup

1. **Install Pygame:**
   ```bash
   pip install -r requirements.txt
   ```

   Or directly:
   ```bash
   pip install pygame
   ```

2. **Launch graphics mode:**
   - Start the game: `python3 main.py`
   - Create armies (options 1-2)
   - Select option 5: "Play Battle (Graphics Mode)" 🎨
   - OR option 6: "View Battlefield (Graphics)" 🖼️

3. **Graphics controls:**
   - **Left Click**: Select units
   - **Space**: Deselect
   - **ESC**: Exit
   - Follow text prompts for phase actions

For detailed graphics instructions, see [GRAPHICS_GUIDE.md](GRAPHICS_GUIDE.md)

## Game Features

### Army Building
- Regiment-based army construction
- Point limits and validation
- Multiple factions supported:
  - Stormcast Eternals
  - Skaven
  - (More can be added by creating warscroll files)

### Battle Phases

Each turn consists of 7 phases:
1. **Hero Phase** - Hero abilities (simplified)
2. **Movement Phase** - Move, run, or retreat units
3. **Shooting Phase** - Ranged attacks
4. **Charge Phase** - Charge into combat (2D6 roll)
5. **Combat Phase** - Melee attacks with pile-in
6. **End of Turn** - Objective control and victory points

### Combat System

Complete attack sequence:
- **Hit Rolls** - Roll to hit (unmodified 1 always fails, 6 is critical)
- **Wound Rolls** - Roll to wound (unmodified 1 always fails)
- **Save Rolls** - Opponent rolls saves (modified by Rend)
- **Damage** - Failed saves result in damage

### Damage Allocation
- Damage pooling
- Ward saves (if unit has Ward ability)
- Model removal when Health is exceeded
- Unit destruction tracking

### Objective Control
- Units within 3" of objectives contest them
- Control score = Control characteristic × model count
- Standard bearers add +1 to control
- Victory points awarded for controlled objectives

## Warscroll File Format

Warscrolls are stored in tab-delimited text files:

```
UnitName	Move	Health	Control	Save	UnitSize	Points	Keywords	Weapons	Abilities
```

**Weapon Format:**
```
WeaponName[Type,Attacks,Hit,Wound,Rend,Damage,Range]
```

Example:
```
Liberators	5	2	1	4	5	110	INFANTRY,BATTLELINE,ORDER,STORMCAST ETERNALS	Warhammer[MELEE,2,4,3,1,1,1]	Lay Low the Tyrants
```

## Adding New Factions

To add a new faction:

1. Create a file named `Warscrolls_FactionName.txt`
2. Add the header line
3. Add unit entries in tab-delimited format
4. The file will be automatically loaded on startup

## Game State Management

- **Save Game**: Option 7 - Saves current game state
- **Load Game**: Option 8 - Loads a saved game

Save files are stored as `.sav` files with timestamp.

## Implementation Details

### Based on Cambridge AS & A Level Computer Science 9618 Standards

This implementation demonstrates:
- ✓ User-defined data types (dataclasses)
- ✓ Enumerated types
- ✓ Complex data structures (arrays/lists)
- ✓ File operations (reading/writing)
- ✓ Procedures and functions
- ✓ Parameter passing (by value and reference)
- ✓ Record types
- ✓ Algorithm design
- ✓ Validation and error handling

### Core Rules Implemented

Based on Warhammer Age of Sigmar 4th Edition (April 2025):
- ✓ Regiment-based army construction
- ✓ Complete battle sequence
- ✓ Movement rules (normal, run, retreat, charge)
- ✓ Shooting and combat phases
- ✓ Attack sequence (hit, wound, save)
- ✓ Damage allocation
- ✓ Objective control system
- ✓ Victory point scoring
- ✓ Command points
- ✓ Underdog bonus

## Limitations and Future Enhancements

**Current Limitations:**
- Hero abilities are simplified
- Spells and prayers not fully implemented
- Terrain effects are basic
- Line of sight is simplified
- Battle tactics not implemented
- Enhancements/artefacts not fully implemented

**Potential Enhancements:**
- Add more factions
- Implement spell casting system
- Add battle tactics
- Implement grand strategies
- Add graphical battlefield display
- Network multiplayer support
- AI opponent

## Testing

To test the combat system:
1. Create two small armies (one unit each)
2. Deploy them close together
3. Use the movement phase to get into combat
4. Test the combat resolution

Sample test scenario:
- Player 1: Liberators (5 models)
- Player 2: Clanrats (20 models)
- Deploy within charge range
- Execute charge and combat

## Credits

**Game System**: Games Workshop - Warhammer Age of Sigmar 4th Edition
**Implementation**: Based on Cambridge International AS & A Level Computer Science 9618 pseudocode standards
**Author**: Implemented as educational demonstration of game systems programming

## License

This is an educational implementation for demonstrating programming concepts.
Warhammer Age of Sigmar is © Games Workshop Limited.
This project is not affiliated with or endorsed by Games Workshop.

## Support

For issues or questions:
- Check that all required files are present
- Verify Python version (3.7+)
- Check warscroll file format
- Review error messages for debugging information
