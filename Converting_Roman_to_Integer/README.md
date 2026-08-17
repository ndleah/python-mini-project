<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Roman to Integer & Integer to Roman Converter

A versatile, user-friendly Python CLI tool and importable module that accurately converts standard Roman numerals (1 to 3999) to integers and vice versa. It includes rigorous input validation, error handling, interactive console mode, command-line arguments support, and comprehensive unit tests.

## 🛠️ Description

This script provides bidirectional conversion between Roman numerals and Arabic integers:
1. **Roman to Integer Conversion**: Converts Roman numeral strings (e.g., `MCMXCIV` $\rightarrow$ `1994`, `XIV` $\rightarrow$ `14`).
2. **Integer to Roman Conversion**: Converts integers (1 to 3999) to standard Roman numerals (e.g., `2024` $\rightarrow$ `MMXXIV`).
3. **Syntax & Character Validation**: Validates standard Roman numeral grammar using regular expressions to prevent illegal combinations like `IIII` or `VV`.
4. **Input Sanitization**: Handles case-insensitive input (`xiv`, `MCMXCIV`) and trims extraneous whitespaces.
5. **Interactive & CLI Support**: Run with arguments for instant answers or launch without arguments for an interactive loop.

## ⚙️ Languages or Frameworks Used

- **Language:** Python 3 (standard library only)
- **Built-in Modules:** `re`, `sys`, `unittest`, `typing`

## 🌟 How to run

### 1. Interactive Mode
Run the script without arguments to start the interactive prompt:
```bash
python Converting_Roman_to_Integer.py
```
**Example Session:**
```text
==================================================
  Welcome to the Roman Numeral Converter!
  Enter a Roman numeral or integer (or 'q' to quit)
==================================================

Enter input: XIV
 Roman Numeral: XIV  -->  Integer: 14

Enter input: 1994
 Integer: 1994  -->  Roman Numeral: MCMXCIV

Enter input: q
Goodbye!
```

### 2. Command Line Arguments
Pass a Roman numeral or integer directly via CLI:
```bash
# Convert Roman numeral to integer
python Converting_Roman_to_Integer.py MCMXCIV
# Output: 1994

# Convert integer to Roman numeral
python Converting_Roman_to_Integer.py 2024
# Output: MMXXIV

# View help and usage
python Converting_Roman_to_Integer.py --help
```

### 3. Running Unit Tests
Run the unit test suite to verify conversions and edge cases:
```bash
python -m unittest test_roman_to_integer.py
```

## 📺 Demo

```text
$ python Converting_Roman_to_Integer.py MCMXCIV
1994

$ python Converting_Roman_to_Integer.py 58
LVIII

$ python Converting_Roman_to_Integer.py IIII
Error: 'IIII' is not a valid standard Roman numeral.
```

## 🤖 Author

- Open Source Contribution
- Repository: [python-mini-project](https://github.com/ndleah/python-mini-project)
