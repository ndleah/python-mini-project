"""
Roman to Integer (and Integer to Roman) Converter
=================================================
A robust, flexible utility to convert Roman numerals to integers
and vice versa, supporting both CLI arguments and interactive mode.
"""

import re
import sys
from typing import Dict

# Mapping of Roman numeral symbols to integer values
ROMAN_VALUES: Dict[str, int] = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000,
}

# Value-to-symbol pairs for Integer to Roman conversion
INTEGER_TO_ROMAN_MAP = [
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I'),
]

# Standard Roman Numeral Regex Pattern (1 to 3999)
ROMAN_REGEX = re.compile(r'^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')


def is_valid_roman(roman_str: str) -> bool:
    """
    Validate if a given string is a syntactically valid standard Roman numeral (1 - 3999).
    """
    if not roman_str or not isinstance(roman_str, str):
        return False
    return bool(ROMAN_REGEX.fullmatch(roman_str.strip().upper()))


def roman_to_int(roman_str: str, validate: bool = True) -> int:
    """
    Convert a Roman numeral string to an integer.

    Parameters:
        roman_str (str): The Roman numeral string (case-insensitive).
        validate (bool): Whether to strictly validate standard Roman numeral syntax.

    Returns:
        int: The integer value of the Roman numeral.

    Raises:
        ValueError: If input is empty, contains invalid characters, or fails validation.
    """
    if not isinstance(roman_str, str):
        raise TypeError("Input must be a string.")

    cleaned_str = roman_str.strip().upper()

    if not cleaned_str:
        raise ValueError("Input string cannot be empty.")

    # Check for invalid characters
    invalid_chars = [c for c in cleaned_str if c not in ROMAN_VALUES]
    if invalid_chars:
        raise ValueError(
            f"Invalid Roman character(s) found: {', '.join(set(invalid_chars))}. "
            f"Valid characters are {', '.join(ROMAN_VALUES.keys())}."
        )

    # Validate standard syntax if requested
    if validate and not is_valid_roman(cleaned_str):
        raise ValueError(f"'{roman_str.strip()}' is not a valid standard Roman numeral.")

    total = 0
    prev_value = 0

    # Parse right-to-left
    for char in reversed(cleaned_str):
        current_value = ROMAN_VALUES[char]
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        prev_value = current_value

    return total


def int_to_roman(number: int) -> str:
    """
    Convert an integer (1 - 3999) to its standard Roman numeral representation.

    Parameters:
        number (int): Integer to convert (between 1 and 3999).

    Returns:
        str: The corresponding Roman numeral.

    Raises:
        ValueError: If number is not within the range 1 to 3999.
    """
    if not isinstance(number, int):
        raise TypeError("Input must be an integer.")

    if not (1 <= number <= 3999):
        raise ValueError("Number must be between 1 and 3999.")

    roman_digits = []
    for value, symbol in INTEGER_TO_ROMAN_MAP:
        if number == 0:
            break
        count, number = divmod(number, value)
        roman_digits.append(symbol * count)

    return "".join(roman_digits)


def print_help() -> None:
    """Print command-line usage information."""
    print("Roman to Integer & Integer to Roman Converter")
    print("---------------------------------------------")
    print("Usage:")
    print("  python Converting_Roman_to_Integer.py <ROMAN_NUMERAL>")
    print("  python Converting_Roman_to_Integer.py <INTEGER>")
    print("  python Converting_Roman_to_Integer.py --help")
    print("\nExamples:")
    print("  python Converting_Roman_to_Integer.py XIV       -> 14")
    print("  python Converting_Roman_to_Integer.py MCMXCIV   -> 1994")
    print("  python Converting_Roman_to_Integer.py 2024      -> MMXXIV")
    print("\nIf no argument is passed, interactive mode will start.")


def interactive_mode() -> None:
    """Run an interactive console loop for conversions."""
    print("=" * 50)
    print("  Welcome to the Roman Numeral Converter!")
    print("  Enter a Roman numeral or integer (or 'q' to quit)")
    print("=" * 50)

    while True:
        try:
            user_input = input("\nEnter input: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ('q', 'quit', 'exit'):
                print("Goodbye!")
                break

            # If input is digits, convert integer -> Roman
            if user_input.isdigit():
                val = int(user_input)
                result = int_to_roman(val)
                print(f" Integer: {val}  -->  Roman Numeral: {result}")
            else:
                # Convert Roman -> Integer
                result = roman_to_int(user_input)
                print(f" Roman Numeral: {user_input.upper()}  -->  Integer: {result}")

        except ValueError as err:
            print(f" Error: {err}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


def main() -> None:
    """Main CLI entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip()

        if arg in ('-h', '--help', 'help'):
            print_help()
            sys.exit(0)

        # Check if argument is integer or Roman numeral
        try:
            if arg.isdigit():
                val = int(arg)
                print(int_to_roman(val))
            else:
                print(roman_to_int(arg))
        except ValueError as err:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)
    else:
        interactive_mode()


if __name__ == '__main__':
    main()