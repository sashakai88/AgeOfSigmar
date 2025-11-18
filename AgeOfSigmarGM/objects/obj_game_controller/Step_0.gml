/// @description Game Loop and Input Handling

// ---------------------------------------------------------------------------
// CAMERA CONTROLS (WASD)
// ---------------------------------------------------------------------------

var _camera_speed = 5;

if (keyboard_check(ord("W"))) {
    global.camera_y -= _camera_speed;
}
if (keyboard_check(ord("S"))) {
    global.camera_y += _camera_speed;
}
if (keyboard_check(ord("A"))) {
    global.camera_x -= _camera_speed;
}
if (keyboard_check(ord("D"))) {
    global.camera_x += _camera_speed;
}

// Camera zoom (mouse wheel)
if (mouse_wheel_up()) {
    global.camera_zoom = min(global.camera_zoom * 1.1, 3.0);
}
if (mouse_wheel_down()) {
    global.camera_zoom = max(global.camera_zoom * 0.9, 0.3);
}

// Clamp camera to battlefield bounds
global.camera_x = clamp(global.camera_x, 0, global.battlefield_width * global.scale);
global.camera_y = clamp(global.camera_y, 0, global.battlefield_height * global.scale);

// ---------------------------------------------------------------------------
// MOUSE INPUT
// ---------------------------------------------------------------------------

// Left click - Select unit
if (mouse_check_button_pressed(mb_left)) {
    var _world = screen_to_world(mouse_x, mouse_y);
    var _world_x = _world[0];
    var _world_y = _world[1];

    // Check if clicked on unit
    var _clicked_unit = get_unit_at_position(_world_x, _world_y);

    if (_clicked_unit != noone) {
        selected_unit = _clicked_unit;
        show_debug_message("Selected unit: " + selected_unit.unit_id);

        // Clear previous selection
        ds_list_clear(global.selected_units);
        ds_list_add(global.selected_units, selected_unit);
    } else {
        // Start selection box
        selection_box_active = true;
        selection_box_start_x = mouse_x;
        selection_box_start_y = mouse_y;
    }
}

// Left button released - End selection box
if (mouse_check_button_released(mb_left)) {
    if (selection_box_active) {
        finalize_box_selection();
        selection_box_active = false;
    }
}

// Right click - Issue command
if (mouse_check_button_pressed(mb_right)) {
    if (ds_list_size(global.selected_units) > 0) {
        var _world = screen_to_world(mouse_x, mouse_y);
        var _world_x = _world[0];
        var _world_y = _world[1];

        var _target_unit = get_unit_at_position(_world_x, _world_y);

        if (_target_unit != noone && _target_unit.owner_player != global.active_player) {
            // Attack command
            show_debug_message("Attack command issued");
            var _attacker = global.selected_units[| 0];
            execute_fight(_attacker, _target_unit);
        } else {
            // Move command
            show_debug_message("Move command issued");
            var _mover = global.selected_units[| 0];
            execute_normal_move(_mover, _world_x, _world_y);
        }
    }
}

// ---------------------------------------------------------------------------
// HOTKEYS
// ---------------------------------------------------------------------------

// Space - Center camera on selection
if (keyboard_check_pressed(vk_space)) {
    if (ds_list_size(global.selected_units) > 0) {
        var _unit = global.selected_units[| 0];
        global.camera_x = _unit.x_pos * global.scale;
        global.camera_y = _unit.y_pos * global.scale;
    }
}

// Tab - Cycle selection
if (keyboard_check_pressed(vk_tab)) {
    cycle_unit_selection();
}

// N - Next phase
if (keyboard_check_pressed(ord("N"))) {
    advance_to_next_phase();
}

// R - Retreat
if (keyboard_check_pressed(ord("R"))) {
    if (ds_list_size(global.selected_units) > 0) {
        var _unit = global.selected_units[| 0];
        if (_unit.is_in_combat) {
            show_debug_message("Initiate retreat (click destination)");
            // Set retreat mode
        }
    }
}

// F - Fight
if (keyboard_check_pressed(ord("F"))) {
    if (ds_list_size(global.selected_units) > 0) {
        var _unit = global.selected_units[| 0];
        if (_unit.is_in_combat) {
            show_debug_message("Initiate fight");
            // Enter target selection mode
        }
    }
}

// ESC - Deselect
if (keyboard_check_pressed(vk_escape)) {
    ds_list_clear(global.selected_units);
    selected_unit = noone;
}
