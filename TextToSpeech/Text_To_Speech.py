import sys
import tkinter as tk
from tkinter import messagebox

def speak(text: str) -> bool:
    """Helper function to convert text to speech using pyttsx3."""
    if not text or not text.strip():
        return False
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return True
    except ImportError:
        print("Error: 'pyttsx3' package is required. Install it via 'pip install pyttsx3'.")
        return False
    except Exception as e:
        print(f"Text to speech error: {e}")
        return False

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text To Speech")
        self.root.geometry("500x300")

        self.label = tk.Label(self.root, text="Type what you want me to say!", font=('Arial', 16))
        self.label.pack(padx=10, pady=20)

        self.textbox = tk.Entry(self.root, font=('Arial', 16), width=30)
        self.textbox.pack(padx=10, pady=10)
        self.textbox.focus_set()

        self.button = tk.Button(self.root, text="SPEAK!", font=('Arial', 14, 'bold'), bg='green', fg='white', command=self.button_click)
        self.button.pack(padx=10, pady=20)

    def button_click(self):
        text = self.textbox.get().strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text to speak.")
            return
        if not speak(text):
            messagebox.showerror("Error", "Could not convert text to speech. Ensure 'pyttsx3' is installed.")

    def run(self):
        self.root.mainloop()

def main():
    if len(sys.argv) > 1:
        text_to_say = " ".join(sys.argv[1:])
        speak(text_to_say)
    else:
        app = GUI()
        app.run()

if __name__ == '__main__':
    main()