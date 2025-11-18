# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Start the Game
```bash
python3 main.py
```

### 2. Create Player 1 Army
```
Select option: 1
Enter points limit: 2000  (or press Enter for default)
Select Faction: 1  (Stormcast Eternals)
```

### 3. Add a Regiment
```
1. Add Regiment
Select option: 1
Select Hero: 1  (Lord-Imperatant)
Add unit to regiment? Y
Select unit: 1  (Liberators)
Add unit to regiment? N
```

### 4. Finish Army and Select General
```
3. Finish Roster
Select option: 3
Select general: 1
```

### 5. Create Player 2 Army
```
Select option: 2
(Repeat steps 2-4, but choose Faction: 2 for Skaven)
```

### 6. Start Battle!
```
Select option: 4
```

## Sample Warscrolls

### Stormcast Eternals
- **Lord-Imperatant** (180 pts) - Fast hero with good attacks
- **Liberators** (110 pts) - Basic battleline infantry
- **Vindictors** (130 pts) - Defensive infantry
- **Judicators** (180 pts) - Ranged infantry
- **Annihilators** (180 pts) - Elite shock troops

### Skaven
- **Grey Seer** (140 pts) - Wizard hero
- **Clanrats** (120 pts) - Cheap battleline horde
- **Stormvermin** (140 pts) - Elite infantry
- **Plague Monks** (160 pts) - Frenzied attackers
- **Warplock Jezzails** (110 pts) - Long-range snipers

## Battle Sequence Quick Reference

### Each Battle Round:
1. **Priority Roll** - Highest roll chooses who goes first
2. **Player 1 Turn**
   - Hero Phase
   - Movement Phase (move, run, or retreat)
   - Shooting Phase (ranged attacks)
   - Charge Phase (2D6" charge move)
   - Combat Phase (melee attacks)
   - End of Turn (control objectives, score VP)
3. **Player 2 Turn** (same phases)

### Movement Options:
- **Normal Move**: Move up to Move characteristic
- **Run**: Move + D6" (cannot charge this turn)
- **Retreat**: Move away from combat (take D3 mortal damage)
- **Charge**: Roll 2D6, move that distance toward enemy

### Combat Sequence:
1. **Pile In** - Move up to 3" toward enemy
2. **Hit Rolls** - Roll D6 per attack, need Hit value or higher
3. **Wound Rolls** - Roll D6 per hit, need Wound value or higher
4. **Save Rolls** - Defender rolls D6, need Save - Rend or higher
5. **Allocate Damage** - Failed saves cause damage

### Victory:
- Control objectives (within 3")
- Score 2 VP per objective controlled each turn
- Most VP at end of round 5 wins

## Tips for First Game

1. **Keep it simple**: Start with 1-2 units per side
2. **Deploy close**: Put units within charge range (12")
3. **Test combat**: Focus on learning the attack sequence
4. **Don't worry about abilities**: Core mechanics first
5. **Use the menu**: Browse warscrolls (option 5) to see stats

## Common Questions

**Q: How do I know if I'm in combat?**
A: If any enemy unit is within 3", you're in combat.

**Q: When can I shoot?**
A: Units with ranged weapons can shoot in your shooting phase.

**Q: What's a critical hit?**
A: An unmodified 6 on a hit roll (currently just noted, special effects not fully implemented).

**Q: How do I win?**
A: Control more objectives to score more victory points. Player with most VP after 5 rounds wins.

**Q: Can I save my game?**
A: Yes! Use option 7 from main menu.

## Example 500pt Armies

### Stormcast Eternals (500 pts)
- Lord-Imperatant (180 pts)
- Liberators (110 pts)
- Vindictors (130 pts)
- Prosecutors (100 pts)
Total: 520 pts (slightly over, adjust as needed)

### Skaven (500 pts)
- Grey Seer (140 pts)
- Clanrats x20 (120 pts)
- Stormvermin (140 pts)
- Warplock Jezzails (110 pts)
Total: 510 pts

## Troubleshooting

**Game won't start:**
- Check Python version: `python3 --version` (need 3.7+)
- Make sure all .py files are in the same directory
- Check warscroll files are present

**No units available:**
- Warscroll files must be in same directory as main.py
- Check file names match exactly: `Warscrolls_FactionName.txt`
- Files must be tab-delimited

**Combat not working:**
- Make sure units are within 3" of each other
- Units must have moved/charged into combat
- Check unit has melee weapons

## Next Steps

Once comfortable with basics:
1. Try larger armies (1000-2000 pts)
2. Experiment with different unit combinations
3. Learn unit abilities and special rules
4. Create custom warscrolls
5. Add new factions

Enjoy your battles in the Mortal Realms! ⚡🔨
