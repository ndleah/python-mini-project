import os
import sys
import random

FALLBACK_WORDS = ["python", "hangman", "developer", "algorithm", "software", "keyboard", "computer", "variable"]

def is_valid_guess(guess: str) -> bool:
    """Check if guess is a single lowercase letter."""
    return guess.isalpha() and len(guess) == 1

def display_word(secret_word: str, guessed: set):
    """Display secret word with guessed letters revealed and underscores for hidden letters."""
    out = [letter if letter in guessed else "_" for letter in secret_word]
    print(" ".join(out))

def get_random_word_from_file(filename: str = "words.txt") -> str:
    """Load random word from file or fallback word list."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename) if not os.path.isabs(filename) else filename

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                words = [w.strip().lower() for w in file.readlines() if w.strip()]
                if words:
                    return random.choice(words)
        except Exception as e:
            print(f"Notice: Error reading '{file_path}' ({e}). Using fallback words.")

    return random.choice(FALLBACK_WORDS)

def play_game():
    secret_word = get_random_word_from_file("words.txt")
    guessed = set()
    max_attempts = 6
    attempts = 0

    print("\nWelcome to Hangman!")
    print("Try to guess the secret word!")

    while attempts < max_attempts:
        print("\nWord:", end=" ")
        display_word(secret_word, guessed)

        guess = input("Guess a letter: ").strip().lower()

        if not is_valid_guess(guess):
            print("Invalid guess. Please enter a single letter (a-z).")
            continue

        if guess in guessed:
            print("You've already guessed that letter!")
            continue

        guessed.add(guess)

        if guess not in secret_word:
            attempts += 1
            print(f"Incorrect guess! Attempts remaining: {max_attempts - attempts}")
        elif all(letter in guessed for letter in secret_word):
            print(f"\n🎉 Congratulations! You've guessed the word: '{secret_word}'!")
            return True

    print(f"\nGame Over! You've run out of attempts. The word was: '{secret_word}'")
    return False

def main():
    while True:
        play_game()
        play_again = input("\nDo you want to play again? (Y/N): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing Hangman! Goodbye!")
            break

if __name__ == "__main__":
    main()

