# Roman & Integer Converter

A Python script to convert Roman numerals to integers and integers to Roman numerals.

## Features
- **Bidirectional Conversion**: Convert Roman numerals to integers (e.g. `XIV` -> `14`) and integers to Roman numerals (e.g. `1994` -> `MCMXCIV`).
- **Input Validation**: Validates characters and prevents invalid Roman numeral formatting sequences (e.g. `VV`, `IIII`).
- **Modular Design**: Provides reusable `roman_to_int(s)` and `int_to_roman(n)` functions.

## Usage

### Roman to Integer
```bash
python Converting_Roman_to_Integer/Converting_Roman_to_Integer.py XIV
# Output: Roman: XIV -> Integer: 14
```

### Integer to Roman
```bash
python Converting_Roman_to_Integer/Converting_Roman_to_Integer.py 1994
# Output: Integer: 1994 -> Roman: MCMXCIV
```
