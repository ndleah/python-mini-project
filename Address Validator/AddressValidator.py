import re

print("This program will decide if your input is a valid email address")
while(True):
    print("A valid email address must be in the format example@example.com.")
    x = input("Input your email address: ")

    result = re.fullmatch(r'^\S+@\S+\.\S+', x)
    
    if result:
        break