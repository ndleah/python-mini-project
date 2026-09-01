import os
import sys
import time
import cv2

def run_motion_detection(video_path: str = None):
    try:
        import mediapipe as mp
    except ImportError:
        print("Error: 'mediapipe' and 'opencv-python' are required for Motion Detection.")
        return

    script_dir = os.path.dirname(__file__)
    if video_path is None:
        video_path = os.path.join(script_dir, 'workout.mp4')

    if not os.path.exists(video_path):
        print(f"Notice: Video file '{video_path}' not found. Defaulting to webcam (0)...")
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    pTime = 0

    print("Starting motion pose detection... Press 'q' to quit.")

    while True:
        success, img = cap.read()
        if not success or img is None:
            print("Video playback completed or frame unreadable.")
            break

        height, width, _ = img.shape
        max_width = 1000
        max_height = 800
        scale = min(max_width / width, max_height / height)
        img = cv2.resize(img, None, fx=scale, fy=scale)

        # Convert OpenCV BGR image to RGB for MediaPipe Pose processing
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pose.process(imgRGB)

        if result.pose_landmarks:
            mpDraw.draw_landmarks(
                img,
                result.pose_landmarks,
                mpPose.POSE_CONNECTIONS,
                landmark_drawing_spec=mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2)
            )

        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime

        cv2.putText(img, f"FPS : {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        try:
            cv2.imshow("Motion Detection Pose Tracking", img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        except Exception:
            break

    cap.release()
    try:
        cv2.destroyAllWindows()
    except Exception:
        pass

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    run_motion_detection(src)

if __name__ == '__main__':
    main()