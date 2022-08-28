text = [
    'yes ✔',
    'no ⭕',
    'maybe 🤔',
    'go for it 🤪',
    'come on man, do it 😤',
    'bruh are you serious ? 🙄',
    "let's keep that part aside 💨",
    'you can do it 🤟',
    'try it, maybe ? 🙃'
]

from random import choice

run = True

while run:
    print("Welcome to Decision Maker :). Please say What you want to decide ?")
    print("If want to quit, Please type 'quit'")
    decision = input("Here: ")
    if decision.lower() == 'quit':
        run = False
    else:
        print(choice(text))
    print(" " * 100)