import os
import sys

def convert_images_to_pdf_pil(image_files: list, output_pdf_path: str) -> bool:
    """Fallback conversion using PIL/Pillow."""
    try:
        from PIL import Image
        pil_images = []
        for f in image_files:
            img = Image.open(f)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            pil_images.append(img)

        if not pil_images:
            return False

        first_img = pil_images[0]
        first_img.save(output_pdf_path, save_all=True, append_images=pil_images[1:])
        print(f"PDF generated via PIL -> {output_pdf_path}")
        return True
    except Exception as e:
        print(f"PIL fallback failed: {e}")
        return False

def images_to_pdf(image_folder_path: str = None, output_pdf_path: str = "Output.pdf") -> str:
    """Convert all image files in a folder into a single PDF document."""
    if not image_folder_path:
        script_dir = os.path.dirname(__file__)
        image_folder_path = script_dir

    if not os.path.exists(image_folder_path):
        print(f"Error: Specified folder path '{image_folder_path}' does not exist.")
        return None

    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    image_names = [f for f in os.listdir(image_folder_path) if f.lower().endswith(valid_extensions)]
    image_names.sort()

    if not image_names:
        print(f"Notice: No supported images found in '{image_folder_path}'.")
        return None

    full_paths = [os.path.join(image_folder_path, img) for img in image_names]

    try:
        import img2pdf
        images_bytes = []
        for fpath in full_paths:
            with open(fpath, "rb") as im:
                images_bytes.append(im.read())

        pdf_image_bytes = img2pdf.convert(images_bytes)
        with open(output_pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_image_bytes)
        print(f"Successfully converted {len(image_names)} images to PDF -> {output_pdf_path}")
        return output_pdf_path
    except Exception as e:
        print(f"Notice: img2pdf conversion failed ({e}). Trying PIL fallback...")
        if convert_images_to_pdf_pil(full_paths, output_pdf_path):
            return output_pdf_path
        return None

def main():
    folder_arg = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(__file__)
    out_arg = sys.argv[2] if len(sys.argv) > 2 else "Output.pdf"
    images_to_pdf(folder_arg, out_arg)

if __name__ == '__main__':
    main()