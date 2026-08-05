import sys

if len(sys.argv) > 1:
    romanStr = sys.argv[1]
else:
    romanStr = input("Enter a Roman numeral: ")

romanStr = str(romanStr).strip().upper()

if not romanStr:
    print("Error: No Roman numeral provided.")
    sys.exit(1)

ROMAN_VALUES = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

invalid_chars = [char for char in romanStr if char not in ROMAN_VALUES]
if invalid_chars:
    print(f"Error: Invalid Roman numeral character(s) '{''.join(set(invalid_chars))}'.")
    sys.exit(1)

num = 0

romanStr = romanStr.replace("IV", "IIII")
romanStr = romanStr.replace("IX", "VIIII")
romanStr = romanStr.replace("XL", "XXXX")
romanStr = romanStr.replace("XC", "LXXXX")
romanStr = romanStr.replace("CD", "CCCC")
romanStr = romanStr.replace("CM", "DCCCC")

for char in romanStr:
    num += ROMAN_VALUES[char]

print(num)