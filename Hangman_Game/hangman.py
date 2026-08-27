import random

HANGMAN_PICS = {
    9: "  --------  ",
    8: "  ---------  \n      O      ",
    7: "  ---------  \n      O      \n      |      ",
    6: "  ---------  \n      O      \n      |      \n     /       ",
    5: "  ---------  \n      O      \n      |      \n     / \\     ",
    4: "  ---------  \n    \\ O      \n      |      \n     / \\     ",
    3: "  ---------  \n    \\ O /    \n      |      \n     / \\     ",
    2: "  ---------  \n    \\ O /|   \n      |      \n     / \\     ",
    1: "  ---------  \n    \\ O_|/   \n      |      \n     / \\     ",
    0: "  ---------  \n      O_|    \n     /|\\     \n     / \\     "
}

def print_stage(turns):
    if turns in HANGMAN_PICS:
        if turns == 1:
            print("Last breaths counting. Take care!")
        print(f"{turns} turns left")
        print(HANGMAN_PICS[turns])

def hangman():
    words = ["tiger", "superman", "thor", "doraemon", "avenger", "water", "stream"]
    word = random.choice(words)
    turns = 10
    guessed_letters = set()

    while turns > 0:
        display_word = " ".join([letter if letter in guessed_letters else "_" for letter in word])
        print("\nGuess the word:", display_word)

        if all(letter in guessed_letters for letter in word):
            print(f"\nCongratulations! You guessed the word '{word}'!")
            print("You win!")
            return True

        guess = input("Enter a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input! Please enter a single alphabetic character.")
            continue

        if guess in guessed_letters:
            print(f"You have already guessed '{guess}'. Try another letter!")
            continue

        guessed_letters.add(guess)

        if guess not in word:
            turns -= 1
            print_stage(turns)

    print("\nYou lose!")
    print("You let a kind man die.")
    print(f"The word was: '{word}'")
    return False

def main():
    name = input("Enter your name: ").strip()
    if not name:
        name = "Player"
    print(f"Welcome {name}")
    print("=====================")
    print("Try to guess the word in 10 attempts or less!")
    hangman()

if __name__ == "__main__":
    main()

