#TOWER OF HANOI

# GAME GRID:
#  3  |  |
#  2  |  |
#  1  |  |
#    a  b  c

#a1,a2,a3,b1,b2,b3,c1,c2,c3

charon = 999
a1 = 3
a2 = 2
a3 = 1
b1 = " "
b2 = " "
b3 = " "
c1 = " "
c2 = " "
c3 = " "

def main():

    print("")
    print(f"{a3} | {b3} | {c3}")
    print(f"{a2} | {b2} | {c2}")
    print(f"{a1} | {b1} | {c1}")
    print("")

    hanoi()

print("")    
print("Choose a column (1, 2, or 3) to pull the top number, then choose a column to move that number to. Numbers must always be less than the number beneath them.")
print("Goal: move the full stack to another column.")

def hanoi():
    global a1
    global a2
    global a3
    global b1
    global b2
    global b3
    global c1
    global c2
    global c3
    global charon

    col = input("Column? ")
    if col.isdigit():


        if int(col) == 1:
            if a3 == " ":
                if a2 == " ":
                    if a1 == " ":
                        print("empty.")
                        hanoi()
                    else:
                        charon = a1
                        a1 = " "
                else:
                    charon = a2
                    a2 = " "
            else:
                charon = a3
                a3 = " "

            move = int(input("Move to? "))

            if move == 1:
                if a1 == " ":
                    a1 = charon
                else:
                    if a2 == " ":
                        a2 = charon
                    else:
                        a3 = charon

            elif int(move) == 2:
                if b1 == " ":
                    b1 = charon
                
                elif b1 < charon:
                    #print("broken")
                    if a1 == " ":
                        a1 = charon
                    else:
                        if a2 == " ":
                            a2 = charon
                        else:
                            a3 = charon

                else:
                    if b2 == " ":
                        b2 = charon

                    elif b2 < charon:
                        #double broke
                        if a1 == " ":
                            a1 = charon
                        else:
                            if a2 == " ":
                                a2 = charon
                            else:
                                a3 = charon    

                    else:
                        b3 = charon


            elif int(move) == 3:
                if c1 == " ":
                    c1 = charon

                elif c1 < charon:
                    #broke
                    if a1 == " ":
                        a1 = charon
                    else:
                        if a2 == " ":
                            a2 = charon
                        else:
                            a3 = charon                

                else:
                    if c2 == " ":
                        c2 = charon

                    elif c2 < charon:
                        #double broke
                        if a1 == " ":
                            a1 = charon
                        else:
                            if a2 == " ":
                                a2 = charon
                            else:
                                a3 = charon    

                    else:
                        c3 = charon
            
            else:
                print("stew")

#######################################################

        elif int(col) == 2:
            if b3 == " ":
                if b2 == " ":
                    if b1 == " ":
                        print("empty.")
                        hanoi()
                    else:
                        charon = b1
                        b1 = " "
                else:
                    charon = b2
                    b2 = " "
            else:
                charon = b3
                b3 = " "

            move = int(input("Move to? "))
            if move == 2:
                if b1 == " ":
                    b1 = charon            
                else:
                    if b2 == " ":
                        b2 = charon
                    else:
                        b3 = charon

            elif int(move) == 1:
                if a1 == " ":
                    a1 = charon

                elif a1 < charon:
                    #broke
                    if b1 == " ":
                        b1 = charon
                    else:
                        if b2 == " ":
                            b2 = charon
                        else:
                            b3 = charon    

                else:
                    if a2 == " ":
                        a2 = charon

                    elif a2 < charon:
                        #double broke
                        if b1 == " ":
                            b1 = charon
                        else:
                            if b2 == " ":
                                b2 = charon
                            else:
                                b3 = charon    

                    else:
                        a3 = charon


            elif int(move) == 3:
                if c1 == " ":
                    c1 = charon
                elif c1 < charon:
                    #broke
                    if b1 == " ":
                        b1 = charon
                    else:
                        if b2 == " ":
                            b2 = charon
                        else:
                            b3 = charon    
                
                else:
                    if c2 == " ":
                        c2 = charon

                    elif c2 < charon:
                        #double broke
                        if b1 == " ":
                            b1 = charon
                        else:
                            if b2 == " ":
                                b2 = charon
                            else:
                                b3 = charon    
                    else:
                        c3 = charon
            
            else:
                print("stew")

#######################################################

        elif int(col) == 3:
            if c3 == " ":
                if c2 == " ":
                    if c1 == " ":
                        print("empty.")
                        hanoi()
                    else:
                        charon = c1
                        c1 = " "
                else:
                    charon = c2
                    c2 = " "
            else:
                charon = c3
                c3 = " "

            move = int(input("Move to? "))
            if move == 3:
                if c1 == " ":
                    c1 = charon
                else:
                    if c2 == " ":
                        c2 = charon
                    else:
                        c3 = charon

            elif int(move) == 1:
                if a1 == " ":
                    a1 = charon

                elif a1 < charon:
                    #broke
                    if c1 == " ":
                        c1 = charon
                    else:
                        if c2 == " ":
                            c2 = charon
                        else:
                            c3 = charon    

                else:
                    if a2 == " ":
                        a2 = charon

                    elif a2 < charon:
                        #double broke
                        if c1 == " ":
                            c1 = charon
                        else:
                            if c2 == " ":
                                c2 = charon
                            else:
                                c3 = charon    

                    else:
                        a3 = charon


            elif int(move) == 2:
                if b1 == " ":
                    b1 = charon

                elif b1 < charon:
                    #broke
                    if c1 == " ":
                        c1 = charon
                    else:
                        if c2 == " ":
                            c2 = charon
                        else:
                            c3 = charon    

                else:
                    if b2 == " ":
                        b2 = charon

                    elif b2 < charon:
                        #double broke
                        if c1 == " ":
                            c1 = charon
                        else:
                            if c2 == " ":
                                c2 = charon
                            else:
                                c3 = charon    

                    else:
                        b3 = charon
            
            else:
                print("stew")
    else:
        print("1 2 or 3")
        hanoi()

#######################################################

    print("")
    print(f"{a3} | {b3} | {c3}")
    print(f"{a2} | {b2} | {c2}")
    print(f"{a1} | {b1} | {c1}")
    print("")


    #WINNING MESSAGE
    if b3 == 1:
        print("CONGRADULATIONS!")
        print("")


    if c3 == 1:
        print("CONGRADULATIONS!")
        print("")




    hanoi()

def test():

    global a1
    global a2
    global a3
    global b1
    global b2
    global b3
    global c1
    global c2
    global c3

    print(f"{a3}")
    a3 = c3
    print(f"{a3}")


main()