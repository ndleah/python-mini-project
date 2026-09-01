import os
import sys

def detect_shapes(image_path=None):
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("Error: OpenCV ('cv2') and 'numpy' are required.")
        return

    if image_path is None:
        image_path = os.path.join(os.path.dirname(__file__), 'shape.jpg')

    if not os.path.exists(image_path):
        print(f"Notice: '{image_path}' not found. Generating sample image...")
        # Create a synthetic image with shapes
        img = np.zeros((400, 500, 3), dtype=np.uint8) + 255
        cv2.rectangle(img, (50, 50), (150, 150), (0, 0, 0), -1)      # Square
        cv2.rectangle(img, (200, 50), (380, 120), (0, 0, 0), -1)     # Rectangle
        cv2.circle(img, (100, 280), 50, (0, 0, 0), -1)               # Circle
        pts = np.array([[300, 200], [220, 350], [380, 350]], np.int32) # Triangle
        cv2.drawContours(img, [pts], 0, (0, 0, 0), -1)
        cv2.imwrite(image_path, img)

    IMAGE = cv2.imread(image_path)
    if IMAGE is None:
        print(f"Error: Could not read image at '{image_path}'.")
        return

    GREYSCALE = cv2.cvtColor(IMAGE, cv2.COLOR_BGR2GRAY)
    _, PARAM2 = cv2.threshold(GREYSCALE, 127, 255, cv2.THRESH_BINARY_INV)
    CONTOURS, _ = cv2.findContours(PARAM2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    RECTANGLES = 0
    SQUARES = 0
    TRIANGLES = 0
    CIRCLES = 0

    for cnt in CONTOURS:
        area = cv2.contourArea(cnt)
        if area < 100:
            continue

        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        vertices = len(approx)

        if vertices == 3:
            TRIANGLES += 1
            cv2.drawContours(IMAGE, [cnt], -1, (255, 0, 0), 3)
        elif vertices == 4:
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = float(w) / h
            if 0.95 <= ratio <= 1.05:
                SQUARES += 1
                cv2.drawContours(IMAGE, [cnt], -1, (0, 255, 0), 3)
            else:
                RECTANGLES += 1
                cv2.drawContours(IMAGE, [cnt], -1, (0, 165, 255), 3)
        elif vertices > 6:
            CIRCLES += 1
            cv2.drawContours(IMAGE, [cnt], -1, (0, 0, 255), 3)

    cv2.putText(IMAGE, f"Squares: {SQUARES}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(IMAGE, f"Rectangles: {RECTANGLES}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
    cv2.putText(IMAGE, f"Triangles: {TRIANGLES}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(IMAGE, f"Circles: {CIRCLES}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    print(f"Shape Recognition Results -> Squares: {SQUARES}, Rectangles: {RECTANGLES}, Triangles: {TRIANGLES}, Circles: {CIRCLES}")

    try:
        cv2.imshow("Shape Recognition", IMAGE)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    except Exception:
        pass

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    detect_shapes(path)

if __name__ == '__main__':
    main()