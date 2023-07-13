import random
import tkinter as tk

colours = ['Red', 'Blue', 'Green', 'Yellow', 'Orange', 'Purple', 'Pink', 'Black', 'White']
score = 0
timeleft = 30

def start_game(event):
    global timeleft
    if timeleft == 30:
        countdown()
    next_colour()

def next_colour():
    global score, timeleft

    if timeleft > 0:
        user_input = e.get().lower()
        correct_color = colours[1].lower()

        if user_input == correct_color:
            score += 1

        e.delete(0, tk.END)
        random.shuffle(colours)
        label.config(fg=colours[1], text=colours[0])
        score_label.config(text=f"Score: {score}")

def countdown():
    global timeleft
    if timeleft > 0:
        timeleft -= 1
        time_label.config(text=f"Time left: {timeleft}")
        time_label.after(1000, countdown)
    else:
        record_highest_score()

def record_highest_score():
    highest_score = load_highest_score()
    if score > highest_score:
        save_highest_score(score)

def save_highest_score(score):
    with open("highest_score.txt", "w") as file:
        file.write(f"The highest score is: {score}")

def load_highest_score():
    try:
        with open("highest_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

window = tk.Tk()
font = 'Helvetica'
window.title("Color Game")
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

e = tk.Entry(window)
window.bind('<Return>', start_game)
e.pack()

e.focus_set()

window.mainloop()
