import random
import time
from ascii import ascii_art
import os

def is_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# check if user wants to flip another coin with a boolean. raise exception if necessary
def yes_or_no(user_input):
    if user_input == "y" or user_input == "Y":
        flip_again = True
    elif user_input == "n" or user_input == "N":
        flip_again = False
    else:
        raise Exception("Please enter y or n")
    return flip_again
    

def main(): 
    last_flip = None
    sequential_flip = 1
    heads_or_tails = None
    flip_again = True
    username = None
    score = 0
    high_score = 0

    clear_terminal()
    print("Hi! please enter a username:")
    username = input()

    clear_terminal()
    print("Press ENTER to flip a coin!")
    input()

    while flip_again == True:
        coin_flip = random.randint(0, 1)

        if coin_flip == 1:
            heads_or_tails = "heads"
        else:
            heads_or_tails = "tails"
        
        clear_terminal()
        print("Flipping coin now...")
        time.sleep(2)

        #display coin flip art
        ascii_art(coin_flip)

        #display message if coin is heads or tails multiple times in a row plus user score           
        if sequential_flip >= 9 and coin_flip == last_flip:
            sequential_flip += 1
            score += 10 ** sequential_flip
            high_score = is_high_score(score, high_score)
            print(f"\n Unbelievable! {username} flipped {sequential_flip} {heads_or_tails} in a row!!!    Score:{score}  High Score:{high_score}")
        elif sequential_flip >= 4 and coin_flip == last_flip:
            sequential_flip += 1
            score += 10 * sequential_flip ** 2
            high_score = is_high_score(score, high_score)
            print(f"\n Crazy! {username} flipped {sequential_flip} {heads_or_tails} in a row!!!    Score:{score}  High Score:{high_score}")
        elif coin_flip == last_flip:
            sequential_flip += 1
            score += 10 * sequential_flip
            high_score = is_high_score(score, high_score)
            print(f"\nWow! {username} flipped {sequential_flip} {heads_or_tails} in a row!!    Score:{score}  High Score:{high_score}")
        elif sequential_flip > 1 and coin_flip != last_flip:
            sequential_flip = 1
            score = 10
            print(f"\nYou got {heads_or_tails}, streak lost!    Score:{score}  High Score:{high_score}")
        else:
            score = 10
            high_score = is_high_score(score, high_score)
            print(f"\nYou got {heads_or_tails}!    Score:{score}  High Score:{high_score}")

        # next iteration this is used to see if user got 2 or more heads/tails in a row
        last_flip = coin_flip
        
        print("\n\nFlip another coin?")

        while True:
            try:
                flip_again = yes_or_no(input())
                break
            except Exception as e:
                print(e)


main()