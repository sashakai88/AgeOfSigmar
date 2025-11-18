// ===========================================================================
// WARHAMMER AGE OF SIGMAR - GameMaker Edition
// Movement System Scripts
// ===========================================================================

/// @function can_unit_move(_unit)
/// @description Check if unit can move
/// @param {struct} _unit Unit to check
/// @return {bool} True if can move
function can_unit_move(_unit) {
    return _unit.model_count > 0 && !_unit.has_moved;
}

/// @function execute_normal_move(_unit, _target_x, _target_y)
/// @description Execute normal move
/// @param {struct} _unit Unit to move
/// @param {real} _target_x Target X (world coordinates)
/// @param {real} _target_y Target Y (world coordinates)
/// @return {bool} True if successful
function execute_normal_move(_unit, _target_x, _target_y) {
    var _warscroll = global.warscrolls[| _unit.warscroll_ref];
    var _max_move = _warscroll.move;

    var _dist = distance_2d(_unit.x_pos, _unit.y_pos, _target_x, _target_y);

    if (_dist > _max_move) {
        show_debug_message("Move too far! Distance: " + string(_dist) + " Max: " + string(_max_move));
        return false;
    }

    _unit.x_pos = _target_x;
    _unit.y_pos = _target_y;
    _unit.has_moved = true;

    show_debug_message("Unit moved to (" + string(_target_x) + ", " + string(_target_y) + ")");

    // Update combat status
    update_combat_status();

    return true;
}

/// @function execute_run(_unit, _target_x, _target_y)
/// @description Execute run move
/// @param {struct} _unit Unit to move
/// @param {real} _target_x Target X
/// @param {real} _target_y Target Y
/// @return {bool} True if successful
function execute_run(_unit, _target_x, _target_y) {
    var _warscroll = global.warscrolls[| _unit.warscroll_ref];
    var _run_roll = roll_d6();
    var _total_move = _warscroll.move + _run_roll;

    show_debug_message("Run: " + string(_warscroll.move) + "\" + " + string(_run_roll) + " = " + string(_total_move) + "\"");

    var _dist = distance_2d(_unit.x_pos, _unit.y_pos, _target_x, _target_y);

    if (_dist > _total_move) {
        show_debug_message("Run too far!");
        return false;
    }

    _unit.x_pos = _target_x;
    _unit.y_pos = _target_y;
    _unit.has_moved = true;

    return true;
}

/// @function execute_retreat(_unit, _target_x, _target_y)
/// @description Execute retreat move
/// @param {struct} _unit Unit to retreat
/// @param {real} _target_x Target X
/// @param {real} _target_y Target Y
/// @return {bool} True if successful
function execute_retreat(_unit, _target_x, _target_y) {
    if (!_unit.is_in_combat) {
        show_debug_message("Unit not in combat - cannot retreat");
        return false;
    }

    // Inflict D3 mortal damage
    var _mortal_damage = roll_d3();
    show_debug_message("Retreating inflicts " + string(_mortal_damage) + " mortal damage");

    _unit.damage_pool = _mortal_damage;
    process_damage_sequence(_unit);

    if (_unit.model_count == 0) {
        show_debug_message("Unit destroyed during retreat!");
        return false;
    }

    var _warscroll = global.warscrolls[| _unit.warscroll_ref];
    var _max_move = _warscroll.move;

    var _dist = distance_2d(_unit.x_pos, _unit.y_pos, _target_x, _target_y);

    if (_dist > _max_move) {
        return false;
    }

    _unit.x_pos = _target_x;
    _unit.y_pos = _target_y;
    _unit.has_moved = true;
    _unit.is_in_combat = false;

    show_debug_message("Unit retreated successfully");

    return true;
}

/// @function execute_charge(_unit, _target_x, _target_y)
/// @description Execute charge move
/// @param {struct} _unit Unit to charge
/// @param {real} _target_x Target X
/// @param {real} _target_y Target Y
/// @return {bool} True if successful
function execute_charge(_unit, _target_x, _target_y) {
    var _charge_roll = roll_2d6();

    show_debug_message("Charge roll: " + string(_charge_roll) + "\"");

    var _dist = distance_2d(_unit.x_pos, _unit.y_pos, _target_x, _target_y);

    if (_charge_roll < _dist) {
        show_debug_message("Charge failed - insufficient distance");
        return false;
    }

    // Check if movement is valid
    if (_dist > _charge_roll) {
        return false;
    }

    _unit.x_pos = _target_x;
    _unit.y_pos = _target_y;
    _unit.has_charged = true;
    _unit.is_in_combat = true;

    show_debug_message("Charge successful!");

    // Update combat status
    update_combat_status();

    return true;
}

/// @function reset_unit_actions(_player)
/// @description Reset all unit actions for a player
/// @param {real} _player Player number
function reset_unit_actions(_player) {
    var _unit_count = ds_list_size(global.battlefield_units);

    for (var i = 0; i < _unit_count; i++) {
        var _unit = global.battlefield_units[| i];

        if (_unit.owner_player == _player) {
            _unit.has_moved = false;
            _unit.has_shot = false;
            _unit.has_fought = false;
            _unit.has_charged = false;
            _unit.commands_used = 0;
        }
    }
}

show_debug_message("Movement system loaded");
