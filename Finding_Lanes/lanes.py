import cv2
import numpy as np


# 1. Convert image to grayscale
# 2. Blur the image
# 3. Detect edges
# 4. Create a region-of-interest mask
# 5. Apply the mask
# 6. Detect lines using Hough Transform
# 7. Average the detected lines
# 8. Display the detected lane lines


def make_coordinate(image, line_parameters):
    """Convert slope/intercept into line coordinates."""

    slope, intercept = line_parameters

    # Protect against invalid slope/intercept values
    if not np.isfinite(slope) or not np.isfinite(intercept):
        return None

    # Protect against zero or nearly-zero slope
    if abs(slope) < 1e-3:
        return None

    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2], dtype=int)


def average_lines_intercept(image, lines):
    """Average detected lines into left and right lane lines."""

    left_fit = []
    right_fit = []

    # No lines detected
    if lines is None:
        return np.empty((0, 4), dtype=int)

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        # Ignore vertical lines because polyfit can become unstable
        if x1 == x2:
            continue

        parameters = np.polyfit(
            (x1, x2),
            (y1, y2),
            1
        )

        slope = parameters[0]
        intercept = parameters[1]

        # Ignore invalid values
        if not np.isfinite(slope) or not np.isfinite(intercept):
            continue

        # Ignore horizontal/nearly-horizontal lines
        if abs(slope) < 1e-3:
            continue

        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    averaged_lines = []

    # Average left lane
    if left_fit:
        left_fit_average = np.average(left_fit, axis=0)
        left_line = make_coordinate(image, left_fit_average)

        if left_line is not None:
            averaged_lines.append(left_line)

    # Average right lane
    if right_fit:
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_coordinate(image, right_fit_average)

        if right_line is not None:
            averaged_lines.append(right_line)

    if not averaged_lines:
        return np.empty((0, 4), dtype=int)

    return np.array(averaged_lines, dtype=int)


def canny(image):
    """Convert image to edges using the Canny algorithm."""

    # OpenCV reads video frames in BGR format
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blur,
        50,
        150
    )

    return edges


def display_lines(image, lines):
    """Draw detected lane lines on a blank image."""

    line_image = np.zeros_like(image)

    if lines is not None:
        for line in lines:

            if line is None:
                continue

            x1, y1, x2, y2 = line

            cv2.line(
                line_image,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 0, 255),
                10
            )

    return line_image


def roi(image):
    """Create a triangular region of interest."""

    height = image.shape[0]
    width = image.shape[1]

    polygons = np.array([
        [
            (int(width * 0.10), height),
            (int(width * 0.90), height),
            (int(width * 0.50), int(height * 0.60))
        ]
    ])

    mask = np.zeros_like(image)

    cv2.fillPoly(
        mask,
        polygons,
        255
    )

    masked_image = cv2.bitwise_and(
        image,
        mask
    )

    return masked_image


# ---------------------------------------------------------
# VIDEO
# ---------------------------------------------------------

# Because lanes.py and video.mp4 are in the same folder,
# use simply "video.mp4".
cap = cv2.VideoCapture("video.mp4")


# Check whether the video was opened successfully
if not cap.isOpened():
    print("ERROR: Could not open video.mp4")
    print("Make sure video.mp4 is inside the Finding_Lanes folder.")
    raise SystemExit


while cap.isOpened():

    # Read one frame
    ret, frame = cap.read()

    # Stop safely when video ends or frame cannot be read
    if not ret or frame is None:
        break

    # Detect edges
    canny_image = canny(frame)

    # Keep only the road region
    cropped_image = roi(canny_image)

    # Detect lines
    lines = cv2.HoughLinesP(
        cropped_image,
        2,
        np.pi / 180,
        100,
        np.array([]),
        minLineLength=40,
        maxLineGap=5
    )

    # Average the detected lines
    averaged_lines = average_lines_intercept(
        frame,
        lines
    )

    # Draw lane lines
    line_image = display_lines(
        frame,
        averaged_lines
    )

    # Combine original video and lane lines
    combo_image = cv2.addWeighted(
        frame,
        0.8,
        line_image,
        1,
        1
    )

    # Display result
    cv2.imshow(
        "Lane Detection",
        combo_image
    )

    # Press Q to quit
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break


# Release resources
cap.release()
cv2.destroyAllWindows()