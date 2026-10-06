"""Finding Lanes - Pipeline Visualizer.

This utility visualizes each stage of the computer vision lane detection pipeline
(Original Image, Canny Edges, ROI Masked Edges, and Final Lane Overlay)
side-by-side using Matplotlib.
"""

import argparse
import os
import sys

import cv2
import matplotlib.pyplot as plt

# Import core lane detection functions
try:
    from lanes import process_frame, resolve_asset_path
except ImportError:
    from Finding_Lanes.lanes import process_frame, resolve_asset_path


def visualize_pipeline(
    image_path: str,
    output_path: str = None,
    show: bool = True,
    fill_lane: bool = False
) -> bool:
    """Visualize all intermediate stages of the lane detection pipeline.

    Args:
        image_path: Path to the input image.
        output_path: Optional path to save the generated subplot figure.
        show: Whether to display the plot interactively.
        fill_lane: Whether to fill the drivable corridor between lane lines.

    Returns:
        True if visualization completed successfully, False otherwise.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image '{image_path}' does not exist.", file=sys.stderr)
        return False

    # Read image using OpenCV (BGR format)
    bgr_img = cv2.imread(image_path)
    if bgr_img is None:
        print(f"Error: Failed to read image from '{image_path}'.", file=sys.stderr)
        return False

    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

    # Process frame and retrieve intermediate stages
    combo_bgr, lanes, intermediates = process_frame(
        bgr_img,
        return_intermediates=True,
        fill_lane=fill_lane
    )
    combo_rgb = cv2.cvtColor(combo_bgr, cv2.COLOR_BGR2RGB)

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle("Finding Lanes - Computer Vision Pipeline Stages", fontsize=16, fontweight="bold")

    # 1. Original Image
    axes[0, 0].imshow(rgb_img)
    axes[0, 0].set_title("1. Original Image (RGB)", fontsize=12)
    axes[0, 0].axis("off")

    # 2. Canny Edge Detection
    axes[0, 1].imshow(intermediates["canny"], cmap="gray")
    axes[0, 1].set_title("2. Canny Edge Detection", fontsize=12)
    axes[0, 1].axis("off")

    # 3. Region of Interest (ROI) Masked
    axes[1, 0].imshow(intermediates["roi"], cmap="gray")
    axes[1, 0].set_title("3. Dynamic Region of Interest (ROI)", fontsize=12)
    axes[1, 0].axis("off")

    # 4. Final Lane Overlay
    axes[1, 1].imshow(combo_rgb)
    axes[1, 1].set_title("4. Hough Lines & Averaged Lane Detection", fontsize=12)
    axes[1, 1].axis("off")

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight")
        print(f"Pipeline stages figure saved to: {output_path}")

    if show:
        plt.show()
    else:
        plt.close(fig)

    return True


def main() -> None:
    """Parse CLI arguments and run visualization."""
    parser = argparse.ArgumentParser(
        description="Finding Lanes: Multi-stage Computer Vision Pipeline Visualizer."
    )
    parser.add_argument(
        "-i", "--image",
        type=str,
        default=None,
        help="Path to an input image (default: picture.jpg)."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Path to save the pipeline stages plot image."
    )
    parser.add_argument(
        "--fill-lane",
        action="store_true",
        help="Highlight the drivable corridor between lanes in the visualization."
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Run without displaying the Matplotlib window."
    )

    args = parser.parse_args()
    image_path = args.image or resolve_asset_path("picture.jpg")
    success = visualize_pipeline(
        image_path,
        output_path=args.output,
        show=not args.no_show,
        fill_lane=args.fill_lane
    )
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
