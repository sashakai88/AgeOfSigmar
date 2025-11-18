/// @description Draw GUI - HUD and UI Elements

// ---------------------------------------------------------------------------
// TOP BAR - Game Info
// ---------------------------------------------------------------------------

draw_set_color(c_black);
draw_set_alpha(0.7);
draw_rectangle(0, 0, room_width, 80, false);
draw_set_alpha(1);

draw_set_color(c_white);
draw_set_halign(fa_left);
draw_set_valign(fa_top);
draw_set_font(-1);

// Round and Phase
draw_text(20, 10, "Round: " + string(global.current_round) + "/5");
draw_text(20, 35, "Phase: " + phase_to_string(global.current_phase));

// Active Player
var _player_color = (global.active_player == 1) ? c_aqua : c_red;
draw_set_color(_player_color);
draw_text(200, 10, "Active: Player " + string(global.active_player));
draw_set_color(c_white);

// Victory Points
draw_text(400, 10, "VP - P1: " + string(global.player1_points) + "  P2: " + string(global.player2_points));

// Command Points
draw_text(400, 35, "CP - P1: " + string(global.player1_commands) + "  P2: " + string(global.player2_commands));

// ---------------------------------------------------------------------------
// BOTTOM BAR - Unit Info and Abilities
// ---------------------------------------------------------------------------

if (ds_list_size(global.selected_units) > 0) {
    var _unit = global.selected_units[| 0];
    var _warscroll = global.warscrolls[| _unit.warscroll_ref];

    draw_set_color(c_black);
    draw_set_alpha(0.7);
    draw_rectangle(0, room_height - 150, room_width, room_height, false);
    draw_set_alpha(1);

    draw_set_color(c_yellow);
    draw_text(20, room_height - 140, _warscroll.unit_name);

    draw_set_color(c_white);
    draw_text(20, room_height - 115, "Models: " + string(_unit.model_count) + "/" + string(_warscroll.unit_size));
    draw_text(20, room_height - 90, "Move: " + string(_warscroll.move) + "\"  Health: " + string(_warscroll.health) + "  Save: " + string(_warscroll.save) + "+");

    // Status
    var _status = "";
    if (_unit.has_moved) _status += "[Moved] ";
    if (_unit.has_shot) _status += "[Shot] ";
    if (_unit.has_charged) _status += "[Charged] ";
    if (_unit.has_fought) _status += "[Fought] ";
    if (_unit.is_in_combat) _status += "[IN COMBAT] ";

    if (_status != "") {
        draw_text(20, room_height - 65, _status);
    }

    // Ability buttons (placeholders)
    var _btn_x = 400;
    var _btn_y = room_height - 130;

    for (var i = 0; i < 5; i++) {
        draw_set_color(c_dkgray);
        draw_rectangle(_btn_x + (i * 90), _btn_y, _btn_x + (i * 90) + 80, _btn_y + 80, false);
        draw_set_color(c_white);
        draw_rectangle(_btn_x + (i * 90), _btn_y, _btn_x + (i * 90) + 80, _btn_y + 80, true);
        draw_text(_btn_x + (i * 90) + 20, _btn_y + 30, string(i + 1));
    }
}

// ---------------------------------------------------------------------------
// RIGHT PANEL - Controls Help
// ---------------------------------------------------------------------------

draw_set_color(c_black);
draw_set_alpha(0.7);
draw_rectangle(room_width - 250, 100, room_width, 600, false);
draw_set_alpha(1);

draw_set_color(c_white);
draw_text(room_width - 240, 110, "=== CONTROLS ===");
draw_text(room_width - 240, 140, "WASD - Move Camera");
draw_text(room_width - 240, 160, "Mouse Wheel - Zoom");
draw_text(room_width - 240, 180, "Left Click - Select");
draw_text(room_width - 240, 200, "Right Click - Command");
draw_text(room_width - 240, 220, "Space - Center Camera");
draw_text(room_width - 240, 240, "Tab - Cycle Units");
draw_text(room_width - 240, 260, "N - Next Phase");
draw_text(room_width - 240, 280, "R - Retreat");
draw_text(room_width - 240, 300, "F - Fight");
draw_text(room_width - 240, 320, "ESC - Deselect");

// Selection box
if (selection_box_active) {
    draw_set_color(c_yellow);
    draw_set_alpha(0.3);
    draw_rectangle(selection_box_start_x, selection_box_start_y, mouse_x, mouse_y, false);
    draw_set_alpha(1);
    draw_rectangle(selection_box_start_x, selection_box_start_y, mouse_x, mouse_y, true);
}

// Reset drawing settings
draw_set_color(c_white);
draw_set_alpha(1);
draw_set_halign(fa_left);
draw_set_valign(fa_top);
