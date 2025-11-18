/// @description Initialize Game Controller

// Load core data
scr_core_data();
scr_combat();
scr_movement();

// Initialize game state
global.current_round = 0;
global.current_phase = GamePhase.Deployment;
global.active_player = 1;
global.player1_points = 0;
global.player2_points = 0;

// Camera setup
global.camera_x = (global.battlefield_width * global.scale) / 2;
global.camera_y = (global.battlefield_height * global.scale) / 2;
global.camera_zoom = 1.0;

// Input state
mouse_dragging = false;
drag_start_x = 0;
drag_start_y = 0;
selection_box_active = false;
selection_box_start_x = 0;
selection_box_start_y = 0;

// Selected unit
selected_unit = noone;

// Load sample warscrolls
load_sample_warscrolls();

// Place objectives
place_objectives();

// ===================================================================
// SPAWN STARTING UNITS - CUSTOMIZE HERE!
// ===================================================================
// Usage: spawn_unit(warscroll_id, x_inches, y_inches, player, model_count)
// Warscroll IDs: 0=Liberators, 1=Clanrats (add more in load_sample_warscrolls())

// Player 1 (Blue) - Stormcast Eternals
spawn_unit(0, 10, 54, 1, 5);  // Liberators at (10", 54")
spawn_unit(0, 20, 54, 1, 5);  // Liberators at (20", 54")
spawn_unit(0, 30, 52, 1, 5);  // Liberators at (30", 52")

// Player 2 (Red) - Skaven
spawn_unit(1, 15, 6, 2, 20);  // Clanrats at (15", 6")
spawn_unit(1, 25, 8, 2, 20);  // Clanrats at (25", 8")
spawn_unit(1, 35, 6, 2, 20);  // Clanrats at (35", 6")

show_debug_message("Game Controller initialized");
show_debug_message("=== WARHAMMER AGE OF SIGMAR ===");
show_debug_message("GameMaker Edition");
show_debug_message("Spawned " + string(ds_list_size(global.battlefield_units)) + " units");
show_debug_message("Ready to play!");
