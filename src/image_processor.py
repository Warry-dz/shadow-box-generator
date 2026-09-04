import cv2

def apply_black_and_white(image_path):
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Image not found at {image_path}")
        return

    cv2.imshow("1 - Original Image", img)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    _, bw_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

    cv2.imshow("2 - Black and White Image", bw_img)

    print("Press any key to close the windows...")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    apply_black_and_white("inputs/im1.png")