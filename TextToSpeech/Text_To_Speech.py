import pyttsx3
import tkinter as tk

# saytext = input("What should I say? ")

class GUI:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Text To Speech")
        self.root.geometry("500x500")

        self.label = tk.Label(self.root, text="Type what you want me to say!", font=('Arial', 16))
        self.label.pack(padx=10, pady=10)

        self.textbox = tk.Entry(font=('Arial', 16))
        self.textbox.pack(padx=10, pady=10)

        self.button = tk.Button(text="CLICK ME!", font=('Arial', 16), command=self.button_click)
        self.button.pack(padx=10, pady=10)

        self.root.mainloop()

    def button_click(self):
        engine = pyttsx3.init()
        engine.say(self.textbox.get())
        engine.runAndWait()

GUI()