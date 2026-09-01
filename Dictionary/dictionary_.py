import os
import json
import logging
import sys
from difflib import get_close_matches

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s: %(message)s')

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

class Translate:

    def __init__(self, file_name=DEFAULT_DATA_FILE, word=""):
        self.file_name = file_name
        self.word = word
        self.data = self.read_file()

    def read_file(self):
        logging.debug(f"reading the file: {self.file_name}")
        try:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logging.debug(f'The type of data: {type(data)}')
                return data
        except FileNotFoundError:
            logging.error(f"File not found: {self.file_name}")
            return {}

    def _translate(self):
        if not self.data:
            return "Dictionary data unavailable."

        word = str.lower(self.word).strip()
        if word in self.data:
            logging.debug(f"Found the word({word}) in the json file...")
            return self.data[word]
        elif word.title() in self.data:
            logging.debug(f"Found the word title({word.title()}) in the json file...")
            return self.data[word.title()]
        elif word.upper() in self.data:
            logging.debug(f"Found the word upper({word.upper()}) in the json file...")
            return self.data[word.upper()]
        else:
            matches = get_close_matches(word, self.data.keys())
            if len(matches) > 0:
                suggestion = matches[0]
                print(f"Did you mean '{suggestion}' instead?")
                decide = input("press y for yes or n for no: ").strip().lower()
                if decide == "y":
                    return self.data[suggestion]
                else:
                    return "Search cancelled."
            else:
                logging.debug(f"Couldn't find the word({word}) in the json file...")
                return "The word does not exist in the dictionary."

if __name__ == "__main__":
    if len(sys.argv) > 1:
        word = ' '.join(sys.argv[1:])
    else:
        word = input("Enter the word you want to search: ")

    t = Translate(DEFAULT_DATA_FILE, word)
    output = t._translate()
    print(f'The output is: {output}')
