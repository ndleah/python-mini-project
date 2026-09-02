import random
import time

def play_game(total_chances: int = 4):
    print('Hello World! Welcome to the Number Guessing Game')
    time.sleep(0.5)

    n = random.randint(1, 10)
    print(f'Number has been generated between 1 and 10!!\nYou have {total_chances} chances to guess the number.')

    count = total_chances
    won = False

    while count > 0:
        raw_val = input(f'\nChances remaining: {count} - Guess the number: ').strip()
        try:
            a = int(raw_val)
        except ValueError:
            print("Invalid input! Please enter a valid integer between 1 and 10.")
            continue

        if a == n:
            print("Yay! That's right. You won! 🎉")
            won = True
            break
        elif a > n:
            print(f'The secret number is LESS than {a}')
        else:
            print(f'The secret number is GREATER than {a}')

        count -= 1

    if not won:
        print(f"\nGame Over! The correct number was {n}.")

def main():
    play_game()

if __name__ == '__main__':
    main()