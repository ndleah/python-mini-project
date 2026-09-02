import random

one = """
+-----------+
|           |
|     O     |
|           |
+-----------+
"""

two = """
+-----------+
| O         |
|           |
|         O |
+-----------+
"""

three = """
+-----------+
| O         |
|     O     |
|         O |
+-----------+
"""

four = """
+-----------+
| O       O |
|           |
| O       O |
+-----------+
"""

five = """
+-----------+
| O       O |
|     O     |
| O       O |
+-----------+
"""

six = """
+-----------+
| O       O |
| O       O |
| O       O |
+-----------+
"""

DICE_FACES = {
    1: one,
    2: two,
    3: three,
    4: four,
    5: five,
    6: six
}

def roll_dice(num_dice=2):
    """Roll a specified number of independent dice with replacement."""
    return [random.randint(1, 6) for _ in range(num_dice)]

def main():
    print("=================================")
    print("    Welcome to Dice Simulator    ")
    print("=================================")

    rolling = True
    while rolling:
        dice_values = roll_dice(2)

        print(f"\nYou rolled: {dice_values[0]} and {dice_values[1]} (Total: {sum(dice_values)})")
        for val in dice_values:
            print(DICE_FACES[val])

        response = input("Press [Enter] or 'y' to roll again, or 'q' to quit: ").strip().lower()
        if response in ('q', 'quit', 'n', 'no', 'exit'):
            rolling = False
            print("Thanks for playing!")

if __name__ == "__main__":
    main()