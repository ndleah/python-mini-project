"""Finding Lanes: Road Lane Detection using OpenCV & NumPy.

This module provides a modular computer vision pipeline to detect road lane
markings in static images, pre-recorded video files, or live camera streams.
It uses Gaussian blurring, Canny edge detection, dynamic Region of Interest
(ROI) masking, Hough Transform line detection, slope-intercept linear
regression averaging, and temporal smoothing to render clear lane boundaries.
"""

import argparse
import os
import sys
from typing import Dict, List, Optional, Tuple, Union

import cv2
import numpy as np


class LaneTracker:
    """Temporal smoothing filter for video and live camera lane detection.

    Maintains an exponential moving average (EMA) of left and right lane
    parameters across consecutive frames to eliminate jitter, and preserves
    lane estimates during brief detection dropouts (e.g. dashed line gaps).
    """

    def __init__(self, alpha: float = 0.2, max_missed_frames: int = 15) -> None:
        """Initialize the lane tracker.

        Args:
            alpha: Weight of the new measurement (0 < alpha <= 1.0).
                   Smaller values produce smoother transitions.
            max_missed_frames: Maximum frames to retain previous lane estimate
                               if no lines are detected before clearing.
        """
        self.alpha = float(alpha)
        self.max_missed_frames = int(max_missed_frames)
        self.left_fit: Optional[Tuple[float, float]] = None
        self.right_fit: Optional[Tuple[float, float]] = None
        self.left_missed: int = 0
        self.right_missed: int = 0

    def update(
        self,
        left_measurement: Optional[Tuple[float, float]],
        right_measurement: Optional[Tuple[float, float]]
    ) -> Tuple[Optional[Tuple[float, float]], Optional[Tuple[float, float]]]:
        """Update tracker state with new measurements from the current frame.

        Args:
            left_measurement: Tuple of (slope, intercept) for left lane, or None.
            right_measurement: Tuple of (slope, intercept) for right lane, or None.

        Returns:
            Tuple of (smoothed_left, smoothed_right) parameters.
        """
        # Update left lane
        if left_measurement is not None:
            if self.left_fit is None:
                self.left_fit = (float(left_measurement[0]), float(left_measurement[1]))
            else:
                s = self.alpha * left_measurement[0] + (1.0 - self.alpha) * self.left_fit[0]
                i = self.alpha * left_measurement[1] + (1.0 - self.alpha) * self.left_fit[1]
                self.left_fit = (float(s), float(i))
            self.left_missed = 0
        else:
            self.left_missed += 1
            if self.left_missed > self.max_missed_frames:
                self.left_fit = None

        # Update right lane
        if right_measurement is not None:
            if self.right_fit is None:
                self.right_fit = (float(right_measurement[0]), float(right_measurement[1]))
            else:
                s = self.alpha * right_measurement[0] + (1.0 - self.alpha) * self.right_fit[0]
                i = self.alpha * right_measurement[1] + (1.0 - self.alpha) * self.right_fit[1]
                self.right_fit = (float(s), float(i))
            self.right_missed = 0
        else:
            self.right_missed += 1
            if self.right_missed > self.max_missed_frames:
                self.right_fit = None

        return self.left_fit, self.right_fit

    def reset(self) -> None:
        """Reset tracker state to initial uninitialized values."""
        self.left_fit = None
        self.right_fit = None
        self.left_missed = 0
        self.right_missed = 0


def make_coordinate(
    image: np.ndarray,
    line_parameters: Union[Tuple[float, float], np.ndarray, List[float]],
    y_min_ratio: float = 0.6,
    y_max_ratio: float = 1.0
) -> Optional[np.ndarray]:
    """Calculate (x1, y1, x2, y2) pixel coordinates from slope and intercept.

    Args:
        image: Source image frame as a NumPy ndarray.
        line_parameters: Tuple or array containing (slope, intercept).
        y_min_ratio: Ratio of frame height for upper line coordinate.
        y_max_ratio: Ratio of frame height for lower line coordinate.

    Returns:
        NumPy array [x1, y1, x2, y2] or None if line is invalid.
    """
    if line_parameters is None:
        return None

    params = np.asarray(line_parameters).ravel()
    if len(params) < 2:
        return None

    slope = float(params[0])
    intercept = float(params[1])

    # Guard against zero slope, NaN, or non-finite values
    if abs(slope) < 1e-4 or not np.isfinite(slope) or not np.isfinite(intercept):
        return None

    height, width = image.shape[:2]
    y1 = int(height * y_max_ratio)
    y2 = int(height * y_min_ratio)

    try:
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
    except (ValueError, OverflowError, ZeroDivisionError):
        return None

    # Clip coordinates within safe display bounds
    x1 = max(-width, min(2 * width, x1))
    x2 = max(-width, min(2 * width, x2))

    return np.array([x1, y1, x2, y2], dtype=np.int32)


def average_lines_intercept(
    image: np.ndarray,
    lines: Optional[np.ndarray],
    min_slope: float = 0.3,
    tracker: Optional[LaneTracker] = None
) -> Optional[np.ndarray]:
    """Average and extrapolate detected Hough line segments into left and right lane lines.

    Separates left and right lane candidates using both slope sign and spatial
    positioning relative to the frame midpoint to prevent cross-lane contamination.
    Optionally smooths estimates across frames using a LaneTracker.

    Args:
        image: Source image frame.
        lines: Array of line segments from cv2.HoughLinesP.
        min_slope: Minimum absolute slope threshold to filter horizontal noise lines.
        tracker: Optional LaneTracker instance for temporal smoothing.

    Returns:
        NumPy array containing coordinates for left and right lanes, or None.
    """
    if lines is None or len(lines) == 0:
        if tracker is not None:
            smooth_left, smooth_right = tracker.update(None, None)
            lane_lines: List[np.ndarray] = []
            if smooth_left is not None:
                line = make_coordinate(image, smooth_left)
                if line is not None:
                    lane_lines.append(line)
            if smooth_right is not None:
                line = make_coordinate(image, smooth_right)
                if line is not None:
                    lane_lines.append(line)
            return np.array(lane_lines, dtype=np.int32) if len(lane_lines) > 0 else None
        return None

    height, width = image.shape[:2]
    midpoint = width / 2.0

    left_fit: List[Tuple[float, float]] = []
    right_fit: List[Tuple[float, float]] = []

    for line in lines:
        coords = line.reshape(4)
        x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])

        # Ignore purely vertical lines to prevent division by zero
        if x1 == x2:
            continue

        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = float(parameters[0])
        intercept = float(parameters[1])

        # Filter out near-horizontal noise lines (crosswalks, shadows)
        if abs(slope) < min_slope:
            continue

        # In image coordinates, y increases downward:
        # Left lane has a negative slope AND lies on the left side of the vehicle/frame
        # Right lane has a positive slope AND lies on the right side of the vehicle/frame
        line_mid_x = (x1 + x2) / 2.0

        if slope < -min_slope and line_mid_x < midpoint:
            left_fit.append((slope, intercept))
        elif slope > min_slope and line_mid_x > midpoint:
            right_fit.append((slope, intercept))

    current_left = tuple(np.average(left_fit, axis=0)) if len(left_fit) > 0 else None
    current_right = tuple(np.average(right_fit, axis=0)) if len(right_fit) > 0 else None

    if tracker is not None:
        target_left, target_right = tracker.update(current_left, current_right)
    else:
        target_left, target_right = current_left, current_right

    lane_lines = []

    if target_left is not None:
        left_line = make_coordinate(image, target_left)
        if left_line is not None:
            lane_lines.append(left_line)

    if target_right is not None:
        right_line = make_coordinate(image, target_right)
        if right_line is not None:
            lane_lines.append(right_line)

    return np.array(lane_lines, dtype=np.int32) if len(lane_lines) > 0 else None


def canny(
    image: np.ndarray,
    low_threshold: int = 50,
    high_threshold: int = 150,
    kernel_size: int = 5
) -> np.ndarray:
    """Apply grayscale conversion, Gaussian blur, and Canny edge detection.

    Args:
        image: Input BGR image array or single-channel grayscale array.
        low_threshold: Lower hysteresis threshold for Canny.
        high_threshold: Upper hysteresis threshold for Canny.
        kernel_size: Gaussian blur kernel size (odd integer).

    Returns:
        Binary edge map as a 2D NumPy array.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    edges = cv2.Canny(blur, low_threshold, high_threshold)
    return edges


def display_lines(
    image: np.ndarray,
    lines: Optional[np.ndarray],
    color: Tuple[int, int, int] = (0, 0, 255),
    thickness: int = 10,
    fill_lane: bool = False,
    fill_color: Tuple[int, int, int] = (0, 255, 0),
    fill_alpha: float = 0.25
) -> np.ndarray:
    """Render detected lane lines onto a blank canvas matching image dimensions.

    Args:
        image: Reference image for dimensions.
        lines: Array of lane line coordinates [[x1, y1, x2, y2], ...].
        color: BGR color tuple for the drawn lines (default: Red (0, 0, 255)).
        thickness: Line thickness in pixels.
        fill_lane: If True and 2 lanes are detected, fills the drivable lane corridor.
        fill_color: BGR color tuple for the filled lane polygon (default: Green).
        fill_alpha: Opacity factor for the filled polygon (0.0 to 1.0).

    Returns:
        Image with rendered lane lines and optional corridor overlay.
    """
    line_image = np.zeros_like(image)

    if lines is not None and len(lines) > 0:
        # If fill_lane requested and two lanes detected, fill drivable corridor
        if fill_lane and len(lines) >= 2:
            l1, l2 = lines[0], lines[1]
            # Order lines from left to right based on bottom x-coordinate
            left_line = l1 if l1[0] < l2[0] else l2
            right_line = l2 if l1[0] < l2[0] else l1

            poly_pts = np.array([
                [
                    [left_line[0], left_line[1]],
                    [left_line[2], left_line[3]],
                    [right_line[2], right_line[3]],
                    [right_line[0], right_line[1]]
                ]
            ], dtype=np.int32)

            poly_mask = np.zeros_like(image)
            cv2.fillPoly(poly_mask, poly_pts, fill_color)
            line_image = cv2.addWeighted(line_image, 1.0, poly_mask, fill_alpha, 0.0)

        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

    return line_image


def roi(
    image: np.ndarray,
    polygons: Optional[np.ndarray] = None
) -> np.ndarray:
    """Apply a Region of Interest (ROI) polygon mask to isolate the road lane area.

    Supports both single-channel (e.g. edge maps) and 3-channel (BGR/RGB) image arrays
    without color channel corruption.

    Args:
        image: Single-channel edge map or 3-channel image.
        polygons: Custom polygon vertices array, or None for dynamic ROI.

    Returns:
        Masked image containing only the region of interest.
    """
    height, width = image.shape[:2]

    if polygons is None:
        # Dynamic triangular ROI proportional to image dimensions
        polygons = np.array([
            [
                (int(width * 0.15), height),
                (int(width * 0.88), height),
                (int(width * 0.45), int(height * 0.35))
            ]
        ], dtype=np.int32)

    mask = np.zeros_like(image)
    fill_color = (255,) * image.shape[2] if image.ndim == 3 else 255
    cv2.fillPoly(mask, polygons, fill_color)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def process_frame(
    frame: np.ndarray,
    min_slope: float = 0.3,
    return_intermediates: bool = False,
    fill_lane: bool = False,
    tracker: Optional[LaneTracker] = None
) -> Union[Tuple[np.ndarray, Optional[np.ndarray]], Tuple[np.ndarray, Optional[np.ndarray], Dict[str, np.ndarray]]]:
    """Execute the full lane detection pipeline on a single frame.

    Pipeline stages:
    1. Canny edge detection (Grayscale -> Gaussian Blur -> Canny)
    2. Dynamic Region of Interest (ROI) masking
    3. Hough Transform line detection
    4. Slope-intercept averaging & spatial filtering
    5. Line rendering & alpha blending with the original frame

    Args:
        frame: BGR input image frame.
        min_slope: Minimum slope threshold to filter noise lines.
        return_intermediates: If True, returns a dict of intermediate pipeline stages.
        fill_lane: If True, fills the drivable lane corridor between lines.
        tracker: Optional LaneTracker instance for video temporal smoothing.

    Returns:
        (combo_image, averaged_lines) or (combo_image, averaged_lines, intermediates_dict)
    """
    canny_image = canny(frame)
    cropped_image = roi(canny_image)
    lines = cv2.HoughLinesP(
        cropped_image,
        rho=2,
        theta=np.pi / 180,
        threshold=100,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=5
    )
    averaged_lines = average_lines_intercept(frame, lines, min_slope=min_slope, tracker=tracker)
    line_image = display_lines(frame, averaged_lines, fill_lane=fill_lane)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1.0, 0.0)

    if return_intermediates:
        intermediates = {
            "canny": canny_image,
            "roi": cropped_image,
            "line_image": line_image,
            "raw_lines": lines
        }
        return combo_image, averaged_lines, intermediates

    return combo_image, averaged_lines


def process_image(
    image_path: str,
    output_path: Optional[str] = None,
    show: bool = True,
    fill_lane: bool = False
) -> Optional[np.ndarray]:
    """Process a static image file and detect road lanes.

    Args:
        image_path: Path to the input image.
        output_path: Optional path to save the annotated result image.
        show: If True, displays the result window using OpenCV GUI.
        fill_lane: If True, fills the drivable corridor between lane lines.

    Returns:
        Annotated image array or None if file cannot be read.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.", file=sys.stderr)
        return None

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image from '{image_path}'.", file=sys.stderr)
        return None

    combo_image, _ = process_frame(image, fill_lane=fill_lane)

    if output_path:
        cv2.imwrite(output_path, combo_image)
        print(f"Saved processed image to: {output_path}")

    if show:
        cv2.imshow("Finding Lanes - Image Result", combo_image)
        print("Press any key to close the window...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return combo_image


def process_video(
    source: Union[str, int],
    output_path: Optional[str] = None,
    show: bool = True,
    fill_lane: bool = False,
    smooth: bool = True
) -> bool:
    """Process a video file or live camera stream frame-by-frame.

    Args:
        source: File path to a video file, or integer webcam device index (e.g., 0).
        output_path: Optional output video path (e.g. 'output.mp4').
        show: If True, displays live video frames using OpenCV GUI.
        fill_lane: If True, highlights the drivable lane corridor between lines.
        smooth: If True, uses temporal smoothing (LaneTracker) to stabilize lines.

    Returns:
        True if video was processed successfully, False on error.
    """
    if isinstance(source, str) and not os.path.exists(source):
        print(f"Error: Video file '{source}' not found.", file=sys.stderr)
        return False

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Error: Could not open video source '{source}'.", file=sys.stderr)
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not np.isfinite(fps) or fps <= 0:
        fps = 30.0

    delay_ms = max(1, int(1000 / fps))

    writer = None
    if output_path:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    tracker = LaneTracker() if smooth else None

    print("Processing video stream... Press 'q' to stop.")
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            combo_image, _ = process_frame(frame, fill_lane=fill_lane, tracker=tracker)

            if writer:
                writer.write(combo_image)

            if show:
                cv2.imshow("Finding Lanes - Video Stream", combo_image)
                if cv2.waitKey(delay_ms) & 0xFF == ord("q"):
                    print("User interrupted video playback.")
                    break
        return True
    finally:
        cap.release()
        if writer:
            writer.release()
            print(f"Saved processed video to: {output_path}")
        if show:
            cv2.destroyAllWindows()


def resolve_asset_path(filename: str) -> str:
    """Resolve file path relative to current script directory or workspace root."""
    dir_path = os.path.dirname(os.path.abspath(__file__))
    direct_path = os.path.join(dir_path, filename)
    if os.path.exists(direct_path):
        return direct_path

    relative_path = os.path.join("Finding_Lanes", filename)
    if os.path.exists(relative_path):
        return relative_path

    return filename


def main() -> None:
    """Parse CLI arguments and execute the lane finding pipeline."""
    parser = argparse.ArgumentParser(
        description="Finding Lanes: Detect and highlight road lane markings in images and video streams."
    )
    parser.add_argument(
        "-i", "--image",
        type=str,
        default=None,
        help="Path to an input image file to process."
    )
    parser.add_argument(
        "-v", "--video",
        type=str,
        default=None,
        help="Path to an input video file to process."
    )
    parser.add_argument(
        "-c", "--camera",
        type=int,
        default=None,
        help="Webcam device index (e.g. 0 for built-in camera)."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Path to save the processed image or video output."
    )
    parser.add_argument(
        "--fill-lane",
        action="store_true",
        help="Fill and highlight the drivable lane corridor between detected lane lines."
    )
    parser.add_argument(
        "--no-smooth",
        action="store_true",
        help="Disable temporal smoothing filter during video/webcam processing."
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Run in headless mode without displaying GUI windows."
    )

    args = parser.parse_args()
    show = not args.no_show
    smooth = not args.no_smooth

    if args.image:
        res = process_image(args.image, output_path=args.output, show=show, fill_lane=args.fill_lane)
        if res is None:
            sys.exit(1)
    elif args.camera is not None:
        success = process_video(args.camera, output_path=args.output, show=show, fill_lane=args.fill_lane, smooth=smooth)
        if not success:
            sys.exit(1)
    elif args.video:
        success = process_video(args.video, output_path=args.output, show=show, fill_lane=args.fill_lane, smooth=smooth)
        if not success:
            sys.exit(1)
    else:
        # Default behavior: run bundled video.mp4 or fallback to picture.jpg
        default_video = resolve_asset_path("video.mp4")
        default_image = resolve_asset_path("picture.jpg")

        if os.path.exists(default_video):
            success = process_video(default_video, output_path=args.output, show=show, fill_lane=args.fill_lane, smooth=smooth)
            if not success:
                sys.exit(1)
        elif os.path.exists(default_image):
            res = process_image(default_image, output_path=args.output, show=show, fill_lane=args.fill_lane)
            if res is None:
                sys.exit(1)
        else:
            print("Error: No input source provided and default assets (video.mp4, picture.jpg) not found.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
