# Built in modules
import io
from tkinter import *
import pathlib

# External Modules
import requests
from bs4 import BeautifulSoup
import PIL.Image
import validators

# Get Current Working Directory path
path = pathlib.Path().resolve()


def get_pdf():
    URL = url_var.get()

    # Only perform scraping if the url is valid.
    if validators.url(URL):
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html5lib")
        imgs = soup.find_all("img", class_="slide-image")

        # Get every image with class slide-image
        imgs = soup.find_all("img", class_="slide-image")

        # Strip out preferred image resolution from the srcset of the img tag
        imgSRC = [
            x.get("srcset").split(",")[-1].strip().split(" ")[0].split("?")[0]
            for x in imgs
        ]

        # List to store all the image objects
        imagesJPG = []

        for index, link in enumerate(imgSRC):
            try:
                # Get image content from the image url
                im = requests.get(link)

                # Convert that image content to a BytesIO file object which is in-memory object,
                # so we don't have to download the image.
                f = io.BytesIO(im.content)

                # Converting that BytesIO object to Image Object for PIL to convert it in PDF
                imgJPG = PIL.Image.open(f)
                imagesJPG.append(imgJPG)

            except Exception as e:
                # Program will fail if the request isn't able to make a proper connection
                info_label_2.configure(text="Some Connection ERROR")

        # Appending all the images object after the first image and exporting it as a PDF in cwd.
        imagesJPG[0].save(
            f"{soup.title.string}.pdf", save_all=True, append_images=imagesJPG[1:]
        )
        info_label_2.configure(text=f"File Downloaded to\n{path}")
    else:
        info_label_2.configure(text=f"Please provide a valid link")


# Basic Tkinter window setup
base = Tk()
base.geometry("300x300")
base.title("Slideshare to PDF")
base.resizable(False, False)
base.configure(background="aliceblue")

# Variable to store user's link and a  entry field,
# a button and a label
url_var = StringVar()
val_entry = Entry(base, textvariable=url_var, width="30")
val_entry.place(x=50, y=50)

button = Button(
    base, text="Get PDF", command=get_pdf, width="25", height="2", bg="grey"
)
button.place(x=50, y=100)
info_label = Label(
    base,
    text="Enter the presentaion link\nMake sure to have a good internet connection.",
)

# label to show error and success message to the user
info_label_2 = Label(base, text="")

info_label.place(x=35, y=200)
info_label_2.place(x=50, y=250)
base.mainloop()
