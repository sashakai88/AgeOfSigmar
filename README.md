# Warhammer Age of Sigmar - Game Management System

A comprehensive Python implementation of the Warhammer Age of Sigmar tabletop wargame system, based on the 4th Edition Core Rules.

## Overview

This project implements a fully functional digital version of Warhammer Age of Sigmar, including:

- **Army Building**: Create army rosters with regiments and heroes
- **Battle Management**: Complete battle sequence with all 7 phases
- **Combat Resolution**: Full attack sequence (hit, wound, save, damage)
- **Movement System**: Normal moves, running, retreating, and charging
- **Shooting Phase**: Ranged combat with weapon profiles
- **Objective Control**: Victory point scoring and objective control
- **Damage System**: Damage allocation, ward saves, and model removal

## System Requirements

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

## File Structure

```
AgeOfSigmar/
├── main.py                  # Main program and menu system
├── data_types.py            # All data classes and enums
├── game_state.py            # Global game state management
├── utilities.py             # Utility functions (dice, distance, etc.)
├── file_operations.py       # Loading/saving game data
├── army_builder.py          # Army roster creation
├── battlefield.py           # Battlefield setup and deployment
├── movement.py              # Movement phase mechanics
├── shooting.py              # Shooting phase
├── combat.py                # Combat phase and attack resolution
├── damage.py                # Damage allocation and model removal
├── objectives.py            # Objective control and scoring
├── battle.py                # Battle rounds and turn management
├── Warscrolls_StormcastEternals.txt  # Stormcast warscroll data
├── Warscrolls_Skaven.txt    # Skaven warscroll data
└── README.md                # This file
```

## How to Run

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
   - Select option 4 from the main menu
   - Follow the deployment process
   - Play through battle rounds

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
