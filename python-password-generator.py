#!/usr/bin/env python
# coding: utf-8

# In[1]:


#The random module allows you to generate random numbers within a specified range
import random
#Contains functions which are helpful for operations on string
import string

total = string.ascii_letters + string.digits + string.punctuation

length = int(input("Enter Length of Password:- "))

password = "".join(random.sample(total,length))

print("Password Generated is: ")
print(password)

#OUTPUT
"""
Enter Length of Password:- 3
Password Generated is: 
c|r

Enter Length of Password:- 23
Password Generated is: 
s^jkN|}I*38US!QB;i">~7u
"""