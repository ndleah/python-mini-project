import pyqrcode
import png
from tkinter import *


# This Function is responsible to take the input -> Convert it to Image Code -> Convert Image code to png.
def get_code():
    data_var = data.get()
    qr = pyqrcode.create(str(data_var))
    qr.png('code.png', scale=6)

#Get a Tk window of 400 * 200
base = Tk()
base.geometry("400x200")
base.title("QR Code Generator")

# variable to store text for QR Code
data = StringVar()

# Field to input text
dataEntry = Entry(textvariable=data, width="30")
dataEntry.place(x=80,y=50)

# Call get_code() on click
button = Button(base,text="Get Code",command=get_code,width="30",height="2",bg="grey")
button.place(x=80,y=100)

base.mainloop()
