import random
import operator

def random_problem():
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    num_1 = random.randint(1, 10)
    num_2 = random.randint(1, 10)
    operation = random.choice(list(operators.keys()))
    answer = operators.get(operation)(num_1, num_2)
    print(f'Quanto é {num_1} {operation} {num_2}')
    return answer

def ask_question():
    answer = random_problem()
    guess = float(input('Digite a sua resposta: '))
    return guess == answer

def game():
    score = 0
    while True:
        if ask_question() == True:
            score += 1
            print('Correto!')
        else:
            print('Incorreto')
            break
    print(f'======== Game Over ========\nSua pontuação foi {score}!')

game()
