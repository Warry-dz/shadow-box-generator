# src/image_processor.py

import cv2

def run_image_pipeline(image_path):
    """
    Loads the image, converts it to black and white, 
    shows it to the user, and returns the mask.
    """
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"[!] Error: Image not found at {image_path}")
        return None

    # Show original image
    cv2.imshow("1 - Original Image", img)

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply binary threshold
    _, bw_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

    # Show black and white mask
    cv2.imshow("2 - Black and White Image", bw_img)

    print("[*] Press any key on the keyboard to close the windows and start Ray Tracing...")
    
    # Wait for the user to press a key, then close windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return bw_img