import os
import sys
from PIL import Image

def compress_image(image_path: str, quality: int = 50, output_path: str = None) -> str:
    """Compress a JPEG or PNG image safely."""
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return None

    filename, file_ext = os.path.splitext(image_path)
    file_ext_lower = file_ext.lower()

    if not output_path:
        output_path = f"{filename}_compressed{file_ext_lower}"

    img = Image.open(image_path)

    if file_ext_lower in (".jpeg", ".jpg"):
        img.save(
            output_path,
            "JPEG",
            optimize=True,
            quality=quality
        )
    elif file_ext_lower == ".png":
        # Convert to adaptive 256-color palette for PNG optimization
        img_converted = img.convert("P", palette=Image.ADAPTIVE, colors=256)
        img_converted.save(
            output_path,
            "PNG",
            optimize=True,
            compress_level=9
        )
    else:
        print(f"Unsupported file extension '{file_ext}'. Supported types: .jpg, .jpeg, .png")
        return None

    print(f"Compressed image saved successfully to: '{output_path}'")
    return output_path

def run_gui():
    try:
        import easygui
    except ImportError:
        print("EasyGUI is not installed. Install it via 'pip install easygui' for GUI mode.")
        return

    print("Please select the image you want to compress...")
    image_file = easygui.fileopenbox(msg="Select Image File", filetypes=["*.jpg", "*.jpeg", "*.png"])

    if not image_file:
        print("No image selected. Exiting.")
        return

    _, file_ext = os.path.splitext(image_file)
    file_ext_lower = file_ext.lower()

    qual = 50
    if file_ext_lower in (".jpeg", ".jpg"):
        user_qual = easygui.integerbox(
            "Enter quality on a scale of 10 to 100 (default is 50):",
            "JPEG Compression Quality",
            default=50,
            lowerbound=10,
            upperbound=100
        )
        if user_qual is not None:
            qual = user_qual

    output_file = compress_image(image_file, quality=qual)

    if output_file:
        if file_ext_lower == ".png":
            easygui.msgbox("PNG file compressed with 256-color palette optimization.\nSaved to original image folder.", "Success")
        else:
            easygui.msgbox(f"Your compressed image has been saved to:\n{output_file}", "Success")

def main():
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        quality = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 50
        compress_image(image_path, quality=quality)
    else:
        run_gui()

if __name__ == '__main__':
    main()