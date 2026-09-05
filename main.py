import os
import cv2
import src.config as cfg
from src.image_processor import run_image_pipeline
from src.ray_tracer import initialize_walls, ray_tracer_algorithm

def main():
    # 1. Define the path to the actual image
    image_path = "inputs/im6.png"
    print(f"[*] Processing actual image: {image_path}")
    
    # 2. Run the image processing pipeline to get the mask
    mask = run_image_pipeline(image_path)
    
    if mask is None:
        print("[!] Error: Mask could not be generated. Check image path.")
        return

    # 3. Initialize the blank walls for the box
    print("[*] Initializing blank walls...")
    blank_walls = initialize_walls()
    
    # 4. Define the light source position from the config
    light_pos = (cfg.LIGHT_X, cfg.LIGHT_Y, cfg.LIGHT_Z)
    
    # 5. Run the ray tracer algorithm to punch holes in the walls
    print("[*] Running Ray Tracer Algorithm...")
    final_walls = ray_tracer_algorithm(blank_walls, light_pos, mask)
    
    # 6. Save the resulting walls as visible images
    output_dir = "outputs/2d_masks"
    os.makedirs(output_dir, exist_ok=True) # Create directory if it doesn't exist
    
    print("[*] Saving final wall masks as images...")
    for wall_name, wall_matrix in final_walls.items():
        
        # The matrix currently contains 0 (hole) and 1 (solid wall).
        # Multiply by 255 to make the solid wall white (255) and holes black (0).
        visible_wall = wall_matrix * 255 
        
        save_path = os.path.join(output_dir, f"{wall_name}_wall.png")
        cv2.imwrite(save_path, visible_wall)
        print(f"    - Saved: {save_path}")

    print("[*] All done! Check the 'outputs/2d_masks' folder to see your generated walls.")

if __name__ == "__main__":
    main()