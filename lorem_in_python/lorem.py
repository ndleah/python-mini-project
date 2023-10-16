# lorem function in python (lol)


import random

alpha = " abcd efgh ijkl mnop qrst uvwx yz"

l = int(input("enter the number rows in ur paragraph:\n"))

with open("lorem_in_python/text.txt","w") as f:
    for i in range(l):
        for j in range(70):
            p = random.randint(0,26)
            f.write(alpha[p])
        f.write("\n")

print("everything is done check the text file\n")