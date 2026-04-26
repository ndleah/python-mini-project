import random
import operator

OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

DIFFICULTY_SETTINGS = {
    'easy':   {'range': (1, 10),  'ops': ['+', '-']},
    'medium': {'range': (1, 20),  'ops': ['+', '-', '*', '/']},
    'hard':   {'range': (1, 50),  'ops': ['+', '-', '*', '/']},
}

def get_valid_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Invalid input — please enter a number.')

def get_difficulty():
    while True:
        choice = input('Choose difficulty (easy / medium / hard): ').strip().lower()
        if choice in DIFFICULTY_SETTINGS:
            return DIFFICULTY_SETTINGS[choice]
        print('Please enter easy, medium, or hard.')

def random_problem(settings):
    low, high = settings['range']
    operation = random.choice(settings['ops'])
    num_1 = random.randint(low, high)

    if operation == '/':
        # Ensure clean division — no ugly decimals
        num_2 = random.randint(1, num_1)
        while num_1 % num_2 != 0:
            num_2 = random.randint(1, num_1)
    else:
        num_2 = random.randint(low, high)

    answer = round(OPERATORS[operation](num_1, num_2), 3)
    print(f'\nWhat is {num_1} {operation} {num_2}?')
    return answer

def ask_question(settings):
    answer = random_problem(settings)
    guess = get_valid_input('Your answer: ')
    return guess == answer

def game():
    print('=== Math Game ===')
    settings = get_difficulty()

    total = int(input('How many questions? '))
    score = 0

    for q in range(1, total + 1):
        print(f'Question {q} of {total}')
        if ask_question(settings):
            score += 1
            print('Correct!')
        else:
            print('Incorrect.')

    pct = round((score / total) * 100)
    print(f'\n======== Game Over ========')
    print(f'Score: {score}/{total} ({pct}%)')
    if pct == 100:
        print('Perfect score!')
    elif pct >= 70:
        print('Nice work!')
    else:
        print('Keep practicing!')

game()