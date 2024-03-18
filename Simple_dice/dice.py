from tkinter import *
import random


def roll():
    r = random.randint(1, 6)
    s = str(r)
    e.delete(0, END)
    e.insert(0, s)

def on_enter(event):
  button1.config(fg="black")

def on_leave(event):
  button1.config(fg="green")

root = Tk()
root.geometry("99x117+1153+210")
root.title("Dice")
label = Label(root, text="Simple Dice" ,wraplength=100)
e = Entry(root, width=5)
button1 = Button(root, text="Roll", command=roll,wraplength=100)

button1.bind("<Enter>", on_enter)
button1.bind("<Leave>", on_leave)


label.grid(row=0, sticky=N)
e.grid(row=2 ,sticky=N)
button1.grid(row=4 ,sticky=S)

root.mainloop()