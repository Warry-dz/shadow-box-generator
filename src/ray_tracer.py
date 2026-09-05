# src/ray_tracer.py

import sys
import os
import numpy as np

# Add the project root directory to sys.path automatically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.config as cfg

def initialize_walls():
    """Generate the four blank walls (value 1 means solid wall)."""
    rows = int(cfg.BOX_HEIGHT * cfg.PIXELS_PER_CM)
    cols_width = int(cfg.BOX_WIDTH * cfg.PIXELS_PER_CM)
    cols_depth = int(cfg.BOX_DEPTH * cfg.PIXELS_PER_CM)
    
    walls = {
        "top": np.ones((rows, cols_width), dtype=np.uint8),
        "bottom": np.ones((rows, cols_width), dtype=np.uint8),
        "left": np.ones((rows, cols_depth), dtype=np.uint8),
        "right": np.ones((rows, cols_depth), dtype=np.uint8)
    }
    return walls

def calculate_intersection(light_position, ray_vector):
    """Calculate when and where the light ray intersects the four box walls."""
    Lx, Ly, Lz = light_position
    Dx, Dy, Dz = ray_vector
    
    half_w = cfg.BOX_WIDTH / 2.0
    half_d = cfg.BOX_DEPTH / 2.0
    
    intersections = []
    
    # Calculate intersection with each wall 
    if Dx != 0:
        t1 = (half_w - Lx) / Dx
        if t1 > 0: intersections.append((t1, "right"))
        t2 = (-half_w - Lx) / Dx
        if t2 > 0: intersections.append((t2, "left"))
            
    if Dy != 0:
        t3 = (half_d - Ly) / Dy
        if t3 > 0: intersections.append((t3, "top"))
        t4 = (-half_d - Ly) / Dy
        if t4 > 0: intersections.append((t4, "bottom"))
    
    # If the ray does not intersect any wall
    if not intersections:
        return None, None
        
    # Choose the closest wall (smallest t distance)
    intersections.sort(key=lambda item: item[0])
    best_t, wall_name = intersections[0]
    
    # Calculate the 3D coordinates (X, Y, Z) of the hit point
    hit_x = Lx + best_t * Dx
    hit_y = Ly + best_t * Dy
    hit_z = Lz + best_t * Dz
    
    # Ensure the hole is within the box height limits
    if hit_z < 0 or hit_z > cfg.BOX_HEIGHT:
        return None, None
        
    return wall_name, (hit_x, hit_y, hit_z)

def map_3d_to_wall_pixel(wall_name, hit_point):
    """Convert the physical 3D coordinate (X, Y, Z) into matrix pixels (row, col)."""
    hx, hy, hz = hit_point
    
    # Rows depend on the height (Z)
    # Z max is row 0 (top of the wall), Z=0 is the last row (attached to the target wall)
    row = int((cfg.BOX_HEIGHT - hz) * cfg.PIXELS_PER_CM)
    
    # Columns depend on the width or depth of the wall
    if wall_name in ["top", "bottom"]:
        # Top and bottom walls rely on the X axis
        col = int((hx + (cfg.BOX_WIDTH / 2.0)) * cfg.PIXELS_PER_CM)
    else:
        # Left and right walls rely on the Y axis
        col = int((hy + (cfg.BOX_DEPTH / 2.0)) * cfg.PIXELS_PER_CM)
        
    return row, col

def ray_tracer_algorithm(walls, light_position, mask):
    """
    Main algorithm: Iterates over the mask, casts rays, and punches holes in walls.
    """
    img_rows, img_cols = mask.shape
    Lx, Ly, Lz = light_position
    
    # --- FIX: Scale the target image to be physically larger than the box ---
    # Make the target shadow size 60x60 cm on the wall (Box is only 20x15 cm)
    TARGET_IMAGE_WIDTH_CM = 60.0 
    TARGET_IMAGE_HEIGHT_CM = 60.0
    
    print(f"[*] Starting inverse ray tracing on {img_cols}x{img_rows} mask...")
    
    holes_punched = 0
    rays_inside_box = 0
    
    # Iterate over every pixel in the mask
    for r in range(img_rows):
        for c in range(img_cols):
            
            # 0 means a black pixel in the mask (target point)
            if mask[r, c] == 0: 
                
                # 1. Convert pixel to a SCALED physical coordinate on the target wall
                # This forces the image to be larger than the box so rays hit the walls
                target_x = ((c / img_cols) - 0.5) * TARGET_IMAGE_WIDTH_CM
                target_y = (0.5 - (r / img_rows)) * TARGET_IMAGE_HEIGHT_CM
                target_z = 0.0
                
                # 2. Calculate the ray vector (Target - Light)
                ray_vector = (target_x - Lx, target_y - Ly, target_z - Lz)
                
                # 3. Calculate intersection with the walls
                wall_name, hit_point = calculate_intersection(light_position, ray_vector)
                
                # 4. Punch a hole (0) in the appropriate box wall with a brush size to prevent gaps
                if wall_name is not None:
                    w_row, w_col = map_3d_to_wall_pixel(wall_name, hit_point)
                    
                    # Define a brush size (e.g., 1 means a 3x3 block of pixels will be punched)
                    brush_size = 1 
                    
                    try:
                        # Punch a small neighborhood around the hit point to eliminate gaps
                        for dr in range(-brush_size, brush_size + 1):
                            for dc in range(-brush_size, brush_size + 1):
                                walls[wall_name][w_row + dr, w_col + dc] = 0
                                
                        holes_punched += 1
                    except IndexError:
                        pass # Ignore if the brush falls slightly outside the matrix
                        
    print("-" * 40)
    print(f"[*] Physics Simulation Results:")
    print(f"    - Holes punched in walls: {holes_punched}")
    print(f"    - Rays that fell directly inside the box (no wall hit): {rays_inside_box}")
    print("-" * 40)
    
    return walls