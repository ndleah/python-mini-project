# Description

### Bug Summary & Feature Limitations

In `Finding_Lanes/lanes.py`, several critical computer vision bugs, filtering defects, missing temporal tracking, and CLI limitations affect the reliability of the lane detection pipeline:

1. **Color Channel Zeroing in `roi()` for Multi-Channel Images**:
   - The docstring for `roi(image, polygons=None)` states that it accepts both single-channel edge maps and 3-channel color images:
     ```python
     Args:
         image: Single-channel edge map or 3-channel image.
     ```
   - However, the mask is created with:
     ```python
     mask = np.zeros_like(image)
     cv2.fillPoly(mask, polygons, 255)
     masked_image = cv2.bitwise_and(image, mask)
     ```
   - When `image` is a 3-channel BGR/RGB image, passing the scalar `255` to `cv2.fillPoly` sets only channel 0 (blue) to 255, while leaving channel 1 (green) and channel 2 (red) as 0. Consequently, `cv2.bitwise_and` zeroes out the green and red channels entirely (`[200, 200, 200]` becomes `[200, 0, 0]`), corrupting color images passed to the ROI mask.

2. **Unconstrained Slope Averaging & Cross-Lane Contamination**:
   - In `average_lines_intercept()`, candidate line segments are partitioned into `left_fit` and `right_fit` solely based on the mathematical sign of the slope:
     ```python
     if slope < -min_slope:
         left_fit.append((slope, intercept))
     elif slope > min_slope:
         right_fit.append((slope, intercept))
     ```
   - Road scenes frequently have shadows, road wear, dashed divider lines, or guardrails on the right half of the road that have a negative slope. Because there was no spatial check against the vehicle/image midpoint, these right-side artifacts were averaged into `left_fit`, severely distorting the left lane line and causing it to cut diagonally across the driving path.

3. **Frame-to-Frame Video Jitter & Dash Dropouts (Missing Temporal Tracking)**:
   - On video streams (`video.mp4` or live webcam), individual frames with dashed road markings frequently experience brief detection dropouts (when the vehicle is between dashes or under uneven lighting).
   - Because each frame was processed completely statelessly, lane lines would flicker, disappear for isolated frames, or violently jitter. There was no exponential moving average (EMA) filter or tracking state to stabilize lines across frames.

4. **Unintended Constant Brightness Offset in `cv2.addWeighted`**:
   - In `process_frame()`:
     ```python
     combo_image = cv2.addWeighted(frame, 0.8, line_image, 1.0, 1.0)
     ```
   - The 5th parameter `gamma=1.0` adds a constant scalar offset of +1 to every pixel in the entire image. Standard alpha blending requires `gamma=0.0`.

5. **Silently Swallowed CLI Errors (Zero Exit Code on Failure)**:
   - When a user provided an invalid file path via CLI (e.g., `python lanes.py --image missing.jpg`), the script printed an error message to stderr but terminated with return code `0`. CI/CD pipelines and automated batch scripts would falsely evaluate the execution as successful.

6. **Missing `requirements.txt`**:
   - `README.md` instructed users to run `pip install -r requirements.txt`, but no `requirements.txt` existed in `Finding_Lanes/`, resulting in `FileNotFoundError`.

7. **Missing Drivable Corridor Visualization Feature**:
   - Standard lane detection systems highlight the drivable lane corridor between the left and right boundary lines. Adding a `--fill-lane` option significantly improves project presentation and utility.

---

## Type of issue

- [x] Bug
- [x] Feature (Enhancement)
- [x] Documentation

---

## Checklist:

- [x] I have read the project guidelines.
- [x] I have checked previous issues to avoid duplicates.
- [x] This issue will be meaningful for the project.
- [x] I have added steps to reproduce the bug
- [x] I have proposed a possible solution for the bug

---

## Steps to Reproduce the Bug:

1. **Verify 3-Channel ROI Color Zeroing Bug**:
   ```python
   import numpy as np
   import cv2
   from lanes import roi

   img = np.full((100, 100, 3), 200, dtype=np.uint8)
   poly = np.array([[[10, 10], [90, 10], [50, 90]]], dtype=np.int32)
   result = roi(img, poly)
   print("Pixel value inside polygon:", result[30, 50])
   ```
   **Observed Output**:
   ```python
   Pixel value inside polygon: [200   0   0]
   ```
   Notice channels 1 and 2 (green and red) are completely zeroed out instead of preserving `[200, 200, 200]`.

2. **Verify Cross-Lane Contamination**:
   Run `average_lines_intercept` with a genuine left segment on the left half and an erroneous negative-slope segment on the right half:
   ```python
   import numpy as np
   from lanes import average_lines_intercept

   frame = np.zeros((720, 1280, 3), dtype=np.uint8)
   left_seg = [[300, 720, 580, 450]]      # Genuine left lane
   corrupt_seg = [[1100, 700, 1150, 600]]  # Negative slope on right side
   lines = np.array([left_seg, corrupt_seg])

   lanes = average_lines_intercept(frame, lines)
   print("Detected lanes count:", len(lanes))
   ```
   **Observed Output**:
   `corrupt_seg` is averaged directly into the left lane fit, distorting its trajectory across the vehicle center.

3. **Verify Missing `requirements.txt`**:
   ```sh
   cd Finding_Lanes
   pip install -r requirements.txt
   ```
   **Observed Output**:
   `ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`

---

## Proposed Solution:

1. **Fix `roi()`**: Use `fill_color = (255,) * image.shape[2] if image.ndim == 3 else 255` so all color channels are preserved in multi-channel inputs.
2. **Add Spatial Midpoint Filtering in `average_lines_intercept()`**: Ensure left segments satisfy `(x1 + x2) / 2 < midpoint` and right segments satisfy `(x1 + x2) / 2 > midpoint`.
3. **Implement `LaneTracker` Class**: Add an exponential moving average (EMA) filter with dropout retention buffer to eliminate video jitter and preserve lane stability.
4. **Fix `cv2.addWeighted`**: Change `gamma` from `1.0` to `0.0`.
5. **Add Drivable Corridor Visualization (`--fill-lane`)**: Draw a semi-transparent filled polygon between detected lane lines.
6. **Fix CLI Exit Codes**: Return exit code 1 when input files cannot be found or read.
7. **Create `requirements.txt`**: Specify `opencv-python`, `numpy`, and `matplotlib`.
8. **Add Comprehensive Unit Tests**: Expand `test_lanes.py` to 22 test cases covering all edge cases, color preservation, EMA smoothing, and corridor fill.
