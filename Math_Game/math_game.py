import math
import random
import operator

def error_handle() -> float:
    """Safely prompt user until a valid numeric answer is entered."""
    while True:
        try:
            val = float(input('Please enter a valid numeric answer: '))
            return val
        except ValueError:
            print("Invalid input! Please enter a number.")

def random_problem() -> tuple:
    """Generate a random math problem and calculate expected answer."""
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    num_1 = random.randint(1, 10)
    num_2 = random.randint(1, 10)
    op_char = random.choice(list(operators.keys()))
    answer = float(operators[op_char](num_1, num_2))

    print(f'What is {num_1} {op_char} {num_2}?')
    return answer, f"{num_1} {op_char} {num_2}"

def ask_question() -> bool:
    answer, prob_str = random_problem()
    try:
        guess = float(input('Enter your answer: '))
    except ValueError:
        guess = error_handle()

    # Use tolerance for float comparison, especially on division
    is_correct = math.isclose(guess, answer, abs_tol=0.01)
    if is_correct:
        print(f"Correct! ({prob_str} = {answer:.3f})")
    else:
        print(f"Incorrect. Expected ~{answer:.3f}, got {guess}")
    return is_correct

def game():
    print("=== Welcome to Math Game ===")
    score = 0
    while True:
        if ask_question():
            score += 1
            print("Keep going!\n")
        else:
            break
    print(f'======== Game Over ========\nYour final score is: {score}\nGreat effort!')

def main():
    game()

if __name__ == '__main__':
    main()

