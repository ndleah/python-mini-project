import random
#CATEGORIZING OUTCOME INTO A LIST

one =   """ 
            ("===========")
            ("|         |")
            ("|    O    |")
            ("|         |")
            ("===========")\n  
        
        """

two =   """ 
            ("===========")
            ("|         |")
            ("| O     O |")
            ("|         |")
            ("===========")\n  
        
        """



three =   """ 
            ("===========")
            ("|    O    |")
            ("|    O    |")
            ("|    O    |")
            ("===========")\n  
        
        """

four =   """ 
            ("===========")
            ("|  O    O |")
            ("|     0   |")
            ("|  O    O |")
            ("===========")\n  
        
        """

five =   """ 
            ("===========")
            ("| O     O |")
            ("|    0    |")
            ("| O     O |")
            ("===========")\n  
        
        """

six =  """
            ("===========") 
            ("| O     O |")
            ("| O     O |")
            ("| O     O |")
            ("===========") \n      
        """



outcomes_list = [one, two, three, four, five, six]


print("This is a dice stimulator")
x = "y"
while x == "y":
    randon_outcome = random.sample(outcomes_list, 2)
    for outcome in randon_outcome:
        print(outcome)
    
    x =  input("Press y to roll again ")