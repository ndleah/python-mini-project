import os
import img2pdf

def images_to_pdf(image_folder_path):

    # Verifying the give path exists or not

    if os.path.exists(image_folder_path):
        print("Given images folder path verified -- processing")
    else:
        print("Given images folder Not exist ")
        return
    
    images = [imgs for imgs in os.listdir(image_folder_path) if imgs.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    images.sort()

    # List to store image bytes of images present in the directory
    images_bytes = list()

    # converting all the images to image-bytes and appending them to a list for further processing
    for i in images:
        with open(os.path.join(image_folder_path, i), "rb") as im:
            images_bytes.append(im.read())

    # To convert image bytes to bytes for pdf
    pdf_image_bytes = img2pdf.convert(images_bytes)
    with open('Output.pdf', "wb") as pdfFile:
        pdfFile.write(pdf_image_bytes)
        
# Call the function to convert the images folder to pdf
images_to_pdf(folder_path)