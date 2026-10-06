# Description

This Pull Request addresses critical computer vision bugs, filtering defects, missing temporal stabilization, and CLI limitations in the `Finding_Lanes` project:

1. **Fix Multi-Channel Color Corruption in `roi()` Mask**:
   - Resolved bug where `cv2.fillPoly(mask, polygons, 255)` applied integer scalar `255`, which only populated channel 0 (blue) and wiped out channels 1 (green) and 2 (red) on 3-channel color images.
   - Dynamically adapts mask fill value: `(255,) * channels` for multi-channel frames, preserving full RGB/BGR color data.

2. **Fix Unconstrained Slope Averaging & Cross-Lane Contamination**:
   - In `average_lines_intercept()`, segments were previously segregated solely based on slope signs (`slope < -min_slope` vs `slope > min_slope`).
   - Added spatial midpoint constraints (`line_mid_x < midpoint` for left lanes, `line_mid_x > midpoint` for right lanes). This prevents negative-slope noise markings, shadows, or guardrails on the right half of the road from contaminating the left lane model.

3. **Add Temporal Lane Tracking & Smoothing (`LaneTracker`)**:
   - Introduced the `LaneTracker` class using an Exponential Moving Average (EMA) filter to eliminate frame-to-frame video jitter.
   - Built in a dropout retention buffer (`max_missed_frames=15`) so that brief gaps between dashed road lane markings no longer cause the lane line to flicker or disappear.

4. **Add Drivable Lane Corridor Visualization (`--fill-lane`)**:
   - Added `--fill-lane` CLI flag and parameter to render a semi-transparent filled polygon between the left and right lane boundaries, highlighting the vehicle's drivable lane corridor.

5. **Fix Gamma Offset (+1 Brightness Shift) in `cv2.addWeighted`**:
   - Changed `gamma=1.0` to standard `gamma=0.0` in `process_frame()` to avoid artificially washing out and brightening image frames.

6. **Fix CLI Exit Codes and Error Handling**:
   - Replaced silent 0-exit returns with `sys.exit(1)` when input files or video streams are invalid or not found, ensuring compatibility with CI/CD and automated scripting pipelines.
   - Synchronized GUI video playback delay with native video FPS.

7. **Add Dependencies Specification (`requirements.txt`)**:
   - Created `requirements.txt` specifying `opencv-python>=4.5.0`, `numpy>=1.20.0`, and `matplotlib>=3.3.0`.

8. **Comprehensive Automated Unit Test Suite (`test_lanes.py`)**:
   - Expanded unit tests from 14 to 22 test cases, testing 3-channel color preservation, spatial cross-contamination rejection, EMA smoothing, dropout retention, drivable corridor rendering, and missing-file error handling.

9. **Documentation Overhaul (`README.md`)**:
   - Updated documentation with new CLI options (`--fill-lane`, `--no-smooth`, `--no-show`), installation instructions, and updated project structure.

---

Fixes #603

- [x] Issue_no: #603
- [ ] Not applicable 

## Type of change

Choosing one or more options from the following as per the nature of your Pull request:

- [ ] New project insert
- [x] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [x] Documentation Update

## Project

- #### **Your Project Name:** Finding Lanes - Computer Vision Lane Detection

- #### **Short Description:** Real-time road lane detection and drivable corridor visualization using OpenCV and NumPy, featuring Canny edge detection, dynamic ROI, Hough transform, slope-intercept regression, and temporal EMA smoothing.

# Checklist:

Please tick all the boxes that are fulfilled by your Pull Request.

- [x] I have named my files and folder, according to this project's guidelines.
- [x] My code follows the style guidelines of this project.
- [x] I have commented on my code, particularly in hard-to-understand areas.
- [x] I have created a helpful and easy to understand `README.md`, according to the given [`README_TEMPLATE.`](https://github.com/nduongthucanh/python-mini-project/blob/master/README_TEMPLATE.md)
- [x] My changes do not produce any warnings.
