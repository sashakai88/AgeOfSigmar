# Graphics Mode Guide

## 🎨 2D Graphics System

The Warhammer Age of Sigmar simulator now includes a comprehensive 2D graphics mode powered by Pygame!

## Installation

### Install Pygame

```bash
pip install pygame
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## Features

### Visual Battlefield
- **44" × 60" battlefield** with grid overlay (6" spacing)
- **Deployment zones** clearly marked
- **Objective markers** with control circles
- **Terrain features** visually represented
- **Smooth rendering** at 60 FPS

### Unit Visualization
- **Color-coded units** (Blue = Player 1, Red = Player 2)
- **Size-based sprites** (Monsters larger than Infantry)
- **Model count display** on each unit
- **Health bars** showing unit status
- **Combat indicators** for units in melee
- **Unit names** displayed below sprites

### Interactive Features
- **Click to select** units
- **Hover highlighting** for units under cursor
- **Range indicators** showing movement/combat ranges
- **Info panel** with complete game state
- **Real-time updates** during gameplay

### Information Display
- **Game state panel** showing:
  - Current round and phase
  - Active player
  - Victory points for both players
  - Command points
- **Selected unit details**:
  - Unit name and stats
  - Current model count
  - Movement and combat status
  - Available actions

## How to Use

### 1. Battlefield Viewer

View the current game state visually:

```
Main Menu > 6. View Battlefield (Graphics)
```

**Controls:**
- **Left Click**: Select unit to view stats
- **Space**: Deselect unit
- **ESC**: Exit viewer

### 2. Graphical Battle Mode

Play a full battle with visual display:

```
Main Menu > 5. Play Battle (Graphics Mode)
```

This mode combines:
- **Visual battlefield** showing all units and objectives
- **Real-time updates** as units move and fight
- **Text-based commands** for phase execution
- **Interactive unit selection** by clicking

**Controls:**
- **Left Click**: Select units during phases
- **Space**: Deselect current unit
- **ESC**: Exit battle (confirmation required)

### 3. Workflow

1. **Create armies** (options 1-2) in text mode
2. **Start graphical battle** (option 5)
3. **View battlefield** with all units deployed
4. **Follow text prompts** for each phase
5. **Watch units move** and combat results visually
6. **Track scores** in the info panel

## Visual Elements

### Color Scheme

| Element | Color |
|---------|-------|
| Battlefield | Dark Gray |
| Grid Lines | Light Gray |
| Player 1 Units | Blue |
| Player 2 Units | Red |
| Objectives | Gold |
| Terrain | Green |
| Selected Unit | Gold Ring |
| Hover Highlight | White Ring |
| Health Bar | Green |
| Combat Indicator | Red Dot |

### Unit Sizes

- **Monsters**: 25px radius
- **Cavalry**: 18px radius
- **Infantry**: 15px radius
- **War Machines**: 15px radius

### Range Indicators

When a unit is selected:
- **Green circle**: Movement range (if not moved)
- **Red circle**: Combat range (if in combat, 3")
- **Yellow circle**: Charge range (varies by roll)

### Objective Markers

- **Gold circle**: Objective position
- **Light circle**: 3" control radius
- **Colored ring**: Controlled by Player 1 (blue) or 2 (red)
- **Number**: Objective ID

### Info Panel (Right Side)

Shows real-time game information:

```
┌─────────────────────────┐
│      Game Info          │
├─────────────────────────┤
│ Round: 3/5              │
│ Phase: Combat           │
│ Active: Player 1        │
│                         │
│ Victory Points:         │
│   Player 1: 12          │
│   Player 2: 8           │
│                         │
│ Command Points:         │
│   Player 1: 4           │
│   Player 2: 4           │
│                         │
│ ─────────────────────   │
│ Selected Unit:          │
│ Liberators              │
│   Move: 5"              │
│   Health: 2             │
│   Save: 4+              │
│   Control: 1            │
│   Models: 5/5           │
│                         │
│ Status:                 │
│   • Moved               │
│   • In Combat           │
└─────────────────────────┘
```

## Graphics Engine Details

### Architecture

```
graphics_engine.py
├── GraphicsEngine (main class)
│   ├── world_to_screen() - coordinate conversion
│   ├── screen_to_world() - reverse conversion
│   ├── draw_battlefield() - grid and zones
│   ├── draw_units() - all unit sprites
│   ├── draw_objectives() - objective markers
│   ├── draw_terrain() - terrain features
│   ├── draw_info_panel() - UI panel
│   ├── handle_events() - mouse/keyboard
│   └── render() - main render loop
│
graphical_game.py
├── play_graphical_battle_interactive()
│   └── Combines graphics with game logic
│
main.py
└── Menu integration
```

### Coordinate System

- **World Coordinates**: Inches (0-44 x 0-60)
- **Screen Coordinates**: Pixels (1400 x 900)
- **Scale Factor**: ~20 pixels per inch

Conversion functions handle transformation automatically.

### Performance

- **60 FPS** target frame rate
- **Efficient rendering** with dirty rect optimization
- **Event-driven updates** minimize CPU usage
- **Smooth animations** for phase transitions

## Customization

### Colors

Edit `graphics_engine.py` to customize colors:

```python
COLOR_PLAYER1 = (52, 152, 219)  # Blue
COLOR_PLAYER2 = (231, 76, 60)   # Red
COLOR_OBJECTIVE = (241, 196, 15) # Gold
# etc.
```

### Unit Sizes

Modify sprite sizes in `draw_unit()`:

```python
if warscroll.unit_type == UnitType.MONSTER:
    radius = 25  # Change this
```

### Screen Resolution

Adjust in `graphics_engine.py`:

```python
SCREEN_WIDTH = 1400   # Change as needed
SCREEN_HEIGHT = 900   # Change as needed
```

## Troubleshooting

### Pygame Not Found

```
Error: pygame not installed
```

**Solution:**
```bash
pip install pygame
```

### Display Issues

**Problem**: Window doesn't appear or is black

**Solutions:**
- Check GPU drivers are up to date
- Try running with software rendering:
  ```bash
  SDL_VIDEODRIVER=x11 python3 main.py
  ```
- Ensure display is configured correctly

### Performance Issues

**Problem**: Low frame rate or stuttering

**Solutions:**
- Close other applications
- Reduce window size in settings
- Check system resources
- Update graphics drivers

### Mouse Not Working

**Problem**: Can't select units

**Solutions:**
- Ensure window has focus
- Check mouse cursor is visible
- Try clicking directly on unit circles
- Verify battlefield coordinates are correct

## Future Enhancements

Potential additions:
- [ ] Animation effects for combat
- [ ] Particle effects for spells
- [ ] Movement trails
- [ ] Attack trajectory visualization
- [ ] Dice roll animations
- [ ] Sound effects
- [ ] Background music
- [ ] Custom unit sprites
- [ ] Zoom and pan controls
- [ ] Minimap
- [ ] Replay system
- [ ] Screenshot capability

## Examples

### Selecting a Unit

1. Move mouse over a unit (circle)
2. Unit highlights with white ring
3. Left click to select
4. Info panel shows unit details
5. Range indicators appear

### Viewing Combat

1. Units in combat show red dots
2. Select attacking unit
3. Red circle shows 3" combat range
4. Watch health bars decrease
5. Units disappear when destroyed

### Tracking Objectives

1. Gold circles mark objectives
2. Light circles show 3" control range
3. Colored rings show current controller
4. Info panel shows victory points
5. Control changes animate in real-time

## Tips for Best Experience

1. **Use fullscreen** if possible for immersion
2. **Click units** to see their full stats
3. **Watch the info panel** for turn progression
4. **Follow text prompts** while viewing graphics
5. **Use Space** to quickly deselect
6. **Take your time** - graphics update in real-time

## Comparison: Text vs Graphics Mode

| Feature | Text Mode | Graphics Mode |
|---------|-----------|---------------|
| Setup | Fast | Slower (loading) |
| Visualization | Coordinates only | Full 2D battlefield |
| Unit Info | Text stats | Visual + stats |
| Interaction | Keyboard only | Mouse + keyboard |
| Immersion | Low | High |
| Performance | Minimal CPU | Moderate GPU/CPU |
| Accessibility | High | Requires display |

Both modes share the same game logic and rules - choose based on preference!

---

Enjoy the enhanced visual experience! ⚔️🎨
