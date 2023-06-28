import cv2
def compare_images(image1_path, image2_path):
    # Read the images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    # Check if the images were loaded successfully
    if image1 is None or image2 is None:
        print("Failed to load the images.")
        return
    # Resize the images to the same dimensions for comparison
    image1 = cv2.resize(image1, (500, 500))
    image2 = cv2.resize(image2, (500, 500))
    
    #calculating difference between two images
    difference = cv2.subtract(image1, image2)
    b, g, r = cv2.split(difference)
    # If the images are identical, the difference should be black (all zeros)
    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        print("The images are identical.")
    else:
        # color the mask red
        conv_hsv_gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(
            conv_hsv_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        )
        difference[mask != 255] = [0, 0, 255]

        # add the red mask to the images to make the differences obvious
        image1[mask != 255] = [0, 0, 255]
        image2[mask != 255] = [0, 0, 255]
        diff ="diff.png"
        cv2.imwrite(diff, difference)
        print("The images are different.")

        
# Provide the paths to the two images you want to compare
image1_path = "image1.jpg"
image2_path = "image2.jpg"
# Call the function to compare the images
compare_images(image1_path, image2_path)
