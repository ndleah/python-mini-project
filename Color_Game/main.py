import os
import random
import tkinter as tk
from tkinter import messagebox

colours = ['Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Pink', 'Black', 'White']
score = 0
timeleft = 30
game_running = False

HIGHEST_SCORE_FILE = os.path.join(os.path.dirname(__file__), "highest_score.txt")

def next_colour():
    global score, timeleft

    if timeleft > 0:
        user_input = e.get().lower().strip()
        correct_color = colours[1].lower()

        if user_input == correct_color:
            score += 1

        e.delete(0, tk.END)
        random.shuffle(colours)
        label.config(fg=colours[1], text=colours[0])
        score_label.config(text=f"Score: {score}")

def countdown():
    global timeleft, game_running
    if timeleft > 0:
        timeleft -= 1
        time_label.config(text=f"Time left: {timeleft}")
        time_label.after(1000, countdown)
    else:
        game_running = False
        scoreshow()

def record_highest_score():
    highest_score = load_highest_score()
    if score > highest_score:
        with open(HIGHEST_SCORE_FILE, "w") as file:
            file.write(str(score))

def load_highest_score():
    try:
        with open(HIGHEST_SCORE_FILE, "r") as file:
            data = file.read().strip()
            if data:
                return int(data)
            else:
                return 0
    except (FileNotFoundError, ValueError):
        return 0

def scoreshow():
    record_highest_score()
    window2 = tk.Toplevel(window)
    window2.title("HIGH SCORE")
    window2.geometry("300x200")

    label_hs = tk.Label(window2, text=f"Highest Score: {load_highest_score()}", font=(font, 14, "bold"))
    label_hs.pack(pady=40)

    score_label.config(text="Game Over! Press Enter to restart")

def start_game(event):
    global timeleft, score, game_running
    if not game_running and timeleft <= 0:
        score = 0
        timeleft = 30
        score_label.config(text=f"Score: {score}")
        time_label.config(text=f"Time left: {timeleft}")

    if not game_running:
        game_running = True
        countdown()

    next_colour()

window = tk.Tk()
font = 'Helvetica'
window.title("Color Game")

icon_path = os.path.join(os.path.dirname(__file__), "color_game_icon.ico")
if os.path.exists(icon_path):
    try:
        window.iconbitmap(icon_path)
    except Exception:
        pass

window.geometry("375x250")
window.resizable(False, False)

instructions = tk.Label(window, text="Enter the color of the text, not the word!", font=(font, 12))
instructions.pack(pady=10)

score_label = tk.Label(window, text="Press Enter to start", font=(font, 12))
score_label.pack()

time_label = tk.Label(window, text=f"Time left: {timeleft}", font=(font, 12))
time_label.pack()

label = tk.Label(window, font=(font, 60))
label.pack(pady=20)

random.shuffle(colours)
label.config(fg=colours[1], text=colours[0])

e = tk.Entry(window)
window.bind('<Return>', start_game)
e.pack()

e.focus_set()

if __name__ == '__main__':
    window.mainloop()