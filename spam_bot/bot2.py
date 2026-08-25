
import os
from bot1 import spammingBot

def run_bot2():
    text_path = os.path.join(os.path.dirname(__file__), 'text.txt')
    if not os.path.exists(text_path):
        print(f"Error: File '{text_path}' not found.")
        return

    with open(text_path, 'r', encoding='utf-8') as txt:
        content = txt.read()
        for word in content.split():
            print(f"Spamming word: {word}")
            spammingBot(word, count=1, delay=0.5)

def main():
    run_bot2()

if __name__ == '__main__':
    main()

