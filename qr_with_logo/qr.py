import os
import sys
import qrcode
from PIL import Image

def generate_qr_with_logo(url: str = 'https://github.com/shashank-amireddy', logo_path: str = None, output_path: str = None) -> str:
    """Generate QR code with embedded logo image."""
    script_dir = os.path.dirname(__file__)
    if logo_path is None:
        logo_path = os.path.join(script_dir, "github-logo.png")

    if output_path is None:
        output_path = os.path.join(script_dir, "qr_with_logo.png")

    if not os.path.exists(logo_path):
        print(f"Error: Logo file '{logo_path}' not found.")
        return None

    try:
        logo_img = Image.open(logo_path).convert("RGBA")

        # Resize logo to fit nicely inside QR code center
        basewidth = 100
        wpercent = basewidth / float(logo_img.size[0])
        hsize = int(float(logo_img.size[1]) * float(wpercent))
        logo_img = logo_img.resize((basewidth, hsize), Image.LANCZOS)

        # Generate QR code with high error correction
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        qr.add_data(url)
        qr.make()

        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        # Calculate center position
        logo_position = (
            (qr_img.size[0] - logo_img.size[0]) // 2,
            (qr_img.size[1] - logo_img.size[1]) // 2
        )

        qr_img.paste(logo_img, logo_position, logo_img)
        qr_img.save(output_path)
        print(f"QR code with logo generated successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating QR code with logo: {e}")
        return None

def main():
    target_url = sys.argv[1] if len(sys.argv) > 1 else 'https://github.com/shashank-amireddy'
    generate_qr_with_logo(url=target_url)

if __name__ == '__main__':
    main()

