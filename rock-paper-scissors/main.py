"""Rock Paper Scissors Game with GUI"""
import random
import tkinter as tk
from tkinter import messagebox

# Global variables
computer_score = 0
player_score = 0
options = ["Scissors", "Rock", "Paper"]

def victory_of_x(X, Y):
    """Determine if X wins against Y"""
    if X == "Scissors" and Y == "Paper":
        return True
    elif X == "Paper" and Y == "Rock":
        return True
    elif X == "Rock" and Y == "Scissors":
        return True
    else:
        return False

def play(player_choice):
    """Handle a round of the game"""
    global player_score, computer_score
    computer_choice = random.choice(options)
    if player_choice == computer_choice:
        result_text.set(f"Both chose {player_choice}. It's a tie!")
    else:
        if victory_of_x(player_choice, computer_choice):
            player_score += 1
            result_text.set(f"Player chose {player_choice}, computer chose {computer_choice}.\nPlayer wins this round!")
        else:
            computer_score += 1
            result_text.set(f"Player chose {player_choice}, computer chose {computer_choice}.\nComputer wins this round!")

    score_text.set(f"Score -> Player: {player_score}, Computer: {computer_score}")


def reset_game():
    """Reset scores and start a new game"""
    global player_score, computer_score
    player_score = 0
    computer_score = 0
    result_text.set("New game started! Make your choice.")
    score_text.set("Score -> Player: 0, Computer: 0")


# Create main window
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("450x300")
root.resizable(False, False)

# Result and Score Labels
result_text = tk.StringVar()
result_text.set("Welcome to Rock Paper Scissors! Make your choice.")
result_label = tk.Label(root, textvariable=result_text, wraplength=400, justify="center", font=("Arial", 12))
result_label.pack(pady=20)

score_text = tk.StringVar()
score_text.set("Score -> Player: 0, Computer: 0")
score_label = tk.Label(root, textvariable=score_text, font=("Arial", 12))
score_label.pack(pady=10)

# Buttons for player choices
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

scissors_button = tk.Button(button_frame, text="Scissors", width=12, command=lambda: play("Scissors"))
scissors_button.grid(row=0, column=0, padx=5)

rock_button = tk.Button(button_frame, text="Rock", width=12, command=lambda: play("Rock"))
rock_button.grid(row=0, column=1, padx=5)

paper_button = tk.Button(button_frame, text="Paper", width=12, command=lambda: play("Paper"))
paper_button.grid(row=0, column=2, padx=5)

# Reset Game Button
reset_button = tk.Button(root, text="New Game", command=reset_game)
reset_button.pack(pady=10)

root.mainloop()
