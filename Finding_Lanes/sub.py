import os
import matplotlib.pyplot as plt
import matplotlib.image as img

script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, "picture.jpg")

if os.path.exists(image_path):
    image_data = img.imread(image_path)
    plt.imshow(image_data)
    plt.title("Lane Detection Source Picture")
    plt.axis("off")
    plt.show(block=False)
else:
    print(f"Picture path '{image_path}' not found.")

