import random
from question_bank import easy_question, hard_question
from answer_bank import answer

def print_congratulations(text: str = "Congratulations!"):
    """Print ASCII art congratulations message or fallback."""
    try:
        from art import tprint
        tprint(text)
    except Exception:
        print(f"\n🎉 {text.upper()} 🎉\n")

def generate_question(seen_questions: set) -> tuple:
    """Generate a random unasked question from easy or hard bank."""
    easy_qlist = [2, 3, 4, 8, 9, 14, 15, 16]
    hard_qlist = [1, 5, 6, 7, 10, 11, 12, 13]

    available_easy = [q for q in easy_qlist if q not in seen_questions]
    available_hard = [q for q in hard_qlist if q not in seen_questions]

    if not available_easy and not available_hard:
        seen_questions.clear()
        available_easy = easy_qlist
        available_hard = hard_qlist

    difficulty = random.choice([1, 2])
    if difficulty == 1 and available_easy:
        q_num = random.choice(available_easy)
        q_text = easy_question(q_num)
    elif available_hard:
        q_num = random.choice(available_hard)
        q_text = hard_question(q_num)
    else:
        q_num = random.choice(available_easy)
        q_text = easy_question(q_num)

    seen_questions.add(q_num)
    return q_num, q_text

def generate_answer(num: int) -> str:
    return answer(num)

def main():
    print("=== Welcome to GK Maestro ===")
    print("Test your general knowledge skills across 10 questions!\n")

    ques_count = 1
    score = 0
    seen_questions = set()

    while ques_count <= 10:
        q_num, question = generate_question(seen_questions)

        print(f"Question {ques_count}/10: {question}")
        user_answer = input("Your Answer: ").strip()

        correct_answer = generate_answer(q_num)

        if user_answer.lower() == correct_answer.lower():
            score += 1
            print(f"✅ Correct! Score: {score}/10\n")
        else:
            print(f"❌ Wrong! Correct answer was: '{correct_answer}'. Score: {score}/10\n")

        ques_count += 1

    print(f"Final Score: {score}/10")

    if score == 10:
        print_congratulations("Congratulations!")
        print("You answered all 10 questions correctly!")
    elif score >= 7:
        print("Great job! You passed with high distinction!")
    else:
        print("Good effort! Try again to get a perfect score!")

if __name__ == "__main__":
    main()

