// ===========================================================================
// WARHAMMER AGE OF SIGMAR - GameMaker Edition
// Combat System Scripts
// ===========================================================================

/// @function make_hit_roll(_hit_characteristic)
/// @description Make a hit roll
/// @param {real} _hit_characteristic Hit value needed
/// @return {bool} True if hit
function make_hit_roll(_hit_characteristic) {
    var _roll = roll_d6();

    // Unmodified 1 always fails
    if (_roll == 1) return false;

    // Unmodified 6 is critical (could track these)
    if (_roll == 6) {
        // Critical hit!
    }

    return _roll >= _hit_characteristic;
}

/// @function make_wound_roll(_wound_characteristic)
/// @description Make a wound roll
/// @param {real} _wound_characteristic Wound value needed
/// @return {bool} True if wounded
function make_wound_roll(_wound_characteristic) {
    var _roll = roll_d6();

    // Unmodified 1 always fails
    if (_roll == 1) return false;

    return _roll >= _wound_characteristic;
}

/// @function make_save_roll(_save_characteristic, _rend)
/// @description Make a save roll
/// @param {real} _save_characteristic Save value
/// @param {real} _rend Rend value
/// @return {bool} True if saved
function make_save_roll(_save_characteristic, _rend) {
    var _roll = roll_d6();

    // Unmodified 1 always fails
    if (_roll == 1) return false;

    // Apply rend
    var _modified_roll = _roll - _rend;

    return _modified_roll >= _save_characteristic;
}

/// @function resolve_weapon_attacks(_attacker, _target, _weapon)
/// @description Resolve attacks with a weapon
/// @param {struct} _attacker Attacking unit
/// @param {struct} _target Target unit
/// @param {struct} _weapon Weapon profile
/// @return {real} Damage dealt
function resolve_weapon_attacks(_attacker, _target, _weapon) {
    var _total_attacks = _weapon.attacks * _attacker.model_count;

    show_debug_message("Resolving " + string(_total_attacks) + " attacks with " + _weapon.weapon_name);

    // Hit rolls
    var _hit_count = 0;
    for (var i = 0; i < _total_attacks; i++) {
        if (make_hit_roll(_weapon.hit)) {
            _hit_count++;
        }
    }

    if (_hit_count == 0) return 0;
    show_debug_message("Hits: " + string(_hit_count));

    // Wound rolls
    var _wound_count = 0;
    for (var i = 0; i < _hit_count; i++) {
        if (make_wound_roll(_weapon.wound)) {
            _wound_count++;
        }
    }

    if (_wound_count == 0) return 0;
    show_debug_message("Wounds: " + string(_wound_count));

    // Get target warscroll
    var _target_warscroll = global.warscrolls[| _target.warscroll_ref];

    // Save rolls
    var _unsaved_count = 0;
    for (var i = 0; i < _wound_count; i++) {
        if (!make_save_roll(_target_warscroll.save, _weapon.rend)) {
            _unsaved_count++;
        }
    }

    show_debug_message("Failed saves: " + string(_unsaved_count));

    // Calculate damage
    var _damage_dealt = _unsaved_count * _weapon.damage;
    return _damage_dealt;
}

/// @function resolve_ward_saves(_unit, _damage_points)
/// @description Resolve ward saves
/// @param {struct} _unit Unit taking damage
/// @param {real} _damage_points Damage points
/// @return {real} Damage after wards
function resolve_ward_saves(_unit, _damage_points) {
    var _warscroll = global.warscrolls[| _unit.warscroll_ref];

    if (!_warscroll.has_ward) return _damage_points;

    show_debug_message("Making ward saves (" + string(_warscroll.ward_value) + "+)");

    var _saved_damage = 0;
    for (var i = 0; i < _damage_points; i++) {
        if (roll_d6() >= _warscroll.ward_value) {
            _saved_damage++;
        }
    }

    show_debug_message("Ward saves: " + string(_saved_damage) + " / " + string(_damage_points));

    return _damage_points - _saved_damage;
}

/// @function allocate_damage(_unit, _damage_points)
/// @description Allocate damage to unit
/// @param {struct} _unit Unit taking damage
/// @param {real} _damage_points Damage to allocate
function allocate_damage(_unit, _damage_points) {
    var _warscroll = global.warscrolls[| _unit.warscroll_ref];
    var _health = _warscroll.health;
    var _models_slain = 0;

    show_debug_message("Allocating " + string(_damage_points) + " damage");

    while (_damage_points > 0 && _unit.model_count > 0) {
        // Allocate 1 damage to first model
        if (array_length(_unit.models) > 0) {
            _unit.models[0].damage_allocated++;

            // Check if model is slain
            if (_unit.models[0].damage_allocated >= _health) {
                show_debug_message("Model slain!");
                _models_slain++;

                // Remove model
                array_delete(_unit.models, 0, 1);
                _unit.model_count--;
            }
        }

        _damage_points--;
    }

    show_debug_message("Models slain: " + string(_models_slain));
    show_debug_message("Models remaining: " + string(_unit.model_count));

    // Check if unit destroyed
    if (_unit.model_count == 0) {
        show_debug_message("UNIT DESTROYED!");
        _unit.is_in_combat = false;
    }
}

/// @function process_damage_sequence(_unit)
/// @description Process complete damage sequence
/// @param {struct} _unit Unit taking damage
function process_damage_sequence(_unit) {
    var _damage = _unit.damage_pool;

    show_debug_message("=== DAMAGE SEQUENCE ===");
    show_debug_message("Damage pool: " + string(_damage));

    // Ward saves
    _damage = resolve_ward_saves(_unit, _damage);

    // Allocate damage
    if (_damage > 0) {
        allocate_damage(_unit, _damage);
    }

    // Reset damage pool
    _unit.damage_pool = 0;
}

/// @function execute_fight(_attacker, _target)
/// @description Execute fight ability
/// @param {struct} _attacker Attacking unit
/// @param {struct} _target Target unit
function execute_fight(_attacker, _target) {
    show_debug_message("=== FIGHT ===");

    var _attacker_warscroll = global.warscrolls[| _attacker.warscroll_ref];

    // Reset target damage pool
    _target.damage_pool = 0;

    // Attack with each melee weapon
    for (var i = 0; i < array_length(_attacker_warscroll.weapons); i++) {
        var _weapon = _attacker_warscroll.weapons[i];

        if (_weapon.weapon_type == WeaponType.Melee) {
            show_debug_message("Attacking with " + _weapon.weapon_name);
            var _damage = resolve_weapon_attacks(_attacker, _target, _weapon);
            _target.damage_pool += _damage;
        }
    }

    // Process damage
    if (_target.damage_pool > 0) {
        process_damage_sequence(_target);
    }

    _attacker.has_fought = true;
}

/// @function execute_shoot(_attacker, _target)
/// @description Execute shoot ability
/// @param {struct} _attacker Shooting unit
/// @param {struct} _target Target unit
function execute_shoot(_attacker, _target) {
    show_debug_message("=== SHOOT ===");

    var _attacker_warscroll = global.warscrolls[| _attacker.warscroll_ref];

    // Reset target damage pool
    _target.damage_pool = 0;

    // Attack with each ranged weapon
    for (var i = 0; i < array_length(_attacker_warscroll.weapons); i++) {
        var _weapon = _attacker_warscroll.weapons[i];

        if (_weapon.weapon_type == WeaponType.Ranged) {
            // Check range
            var _dist = distance_2d(_attacker.x_pos, _attacker.y_pos,
                                   _target.x_pos, _target.y_pos);

            if (_dist <= _weapon.range) {
                show_debug_message("Shooting with " + _weapon.weapon_name);
                var _damage = resolve_weapon_attacks(_attacker, _target, _weapon);
                _target.damage_pool += _damage;
            }
        }
    }

    // Process damage
    if (_target.damage_pool > 0) {
        process_damage_sequence(_target);
    }

    _attacker.has_shot = true;
}

/// @function update_combat_status()
/// @description Update which units are in combat
function update_combat_status() {
    var _unit_count = ds_list_size(global.battlefield_units);

    for (var i = 0; i < _unit_count; i++) {
        var _unit = global.battlefield_units[| i];

        if (_unit.model_count == 0) {
            _unit.is_in_combat = false;
            continue;
        }

        var _in_combat = false;

        // Check all enemy units
        for (var j = 0; j < _unit_count; j++) {
            var _other = global.battlefield_units[| j];

            if (_other.owner_player != _unit.owner_player && _other.model_count > 0) {
                var _dist = distance_2d(_unit.x_pos, _unit.y_pos,
                                       _other.x_pos, _other.y_pos);

                if (_dist <= global.combat_range) {
                    _in_combat = true;
                    break;
                }
            }
        }

        _unit.is_in_combat = _in_combat;
    }
}

show_debug_message("Combat system loaded");
