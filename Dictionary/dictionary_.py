import json
import logging
import sys
from difflib import get_close_matches

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s: %(message)s')


class Translate:

    def __init__(self, file_name, word):
        self.file_name = file_name
        self.word = word
        self.data = self.read_file()

    def read_file(self):
        logging.debug(f"reading the file: {self.file_name}")
        data = json.load(open(self.file_name))
        logging.debug(f'The type of data: {type(data)}')
        return data

    def _translate(self):
        word = str.lower(self.word)
        if word in self.data:
            logging.debug(f"Found the word({word}) in the json file...")
            return self.data[word]
        elif word.title() in self.data:
            logging.debug(f"Found the word title({word.title()}) in the json file...")
            return self.data[word.title()]
        elif word.upper() in self.data:
            logging.debug(f"Found the word upper({word.upper()}) in the json file...")
            return self.data[word.upper()]
        elif len(get_close_matches(word, self.data.keys())) > 0:
            print("did you mean %s instead" % get_close_matches(word, self.data.keys())[0])
            decide = input("press y for yes or n for no: ")
            if decide == "y":
                return self.data[get_close_matches(word, self.data.keys())[0]]
            elif decide == "n":
                return ("pugger your paw steps on working keys ")

        else:
            logging.debug(f"Couldn't find the word({word}) in the json file...")





if __name__ == "__main__":
    word = input("Enter the word you want to search: ")
    t = Translate("data.json", word)
    output = t._translate()
    print(f'The output is :{output}')

