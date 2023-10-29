from difflib import get_close_matches
import json

data = json.load(open("data.json"))

def translate(word):
    word = word.lower()
    close_matches = get_close_matches(word, data.keys())
    
    if word in data:
        return data[word]
    elif word.title() in data:
        return data[word.title()]
    elif word.upper() in data:
        return data[word.upper()]
    elif close_matches:
        suggestion = close_matches[0]
        decide = input(f"Did you mean {suggestion} instead? Press 'y' for yes or 'n' for no: ")
        if decide == "y":
            return data[suggestion]
        elif decide == "n":
            return "Sorry, your word is not found in the dictionary."
        else:
            return "You have entered an incorrect input. Please enter 'y' or 'n."
    else:
        return "You have entered a wrong word. Please try again."

word = input("Enter the word you want to search: ")
output = translate(word)

if type(output) == list:
    for item in output:
        print(item)
    else:
        print(output)
