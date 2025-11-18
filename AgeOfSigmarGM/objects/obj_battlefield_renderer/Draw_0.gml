// ===========================================================================
// WARHAMMER AGE OF SIGMAR - Battlefield Renderer
// Draw Event - Renders battlefield, units, objectives
// ===========================================================================

// LAYER 1: Battlefield Grid
draw_battlefield_grid();

// LAYER 2: Deployment Zones
draw_deployment_zones();

// LAYER 3: Terrain Features
draw_terrain_features();

// LAYER 4: Objectives
draw_objectives();

// LAYER 5: Movement/Range Indicators
draw_range_indicators();

// LAYER 6: Selection Box
draw_selection_box();

// LAYER 7: Units
draw_all_units();

// LAYER 8: Mouse Cursor Info
draw_cursor_info();


// ===========================================================================
// FUNCTION: Draw Battlefield Grid
// ===========================================================================
function draw_battlefield_grid() {
    draw_set_color(grid_color);
    draw_set_alpha(grid_alpha);

    // Vertical lines
    for (var _x = 0; _x <= global.battlefield_width; _x += grid_spacing) {
        var _screen = world_to_screen(_x, 0);
        var _screen_end = world_to_screen(_x, global.battlefield_height);

        draw_line(_screen[0], _screen[1], _screen_end[0], _screen_end[1]);
    }

    // Horizontal lines
    for (var _y = 0; _y <= global.battlefield_height; _y += grid_spacing) {
        var _screen = world_to_screen(0, _y);
        var _screen_end = world_to_screen(global.battlefield_width, _y);

        draw_line(_screen[0], _screen[1], _screen_end[0], _screen_end[1]);
    }

    draw_set_alpha(1.0);
}


// ===========================================================================
// FUNCTION: Draw Deployment Zones
// ===========================================================================
function draw_deployment_zones() {
    draw_set_color(deployment_zone_color);
    draw_set_alpha(deployment_zone_alpha);

    // Player 1 deployment zone (bottom 9")
    var _p1_top_left = world_to_screen(0, global.battlefield_height - 9);
    var _p1_bottom_right = world_to_screen(global.battlefield_width, global.battlefield_height);
    draw_rectangle(_p1_top_left[0], _p1_top_left[1],
                   _p1_bottom_right[0], _p1_bottom_right[1], false);

    // Player 2 deployment zone (top 9")
    var _p2_top_left = world_to_screen(0, 0);
    var _p2_bottom_right = world_to_screen(global.battlefield_width, 9);
    draw_rectangle(_p2_top_left[0], _p2_top_left[1],
                   _p2_bottom_right[0], _p2_bottom_right[1], false);

    draw_set_alpha(1.0);
}


// ===========================================================================
// FUNCTION: Draw Terrain Features
// ===========================================================================
function draw_terrain_features() {
    var _terrain_count = ds_list_size(global.terrain_features);

    for (var i = 0; i < _terrain_count; i++) {
        var _terrain = global.terrain_features[| i];

        var _screen = world_to_screen(_terrain.x_pos, _terrain.y_pos);
        var _radius = _terrain.radius * global.scale * global.camera_zoom;

        // Draw terrain circle
        draw_set_color(make_color_rgb(34, 139, 34)); // Forest green
        draw_set_alpha(0.3);
        draw_circle(_screen[0], _screen[1], _radius, false);

        // Draw outline
        draw_set_alpha(1.0);
        draw_circle(_screen[0], _screen[1], _radius, true);

        // Draw name
        draw_set_color(c_white);
        draw_text(_screen[0] - string_width(_terrain.terrain_name) / 2,
                  _screen[1] - 10, _terrain.terrain_name);
    }

    draw_set_alpha(1.0);
}


// ===========================================================================
// FUNCTION: Draw Objectives
// ===========================================================================
function draw_objectives() {
    var _obj_count = ds_list_size(global.objectives);

    for (var i = 0; i < _obj_count; i++) {
        var _objective = global.objectives[| i];

        var _screen = world_to_screen(_objective.x_pos, _objective.y_pos);
        var _control_radius = global.combat_range * global.scale * global.camera_zoom;

        // Draw control zone (3" radius)
        draw_set_alpha(0.1);
        if (_objective.controlled_by == 1) {
            draw_set_color(c_blue);
        } else if (_objective.controlled_by == 2) {
            draw_set_color(c_red);
        } else {
            draw_set_color(c_gray);
        }
        draw_circle(_screen[0], _screen[1], _control_radius, false);

        // Draw objective marker
        draw_set_alpha(1.0);
        draw_set_color(make_color_rgb(255, 215, 0)); // Gold
        draw_circle(_screen[0], _screen[1], 10, false);
        draw_set_color(c_black);
        draw_circle(_screen[0], _screen[1], 10, true);

        // Draw objective number
        draw_set_halign(fa_center);
        draw_set_valign(fa_middle);
        draw_text(_screen[0], _screen[1], string(_objective.objective_id + 1));
        draw_set_halign(fa_left);
        draw_set_valign(fa_top);
    }

    draw_set_alpha(1.0);
}


// ===========================================================================
// FUNCTION: Draw Range Indicators
// ===========================================================================
function draw_range_indicators() {
    if (ds_list_size(global.selected_units) == 0) return;

    var _selected = global.selected_units[| 0];
    var _warscroll = global.warscrolls[| _selected.warscroll_ref];
    var _screen = world_to_screen(_selected.x_pos, _selected.y_pos);

    // Movement range (if not moved)
    if (!_selected.has_moved) {
        draw_set_color(c_green);
        draw_set_alpha(0.15);
        var _move_radius = _warscroll.move * global.scale * global.camera_zoom;
        draw_circle(_screen[0], _screen[1], _move_radius, false);

        draw_set_alpha(0.5);
        draw_circle(_screen[0], _screen[1], _move_radius, true);
    }

    // Combat range (3")
    draw_set_color(c_red);
    draw_set_alpha(0.2);
    var _combat_radius = global.combat_range * global.scale * global.camera_zoom;
    draw_circle(_screen[0], _screen[1], _combat_radius, false);

    draw_set_alpha(1.0);
}


// ===========================================================================
// FUNCTION: Draw Selection Box
// ===========================================================================
function draw_selection_box() {
    if (!obj_game_controller.selection_box_active) return;

    var _start_x = obj_game_controller.selection_box_start_x;
    var _start_y = obj_game_controller.selection_box_start_y;

    draw_set_color(selection_color);
    draw_set_alpha(0.2);
    draw_rectangle(_start_x, _start_y, mouse_x, mouse_y, false);

    draw_set_alpha(1.0);
    draw_rectangle(_start_x, _start_y, mouse_x, mouse_y, true);
}


// ===========================================================================
// FUNCTION: Draw All Units
// ===========================================================================
function draw_all_units() {
    var _unit_count = ds_list_size(global.battlefield_units);

    for (var i = 0; i < _unit_count; i++) {
        var _unit = global.battlefield_units[| i];

        if (_unit.model_count <= 0) continue;

        var _warscroll = global.warscrolls[| _unit.warscroll_ref];
        var _screen = world_to_screen(_unit.x_pos, _unit.y_pos);

        // Determine unit size
        var _radius = 15; // Default infantry
        if (_warscroll.unit_type == UnitType.Monster) {
            _radius = 25;
        } else if (_warscroll.unit_type == UnitType.Cavalry) {
            _radius = 18;
        }
        _radius *= global.camera_zoom;

        // Determine color
        var _unit_color = c_blue;
        if (_unit.owner_player == 2) {
            _unit_color = c_red;
        }

        // Check if selected or hovered
        var _is_selected = false;
        var _selected_count = ds_list_size(global.selected_units);
        for (var j = 0; j < _selected_count; j++) {
            if (global.selected_units[| j] == _unit) {
                _is_selected = true;
                break;
            }
        }

        // Draw unit circle
        draw_set_alpha(0.8);
        draw_set_color(_unit_color);
        draw_circle(_screen[0], _screen[1], _radius, false);

        // Draw outline
        draw_set_alpha(1.0);
        if (_is_selected) {
            draw_set_color(selection_color);
            draw_circle(_screen[0], _screen[1], _radius + 3, true);
            draw_circle(_screen[0], _screen[1], _radius + 4, true);
        }
        draw_set_color(c_black);
        draw_circle(_screen[0], _screen[1], _radius, true);

        // Draw health bar
        var _health_percent = 1.0;
        if (_unit.model_count > 0 && array_length(_unit.models) > 0) {
            var _max_health = _warscroll.health;
            var _current_health = _max_health - _unit.models[0].damage_allocated;
            _health_percent = _current_health / _max_health;
        }

        var _bar_width = _radius * 2;
        var _bar_height = 4;
        var _bar_x = _screen[0] - _bar_width / 2;
        var _bar_y = _screen[1] + _radius + 5;

        // Background
        draw_set_color(c_black);
        draw_rectangle(_bar_x, _bar_y, _bar_x + _bar_width, _bar_y + _bar_height, false);

        // Health
        draw_set_color(c_lime);
        draw_rectangle(_bar_x, _bar_y,
                      _bar_x + (_bar_width * _health_percent),
                      _bar_y + _bar_height, false);

        // Model count
        draw_set_color(c_white);
        draw_set_halign(fa_center);
        draw_set_valign(fa_middle);
        draw_text(_screen[0], _screen[1], string(_unit.model_count));
        draw_set_halign(fa_left);
        draw_set_valign(fa_top);

        // Unit name (if selected)
        if (_is_selected) {
            draw_set_color(c_white);
            draw_text(_screen[0] - string_width(_warscroll.unit_name) / 2,
                     _screen[1] - _radius - 20, _warscroll.unit_name);
        }

        // Combat status indicator
        if (_unit.is_in_combat) {
            draw_set_color(c_red);
            draw_circle(_screen[0] + _radius - 5, _screen[1] - _radius + 5, 5, false);
        }
    }

    draw_set_alpha(1.0);
}


// ===========================================================================
// FUNCTION: Draw Cursor Info
// ===========================================================================
function draw_cursor_info() {
    // Show world coordinates at mouse position
    var _world = screen_to_world(mouse_x, mouse_y);

    draw_set_color(c_white);
    draw_text(mouse_x + 15, mouse_y + 15,
             string_format(_world[0], 1, 1) + "\", " + string_format(_world[1], 1, 1) + "\"");
}
