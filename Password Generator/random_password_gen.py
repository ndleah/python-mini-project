#!/usr/bin/env python
# coding: utf-8

# In[2]:



import random
import math

#All characters 
alpha =  "abcdefghijklmnopqrstuvwxyz"
#All Numbers
num = "0123456789"
#All special Characters
special = "@#$%&*"

#Taking input of length of password 
pass_len = int(input("Enter Password Length: "))

#Length of Characers in password should be half
alpha_len = pass_len//2
#length of numbers in password should be 30%
num_len = math.ceil(pass_len*30/100)
#Rest 20% of password will be of special characters
special_len = pass_len-(alpha_len+num_len)

#Empty Password Array
password = []


def generate_pass(length,array, is_alpha = False):
    for i in range(length):
        #randint generates random number
        index = random.randint(0, len(array) - 1)
        character = array[index]
        #is_alpha true means they want character in uppercase
        if is_alpha:
            case = random.randint(0,1)
            if case == 1:
                character = character.upper()
        password.append(character)
        
#Calling generation function for characters, numbers and special characters        
generate_pass(alpha_len,alpha,True)
generate_pass(num_len, num)
generate_pass(special_len, special)

#Used for Shuffling 
random.shuffle(password)

#Here Converting Password into string
gen_password = ""
for i in password:
    gen_password = gen_password + str(i)
print(gen_password)

#OUTPUT
"""
Enter Password Length: 10
5I$W1Id5&M

Enter Password Length: 5
T$16q
"""




