from prettytable import PrettyTable
import pyfiglet as fig
import random as rd
import sys

# Declaration of the main varaiables.
options = ("Rock", "Paper", "Scissors")
player_score = 0
cpu_score = 0
div = "-" * 17

# Welcome to the game and collection of important data
welcome = "WELCOME TO THE GAME!!"
print(fig.figlet_format(welcome, font="smkeyboard", width=80, justify="center"))
player_name = input("What's your name? ").upper().strip()
rounds_game = input("How many rounds do yoy want to play? ").strip()


def main():
    rounds_of_games(rounds_game)


def tables(name1, name2, value1, value2):
    table = PrettyTable()
    table.field_names = ["PLAYER", "SCORE"]
    table.add_row([name1, value1])
    table.add_row([name2, value2])
    return table


def rounds_of_games(number_of_rounds):
    try:
        if number_of_rounds.isalnum():
            while True:
                for _ in range(int(number_of_rounds)):
                    print(playing())
                print(tables(player_name, "CPU", player_score, cpu_score))
                print(f"{div}\nYOU HAVE COMPLETED ALL ROUNDS\n{div}")
                still_playing()
        else:
            print("Enter a correct input(only numbers). Start the game again.")
    except ValueError:
        print("Enter a correct input(only numbers). Start the game again.")
        pass
        
        


def valid_player_choice():
    # Call to the user for her/his choice.
    # If the choice is in options, the function return the answers.
    # Else prompt for the input again.
    global options
    while True:
        text = input("Rock, paper or scissors? ").title().strip()
        if text in options:
            return text
        else:
            continue


def computer_choice():
    # Choice a random option from the options list (Paper, Rock, Scissors).
    global options
    return rd.choice(options)


def playing():
    # Compare the cpu and player choices and addition points in each case.
    global player_name, player_score, cpu_score

    player_choice = valid_player_choice()
    cpu_choice = computer_choice()

    if player_choice == cpu_choice:
        return "¡¡NO ONE WON A POINT!!"
    elif (
        (player_choice == "Rock" and cpu_choice == "Scissors")
        or (player_choice == "Scissors" and cpu_choice == "Paper")
        or (player_choice == "Paper" and cpu_choice == "Rock")
    ):
        player_score += 1
        return f"¡¡{player_name} WON!!"
    else:
        cpu_score += 1
        return "¡¡CPU WON YOU!!"


def still_playing():
    global cpu_score, player_score, div, player_name

    while True:
        try:
            user_choice = int(
                input(
                    f"Press 1 to continue\nPress 2 to reset and continue\npress 3 to exit\n{div}\nInput: "
                )
            )
            if user_choice >= 0 and user_choice <= 3:
                if user_choice == 1:
                    # This is executed if the user wants to play more rounds
                    # (Is the same count of rounds as the principle)
                    rounds_of_games(rounds_game)

                elif user_choice == 2:
                    # This is executed if the user wants to reset the scores and play more rounds
                    # (Is the same count of rounds as the principle)
                    # Further shows the new game's score
                    player_score = 0
                    cpu_score = 0
                    print(
                        f"{div}\nNEW SCORE = CPU: {cpu_score} | {player_name}: {player_score}"
                    )
                    rounds_of_games(rounds_game)

                else:
                    # This is executed if the user wants to quit
                    winner = ""
                    if cpu_score > player_score:
                        winner = "¡CPU WON!"
                    elif cpu_score < player_score:
                        winner = f"¡{player_name} WON!"
                    elif cpu_score == player_score:
                        winner = f"¡¡IT'S A TIE, {player_name}!!"
                    print(tables(player_name, "CPU", player_score, cpu_score)) # Show a table with the final score
                    print(winner) # Show who won
                    thanks = f"THANKS FOR PLAY {player_name}"
                    sys.exit(
                        fig.figlet_format(
                            thanks, font="smkeyboard", width=80, justify="center"
                        )
                    ) # ACKNOWLEDGMENTS
            else:
                continue
        except ValueError:
            print("Enter a correct input, please.")
            continue


if __name__ == "__main__":
    main()
