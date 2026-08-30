import random

def jumble_word(word: str) -> str:
    """Convert word into a list of characters and shuffle until distinct from original."""
    if len(word) <= 1:
        return word

    jumbled = list(word)
    while True:
        random.shuffle(jumbled)
        res = ''.join(jumbled)
        if res != word:
            return res

def play_word_jumble():
    words = ['python', 'hangman', 'computer', 'keyboard', 'mouse', 'gamer', 'programming']
    word_to_guess = random.choice(words)
    jumbled_word = jumble_word(word_to_guess)

    print("=== Welcome to Word Jumble ===")
    print("Unscramble the letters to form a valid word. Type 'quit' to exit.")
    print("Jumbled word:", jumbled_word)

    attempts = 0
    while True:
        guess = input("Your guess: ").strip().lower()
        if guess in ('quit', 'q', 'exit'):
            print(f"Game exited. The word was: '{word_to_guess}'")
            return False

        attempts += 1
        if guess == word_to_guess:
            print(f"Congratulations! You guessed the word '{word_to_guess}' in {attempts} attempt(s)!")
            return True

        print("Incorrect guess. Try again!")

def main():
    play_word_jumble()

if __name__ == '__main__':
    main()

