import os
import sys
import shutil
from PIL import Image

def is_image(file_path: str) -> bool:
    """Check if file can be opened as an image using Pillow context manager."""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except (IOError, SyntaxError, Exception):
        return False

def resize_images(source_dir: str = "source", target_dir: str = "resized", ratio: float = 1.0) -> int:
    """Resize all image files in source_dir and save to target_dir."""
    if not os.path.exists(source_dir):
        print(f"Directory '{source_dir}' does not exist. Creating empty '{source_dir}' directory.")
        os.makedirs(source_dir, exist_ok=True)
        return 0

    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    resized_count = 0
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path) and is_image(file_path):
            try:
                with Image.open(file_path) as im:
                    filename_without_ext, ext = os.path.splitext(filename)
                    new_width = max(1, round(im.size[0] * ratio))
                    new_height = max(1, round(im.size[1] * ratio))

                    resized_im = im.resize((new_width, new_height))
                    out_path = os.path.join(target_dir, f"{filename_without_ext}{ext}")
                    resized_im.save(out_path)
                    resized_count += 1
                    print(f"Resized: {filename} ({im.size[0]}x{im.size[1]} -> {new_width}x{new_height}) -> {out_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"Completed! Resized {resized_count} image(s).")
    return resized_count

def main():
    source = sys.argv[1] if len(sys.argv) > 1 else "source"
    target = sys.argv[2] if len(sys.argv) > 2 else "resized"
    try:
        ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    except ValueError:
        ratio = 1.0

    resize_images(source, target, ratio)

if __name__ == '__main__':
    main()

