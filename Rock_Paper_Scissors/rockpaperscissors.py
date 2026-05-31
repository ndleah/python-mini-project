import random

choices = ["rock", "paper", "scissors"]

print("Welcome to Rock, Paper, Scissors!")
print("Best of 3 Rounds")

while True:
    user_score = 0
    computer_score = 0
    round = 0

    while round < 3:
        print("\nRound", round + 1)

        user = input("Enter rock, paper, or scissors: ").lower()

        if user not in choices:
            print("Invalid choice")
            continue

        computer = random.choice(choices)

        print("You chose:", user)
        print("Computer chose:", computer)

        if user == computer:
            print("It's a tie!")
        elif (
            (user == "rock" and computer == "scissors") or
            (user == "paper" and computer == "rock") or
            (user == "scissors" and computer == "paper")
        ):
            user_score += 1
            print("You get a point!")
        else:
            computer_score += 1
            print("Computer gets a point!")

        round += 1

    print("\nFinal Score")
    print("You:", user_score)
    print("Computer:", computer_score)

    if user_score > computer_score:
        print("You win the game!")
    elif computer_score > user_score:
        print("Computer wins the game!")
    else:
        print("The game is a tie!")

    play_again = input("\nDo you want to play again? (yes/no): ").lower()

    if play_again != "yes":
        print("Thanks for playing!")
        break
