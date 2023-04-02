import sys


romanStr = sys.argv[1]
romanStr = str(romanStr)
dict = {
    'I':1,
    'V':5,
    'X':10,
    'L':50,
    'C':100,
    'D':500,
    'M':1000
}

num = 0

romanStr = romanStr.replace("IV","IIII")
romanStr = romanStr.replace("IX","VIIII")
romanStr = romanStr.replace("XL","XXXX")
romanStr = romanStr.replace("XC","LXXXX")
romanStr = romanStr.replace("CD","CCCC")
romanStr = romanStr.replace("CM","DCCCC")
myStr = list(romanStr)
for char in myStr:
    num = num + dict[char]

print(num)