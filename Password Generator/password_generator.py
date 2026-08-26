import secrets
import string
import tkinter as tk
from tkinter import messagebox

def generate_random_password(length: int) -> str:
    """Generate cryptographically secure random password of arbitrary length."""
    if length <= 0:
        return ""
    char_pool = string.ascii_lowercase + string.ascii_uppercase + string.digits + "@#$%&*"
    return "".join(secrets.choice(char_pool) for _ in range(length))

def run_gui():
    gui = tk.Tk()
    gui.title('Password Generator')
    gui.geometry('300x220')
    gui.resizable(False, False)

    string_pass = tk.StringVar(value="12")

    tk.Label(gui, text="Password Length:", font=("Arial", 11, "bold")).pack(pady=15)
    txt = tk.Entry(gui, textvariable=string_pass, font=("Arial", 12), width=10, justify="center")
    txt.pack(pady=5)
    txt.focus_set()

    def process():
        raw_val = string_pass.get().strip()
        try:
            length = int(raw_val)
            if length <= 0:
                messagebox.showwarning("Input Error", "Please enter a positive length greater than 0.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid integer length.")
            return

        password = generate_random_password(length)

        copied_msg = ""
        try:
            import pyperclip
            pyperclip.copy(password)
            copied_msg = "\n(Password copied to clipboard!)"
        except Exception:
            pass

        messagebox.showinfo("Generated Password", f"Your Password:\n{password}{copied_msg}")

    btn = tk.Button(gui, text="Generate Password", font=("Arial", 11, "bold"), bg="navy", fg="white", command=process)
    btn.pack(pady=15)

    gui.mainloop()

def main():
    run_gui()

if __name__ == '__main__':
    main()

