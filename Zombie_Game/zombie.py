import random

def play_zombie_quiz():
    score = 0

    try:
        print("""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠾⠛⠉⠉⠀⠀⠀⠀⠀⠀⢀⡤⠊⠉⠉⠛⠳⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢮⡀⠀⠀⠀⠀⠀⠀⠙⢷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⡡⢤⠀⠀⠀⢰⣛⣉⣉⣓⠢⣄⠀⠀⠀⠈⢉⡁⠐⠒⠒⠂⠉⠉⠉⠛⢶⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡞⠁⣘⡒⠁⢀⠀⠀⠀⣀⣀⣀⣈⣹⣾⣕⠀⢠⡎⠁⡹⠀⣠⠄⠀⠀⠀⠀⠀⠀⠙⢷⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⢀⣎⡩⠃⢠⣏⡴⠞⠛⠉⠉⠀⠀⠀⠀⠹⡏⠀⠉⠉⣠⣾⠖⠋⠉⠻⣅⠀⣠⠖⢲⠌⢻⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⡠⠔⢿⠀⢀⡟⠉⠀⠀⠀⣀⣤⣤⡀⠀⠀⠀⣿⠀⠀⠀⡼⠉⠉⠒⢦⣀⠘⠷⡛⠒⡿⣄⠈⣷⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⣠⠏⠀⢸⠀⠀⠀⠀⢰⣿⣿⣿⡇⠀⠀⢀⡿⠀⠀⣸⠃⠀⠀⣀⣄⡙⢷⣄⡇⠘⠀⢸⡆⢹⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣧⠞⠁⠀⠀⢸⡆⠀⠀⠀⠸⣿⣿⡿⠃⠀⢀⣼⠃⠀⠀⣿⣆⠀⠀⣿⣿⡟⠀⠙⣧⠳⡤⠞⠀⢸⡇⠀⠀⠀⠀
⠀⢀⣠⠤⠤⢄⡀⠈⣧⢈⣧⠀⠀⢸⣿⣄⣀⣀⣠⣬⣥⠴⠶⢚⣿⠋⠀⠀⠀⢻⣿⣦⣄⠈⠁⠀⠀⣰⠟⠆⠀⠀⠀⢸⣡⠴⠖⠶⣦
⢠⠏⠀⠀⠀⢀⠈⠓⢿⡄⢳⠀⠀⠀⢳⣌⠻⠯⣤⣀⣀⣀⣴⣿⠏⢀⣶⢰⣦⠈⢿⣿⣿⣷⣀⣠⡼⠋⠀⢀⡀⠀⢀⣿⠥⢄⠀⠀⣿
⣏⠀⠀⠀⡟⢉⡽⣦⡈⢻⣼⠄⠀⠀⠀⠉⠓⠦⠤⠬⣏⣡⠾⠃⢀⣾⣿⢸⣿⣇⠈⠻⡯⠽⢯⡽⠁⠠⣴⠝⠃⢀⣾⢋⣁⠈⢀⡾⠃
⠘⠶⠲⢦⣷⠸⣤⣸⡇⠀⢻⣦⡀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠘⠛⠋⠘⠋⠋⠀⠀⠑⠚⠉⠀⠀⠀⠈⣠⣠⡾⠳⠤⣿⡀⣾⠁⠀
⠀⠀⠀⠀⠸⢧⠉⠉⠀⢀⡾⠀⠉⠻⣦⠀⠀⠀⠈⢟⡽⠄⠀⠀⢀⣀⣤⣤⣤⣄⣀⠀⠀⠀⢀⡀⠀⠀⣴⡿⠛⠻⢶⣤⣿⡿⠋⠀⠀
⠀⠀⠀⠀⠀⠙⠒⠒⠚⠋⠀⠀⠀⠀⠸⣧⠀⠀⠀⠀⠁⠀⣠⣾⡿⢿⠀⠀⢀⣮⣙⡻⣦⡈⠙⠿⠀⣸⠏⠀⠀⠀⠀⢀⣿⣇⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡆⠀⠀⠀⠀⣼⣿⣿⣇⣸⣷⣶⣾⡀⣯⣻⣿⣿⡄⠀⠀⡿⠀⠀⠀⠀⠀⢻⣾⡛⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⡇⠀⠀⠀⠀⠀⠀⠛⠟⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⡀⠀⢸⣿⣿⡟⢻⡿⠿⣇⣿⢸⠿⣿⣿⣿⡏⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠐⡇⠀⠸⣯⠉⠙⠒⣃⣀⣈⣭⣭⣤⣀⣩⡟⠁⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠃⠀⣀⣽⠷⠞⠛⠉⠉⠁⠀⣠⠤⠤⢤⣉⠙⠢⠤⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⠀⠘⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣶⠀⠹⠂⠀⣰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠶⢦⣤⣀⣀⠀⠀⠀⠀⢀⣈⣛⣥⣤⠴⠾⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""")
    except UnicodeEncodeError:
        print("=== ZOMBIE SURVIVAL QUIZ ===")

    print("Take this quiz and find out how long you would survive amongst the walking dead.")
    print("There are easy, intermediate and hard questions all mixed together.")
    print("There may be more than one correct answer.\nGood luck!")

    # ---- question 1 ----
    print("Your house is burning down. What do you save?")
    print("""(1) your dog\n(2) some food cans\n(3) your clothes\n(4) your cell phone""")
    answer = input(">").strip()
    if answer == "1":
        score += random.randint(10, 20)
    elif answer == "2":
        score += random.randint(5, 10)
    else:
        score += 3
    print("")

    # ---- question 2 ----
    print("It is night, and you will freeze to death soon. Making too much noise/light will attract the zombies. What do you do?")
    print("""(1) keep moving around\n(2) build a tiny fire\n(3) build a normal fire\n(4) try to wait out the night""")
    answer = input(">").strip()
    if answer == "2":
        score += random.randint(10, 20)
    elif answer == "4":
        score += random.randint(5, 10)
    else:
        score += 3
    print("")

    # ---- question 3 ----
    print("You are cornered in a grocery store with only a knife. A horde is moving in from all sides. What do you do?")
    print("""(1) kill zombies to make a path\n(2) try to climb up on the wobbly shelves\n(3) shout for help\n(4) surrender""")
    answer = input(">").strip()
    if answer == "2":
        score += random.randint(10, 20)
    elif answer == "1":
        score += random.randint(5, 10)
    else:
        score += 3
    print("")

    # ---- question 4 ----
    print("You see a group of survivors ahead on the road. What do you do?")
    print("""(1) watch them for a while\n(2) ignore them\n(3) kill them and steal their stuff\n(4) try to greet them""")
    answer = input(">").strip()
    if answer == "1":
        score += random.randint(10, 20)
    elif answer == "3":
        score += random.randint(5, 10)
    else:
        score += 3
    print("")

    # ---- question 5 ----
    print("A group of about 6 people take your stuff at gunpoint, then tell you to get in a storage container. What do you do?")
    print("""(1) get in the container\n(2) try to reason with them\n(3) refuse\n(4) try to fight them""")
    answer = input(">").strip()
    if answer == "1":
        score += random.randint(10, 20)
    elif answer == "4":
        score += random.randint(5, 10)
    else:
        score += 3
    print("")

    # ---- question 6 ----
    print("You and 3 other people are down to 1 last can of food. What do you do?")
    print("""(1) share it\n(2) eat it\n(3) give it to them\n(4) burn it so there is no argument""")
    answer = input(">").strip()
    if answer == "2":
        score += random.randint(10, 20)
    elif answer == "1":
        score += random.randint(5, 10)
    else:
        score += 3
    print("")

    # ---- question 7 ----
    print("You are given the choice between 4 weapons. What do you take?")
    print("""(1) katana\n(2) crossbow\n(3) pistol\n(4) RPG""")
    answer = input(">").strip()
    if answer == "2":
        score += random.randint(10, 20)
    elif answer == "3":
        score += random.randint(5, 10)
    else:
        score += 3
    print("")

    # ---- question 8 ----
    print("You only have room in your pack for 1 more package of food. What do you take?")
    print("""(1) trail mix\n(2) crackers\n(3) oreos\n(4) raw chicken""")
    answer = input(">").strip()
    if answer == "3":
        score += random.randint(10, 20)
    elif answer == "4":
        score += random.randint(5, 10)
    else:
        score += 3  
    print("")

    # ---- question 9 ----
    print("You have some choices on where to set up camp.")
    print("""(1) next to the river\n(2) in the mountains\n(3) near the ocean\n(4) next to the city""")
    answer = input(">").strip()
    if answer == "1":
        score += random.randint(10, 20)
    elif answer == "2":
        score += random.randint(5, 10)
    else:
        score += 3  
    print("")

    # ---- question 10 ----
    print("Your camp, with your group of ~20 people, has been overrun by a horde. What do you do?")
    print("""(1) follow your friends\n(2) run\n(3) try and save the camp\n(4) get your stuff from your tent""")
    answer = input(">").strip()
    if answer == "3":
        score += random.randint(10, 20)
    elif answer == "4":
        score += random.randint(5, 10)
    else:
        score += 3  
    print("")

    # ---- end ----
    print("The results are in!")
    print(f"You scored {score} points!")

    if 0 <= score <= 20:
        print('You would be one of the first people to die in the apocalypse.\nYou panic at the sight of a zombie and have no survival skills, getting eaten within an hour.')
    elif 21 <= score <= 50:
        print('You would live a few days in the apocalypse.\nAs the chaos begins, you attempt to go to emergency shelters, but die when they get overcrowded and overrun.')
    elif 51 <= score <= 80:
        print('You would live a month in the apocalypse.\nYou find a camp and manage to survive for a month, but when the camp gets overrun, you get bit.')
    elif 81 <= score <= 110:
        print('You would live a few months in the apocalypse.\nYour camp moves from place to place before settling at an old school building.')
    elif 111 <= score <= 130:
        print('You would live a few years in the apocalypse.\nYour group settles at a town, fortifying it so that it can withstand a horde.')
    else:
        print('You would live for a really long time in the apocalypse.\nBeing the leader of your group, you help build a utopia named Z-Land.')

def main():
    play_zombie_quiz()

if __name__ == "__main__":
    main()

