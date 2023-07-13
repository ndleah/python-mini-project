from converter_values import *          #import required files

print(options["help"])              #prints help menu
res = input("Response: ")

while res.lower() != "q":           #program loop
    res = res.strip().split(" ")
    
    try:        
        if len(res) == 1:
            print(options[res[0]])                                   #to display help menu
            
        elif len(res) == 4:
            for i in res[3].split(','):
                value = round( eval( "{} * {}['{}'] / {}['{}']".format(res[2],res[0],i,res[0],res[1]) ) , 6 )     #calculating
                print("{} \t : {}".format(i,value))                               #displaying
                 
        else:
            print("Invalid command")
            
    except:
        print("Invalid command")

    res = input("\nResponse: ")

    

