import random
import time

guess = None
upper_boundary = None
lower_boundary = 1

try:
    print('Hello! Welcome to the Number Guessing game')
    time.sleep(1)
    upper_boundary = int(input('Enter an upper boundary: '))
    answer = random.randint(1, upper_boundary)
    time.sleep(1)
    guess = int(input('Guess the answer by enter a number between {0} and {1}: '.format(lower_boundary,upper_boundary)))

    while guess != answer:
        if guess < 1 or guess > upper_boundary:
            time.sleep(1)
            guess = int(input('Invalid input! Please enter a number between {0} and {1}: '.format(lower_boundary,upper_boundary)))
        elif guess < answer:
            print('Your guess is lower than the answer. Try again!')
            lower_boundary = guess
            time.sleep(1)
            guess = int(input('Enter a number between {0} and {1}: '.format(lower_boundary,upper_boundary)))
        elif guess > answer:
            print('Your guess is higher than the answer. Try again!')
            upper_boundary = guess
            time.sleep(1)
            guess = int(input('Enter a number between {0} and {1}: '.format(lower_boundary,upper_boundary)))

    print('Congrats, Your guess is correct!')

except Exception as e:
    if upper_boundary is None:
        upper_boundary = int(input('Please enter a number for upper boundary: '))
    else:
        guess = int(input('Invalid input! Please enter a number between {0} and {1}: '.format(lower_boundary,upper_boundary)))
