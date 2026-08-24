import random

# WINNING PATTERNS
# Scissors cuts Paper, Paper covers Rock, Rock crushes Lizard,
# Lizard poisons Spock, Spock smashes Scissors, Scissors decapitates Lizard,
# Lizard eats Paper, Paper disproves Spock, Spock vaporizes Rock,
# Rock crushes Scissors

WINNING_RULES = {
    ("scissors", "paper"): "Scissors cuts paper",
    ("paper", "rock"): "Paper covers rock",
    ("rock", "lizard"): "Rock crushes lizard",
    ("lizard", "spock"): "Lizard poisons Spock",
    ("spock", "scissors"): "Spock smashes scissors",
    ("scissors", "lizard"): "Scissors decapitates lizard",
    ("lizard", "paper"): "Lizard eats paper",
    ("paper", "spock"): "Paper disproves Spock",
    ("spock", "rock"): "Spock vaporizes rock",
    ("rock", "scissors"): "Rock crushes scissors",
}

CHOICES = ["scissors", "paper", "rock", "lizard", "spock"]

def determine_winner(player_move: str, computer_move: str):
    """Determine outcome between player and computer moves."""
    p_move = player_move.strip().lower()
    c_move = computer_move.strip().lower()

    if p_move not in CHOICES:
        return "invalid", "Invalid response. Computron Wins!"

    if p_move == c_move:
        return "draw", "Draw, Player and Computron get 1 point each."

    if (p_move, c_move) in WINNING_RULES:
        rule_desc = WINNING_RULES[(p_move, c_move)]
        return "player", f"{rule_desc}! You Won!"
    elif (c_move, p_move) in WINNING_RULES:
        rule_desc = WINNING_RULES[(c_move, p_move)]
        return "computer", f"{rule_desc}! Computron Wins!"

    return "invalid", "Invalid response. Computron Wins!"

def play_game(total_rounds: int = 6):
    print("There are 6 rounds.\nYou are playing against Computron.\nYou will win if you have higher points.\nEnter scissors, paper, rock, lizard or Spock.\nLIVE LONG AND PROSPER 🖖\n")

    count = 0
    player_points = 0
    computer_points = 0

    while count < total_rounds:
        raw_player = input(f"Round {count + 1}/{total_rounds} - What is your move? ").strip()
        computer_choice = random.choice(CHOICES)

        result, msg = determine_winner(raw_player, computer_choice)
        print(f"Computron chose: {computer_choice.capitalize()}")
        print(msg)

        if result == "player":
            player_points += 1
        elif result == "computer":
            computer_points += 1
        elif result == "draw":
            player_points += 1
            computer_points += 1
        else:
            computer_points += 1

        print(f"Score -> You: {player_points} | Computron: {computer_points}\n")
        count += 1

    print("--- Final Result ---")
    if player_points > computer_points:
        print("You are the champion! 🏆")
    elif player_points == computer_points:
        print("You are both champions!! 🏆🏆")
    else:
        print("Computron is the champion, Try Again! 💻")

def main():
    play_game()

if __name__ == '__main__':
    main()

