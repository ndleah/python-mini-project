import qrcode
from PIL import Image


#import requests

# Load the logo image
# Logo_link = 'https://cdn.pixabay.com/photo/2022/01/30/13/33/github-6980894_1280.png'
# logo_response = requests.get(Logo_link, stream=True)
# logo_response.raise_for_status()  # Raise an exception for HTTP errors
# logo_img = Image.open(logo_response.raw)

'''
if you want to take an image which is already hosted on web comment lines 18,19 and use the above method
'''

# Path to the logo image file on user's machine
logo_path = "github-logo.png"
logo_img = Image.open(logo_path)

url = 'https://github.com/shashank-amireddy'

# Ensure the logo has an alpha channel (transparency)
logo_img = logo_img.convert("RGBA")

# Resize the logo to fit within the QR code
basewidth = 100
wpercent = basewidth / float(logo_img.size[0])
hsize = int(float(logo_img.size[1]) * float(wpercent))
logo_img = logo_img.resize((basewidth, hsize), Image.LANCZOS)

# Generate QR code
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
QRcode.add_data(url)
QRcode.make()

# Create QR code image with a mode that supports color
QRimg = QRcode.make_image(fill_color="black", back_color="white").convert("RGBA")

# Calculate position to paste the logo
logo_position = (
    (QRimg.size[0] - logo_img.size[0]) // 2,
    (QRimg.size[1] - logo_img.size[1]) // 2
)

# Paste the logo onto the QR code
QRimg.paste(logo_img, logo_position, logo_img)

# Save the final QR code image
QRimg.save('qr_with_logo.png')
print('QR code generated!')
