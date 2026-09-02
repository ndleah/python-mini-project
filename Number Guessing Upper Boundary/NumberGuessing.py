import random
import time

def get_int_input(prompt: str) -> int:
    """Helper to safely prompt user for integer input."""
    while True:
        try:
            val = input(prompt).strip()
            return int(val)
        except ValueError:
            print("Invalid input! Please enter a valid whole integer number.")

def play_game():
    print('Hello! Welcome to the Number Guessing Game')
    time.sleep(0.5)

    upper_boundary = get_int_input('Enter an upper boundary (e.g. 100): ')
    while upper_boundary <= 1:
        print("Upper boundary must be greater than 1.")
        upper_boundary = get_int_input('Enter an upper boundary: ')

    lower_boundary = 1
    answer = random.randint(lower_boundary, upper_boundary)

    current_min = lower_boundary
    current_max = upper_boundary
    attempts = 0

    print(f"Number generated between {lower_boundary} and {upper_boundary}!")

    while True:
        guess = get_int_input(f"Guess the answer (between {current_min} and {current_max}): ")
        attempts += 1

        if guess < lower_boundary or guess > upper_boundary:
            print(f"Out of bounds! Please enter a number between {lower_boundary} and {upper_boundary}.")
            continue

        if guess == answer:
            print(f"Congrats, Your guess '{guess}' is correct! (Total attempts: {attempts}) 🎉")
            break
        elif guess < answer:
            print(f"Your guess ({guess}) is lower than the answer. Try higher!")
            current_min = max(current_min, guess + 1)
        else:
            print(f"Your guess ({guess}) is higher than the answer. Try lower!")
            current_max = min(current_max, guess - 1)

def main():
    play_game()

if __name__ == '__main__':
    main()

