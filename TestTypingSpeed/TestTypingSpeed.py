import time
import random

SAMPLE_SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a versatile programming language used for automation and data science.",
    "Practice makes perfect when developing typing speed and accuracy.",
    "Software engineering requires logical thinking and attention to detail."
]

def get_random_sentence() -> str:
    """Generate a random sentence or fallback if generator library is missing."""
    try:
        from essential_generators import DocumentGenerator
        gen = DocumentGenerator()
        return gen.sentence()
    except Exception:
        return random.choice(SAMPLE_SENTENCES)

def calculate_accuracy(original: str, typed: str) -> float:
    """Calculate typing accuracy percentage based on word token matches."""
    orig_words = original.strip().split()
    typed_words = typed.strip().split()

    if not orig_words:
        return 100.0

    matches = 0
    for o_w, t_w in zip(orig_words, typed_words):
        if o_w.lower().strip(".,!?") == t_w.lower().strip(".,!?"):
            matches += 1

    return round((matches / len(orig_words)) * 100.0, 2)

def typing_speed(custom_input: str = None):
    """Run typing speed test and output performance statistics."""
    sentence = get_random_sentence()
    orig_words = sentence.split()
    word_count = len(orig_words)

    print("\n----------------------------------------")
    print(f"Target Sentence:\n{sentence}")
    print("----------------------------------------")

    start_time = time.time()
    if custom_input is not None:
        text_input = custom_input
        end_time = start_time + 5.0
    else:
        text_input = str(input("Type the sentence above:\n"))
        end_time = time.time()

    time_taken = max(round(end_time - start_time, 2), 0.01)
    accuracy = calculate_accuracy(sentence, text_input)
    wpm = round((word_count / (time_taken / 60.0)))

    print("----------------------------------------")
    print(f"Accuracy   : {accuracy}%")
    print(f"Time Taken : {time_taken} seconds")
    print(f"Typing Speed: {wpm} Words Per Minute (WPM)")
    print("----------------------------------------")

    if accuracy < 50 or wpm < 30:
        print("Keep practicing to improve your speed and accuracy!")
    elif accuracy < 80 or wpm < 60:
        print("Great job! You are doing very well.")
    else:
        print("Outstanding! You have exceptional typing skills!")

def main():
    print("=== Typing Speed Test ===")
    typing_speed()

    while True:
        try:
            retry = input("\nDo you want to try again? (y/n): ").strip().lower()
            if retry == 'y':
                typing_speed()
            else:
                print("Thanks for playing!")
                break
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()
    