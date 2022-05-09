import random

# WINNING PATTERNS
# Scissors cuts Paper, Paper covers Rock, Rock crushes Lizard,
# Lizard poisons Spock, Spock smashes Scissors, Scissors decapitates Lizard,
# Lizard eats Paper, Paper disproves Spock, Spock vaporizes Rock,
# Rock crushes Scissors

win = [("scissors","paper"), ("paper","rock"), ("rock","lizard"),
       ("lizard","Spock"), ("Spock","scissors"), ("scissors","lizard"),
       ("lizard","paper"), ("paper","Spock"), ("Spock","rock"),
       ("rock","scissors")]

# INSTRUCTIONS
print("There are 6 rounds.\nYou are playing against Computron.\nYou will win if you have a higher point.\nEnter scissors, paper, rock, lizard or Spock.\nLIVE LONG AND PROSPER🖖\n")

# CHOICES FOR THE COMPUTRON TO CHOOSE FROM
choices = ["scissors", "paper", "rock", "lizard", "Spock"]

# TO COUNT THE NUMBER OF ROUNDS
count = 0
# TO COUNT THE PLAYER'S POINTS
playerPoints = 0
# TO COUNT THE COMPUTRONS' POINTS
computerPoints = 0

# WHILE LOOP TO SET THE NUMBER OF ROUNDS
while count != 6:
    # INPUT FOR PLAYER'S CHOICE
    player = input("What is your move? ")
    # COMPUTRON RANDOMLY SELECT CHOICE FROM CHOICES LIST
    computer = random.choice(choices)
    # UNCOMMENT THE LINE BELOW IF YOU WISH TO SEE COMPUTRONS' CHOICE
    #print(computer)

    # DIFFERENT CHOICES
    if player != computer:
        # CHECK FOR PATTERNS
        playerWins = (player,computer)
        computerWins = (computer,player)
        if playerWins in win:
            if playerWins == win[0]:
                #print("✂ cuts 📃 \nYou Won!")
                print("Scissors cuts paper \nYou Won!")
            elif playerWins == win[1]:
                print("Paper covers rock \nYou Won!")
            elif playerWins == win[2]:
                print("Rock crushes lizard \nYou Won!")
            elif playerWins == win[3]:
                print("Lizard poisons Spock \nYou Won!")
            elif playerWins == win[4]:
                print("Spock smashes scissors \nYou Won!")
            elif playerWins == win[5]:
                print("Scissors decapitates lizard \nYou Won!")
            elif playerWins == win[6]:
                print("Lizard eats paper \nYou Won!")
            elif playerWins == win[7]:
                print("Paper disproves Spock \nYou Won!")
            elif playerWins == win[8]:
                print("Spock vapourizes rock \nYou Won!")
            elif playerWins == win[9]:
                print("Rock crushes scissors \nYou Won!")
            playerPoints += 1
        elif computerWins in win:
            if computerWins == win[0]:
                print("Scissors cuts paper \nComputron Wins!")
            elif computerWins == win[1]:
                print("Paper covers rock \nComputron Wins!")
            elif computerWins == win[2]:
                print("Rock crushes lizard \nComputron Wins!")
            elif computerWins == win[3]:
                print("Lizard poisons Spock \nComputron Wins!")
            elif computerWins == win[4]:
                print("Spock smashes scissors \nComputron Wins!")
            elif computerWins == win[5]:
                print("Scissors decapitates lizard \nComputron Wins!")
            elif computerWins == win[6]:
                print("Lizard eats paper \nComputron Wins!")
            elif computerWins == win[7]:
                print("Paper disproves Spock \nComputron Wins!")
            elif computerWins == win[8]:
                print("Spock vapourizes rock \nComputron Wins!")
            elif computerWins == win[9]:
                print("Rock crushes scissors \nComputron Wins!")
            computerPoints += 1
        # PLAYER DID NOT INPUT scissors, paper, rock, lizard or Spock
        else:
            print("Invalid response \nComputron Wins!")
            computerPoints += 1

    # DRAW, SAME CHOICES
    elif player == computer:
        print("Draw, Player and Computron gets 1 point")
        playerPoints += 1
        computerPoints += 1

    # EMPTY LINE FOR A NEATER/CLEARER VIEW
    print("")

    # INCREMENT TO CONTROL THE NUMBER OR ROUNDS
    count += 1

# COMPARISON TO DETERMINE WHO IS THE CHAMPION
if playerPoints > computerPoints:
    print("You are the champion! 🏆")
elif playerPoints == computerPoints:
    print("You are both champions!! 🏆🏆")
else:
    print("Computron is the champion, Try Again! 💻")
