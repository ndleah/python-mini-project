import random, time
print("Welcome to number guessing game !!!")
time.sleep(2)
#generate a random number
x = random.randint(1, 10)
print("The number is generated!!!")
time.sleep(1)
print("You have 4 chances to guess")
#initialize the counter
count = 4
while count != 0:
    a = int(input("Guess the number : "))
    #if number guessed is correct, print correct
    if a == x:
        print("You are right, correct number is ", x)
        print("Congratulations! You won")
        break
    #if guessed number is greater
    elif a > x:
        print("The number is less than ", a)
    #if guessed number is smaller
    else:
        print("The number is greater than ", a)
    #decrease the counter after each guess
    count -= 1
