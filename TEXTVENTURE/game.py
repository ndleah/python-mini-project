"""
Python Text RPG Adeventure Game

Copyright (C) 2022 RAO.exe
"""

# Importing the necessary modules
import os
import sys
import time


# ---- Global Variables ---- #
SCREEN_WIDTH = 100

ZONENAME = ""
DESCRIPTION = "description"
EXAMINATION = "examine"
SOLVED = False

TRADES = ['builder', 'miner', 'fighter']

UP = ["up", "u", "north"]
DOWN = ["down", "d", "south"]
LEFT = ["left", "l", "west"]
RIGHT = ["right", "r", "east"]

SOLVED_PLACES = {   
                    'a1': False, 'a2': False, 'a3': False, 'a4': False,
                    'b1': False, 'b2': False, 'b3': False, 'b4': False,
                    'c1': False, 'c2': False, 'c3': False, 'c4': False,
                    'd1': False, 'd2': False, 'd3': False, 'd4': False,  
                }

ZONE_MAP = {
    'a1': {
        "ZONENAME": "Town Gate",
        "DESCRIPTION": "You are at the north gate of the town",
        "EXAMINATION": "The gate is closed for now",
        "UP": '',
        "DOWN": 'b2',
        "LEFT": '',
        "RIGHT": 'a2',
        "SOLVED": False,
    },
    'a2': {
        "ZONENAME": "Town Entrance",
        "DESCRIPTION": "You are at the entrance of the town",
        "EXAMINATION": "Behold the town of the town",
        "UP": '',
        "DOWN": 'b2',
        "LEFT": 'a1',
        "RIGHT": 'a3',
        "SOLVED": False,
    },
    'a3': {
        "ZONENAME": "Town Square",
        "DESCRIPTION": "You are at the town square",
        "EXAMINATION": "The town square is bustling with people",
        "UP": '',
        "DOWN": 'b3',
        "LEFT": 'a2',
        "RIGHT": 'a4',
        "SOLVED": False,
    },
    'a4': {
        "ZONENAME": "Town Gate",
        "DESCRIPTION": "You are at the south gate of the town",
        "EXAMINATION": "The gate is closed for now",
        "UP": '',
        "DOWN": 'b4',
        "LEFT": 'a3',
        "RIGHT": '',
        "SOLVED": False,
    },
    'b1': {
        "ZONENAME": "Main Street",
        "DESCRIPTION": "You are on Main Street",
        "EXAMINATION": "You are on Main Street and there is nothing here",
        "UP": 'a1',
        "DOWN": 'c1',
        "LEFT": '',
        "RIGHT": 'b2',
        "SOLVED": False,
    },
    'b2': {
        "ZONENAME": "Cemetery Street",
        "DESCRIPTION": "You are on Cemetery Street",
        "EXAMINATION": "You are on Cemetery Street looking at the graveyard",
        "UP": 'a2',
        "DOWN": 'c2',
        "LEFT": 'b1',
        "RIGHT": 'b3',
        "SOLVED": False,
    },
    'b3': {
        "ZONENAME": "Town Hall",
        "DESCRIPTION": "You are in the town hall",
        "EXAMINATION": "You are in the town hall talking with the mayor",
        "UP": 'a3',
        "DOWN": 'c3',
        "LEFT": 'b2',
        "RIGHT": 'b4',
        "SOLVED": False,
    },
    'b4': {
        "ZONENAME": "Side Street",
        "DESCRIPTION": "You are on Side Street",
        "EXAMINATION": "Behind the side street dark alley is present which leads to the witch's house",
        "UP": 'a4',
        "DOWN": 'c4',
        "LEFT": 'b3',
        "RIGHT": '',
        "SOLVED": False,
    },
    'c1': {
        "ZONENAME": "Town Stadium",
        "DESCRIPTION": "You are at the town stadium",
        "EXAMINATION": "Stadium is full of people and you can't see anything",
        "UP": 'b1',
        "DOWN": 'd1',
        "LEFT": '',
        "RIGHT": 'c2',
        "SOLVED": False,
    },
    'c2': {
        "ZONENAME": "Town Market",
        "DESCRIPTION": "You are at the town market",
        "EXAMINATION": "Market is closed for now! Come back later",
        "UP": 'b2',
        "DOWN": 'd2',
        "LEFT": 'c1',
        "RIGHT": 'c3',
        "SOLVED": False,
    },
    'c3': {
        "ZONENAME": "Town Library",
        "DESCRIPTION": "You are at the town library",
        "EXAMINATION": "Library is filled with books. Librarian is waiting for you",
        "UP": 'b3',
        "DOWN": 'd3',
        "LEFT": 'c2',
        "RIGHT": 'c4',
        "SOLVED": False,
    },
    'c4': {
        "ZONENAME": "Town Jail",
        "DESCRIPTION": "You are at the town jail",
        "EXAMINATION": "One of the guards is suspicious of you, run away!",
        "UP": 'b4',
        "DOWN": 'd4',
        "LEFT": 'c3',
        "RIGHT": '',
        "SOLVED": False,
    },
    'd1': {
        "ZONENAME": "Town University",
        "DESCRIPTION": "You are at the town university",
        "EXAMINATION": "One of the biggest universities in the world is here",
        "UP": 'c1',
        "DOWN": '',
        "LEFT": '',
        "RIGHT": 'd2',
        "SOLVED": False,
    },
    'd2': {
        "ZONENAME": "Town School",
        "DESCRIPTION": "You are at the town school",
        "EXAMINATION": "Kids are playing here",
        "UP": 'c2',
        "DOWN": '',
        "LEFT": 'd1',
        "RIGHT": 'd3',
        "SOLVED": False,
    },
    'd3': {
        "ZONENAME": "Town Museum",
        "DESCRIPTION": "You are at the town museum",
        "EXAMINATION": "Museum is full of artifacts! Remember to keep your distance",
        "UP": 'c3',
        "DOWN": '',
        "LEFT": 'd2',
        "RIGHT": 'd4',
        "SOLVED": False,
    },
    'd4': {
        "ZONENAME": "Town Exit",
        "DESCRIPTION": "You are at the town exit",
        "EXAMINATION": "Goodbye! little friend. See you soon",
        "UP": 'c4',
        "DOWN": '',
        "LEFT": 'd3',
        "RIGHT": '',
        "SOLVED": False,
    },
}



# ---- PLayer Class ---- #
class Player:

    # Initializing the player
    def __init__(self):
        self.name = ''
        self.username = ''
        self.trade = ''
        self.hp = 0
        self.magic_points = 0
        self.effects = []
        self.location = 'Town Market'
        self.gave_over = False

# ---- Creating the Player ---- #
player = Player()

# ---- Play Game Function ---- #
"""
This function is used to play the game.
It is called when the player enters the 'play' command.
"""
def play_game():

    # MAP of the game
    """
    Index:
      1   2   3   4...
    -----------------
    |   |   |   |   | a
    -----------------
    |   |   |   |   | b
    -----------------
    |   |   |   |   | c
    ----------------- .
    |   |   |   |   | .
    ----------------- .
    """

    setup_game()


# ---- Help Screen ---- #
"""
This function displays the help screen and calls the main screen function.
"""
def help_screen():
    os.system('clear')

    # Displaying the Title
    print("\t#############################################\n")
    print("\t🎮     Welcome to TEXVENTURE ROG           🎮\n")
    print("\t#############################################\n")

    # Displaying the Help Screen
    print("\n\tHelp Screen\n     ")
    print("\t[1] Use 'up', 'down', 'left', and 'right' to move around,\n")
    print("\t[2] Type the commands to perform actions.\n")
    print("\t[3] Type 'look' to look around,\n")
    print("\n\tMade with ❤️" + " and 🐍 by RAO.exe\n")

    # Calling the main screen selection function
    main_screen_selection()

#  ---- Quit Game Function ---- #
"""
This function is used to quit the game.
It is called when the player enters the 'quit' command.
"""
def quit_game():
    os.system('clear')
    print("\n\t\tThanks for playing!\n")
    print("\t\tMade with ❤️ and 🐍 by RAO.exe\n")
    sys.exit()

# ---- Main Screen Selection ---- #
"""
    Interactive screen.
    Navigation through the command line.
    Commands:
        - play
        - help
        - quit
"""
def main_screen_selection():
    option = input("\nWhat would you like to do? 🎮\n> ")

    if option.lower() == "play":
        play_game()

    elif option.lower() == "help":
        help_screen()

    elif option.lower() == "quit":
        quit_game()

    else:
        print("\nI don't understand that command.\nPlease enter a valid command. ⚠️\n")
        main_screen_selection()

# ---- Main Screen ---- #
"""
This is the main screen of the game.
All the commands are listed here.
"""
def main_screen():
    os.system('clear')

    # Displaying the Title
    print("\t#############################################\n")
    print("\t🎮     Welcome to TEXVENTURE ROG           🎮\n")
    print("\t#############################################\n")

    # Displaying the Main Menu
    print("\n\t\tMain Menu\n     ")
    print("\t\t[1] Play Game > type 'play'\n")
    print("\t\t[2] Help > type 'help'\n")
    print("\t\t[3] Quit > type 'quit'\n")
    print("\n\t\tMade with ❤️ and 🐍 by RAO.exe\n")

    # Calling the main screen selection function
    main_screen_selection()


# ---- Game Interactions ---- #
"""
All the interactions with the game are listed here.
"""

# Player Interaction
def player_interact(action):
    if ZONE_MAP[player.location]["SOLVED"]:
        print("\nYou visited this place earlier. Move further!\n")
        return

    else:
        if action == 'inspect':
            print("\n" + ZONE_MAP[player.location]["DESCRIPTION"])
            return

        elif action == 'examine' or action == 'interact':
            print("\n" + ZONE_MAP[player.location]["EXAMINATION"])
            return

        elif action == 'look':
            # Display effects if there are any.
            if len(player.effects) > 0:
                print("\nYou have entitled with the following effects:")
                for effect in player.effects:
                    sys.stdout.write("\t" + effect + "\n")
                    sys.stdout.flush()
                    time.sleep(0.5)

                return

            else: 
                print("\nYou have no effects.\n")
                return

        else:
            print("\nI don't understand that command.\nPlease enter a valid command. ⚠️\n")
            return


# Movement Handler
def movement_handler(destination):
    if destination == '':
        print("\nYou cannot go that way.\n")
        return
    
    else:
        print("\n" + "You moved to the " + destination + ".")
        player.location = destination
        ZONE_MAP [player.location]["SOLVED"] = True

        show_location()
        return

# Player Movement
def player_move(myAction):
    dest = input("\nWhere would you like to move? 🚶\n> ")

    if dest in "UP":
        destination = ZONE_MAP[player.location]["UP"]
        
        movement_handler(destination)

    elif dest in "DOWN":
        destination = ZONE_MAP[player.location]["DOWN"]

        movement_handler(destination)

    elif dest in "LEFT":
        destination = ZONE_MAP[player.location]["LEFT"]

        movement_handler(destination)

    elif dest in "RIGHT":
        destination = ZONE_MAP[player.location]["RIGHT"]

        movement_handler(destination)

    else:
        print("\nI don't understand that command.\nPlease enter a valid command. ⚠️\n")
        player_move(myAction)


# Player Location
def show_location():
    print("\n" + ("#" * (4 + len(player.location))) )
    print("# " + player.location.upper() + " #")
    print("# " + ZONE_MAP[player.location]["DESCRIPTION"] + " #")
    print("\n" + ("#" * (4 + len(player.location))) )

# Prompt for Player Input
def prompt():
    acceptable_actions = ['move', 'travel', 'go', 'walk', 'inspect', 'examine', 'look', 'interact', 'quit']

    print("\n======================================")
    print("What would you like to do? ❔")
    action = input("> ")

    while action.lower() not in acceptable_actions:
        print("\nI don't understand that command.\nPlease enter a valid command. ⚠️\n")
        action = input("> ")

    if action.lower() == "quit":
        quit_game()

    elif action.lower() in ['move', 'travel', 'go', 'walk']:
        player_move(action.lower())

    elif action.lower() in ['inspect', 'examine', 'look', 'interact']:
        player_interact(action.lower())

# ---- Solved ---- #
"""
If the player has visited all the locations,
the game will end and the player will be congratulated.
"""
def ifSolved():
    count = 0

    for obj in ZONE_MAP:
        if obj["SOLVED"]: count += 1

    if count == len(ZONE_MAP): player.game_over = True

# Main Game Loop
def main_game_loop():
    
    while player.gave_over is False:
        prompt()


# ---- Setup Game ---- #
def setup_game():
    os.system('clear')

    # Name Input
    Q1 = "Are you new here?\nWhat is your name? 🤖"
    # Printing the question character by character
    for char in Q1:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.07)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)

    player_name = input("\n> ")

    # Name Validation
    if len(player_name) < 3:
        print("\nYour name is too short.\nPlease enter a valid name. ⚠️\n")
        setup_game()

    player.name = player_name

    # Username Input
    Q2 = "\nWhat should we call you Cheif? 💬"
    # Printing the question character by character
    for char in Q2:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.07)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)

    player_username = input("\n> ")

    # Username Validation
    if(len(player_username) < 3):
        shortUsrname = "\nYour username is too short.\nPlease enter a valid username. ⚠️\n"

        for char in shortUsrname:
            if char == " ":
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.03)
            else:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.02)
        
        # wait for user to press enter
        print("\nPress any key on the keyboard to continue. ")
        input("\n> ")

        setup_game()

    player.username = player_username

    # Player Trade
    Q3 = "\nWhat is your favorite trade? (Builder[⚒️], Miner[⛏], Fighter[⚔️])"
    # Printing the question character by character
    for char in Q3:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.07)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)

    player_trade = input("\n> ")

    # Trade Validation
    if player_trade.lower() not in TRADES:
        print("\nI don't understand that command.\nPlease enter a valid command. ⚠️\n")
        setup_game()

    player.trade = player_trade.lower()

    # Setting player hp, magic points and effects
    if player.trade == 'builder':
        player.hp = 100
        player.mp = 0
        player.effects = ['Medieval', 'Colonial', 'Futuristic']

    elif player.trade == 'miner':
        player.hp = 130
        player.mp = 0
        player.effects = ['Staircasing', 'Blast', 'Sea']

    elif player.trade == 'fighter':
        player.hp = 150
        player.mp = 50
        player.effects = ['Pillager Power', 'Warden Garden', 'Nether Nomad']

    
    # Welcoming the player
    O1 = "\nWelcome, " + player.name + "! The " + player.trade.upper() + "\n"
    for char in O1:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)

    O2 = player.username + " is your username" + ".\n"
    for char in O2:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)

    O3 = "Your health is " + str(player.hp) + ".\n"
    for char in O3:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)


    O4 = "Your magic points are " + str(player.mp) + "."
    for char in O4:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)

    # Starting the game
    O4 = "\nYou are in the " + player.location + "."
    for char in O4:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.06)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.04)

    O5 = "Type 'continue' or 'start' to begin."
    for char in O5:
        if char == " ":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.06)
        else:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.04)

    # Starting the game
    cont = input("\n> ")
    if cont.lower() in ['continue', 'start', 'c', 's']:
        main_game_loop()

    print("##########################")
    print("#  Welcome to the game!  #")
    print("#   Let's get started!   #")
    print("##########################")

    main_game_loop()

# ---- Game Start ---- #
main_screen()