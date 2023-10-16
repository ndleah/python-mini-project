# the below program converts an image to ascii text
import pywhatkit as kt


# enter the image location
# input the image location -- for ease please place the image file in the same directory
img_loc=input("Enter the image location: ")
kt.image_to_ascii_art(img_loc,"ascii_text.txt")
