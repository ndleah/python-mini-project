import random
import tkinter as tk

def roll_dice() -> int:
    """Generate a random dice roll between 1 and 6."""
    return random.randint(1, 6)

def run_gui():
    root = tk.Tk()
    root.geometry("220x180")
    root.title("Dice Roller")
    root.configure(bg="#f0f0f0")

    title_label = tk.Label(root, text="Simple Dice", font=("Arial", 14, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    result_var = tk.StringVar(value="-")
    result_label = tk.Label(root, textvariable=result_var, font=("Arial", 28, "bold"), fg="darkblue", bg="#f0f0f0")
    result_label.pack(pady=5)

    def on_roll():
        r = roll_dice()
        result_var.set(str(r))

    roll_button = tk.Button(root, text="Roll Dice 🎲", font=("Arial", 12, "bold"), bg="green", fg="white", activebackground="darkgreen", command=on_roll)
    roll_button.pack(pady=10)

    def on_enter(event):
        roll_button.config(bg="darkgreen")

    def on_leave(event):
        roll_button.config(bg="green")

    roll_button.bind("<Enter>", on_enter)
    roll_button.bind("<Leave>", on_leave)

    root.mainloop()

def main():
    run_gui()

if __name__ == '__main__':
    main()