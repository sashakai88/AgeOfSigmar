// ===========================================================================
// WARHAMMER AGE OF SIGMAR - GameMaker Edition
// Helper Functions
// ===========================================================================

/// @function get_unit_at_position(_world_x, _world_y)
/// @description Get unit at world position
/// @param {real} _world_x World X coordinate
/// @param {real} _world_y World Y coordinate
/// @return {struct} Unit or noone
function get_unit_at_position(_world_x, _world_y) {
    var _closest_unit = noone;
    var _closest_dist = 2.0; // Max selection distance in inches

    var _unit_count = ds_list_size(global.battlefield_units);

    for (var i = 0; i < _unit_count; i++) {
        var _unit = global.battlefield_units[| i];

        if (_unit.model_count > 0) {
            var _dist = distance_2d(_world_x, _world_y, _unit.x_pos, _unit.y_pos);

            if (_dist < _closest_dist) {
                _closest_dist = _dist;
                _closest_unit = _unit;
            }
        }
    }

    return _closest_unit;
}

/// @function cycle_unit_selection()
/// @description Cycle to next friendly unit
function cycle_unit_selection() {
    var _unit_count = ds_list_size(global.battlefield_units);

    if (_unit_count == 0) return;

    var _start_index = 0;
    if (ds_list_size(global.selected_units) > 0) {
        var _current = global.selected_units[| 0];
        _start_index = ds_list_find_index(global.battlefield_units, _current) + 1;
    }

    // Find next unit owned by active player
    for (var i = 0; i < _unit_count; i++) {
        var _index = (_start_index + i) mod _unit_count;
        var _unit = global.battlefield_units[| _index];

        if (_unit.owner_player == global.active_player && _unit.model_count > 0) {
            ds_list_clear(global.selected_units);
            ds_list_add(global.selected_units, _unit);

            // Center camera on unit
            global.camera_x = _unit.x_pos * global.scale;
            global.camera_y = _unit.y_pos * global.scale;

            show_debug_message("Selected next unit");
            break;
        }
    }
}

/// @function finalize_box_selection()
/// @description Finalize box selection
function finalize_box_selection() {
    var _min_x = min(selection_box_start_x, mouse_x);
    var _max_x = max(selection_box_start_x, mouse_x);
    var _min_y = min(selection_box_start_y, mouse_y);
    var _max_y = max(selection_box_start_y, mouse_y);

    ds_list_clear(global.selected_units);

    var _unit_count = ds_list_size(global.battlefield_units);

    for (var i = 0; i < _unit_count; i++) {
        var _unit = global.battlefield_units[| i];

        if (_unit.owner_player == global.active_player && _unit.model_count > 0) {
            var _screen = world_to_screen(_unit.x_pos, _unit.y_pos);
            var _screen_x = _screen[0];
            var _screen_y = _screen[1];

            if (_screen_x >= _min_x && _screen_x <= _max_x &&
                _screen_y >= _min_y && _screen_y <= _max_y) {
                ds_list_add(global.selected_units, _unit);
            }
        }
    }

    show_debug_message("Box selection: " + string(ds_list_size(global.selected_units)) + " units");
}

/// @function advance_to_next_phase()
/// @description Advance to next game phase
function advance_to_next_phase() {
    global.current_phase++;

    if (global.current_phase > GamePhase.EndOfTurn) {
        // End turn
        end_current_turn();
    } else {
        show_debug_message("Entering phase: " + phase_to_string(global.current_phase));

        // Reset actions for new phase
        if (global.current_phase == GamePhase.Hero) {
            reset_unit_actions(global.active_player);
        }
    }
}

/// @function end_current_turn()
/// @description End current player's turn
function end_current_turn() {
    show_debug_message("=== END OF TURN ===");

    // Determine objective control
    determine_objective_control();

    // Score victory points
    score_victory_points();

    // Switch player
    if (global.active_player == 1) {
        global.active_player = 2;
        global.current_phase = GamePhase.Hero;
    } else {
        // End of round
        global.active_player = 1;
        global.current_round++;
        global.current_phase = GamePhase.Hero;

        if (global.current_round > 5) {
            show_debug_message("=== BATTLE COMPLETE ===");
            determine_winner();
        }
    }

    reset_unit_actions(global.active_player);
}

/// @function determine_objective_control()
/// @description Determine who controls objectives
function determine_objective_control() {
    var _obj_count = ds_list_size(global.objectives);

    for (var i = 0; i < _obj_count; i++) {
        var _objective = global.objectives[| i];

        var _p1_score = 0;
        var _p2_score = 0;

        // Check each unit
        var _unit_count = ds_list_size(global.battlefield_units);
        for (var j = 0; j < _unit_count; j++) {
            var _unit = global.battlefield_units[| j];

            if (_unit.model_count > 0) {
                var _dist = distance_2d(_unit.x_pos, _unit.y_pos,
                                       _objective.x_pos, _objective.y_pos);

                if (_dist <= global.combat_range) {
                    var _warscroll = global.warscrolls[| _unit.warscroll_ref];
                    var _control = _warscroll.control * _unit.model_count;

                    if (_unit.owner_player == 1) {
                        _p1_score += _control;
                    } else {
                        _p2_score += _control;
                    }
                }
            }
        }

        // Determine control
        if (_p1_score > _p2_score) {
            _objective.controlled_by = 1;
        } else if (_p2_score > _p1_score) {
            _objective.controlled_by = 2;
        }
    }
}

/// @function score_victory_points()
/// @description Award victory points
function score_victory_points() {
    var _p1_objectives = 0;
    var _p2_objectives = 0;

    var _obj_count = ds_list_size(global.objectives);

    for (var i = 0; i < _obj_count; i++) {
        var _objective = global.objectives[| i];

        if (_objective.controlled_by == 1) _p1_objectives++;
        if (_objective.controlled_by == 2) _p2_objectives++;
    }

    global.player1_points += _p1_objectives * 2;
    global.player2_points += _p2_objectives * 2;

    show_debug_message("VP scored - P1: " + string(_p1_objectives * 2) + "  P2: " + string(_p2_objectives * 2));
}

/// @function determine_winner()
/// @description Determine winner
function determine_winner() {
    show_debug_message("=== BATTLE CONCLUDED ===");
    show_debug_message("Player 1: " + string(global.player1_points) + " VP");
    show_debug_message("Player 2: " + string(global.player2_points) + " VP");

    if (global.player1_points > global.player2_points) {
        show_debug_message("PLAYER 1 WINS!");
    } else if (global.player2_points > global.player1_points) {
        show_debug_message("PLAYER 2 WINS!");
    } else {
        show_debug_message("DRAW!");
    }
}

/// @function load_sample_warscrolls()
/// @description Load sample unit warscrolls
function load_sample_warscrolls() {
    // Liberators (Stormcast Eternals)
    var _liberators = new UnitWarscroll();
    _liberators.unit_id = 0;
    _liberators.unit_name = "Liberators";
    _liberators.faction = FactionType.StormcastEternals;
    _liberators.unit_type = UnitType.Infantry;
    _liberators.move = 5;
    _liberators.health = 2;
    _liberators.control = 1;
    _liberators.save = 4;
    _liberators.unit_size = 5;
    _liberators.points_cost = 110;

    var _warhammer = new WeaponProfile();
    _warhammer.weapon_name = "Warhammer";
    _warhammer.weapon_type = WeaponType.Melee;
    _warhammer.attacks = 2;
    _warhammer.hit = 4;
    _warhammer.wound = 3;
    _warhammer.rend = 1;
    _warhammer.damage = 1;
    _warhammer.range = 1;

    _liberators.weapons = [_warhammer];
    ds_list_add(global.warscrolls, _liberators);

    // Clanrats (Skaven)
    var _clanrats = new UnitWarscroll();
    _clanrats.unit_id = 1;
    _clanrats.unit_name = "Clanrats";
    _clanrats.faction = FactionType.Skaven;
    _clanrats.unit_type = UnitType.Infantry;
    _clanrats.move = 6;
    _clanrats.health = 1;
    _clanrats.control = 1;
    _clanrats.save = 5;
    _clanrats.unit_size = 20;
    _clanrats.points_cost = 120;

    var _blade = new WeaponProfile();
    _blade.weapon_name = "Rusty Blade";
    _blade.weapon_type = WeaponType.Melee;
    _blade.attacks = 1;
    _blade.hit = 4;
    _blade.wound = 4;
    _blade.rend = 0;
    _blade.damage = 1;
    _blade.range = 1;

    _clanrats.weapons = [_blade];
    ds_list_add(global.warscrolls, _clanrats);

    show_debug_message("Loaded " + string(ds_list_size(global.warscrolls)) + " warscrolls");
}

/// @function place_objectives()
/// @description Place objective markers
function place_objectives() {
    var _positions = [[12, 12], [32, 12], [12, 48], [32, 48]];

    for (var i = 0; i < array_length(_positions); i++) {
        var _obj = new ObjectiveMarker();
        _obj.objective_id = i;
        _obj.x_pos = _positions[i][0];
        _obj.y_pos = _positions[i][1];
        _obj.controlled_by = 0;

        ds_list_add(global.objectives, _obj);
    }

    show_debug_message("Placed " + string(ds_list_size(global.objectives)) + " objectives");
}

/// @function spawn_unit(_warscroll_id, _x, _y, _player, _model_count)
/// @description Spawn a unit on the battlefield
/// @param {real} _warscroll_id Index of warscroll in global.warscrolls (0=Liberators, 1=Clanrats)
/// @param {real} _x X position in inches
/// @param {real} _y Y position in inches
/// @param {real} _player Owner player (1 or 2)
/// @param {real} _model_count Number of models in unit
function spawn_unit(_warscroll_id, _x, _y, _player, _model_count) {
    var _unit = new BattlefieldUnit();
    _unit.warscroll_ref = _warscroll_id;
    _unit.x_pos = _x;
    _unit.y_pos = _y;
    _unit.owner_player = _player;
    _unit.model_count = _model_count;

    // Get warscroll to determine health per model
    var _warscroll = global.warscrolls[| _warscroll_id];

    // Create model array with proper health tracking
    _unit.models = [];
    for (var i = 0; i < _model_count; i++) {
        var _model = new UnitModel();
        _model.damage_allocated = 0;
        array_push(_unit.models, _model);
    }

    ds_list_add(global.battlefield_units, _unit);

    show_debug_message("Spawned " + _warscroll.unit_name + " at (" + string(_x) + ", " + string(_y) + ")");

    return _unit;
}

show_debug_message("Helper functions loaded");
