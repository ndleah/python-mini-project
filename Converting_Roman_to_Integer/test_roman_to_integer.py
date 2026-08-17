"""
Unit tests for Converting_Roman_to_Integer module.
"""

import unittest
from Converting_Roman_to_Integer import (
    roman_to_int,
    int_to_roman,
    is_valid_roman,
)


class TestRomanToInteger(unittest.TestCase):
    """Test cases for Roman numeral to integer conversions."""

    def test_single_symbols(self):
        self.assertEqual(roman_to_int('I'), 1)
        self.assertEqual(roman_to_int('V'), 5)
        self.assertEqual(roman_to_int('X'), 10)
        self.assertEqual(roman_to_int('L'), 50)
        self.assertEqual(roman_to_int('C'), 100)
        self.assertEqual(roman_to_int('D'), 500)
        self.assertEqual(roman_to_int('M'), 1000)

    def test_additive_combinations(self):
        self.assertEqual(roman_to_int('III'), 3)
        self.assertEqual(roman_to_int('VI'), 6)
        self.assertEqual(roman_to_int('XV'), 15)
        self.assertEqual(roman_to_int('LVIII'), 58)
        self.assertEqual(roman_to_int('MDCLXVI'), 1666)

    def test_subtractive_combinations(self):
        self.assertEqual(roman_to_int('IV'), 4)
        self.assertEqual(roman_to_int('IX'), 9)
        self.assertEqual(roman_to_int('XL'), 40)
        self.assertEqual(roman_to_int('XC'), 90)
        self.assertEqual(roman_to_int('CD'), 400)
        self.assertEqual(roman_to_int('CM'), 900)
        self.assertEqual(roman_to_int('MCMXCIV'), 1994)

    def test_case_insensitivity_and_whitespace(self):
        self.assertEqual(roman_to_int('iv'), 4)
        self.assertEqual(roman_to_int('  mcmxciv  '), 1994)
        self.assertEqual(roman_to_int('lViIi'), 58)

    def test_invalid_characters(self):
        with self.assertRaises(ValueError):
            roman_to_int('ABC')
        with self.assertRaises(ValueError):
            roman_to_int('123')
        with self.assertRaises(ValueError):
            roman_to_int('XIV12')

    def test_invalid_syntax(self):
        with self.assertRaises(ValueError):
            roman_to_int('IIII')
        with self.assertRaises(ValueError):
            roman_to_int('VV')
        with self.assertRaises(ValueError):
            roman_to_int('IC')
        with self.assertRaises(ValueError):
            roman_to_int('IL')
        with self.assertRaises(ValueError):
            roman_to_int('XD')

    def test_empty_and_non_string_inputs(self):
        with self.assertRaises(ValueError):
            roman_to_int('')
        with self.assertRaises(ValueError):
            roman_to_int('   ')
        with self.assertRaises(TypeError):
            roman_to_int(123)  # type: ignore


class TestIntegerToRoman(unittest.TestCase):
    """Test cases for integer to Roman numeral conversions."""

    def test_valid_integers(self):
        self.assertEqual(int_to_roman(1), 'I')
        self.assertEqual(int_to_roman(4), 'IV')
        self.assertEqual(int_to_roman(9), 'IX')
        self.assertEqual(int_to_roman(58), 'LVIII')
        self.assertEqual(int_to_roman(1994), 'MCMXCIV')
        self.assertEqual(int_to_roman(3999), 'MMMCMXCIX')

    def test_round_trip_conversion(self):
        for num in [1, 4, 9, 14, 44, 99, 400, 944, 1994, 2024, 3999]:
            roman = int_to_roman(num)
            self.assertEqual(roman_to_int(roman), num)

    def test_out_of_range_integers(self):
        with self.assertRaises(ValueError):
            int_to_roman(0)
        with self.assertRaises(ValueError):
            int_to_roman(-5)
        with self.assertRaises(ValueError):
            int_to_roman(4000)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            int_to_roman("123")  # type: ignore


class TestRomanValidation(unittest.TestCase):
    """Test cases for Roman numeral validator."""

    def test_valid_patterns(self):
        self.assertTrue(is_valid_roman('I'))
        self.assertTrue(is_valid_roman('MMMCMXCIX'))
        self.assertTrue(is_valid_roman('MCMXCIV'))
        self.assertTrue(is_valid_roman('CDXLIV'))

    def test_invalid_patterns(self):
        self.assertFalse(is_valid_roman(''))
        self.assertFalse(is_valid_roman('IIII'))
        self.assertFalse(is_valid_roman('MMMM'))
        self.assertFalse(is_valid_roman('VX'))
        self.assertFalse(is_valid_roman('123'))


if __name__ == '__main__':
    unittest.main()
