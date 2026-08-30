import os
import sys

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def convert_image_to_ascii_pil(image_path: str, output_path: str = "ascii_text.txt", new_width: int = 100) -> str:
    """Convert an image to ASCII art using PIL/Pillow library."""
    from PIL import Image

    image = Image.open(image_path)

    # Resize image maintaining aspect ratio
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_image = image.resize((new_width, new_height))

    # Convert to grayscale
    grayscale_image = resized_image.convert("L")

    # Map pixels to ascii characters
    pixels = grayscale_image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])

    # Format into rows
    pixel_count = len(characters)
    ascii_art = "\n".join([characters[i:(i + new_width)] for i in range(0, pixel_count, new_width)])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ascii_art)

    print(f"ASCII art generated successfully via PIL -> {output_path}")
    return ascii_art

def convert_image_to_ascii(image_path: str = None, output_path: str = "ascii_text.txt"):
    """Convert image to ASCII art with pywhatkit and PIL fallback."""
    script_dir = os.path.dirname(__file__)
    if not image_path:
        default_img = os.path.join(script_dir, "python_img.jpg")
        if os.path.exists(default_img):
            image_path = default_img
        else:
            image_path = input("Enter the image location: ").strip()

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'")
        return None

    try:
        import pywhatkit as kt
        kt.image_to_ascii_art(image_path, output_path)
        print(f"ASCII art saved to '{output_path}' via PyWhatKit.")
    except Exception as e:
        print(f"Notice: pywhatkit unavailable or failed ({e}). Using PIL converter fallback...")
        try:
            return convert_image_to_ascii_pil(image_path, output_path)
        except Exception as err:
            print(f"Error generating ASCII art: {err}")
            return None

def main():
    img_arg = sys.argv[1] if len(sys.argv) > 1 else None
    convert_image_to_ascii(img_arg)

if __name__ == '__main__':
    main()

