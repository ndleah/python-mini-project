 #Minimum number of guessing = log2(Upper bound – lower bound + 1)

import random as r
import math

#taking lower bound
lower = int(input("enter lower bound : -> "))

#taking upper bound
upper = int(input("enter upper bound : -> "))

#generating random number btw lower and upper ---> randit()
x = r.randint(lower, upper)

#definfg number of chances as per bounds
chance = round(math.log(upper - lower + 1))
print(f'you got {chance} chances lets start the game')

#initializing the number of guesss
guess_count = 0

while guess_count < chance:
    guess_count += 1

    #taking guessing number as input
    guss_num = int(input("Guess a number:-> "))

    #condition testing
    if x == guss_num:
        print('congratulation you did it right')
        # once num gueesed, loop will break
        break

    elif x > guss_num:
        print('You guessed to small')

    elif x < guss_num:
        print('You guessed to large')        

#if guessing is more than reqired guess --> show this output
if guss_num > chance:
    print(f"\n the number is this = {x}")
    print(f"\t Better luck next time")






