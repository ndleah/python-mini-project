import random

def play_madlibs(inputs: dict = None) -> str:
    """Generate Madlibs story interactively or using provided inputs dictionary."""
    print("--- Title: Eat, Drink, And Be Sick ---")

    if inputs is None:
        inputs = {}

    def get_input(key, prompt):
        if key in inputs:
            return inputs[key]
        return input(prompt).strip() or "something"

    noun = inputs.get("noun")
    if not noun:
        noun = [get_input(f"noun_{i}", f"Enter noun ({i+1}/4): ") for i in range(4)]

    plural = inputs.get("plural")
    if not plural:
        plural = [get_input(f"plural_{i}", f"Enter plural noun ({i+1}/6): ") for i in range(6)]

    adjective = inputs.get("adjective")
    if not adjective:
        adjective = [get_input(f"adj_{i}", f"Enter adjective ({i+1}/2): ") for i in range(2)]

    adverb = get_input("adverb", "Enter adverb: ")
    letter = get_input("letter", "Enter any letter: ")
    body_part = get_input("body_part", "Enter any body part: ")

    lines = [
        f"An inspector from the Department of Health and {random.choice(noun)} Services paid a surprise visit to our {random.choice(adjective)} school cafeteria.",
        f"The lunch special, prepared by our {random.choice(adjective)} dietician, was spaghetti and {random.choice(noun)} balls with a choice of either a {random.choice(noun)} salad or French {random.choice(plural)}.",
        f"The inspector found the meat-{random.choice(plural)} to be overcooked and discovered a live {random.choice(noun)} in the fries, causing him to have a {body_part} ache.",
        f"In response, he threw up all over his {random.choice(plural)}.",
        f"In his report, the inspector {adverb} recommended that the school cafeteria serve only nutritious {random.choice(plural)} as well as low-calorie {random.choice(plural)} and that all of the saturated {random.choice(plural)} be eliminated.",
        f"He rated the cafeteria a {letter}-minus."
    ]

    story = "\n".join(lines)
    print("\n" + story)
    return story

def main():
    play_madlibs()

if __name__ == '__main__':
    main()

