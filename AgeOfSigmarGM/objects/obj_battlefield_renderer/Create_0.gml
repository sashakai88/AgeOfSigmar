// ===========================================================================
// WARHAMMER AGE OF SIGMAR - Battlefield Renderer
// Create Event
// ===========================================================================

// This object handles all battlefield rendering
// Units, objectives, terrain, grid, etc.

// Visual settings
draw_set_font(-1);
draw_set_halign(fa_left);
draw_set_valign(fa_top);

// Grid settings
grid_color = make_color_rgb(60, 60, 80);
grid_alpha = 0.3;
grid_spacing = 6.0; // 6 inches

// Deployment zone colors
deployment_zone_color = make_color_rgb(100, 100, 255);
deployment_zone_alpha = 0.1;

// Selection colors
selection_color = make_color_rgb(255, 215, 0); // Gold
hover_color = make_color_rgb(255, 255, 255); // White
enemy_color = make_color_rgb(255, 100, 100); // Red tint

show_debug_message("Battlefield renderer initialized");
