import pyqrcode
import png
from tkinter import *
from PIL import ImageTk, Image

def get_code():
    data_var = data.get()
    qr = pyqrcode.create(str(data_var))
    qr.png('code.png', scale=6)

base = Tk()
base.geometry("400x200")
base.title("QR Code Generator")

data = StringVar()

dataEntry = Entry(textvariable=data, width="30")
dataEntry.place(x=80,y=50)

button = Button(base,text="Get Code",command=get_code,width="30",height="2",bg="grey")
button.place(x=80,y=100)

base.mainloop()