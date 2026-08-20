import os
import sys

def check_dependencies():
    try:
        import cv2
        import numpy as np
        return cv2, np
    except ImportError:
        print("Error: OpenCV and NumPy are required. Install them via 'pip install opencv-python numpy'.")
        sys.exit(1)

def compare_images(image1_path: str, image2_path: str, diff_output: str = "diff.png", target_size=(500, 500)):
    cv2, np = check_dependencies()

    if not os.path.exists(image1_path):
        print(f"Error: Image 1 not found at '{image1_path}'.")
        return False, 0.0, None

    if not os.path.exists(image2_path):
        print(f"Error: Image 2 not found at '{image2_path}'.")
        return False, 0.0, None

    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    if image1 is None or image2 is None:
        print("Error: Failed to load one or both images.")
        return False, 0.0, None

    image1_resized = cv2.resize(image1, target_size)
    image2_resized = cv2.resize(image2, target_size)

    difference = cv2.subtract(image1_resized, image2_resized)
    b, g, r = cv2.split(difference)

    total_pixels = target_size[0] * target_size[1] * 3
    non_zero_pixels = np.count_nonzero(difference)
    similarity = round(100.0 * (1.0 - (non_zero_pixels / total_pixels)), 2)

    is_identical = (cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0)

    if is_identical:
        print(f"The images are identical! (Similarity: {similarity}%)")
        return True, similarity, None
    else:
        conv_hsv_gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(
            conv_hsv_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )
        difference[mask != 255] = [0, 0, 255]

        cv2.imwrite(diff_output, difference)
        print(f"The images are different. (Similarity: {similarity}%)")
        print(f"Difference mask saved to: '{diff_output}'")
        return False, similarity, diff_output

def main():
    if len(sys.argv) >= 3:
        image1_path = sys.argv[1]
        image2_path = sys.argv[2]
        diff_output = sys.argv[3] if len(sys.argv) > 3 else "diff.png"
    else:
        print("--- Image Comparator ---")
        image1_path = input("Enter path to first image: ").strip()
        image2_path = input("Enter path to second image: ").strip()
        diff_output = "diff.png"

    if not image1_path or not image2_path:
        print("Error: Both image paths must be provided.")
        sys.exit(1)

    compare_images(image1_path, image2_path, diff_output)

if __name__ == "__main__":
    main()

