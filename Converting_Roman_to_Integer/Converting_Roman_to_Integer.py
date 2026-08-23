import sys
import re

ROMAN_VALUES = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

INT_TO_ROMAN_MAP = [
    (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
    (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
    (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
]

def validate_roman_sequence(roman_str: str) -> bool:
    """Validate Roman numeral sequence formatting rules."""
    if re.search(r'(V{2,}|L{2,}|D{2,})', roman_str):
        return False
    if re.search(r'(I{4,}|X{4,}|C{4,}|M{4,})', roman_str):
        return False
    return True

def roman_to_int(roman_str: str) -> int:
    roman_str = roman_str.strip().upper()
    if not roman_str:
        raise ValueError("No Roman numeral provided.")

    invalid_chars = [char for char in roman_str if char not in ROMAN_VALUES]
    if invalid_chars:
        raise ValueError(f"Invalid Roman numeral character(s): '{''.join(set(invalid_chars))}'.")

    if not validate_roman_sequence(roman_str):
        raise ValueError(f"Invalid Roman numeral sequence: '{roman_str}'.")

    temp_str = roman_str
    temp_str = temp_str.replace("IV", "IIII")
    temp_str = temp_str.replace("IX", "VIIII")
    temp_str = temp_str.replace("XL", "XXXX")
    temp_str = temp_str.replace("XC", "LXXXX")
    temp_str = temp_str.replace("CD", "CCCC")
    temp_str = temp_str.replace("CM", "DCCCC")

    num = sum(ROMAN_VALUES[char] for char in temp_str)
    return num

def int_to_roman(num: int) -> str:
    if not (1 <= num <= 3999):
        raise ValueError("Integer out of range (must be 1 to 3999).")

    result = []
    for value, symbol in INT_TO_ROMAN_MAP:
        while num >= value:
            result.append(symbol)
            num -= value
    return "".join(result)

def main():
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Enter a Roman numeral or Integer: ")

    user_input = str(user_input).strip()

    if not user_input:
        print("Error: No input provided.")
        sys.exit(1)

    try:
        if user_input.isdigit():
            val = int(user_input)
            roman_res = int_to_roman(val)
            print(f"Integer: {val} -> Roman: {roman_res}")
        else:
            int_res = roman_to_int(user_input)
            print(f"Roman: {user_input.upper()} -> Integer: {int_res}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
