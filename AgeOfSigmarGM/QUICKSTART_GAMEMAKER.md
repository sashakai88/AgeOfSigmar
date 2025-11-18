# ⚡ QUICK START - GameMaker Edition

Get up and running with the Warhammer Age of Sigmar GameMaker implementation in minutes!

## 🚀 Installation (2 minutes)

### Step 1: Install GameMaker
1. Download [GameMaker Studio 2](https://gamemaker.io/en/download) (free version works!)
2. Install and create a free account
3. Launch GameMaker Studio 2

### Step 2: Open Project
1. In GameMaker, select `File → Open Project`
2. Navigate to: `/AgeOfSigmarGM/AgeOfSigmarGM.yyp`
3. Click `Open`

### Step 3: Run the Game
1. Press **F5** (or click the green Play button)
2. The battlefield window will open!

**That's it!** You're ready to play! 🎉

## 🎮 First Battle (5 minutes)

### Understanding the Screen

When you launch, you'll see:

```
┌─────────────────────────────────────────────────┐
│ Round: 1/5    Phase: Hero    VP: P1:0  P2:0   │  ← Top Bar
├─────────────────────────────────────────────────┤
│                                                 │
│        [Blue Unit]    [Objective 1]             │
│                                                 │
│              [Objective 2]                      │  ← Battlefield
│                                                 │
│        [Objective 3]    [Red Unit]              │
│                                                 │
├─────────────────────────────────────────────────┤
│ Selected: Liberators (5 models) Move:5" HP:2   │  ← Bottom Panel
└─────────────────────────────────────────────────┘
```

**Blue units** = Player 1 (your units)
**Red units** = Player 2 (enemy units)
**Gold circles** = Objectives (capture these!)

### Basic Controls (Try These Now!)

1. **Move Camera**: Press **W/A/S/D** to look around the battlefield
2. **Select Unit**: **Left-click** on a blue unit
   - You'll see a gold ring appear around it
   - Bottom panel shows unit stats
3. **Move Unit**: **Right-click** on empty ground
   - Unit moves to that position
4. **Attack Enemy**: **Right-click** on a red unit
   - Your unit will fight if in range
5. **Zoom**: Use **mouse wheel** to zoom in/out

### Your First Turn

Let's play through one turn:

#### Phase 1: Hero Phase
- *Currently simplified - press **N** to skip*

#### Phase 2: Movement Phase
1. **Left-click** your blue unit (Liberators)
2. **Right-click** near Objective 1
3. Watch it move! (max 5" movement)
4. Press **N** for next phase

#### Phase 3: Shooting Phase
- *No ranged weapons yet - press **N***

#### Phase 4: Charge Phase
- If enemy is 12" or less away:
  1. **Right-click** enemy unit
  2. Game rolls 2D6 for charge
  3. If successful, unit charges!
- Press **N** for next phase

#### Phase 5: Combat Phase
- If your unit is in combat (within 3"):
  1. **Right-click** enemy unit
  2. Watch combat resolution in console
  3. Damage is applied automatically
- Press **N** for next phase

#### Phase 6: End of Turn
- Objectives are scored
- Victory points awarded
- Press **N** to end your turn

**Enemy Turn**: Same phases for Player 2 (red units)

**After Both Players**: Round 1 complete! Repeat for 5 rounds.

### Winning the Game

**Goal**: Control objectives to score victory points!

- Get units within **3"** of gold objective circles
- At end of turn, you capture objectives where you have more Control
- Each captured objective = **2 Victory Points**
- After **5 rounds**, highest VP wins!

**Quick Win**: If you ever have 3× opponent's VP (and 20+ VP difference), you win immediately!

## 🎯 Essential Hotkeys

| Key | Action | When to Use |
|-----|--------|-------------|
| **WASD** | Move camera | Anytime - look around battlefield |
| **Left Click** | Select unit | Click blue units to command them |
| **Right Click** | Command | Click ground = move, enemy = attack |
| **Tab** | Next unit | Cycle through your units |
| **Space** | Deselect | Clear selection |
| **N** | Next phase | Advance to next game phase |
| **Mouse Wheel** | Zoom | Get closer/farther view |
| **ESC** | Pause | Pause the game |

## 📊 Reading Unit Stats

When you select a unit, the bottom panel shows:

```
Liberators (5 models) - Move:5" Health:2 Save:4+ Control:1
Weapons: Warhammer (2 attacks, 4+/3+/-1/1)
Status: ✓ Can Move  ✓ Can Fight
```

**What it means:**
- **Liberators** = Unit name
- **(5 models)** = 5 miniatures in the unit
- **Move:5"** = Can move up to 5 inches
- **Health:2** = Each model has 2 wounds
- **Save:4+** = Needs 4+ on D6 to save damage
- **Control:1** = Adds 1 to objective control
- **Warhammer** = Weapon name
  - **2 attacks** = Rolls 2 hit dice
  - **4+/3+** = Hits on 4+, Wounds on 3+
  - **-1** = -1 to enemy save (armor piercing)
  - **1** = 1 damage per successful attack

## 🎲 Combat Example

Let's say you attack an enemy unit:

```
Your Liberators attack enemy Clanrats:

1. HIT ROLL: Rolling 10 dice (5 models × 2 attacks)
   → Results: 6, 5, 4, 3, 2, 1
   → Need 4+ to hit
   → 3 hits! (6, 5, 4)

2. WOUND ROLL: Rolling 3 dice
   → Results: 6, 4, 2
   → Need 3+ to wound
   → 2 wounds! (6, 4)

3. SAVE ROLL (Enemy): Rolling 2 dice
   → Enemy save is 5+ (normal 5, minus -1 rend = 6+)
   → Results: 5, 3
   → 0 saves! (need 6+)

4. DAMAGE: 2 wounds × 1 damage = 2 damage
   → 2 Clanrats slain! (each has 1 health)
   → 18 Clanrats remaining
```

All of this happens automatically when you right-click an enemy!

## 🏆 Sample Warscrolls

### Liberators (Stormcast Eternals) - Your Units
```
Type: Infantry (Blue)
Move: 5"    Health: 2    Save: 4+    Control: 1
Unit Size: 5 models

Weapon: Warhammer (Melee, 1" range)
- Attacks: 2
- Hit: 4+
- Wound: 3+
- Rend: -1
- Damage: 1

Tactics:
- Tough defenders (2 health, 4+ save)
- Good at holding objectives (Control 1)
- Decent melee fighters
```

### Clanrats (Skaven) - Enemy Units
```
Type: Infantry (Red)
Move: 6"    Health: 1    Save: 5+    Control: 1
Unit Size: 20 models

Weapon: Rusty Blade (Melee, 1" range)
- Attacks: 1
- Hit: 4+
- Wound: 4+
- Rend: 0
- Damage: 1

Tactics:
- Fast movers (6" move)
- Weak individually (1 health, 5+ save)
- Strong in numbers (20 models = 20 attacks!)
```

## 💡 Pro Tips

### Tip 1: Capture Objectives Early
- Objectives score every turn
- Early capture = more total VP
- Send fast units (6" move) to objectives first

### Tip 2: Use Range Indicators
- When you select a unit, green circle = movement range
- Red circle = combat range (3")
- Plan moves using these circles!

### Tip 3: Concentrate Fire
- Don't spread attacks across multiple enemies
- Focus on destroying one unit at a time
- Dead units can't fight back!

### Tip 4: Box Select
- Click and drag to select multiple units
- Move groups together
- Faster than clicking each unit

### Tip 5: Watch the Console
- Press **~** to open console (may vary by OS)
- See combat rolls, movement, objectives
- Debug messages show what's happening

## 🔧 Customization

### Change Camera Speed
Open `obj_game_controller/Step_0.gml`, line ~15:
```gml
var _camera_speed = 8;  // Change this number (default: 8)
```

### Adjust Zoom Limits
Same file, line ~25:
```gml
global.camera_zoom = clamp(global.camera_zoom * 1.1, 0.5, 3.0);
//                                                    ^^^  ^^^
//                                              min zoom  max zoom
```

### Add More Units
Open `scr_helpers/scr_helpers.gml`, find `load_sample_warscrolls()`, add:
```gml
// Create 5 more Liberators for Player 1
var _unit = new BattlefieldUnit();
_unit.warscroll_ref = 0;  // 0 = Liberators
_unit.x_pos = 10;
_unit.y_pos = 50;
_unit.owner_player = 1;
_unit.model_count = 5;
ds_list_add(global.battlefield_units, _unit);
```

## 🐛 Troubleshooting

### Problem: "Nothing happens when I click Run"
**Solution**: Check the Output window at bottom of GameMaker for errors

### Problem: "Units aren't moving"
**Solution**:
1. Make sure unit is selected (gold ring visible)
2. Check if unit has already moved this turn (status in bottom panel)
3. Verify you're in Movement phase (top bar shows current phase)

### Problem: "Can't see the whole battlefield"
**Solution**: Use WASD to pan camera, or zoom out with mouse wheel

### Problem: "Combat damage seems wrong"
**Solution**: Open console (~) and check debug messages - all rolls are logged

### Problem: "Game is too fast/slow"
**Solution**: This is turn-based! Use **N** key to control pacing

## 📚 Next Steps

### Learn More
- Read full **README_GAMEMAKER.md** for complete documentation
- Check `scr_combat.gml` to understand combat resolution
- Look at `scr_helpers.gml` to see how warscrolls work

### Modify the Game
- Add new factions (edit enums in `scr_core_data.gml`)
- Create custom warscrolls (copy patterns in `load_sample_warscrolls()`)
- Design new abilities (add functions in `scr_helpers.gml`)
- Customize visuals (change colors in `obj_battlefield_renderer/Draw_0.gml`)

### Advanced Features
- Implement ability system (use number keys 1-5)
- Add terrain effects (forests, ruins, hills)
- Create army builder UI
- Add save/load functionality
- Implement AI for solo play

## 🎓 Learning GML

If you're new to GameMaker Language:

**Key Concepts:**
```gml
// Variables
var my_variable = 10;

// Functions
function my_function(_parameter) {
    return _parameter * 2;
}

// Constructors (like classes)
function MyObject() constructor {
    x = 0;
    y = 0;
}

// Data Structures
var my_list = ds_list_create();
ds_list_add(my_list, "item");

// Loops
for (var i = 0; i < 10; i++) {
    // Do something
}

// Conditionals
if (condition) {
    // Do something
} else {
    // Do something else
}
```

**Resources:**
- [GameMaker Manual](https://manual.yoyogames.com/)
- [GML Overview](https://manual.yoyogames.com/GameMaker_Language/GameMaker_Language_Index.htm)
- [YoYo Games Tutorials](https://www.youtube.com/c/yoyogames)

## 🎮 Have Fun!

You now know enough to play a full battle! Remember:

1. **Move** units with right-click
2. **Attack** enemies within 3"
3. **Capture** objectives (gold circles)
4. **Score** 2 VP per objective
5. **Win** after 5 rounds!

*For the glory of Sigmar! ⚔️*

---

**Need Help?**
- Check the console for debug messages (~)
- Read README_GAMEMAKER.md for detailed docs
- Look at the GML scripts to see how everything works

**Version**: 1.0.0
**Last Updated**: 2025-11-18
