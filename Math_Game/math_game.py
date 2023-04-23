import random
import operator

def random_problem(level):
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    num_1 = random.randint(1, 10*level)
    num_2 = random.randint(1, 10*level)
    operation = random.choice(list(operators.keys()))
    answer = operators.get(operation)(num_1, num_2)
    print(f'What is {num_1} {operation} {num_2}')
    return round(answer,1)

def ask_question(level):
    answer = random_problem(level)
    guess = float(input('Enter you answer: '))
    return guess == answer

def game():
    score = 0
    level = 1
    while True:
        if ask_question(level) == True:
            score += 1
            print('Correct !')
            if score/level >=5 :
                level +=1
                print(f"Level Up : Level {level}")
        else:
            print('Incorrect')
            break
    print(f'======== Game Over ========\nYou score is {score}\nKepp going!')

game()