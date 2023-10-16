instruction = '''
        firstly we have to take input of capital String/single word without spaces

        game rules:
        1) Both players are given the same string, .
        2) Both players have to make substrings using the letters of the string .
        3) Stuart has to make words starting with consonants.
        4) Kevin has to make words starting with vowels.
        5) The game ends when both players have made all possible substrings.

        A player gets +1 point for each occurrence of the substring in the string .
'''


def check(alpha) :
    vowels = ['a','e','i','o','u']
    for vowel in vowels:
        if alpha == vowel:
            return True
    return False


def minion_game(s):
    p1 = input("enter name of player 1 who is taken strings are starts from consonant: \n")
    p2 = input("enter name of player 2 who is taken strings are starts from vowel: \n")
    s.lower()
    k =len(s)
    v = []
    c = []
    vowel = 0
    const = 0
    for a in range(k):
        if(check(s[a])):
            v.append(a)
            vowel += 1
        else:
            c.append(a)
            const += 1
    # print(c)
    cPossible = []
    vPossible = []
    list = [c,v]
    for i1 in list:
        for value in i1:
            l = value
            i = 1
            for _ in range(k-l):
                temp = ''
                for _ in range(k - (k - i)):
                    # print(s[l], end="")
                    temp = temp + s[l]
                    l += 1
                if i1 == c:
                    cPossible.append(temp)
                else:
                    vPossible.append(temp)
                temp = ''
                l = value  
                i += 1              

    print('overall score is given by:')
    print(f'{p1} : {cPossible}')
    print(f'{p2} : {vPossible}')

    if len(cPossible) > len(vPossible):
        print(f"{p1} wins with score {len(cPossible)}")
    elif len(cPossible) < len(vPossible):
        print(f"{p2} wins with score {len(vPossible)}")
    else:
        print("Draw")

print(instruction)
s = input("enter any String / single Word: \n")
minion_game(s)