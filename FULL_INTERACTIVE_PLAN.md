# Full Interactive Control System - Implementation Plan

## Overview

This document outlines the complete transformation to a fully interactive, point-and-click control system with NO text prompts.

## Current Status

✅ **Completed**:
- Basic input handler (mouse and keyboard states)
- UI components (buttons, panels, context menus, tooltips)
- Graphics engine with basic rendering

## Required Implementation

### 1. Interactive Graphics Engine (`graphics_engine.py`)

**Major Updates Needed**:
- ✅ Integrate `InputManager` for all input handling
- ✅ Integrate `UIManager` for all UI rendering
- ✅ Add camera controls (WASD movement, Q/E rotation, scroll zoom)
- ✅ Add unit selection modes:
  - Left-click: Select single unit
  - Shift-click: Add/remove from selection
  - Drag: Box selection
- ✅ Add right-click commands:
  - On ground: Move selected units
  - On enemy: Attack with selected units
  - On empty: Show context menu
- ✅ Add phase progression UI buttons
- ✅ Add ability hotbar (1-5 keys)
- ✅ Add targeting mode for abilities
- ✅ Add visual feedback (selection rings, range circles)

**New Features**:
```python
class InteractiveGraphicsEngine(GraphicsEngine):
    def __init__(self):
        super().__init__()
        self.input = InputManager()
        self.ui = UIManager(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Selection
        self.selected_units = []

        # Game state
        self.current_phase_index = 0
        self.phases = ["Hero", "Movement", "Shooting", "Charge", "Combat", "End Turn"]

        # UI panels
        self.create_ui()

    def create_ui(self):
        """Create all UI panels and buttons"""
        # Top bar (phase buttons)
        # Bottom bar (unit info + abilities)
        # Right panel (army roster)
        # Phase progression button

    def handle_input(self):
        """Process all input"""
        # Keyboard: WASD camera, hotkeys
        # Mouse: selection, commands, UI clicks

    def handle_left_click(self, world_x, world_y):
        """Handle left click on battlefield"""
        if self.input.keyboard.shift:
            self.add_to_selection(world_x, world_y)
        else:
            self.select_unit_at(world_x, world_y)

    def handle_right_click(self, world_x, world_y):
        """Handle right click - issue command"""
        if self.selected_units:
            target_unit = self.get_unit_at(world_x, world_y)
            if target_unit and target_unit.owner != current_player:
                self.issue_attack_command(target_unit)
            else:
                self.issue_move_command(world_x, world_y)
        else:
            self.show_context_menu()

    def advance_phase(self):
        """Move to next phase"""
        self.current_phase_index += 1
        if self.current_phase_index >= len(self.phases):
            self.end_turn()
        else:
            self.enter_phase(self.phases[self.current_phase_index])
```

### 2. Interactive Game Mode (`interactive_game.py` - NEW FILE)

**Replaces**: `graphical_game.py`

**Features**:
- Full battle without ANY text prompts
- All actions via mouse/keyboard
- Phase progression via UI button clicks
- Real-time unit commands
- Visual feedback for all actions

**Flow**:
1. Game starts in deployment phase
2. Players click to place units (no text input)
3. Click "Start Battle" button
4. Each phase has automatic progression when all actions done OR player clicks "Next Phase"
5. Right-click units to move/attack
6. Use 1-5 keys or click abilities
7. Everything visual

### 3. Camera System

**WASD Controls**:
```python
def process_camera_movement(self, dt):
    move_speed = 10.0 * dt
    if self.input.keyboard.shift:
        move_speed *= 2

    if self.input.keyboard.is_down(KEY_W):
        self.camera_y += move_speed
    if self.input.keyboard.is_down(KEY_S):
        self.camera_y -= move_speed
    if self.input.keyboard.is_down(KEY_A):
        self.camera_x -= move_speed
    if self.input.keyboard.is_down(KEY_D):
        self.camera_x += move_speed

    if self.input.keyboard.is_down(KEY_Q):
        self.camera_rotation -= 1.0
    if self.input.keyboard.is_down(KEY_E):
        self.camera_rotation += 1.0

    # Scroll wheel zoom
    self.camera_zoom += self.input.mouse.scroll_delta * 2.0
    self.camera_zoom = max(5, min(100, self.camera_zoom))
```

### 4. Unit Selection System

**Multiple Selection Modes**:
```python
def handle_box_selection(self, start_x, start_y, end_x, end_y):
    """Select all units in rectangle"""
    rect = get_screen_rect(start_x, start_y, end_x, end_y)

    self.selected_units.clear()
    for unit in self.battlefield_units:
        if unit.owner == current_player:
            screen_pos = self.world_to_screen(unit.x, unit.y)
            if rect.collidepoint(screen_pos):
                self.selected_units.append(unit)

    self.update_selection_ui()

def add_to_selection(self, world_x, world_y):
    """Add unit to selection (Shift+Click)"""
    unit = self.get_unit_at(world_x, world_y)
    if unit and unit.owner == current_player:
        if unit in self.selected_units:
            self.selected_units.remove(unit)
        else:
            self.selected_units.append(unit)
        self.update_selection_ui()
```

### 5. Context Menu System

**Right-Click Options**:
```python
def show_unit_context_menu(self, unit, x, y):
    """Show context menu for unit"""
    options = []

    if unit.owner == current_player:
        options.append(("Move", lambda: self.begin_move_command(unit)))
        options.append(("Charge", lambda: self.begin_charge_command(unit)))
        if unit.is_in_combat:
            options.append(("Retreat", lambda: self.execute_retreat(unit)))
        options.append(("Fight", lambda: self.execute_fight(unit)))
        options.append(("View Warscroll", lambda: self.show_warscroll(unit)))
    else:
        options.append(("Target", lambda: self.set_attack_target(unit)))
        options.append(("View Warscroll", lambda: self.show_warscroll(unit)))

    options.append(("Cancel", None))

    self.ui.show_context_menu(x, y, options)
```

### 6. Ability System

**Hotkey Usage**:
```python
def use_ability(self, slot_number):
    """Use ability in slot (1-5 keys)"""
    if not self.selected_units:
        return

    unit = self.selected_units[0]
    ability = unit.get_ability(slot_number)

    if ability.requires_target:
        self.input.begin_targeting(ability.name)
        self.show_targeting_indicator(ability.range)
    else:
        self.execute_ability(unit, ability)
```

### 7. Visual Feedback

**Range Indicators**:
- Green circle: Movement range
- Yellow circle: Charge range (2D6)
- Red circle: Combat range (3")
- Blue circle: Ability range

**Unit States**:
- Gold ring: Selected
- White ring: Hovered
- Red dot: In combat
- Green checkmark: Action completed
- Gray overlay: No actions remaining

### 8. Phase System

**UI-Driven Progression**:
```python
def create_phase_ui(self):
    """Create phase control panel"""
    panel = UIPanel(50, 10, 800, 60, "")

    x = 60
    for phase_name in self.phases:
        button = UIButton(
            x, 20, 120, 40, phase_name,
            lambda p=phase_name: self.go_to_phase(p)
        )
        panel.add_button(button)
        x += 130

    # Next Phase button
    next_btn = UIButton(
        x, 20, 150, 40, "Next Phase >>>",
        self.advance_phase
    )
    panel.add_button(next_btn)

    self.ui.add_panel(panel)
```

### 9. Deployment Phase

**Click-to-Place**:
```python
def handle_deployment_click(self, world_x, world_y):
    """Place unit during deployment"""
    if not self.unit_to_deploy:
        # Select unit from roster
        self.show_deployment_roster()
    else:
        if self.is_valid_deployment(world_x, world_y, current_player):
            self.place_unit(self.unit_to_deploy, world_x, world_y)
            self.unit_to_deploy = None
            self.check_deployment_complete()
        else:
            self.show_error("Invalid deployment zone!")
```

### 10. Complete Removal of Text Mode

**Files to Modify**:
- ❌ Delete: `battle.py` (text-based battle flow)
- ❌ Delete: All text input functions
- ✅ Keep: Core game logic (movement, combat, damage)
- ✅ Modify: All phases to work via UI callbacks

## Implementation Order

1. **Phase 1**: Input & UI Integration
   - ✅ Created `input_handler.py`
   - ✅ Created `ui_components.py`
   - ⏳ Update `graphics_engine.py` to use them

2. **Phase 2**: Camera Controls
   - ⏳ WASD movement
   - ⏳ Q/E rotation
   - ⏳ Scroll zoom
   - ⏳ Boundary clamping

3. **Phase 3**: Selection System
   - ⏳ Single click selection
   - ⏳ Box drag selection
   - ⏳ Shift-click multi-select
   - ⏳ Visual selection indicators

4. **Phase 4**: Command System
   - ⏳ Right-click move
   - ⏳ Right-click attack
   - ⏳ Context menus
   - ⏳ Command queuing

5. **Phase 5**: UI Panels
   - ⏳ Phase progression bar
   - ⏳ Unit info panel
   - ⏳ Ability hotbar
   - ⏳ Army roster panel
   - ⏳ Score display

6. **Phase 6**: Abilities & Targeting
   - ⏳ Hotkey (1-5) abilities
   - ⏳ Targeting mode
   - ⏳ Range indicators
   - ⏳ Ability feedback

7. **Phase 7**: Deployment
   - ⏳ Click-to-place units
   - ⏳ Deployment zone validation
   - ⏳ Alternating deployment UI
   - ⏳ "Start Battle" button

8. **Phase 8**: Polish
   - ⏳ Tooltips everywhere
   - ⏳ Sound effects
   - ⏳ Animations
   - ⏳ Error messages
   - ⏳ Visual feedback

## Estimated Scope

- **Lines of Code**: ~3,000-4,000 new/modified
- **Files Modified**: 8-10
- **Files Created**: 3-4
- **Time Estimate**: 15-20 hours of development

## Testing Checklist

- [ ] Can select units with click
- [ ] Can select multiple units with box
- [ ] Can add to selection with Shift
- [ ] WASD moves camera smoothly
- [ ] Scroll wheel zooms
- [ ] Right-click moves units
- [ ] Right-click attacks enemies
- [ ] Context menu appears on right-click
- [ ] Abilities work with 1-5 keys
- [ ] Targeting mode works
- [ ] Phase progression works
- [ ] Can deploy units by clicking
- [ ] No text input required anywhere
- [ ] All game logic still works
- [ ] Visual feedback for all actions

## Benefits

1. **Intuitive**: Point and click, like any modern strategy game
2. **Fast**: No typing, instant commands
3. **Visual**: See everything, no imagination required
4. **Professional**: Feels like a real game
5. **Accessible**: Easier for new players

## Current Blockers

None - ready to implement! Just need to integrate the modules.

---

**Next Step**: Update `graphics_engine.py` to integrate InputManager and UIManager, then implement each feature incrementally.
