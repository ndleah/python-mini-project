import qrcode
from tkinter import *
from tkinter import filedialog
import os


# This Function is responsible to take the input -> Convert it to Image Code -> Convert Image code to png.
def get_code():
    data_var = data.get()
    qr = qrcode.make(str(data_var))
    # This will ask for the directory the user wants to store the code and save it there.
    base.loc = filedialog.askdirectory()
    os.chdir(base.loc)
    save_as = name_to_save.get()
    label= Label(base, text="Done", bg="red")
    label.place(x=80, y=150)
    qr.save(f"{save_as}.png")
    

#Get a Tk window of 400 * 200
base = Tk()
base.geometry("400x200")
base.title("QR Code Generator")

# variable to store text for QR Code
data = StringVar()
name_to_save = StringVar()
# Field to input text
# Get the name to be saved as
label_1 = Label(base, text="SAVE_AS").place(x=80, y=10)
dataEntry = Entry(textvariable=name_to_save, width="30")
dataEntry.place(x=80,y=30)

# What is suppose to be in the qrcode when scanned
label_1 = Label(base, text="INSIDE QRCODE").place(x=80, y=50)

dataEntry = Entry(textvariable=data, width="30")
dataEntry.place(x=80,y=70)


# Call get_code() on click
button = Button(base,text="Get Code",command=get_code,width="30",height="2",bg="grey")
button.place(x=80,y=100)

base.mainloop()
