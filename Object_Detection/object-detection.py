import os
import sys
import cv2

def run_object_detection(source: str = None):
    """Run YOLO object detection on video stream or static image."""
    try:
        import torch
        from ultralytics import YOLO
    except ImportError:
        print("Error: 'ultralytics' and 'torch' packages are required for object detection.")
        return

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    try:
        model = YOLO('yolov9c.pt')
        model.to(device)
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        return

    script_dir = os.path.dirname(__file__)
    fallback_image = os.path.join(script_dir, "image.png")

    # If source is an image path or webcam index
    if source is None:
        source_val = 0  # Default webcam
    else:
        source_val = source

    cap = cv2.VideoCapture(source_val)

    if not cap.isOpened():
        print(f"Notice: Could not open video source '{source_val}'. Testing fallback image...")
        if os.path.exists(fallback_image):
            frame = cv2.imread(fallback_image)
            if frame is not None:
                results = model(frame)
                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        label_id = int(box.cls[0].item())
                        confidence = box.conf[0].item()
                        class_label = model.names[label_id]
                        label_text = f"{class_label}: {confidence:.2f}"
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(frame, label_text, (int(x1), max(15, int(y1) - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                output_path = os.path.join(script_dir, "detection_result.png")
                cv2.imwrite(output_path, frame)
                print(f"Object detection on static image saved to: {output_path}")
                try:
                    cv2.imshow('Object Detection Result', frame)
                    cv2.waitKey(2000)
                    cv2.destroyAllWindows()
                except Exception:
                    pass
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Video stream ended or frame unreadable.")
            break

        results = model(frame)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                label_id = int(box.cls[0].item())
                confidence = box.conf[0].item()
                class_label = model.names[label_id]
                label_text = f"{class_label}: {confidence:.2f}"

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label_text, (int(x1), max(15, int(y1) - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        try:
            cv2.imshow('Real-Time Object Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
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
    run_object_detection(src)

if __name__ == "__main__":
    main()

