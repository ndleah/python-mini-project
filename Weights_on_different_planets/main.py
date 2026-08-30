import sys
import tkinter as tk
from tkinter import messagebox

GRAVITY_FACTORS = {
    "Mercury": 3.7 / 9.798,
    "Venus": 8.87 / 9.798,
    "Mars": 3.71 / 9.798,
    "Jupiter": 24.92 / 9.798,
    "Saturn": 10.44 / 9.798,
    "Uranus": 8.87 / 9.798,
    "Neptune": 11.15 / 9.798,
    "Pluto": 0.58 / 9.798,
    "Sun": 274.0 / 9.798,
    "Moon": 1.625 / 9.798,
}

def calculate_planet_weight(earth_weight: float, planet: str) -> float:
    """Calculate equivalent weight on target celestial body."""
    if planet not in GRAVITY_FACTORS:
        raise ValueError(f"Unknown planet '{planet}'")
    return round(earth_weight * GRAVITY_FACTORS[planet], 2)

def run_gui():
    root = tk.Tk()
    root.configure(bg="black")
    root.title("Weights on Different Planets")

    mylabel = tk.Label(root, text="Enter Weight on Earth (kg): ", font=("Algerian", 12), bg="black", fg="red")
    e = tk.Entry(root, width=50, borderwidth=5)
    mylabel.grid(row=0, column=0, columnspan=1, pady=10, padx=10)
    e.grid(row=0, column=1, columnspan=2, pady=10, padx=10)
    e.focus_set()

    result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="black", fg="yellow", padx=20, pady=20)
    result_label.grid(row=5, column=0, columnspan=3)

    def calculate_for_planet(planet_name):
        raw_val = e.get().strip()
        if not raw_val:
            messagebox.showwarning("Input Error", "Please enter your weight on Earth first.")
            return

        try:
            earth_w = float(raw_val)
            if earth_w <= 0:
                messagebox.showwarning("Input Error", "Weight must be a positive number.")
                return
            planet_w = calculate_planet_weight(earth_w, planet_name)
            result_label.config(text=f"Your Weight on {planet_name}: {planet_w} kg")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid numeric value for weight.")

    buttons_config = [
        ("Mercury", 1, 0, "green", "white"),
        ("Venus", 1, 1, "blue", "white"),
        ("Mars", 1, 2, "red", "white"),
        ("Jupiter", 2, 0, "green", "white"),
        ("Saturn", 2, 1, "blue", "white"),
        ("Uranus", 2, 2, "red", "white"),
        ("Neptune", 3, 0, "green", "white"),
        ("Pluto", 3, 1, "blue", "white"),
        ("Sun", 3, 2, "red", "white"),
        ("Moon", 4, 1, "yellow", "blue"),
    ]

    for name, r, c, bg_c, fg_c in buttons_config:
        btn = tk.Button(
            root,
            text=name,
            font=("Arial", 12),
            padx=30,
            pady=15,
            command=lambda p=name: calculate_for_planet(p),
            bg=bg_c,
            fg=fg_c
        )
        btn.grid(row=r, column=c, padx=5, pady=5)

    root.mainloop()

def main():
    if len(sys.argv) > 2:
        try:
            w = float(sys.argv[1])
            p = sys.argv[2].capitalize()
            res = calculate_planet_weight(w, p)
            print(f"Weight of {w} kg on Earth = {res} kg on {p}")
        except Exception as err:
            print(f"Error: {err}")
    else:
        run_gui()

if __name__ == '__main__':
    main()