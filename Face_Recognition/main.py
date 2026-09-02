import os
import sys
import cv2

def detect_faces(source=0):
    """Detect faces using OpenCV Haar Cascades from camera or image file."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # If source is an image file path
    if isinstance(source, str) and os.path.exists(source):
        print(f"Detecting faces in static image: '{source}'")
        image = cv2.imread(source)
        if image is None:
            print(f"Error: Unable to read image '{source}'")
            return

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print(f"Found {len(faces)} face(s) in image.")

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 3)

        cv2.imshow("Face Recognition Result", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return len(faces)

    # Webcam video stream mode
    print(f"Opening camera stream (device: {source})... Press 'q' to exit.")
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Notice: Camera index {source} could not be opened. Pass an image file path to test.")
        return

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("End of video stream or camera disconnected.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        cv2.imshow("Face Recognition Camera Stream", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    src_arg = sys.argv[1] if len(sys.argv) > 1 else 0
    detect_faces(src_arg)

if __name__ == '__main__':
    main()

