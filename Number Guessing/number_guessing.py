import random
import time
print('Hello World! Welcome to the game')
time.sleep(2)
n = random.randint(1, 10)
print('Number has been generated!!\nYou have 4 chances to guess the number')

count = 4

while count!=0:
    a = int(input('Guess the number: '))

    if a == n:
        print("Yay! That's right. You won!")
        break
    elif a > n:
        print('The number is less than ', a)
    else:
        print('The number is greater than ', a)
    count=-1