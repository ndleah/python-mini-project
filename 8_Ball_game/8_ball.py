import random

# Randomly generated responses for the 8 Ball.
def magic_8_ball():
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook is good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook is not so good.",
        "Very doubtful."
    ]

# Prompt user to input question for 8 Ball response.
    while True:
        question = input("Ask the Magic 8 Ball a question (type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        answer = random.choice(responses)
        print("Magic 8 Ball says:", answer)

magic_8_ball()
