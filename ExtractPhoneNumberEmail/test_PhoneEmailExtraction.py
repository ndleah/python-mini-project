"""
Unit tests for the Phone and Email Extraction module.
"""

import os
import sys
import unittest

# Ensure current directory is on sys.path for direct imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PhoneEmailExtraction import (
    extract_phone_numbers,
    extract_emails,
    extract_all,
    normalize_phone_number,
    deduplicate_list,
    PhoneNumCheck,
    EmailCheck,
    PrintMatches,
    matches,
)
import PhoneEmailExtraction


class TestPhoneExtraction(unittest.TestCase):
    """Test suite for phone number pattern matching and normalization."""

    def test_standard_10_digit_formats(self):
        """Standard North American 10-digit formats with dashes, spaces, dots, or parens."""
        text = (
            "Reach us at 415-863-9900 or 415 863 9950. "
            "Alternative lines: 541.754.3017 and (541) 754-3017."
        )
        extracted = extract_phone_numbers(text, formatted=True)
        self.assertEqual(len(extracted), 4)
        self.assertIn("415-863-9900", extracted)
        self.assertIn("415-863-9950", extracted)
        self.assertIn("541-754-3017", extracted)
        self.assertIn("(541) 754-3017", extracted)

    def test_international_formats(self):
        """International numbers with + or (00x) prefixes and variable group lengths."""
        text = (
            "Call (+1)541-754-3017 or +19-541-754-3017. "
            "UK office: +44 20 7946 0958, India line: +91 98765 43210."
        )
        extracted = extract_phone_numbers(text, formatted=False)
        self.assertEqual(len(extracted), 4)
        self.assertIn("(+1)541-754-3017", extracted)
        self.assertIn("+19-541-754-3017", extracted)
        self.assertIn("+44 20 7946 0958", extracted)
        self.assertIn("+91 98765 43210", extracted)

    def test_parentheses_code_continuous_digits(self):
        """Numbers with parenthesized country/area code and unseparated digits."""
        text = "Contact line: (001) 8004207240."
        extracted = extract_phone_numbers(text, formatted=True)
        self.assertEqual(len(extracted), 1)
        self.assertEqual(extracted[0], "(001) 800-420-7240")

    def test_phone_extensions(self):
        """Phone numbers with extension indicators (ext, x, ext.)."""
        text = "Dial 415-863-9900 ext. 1234 or (541) 754-3017 x567."
        extracted = extract_phone_numbers(text, formatted=True)
        self.assertEqual(len(extracted), 2)
        self.assertEqual(extracted[0], "415-863-9900 ext. 1234")
        self.assertEqual(extracted[1], "(541) 754-3017 ext. 567")

    def test_phone_negatives(self):
        """Dates, prices, short numbers, and zip codes must not be detected as phones."""
        text = "Today is 2026-09-29. Price: $12.50. Zip code: 90210. ID: 12345."
        extracted = extract_phone_numbers(text)
        self.assertEqual(extracted, [])

    def test_normalize_phone_number_helper(self):
        """Verify normalization outputs for various phone styles."""
        self.assertEqual(normalize_phone_number("  415 863 9900  "), "415-863-9900")
        self.assertEqual(normalize_phone_number("(541) 754-3017"), "(541) 754-3017")
        self.assertEqual(normalize_phone_number("555-4321"), "555-4321")


class TestEmailExtraction(unittest.TestCase):
    """Test suite for email address pattern matching."""

    def test_standard_emails(self):
        """Extract standard common domain emails."""
        text = "Write to info@nostarch.co.in or support@gmail.com and help@yahoo.com."
        extracted = extract_emails(text)
        self.assertEqual(len(extracted), 3)
        self.assertIn("info@nostarch.co.in", extracted)
        self.assertIn("support@gmail.com", extracted)
        self.assertIn("help@yahoo.com", extracted)

    def test_modern_long_tlds(self):
        """Modern top-level domains with >3 characters must not be truncated."""
        text = (
            "Check user@example.info, dev@cloud.digital, "
            "and team@startup.online."
        )
        extracted = extract_emails(text)
        self.assertEqual(len(extracted), 3)
        self.assertIn("user@example.info", extracted)
        self.assertIn("dev@cloud.digital", extracted)
        self.assertIn("team@startup.online", extracted)

    def test_multi_level_subdomains(self):
        """Emails with multiple subdomains."""
        text = "Internal: admin@mail.corp.google.com and lab@cs.stanford.edu."
        extracted = extract_emails(text)
        self.assertEqual(len(extracted), 2)
        self.assertIn("admin@mail.corp.google.com", extracted)
        self.assertIn("lab@cs.stanford.edu", extracted)

    def test_plus_addressing(self):
        """Emails containing + tags must include the full address."""
        text = "Send newsletter to john.doe+updates@example.com."
        extracted = extract_emails(text)
        self.assertEqual(extracted, ["john.doe+updates@example.com"])

    def test_email_negatives(self):
        """Invalid email structures must not match."""
        text = "Not emails: user@, @domain.com, user@.com, user@com, http://example.com, no_at_symbol.org."
        extracted = extract_emails(text)
        self.assertEqual(extracted, [])


class TestExtractAllAndUtilities(unittest.TestCase):
    """Test suite for integrated extraction, deduplication, and file handling."""

    def test_input_data_file_extraction(self):
        """Verify extraction against the bundled Input-Data.txt sample file."""
        data_path = os.path.join(os.path.dirname(__file__), "Input-Data.txt")
        self.assertTrue(os.path.exists(data_path), "Input-Data.txt must exist.")

        with open(data_path, "r", encoding="utf-8") as f:
            content = f.read()

        results = extract_all(content, deduplicate=True, formatted=True)
        phones = results["phone_numbers"]
        emails = results["emails"]

        # Input-Data.txt contains exactly 5 phone numbers and 4 email addresses
        self.assertEqual(len(phones), 5)
        self.assertEqual(len(emails), 4)

        expected_emails = [
            "info@nostarch.co.in",
            "media@gmail.com",
            "academic@nostarch.com",
            "help@yahoo.com",
        ]
        for expected in expected_emails:
            self.assertIn(expected, emails)

    def test_deduplication(self):
        """Ensure deduplication removes identical entries preserving first occurrence."""
        raw_list = ["apple", "banana", "apple", "cherry", "banana"]
        deduped = deduplicate_list(raw_list)
        self.assertEqual(deduped, ["apple", "banana", "cherry"])

        text = "415-863-9900 and 415-863-9900 with info@test.com and info@test.com"
        res = extract_all(text, deduplicate=True)
        self.assertEqual(len(res["phone_numbers"]), 1)
        self.assertEqual(len(res["emails"]), 1)

    def test_empty_input(self):
        """Handling of empty or whitespace-only strings."""
        self.assertEqual(extract_phone_numbers(""), [])
        self.assertEqual(extract_emails(""), [])
        self.assertEqual(extract_all("   "), {"phone_numbers": [], "emails": []})


class TestLegacyCompatibility(unittest.TestCase):
    """Test suite ensuring backward compatibility with legacy global calls."""

    def setUp(self):
        # Reset legacy globals before each test
        PhoneEmailExtraction.matches = []
        PhoneEmailExtraction.text = ""

    def test_legacy_functions(self):
        """PhoneNumCheck and EmailCheck should populate matches list without raising errors."""
        import io
        import contextlib

        PhoneEmailExtraction.text = "Call 415-863-9900 or email test@example.com."
        
        found_phones = PhoneNumCheck()
        self.assertEqual(len(found_phones), 1)
        self.assertIn("415-863-9900", PhoneEmailExtraction.matches)

        found_emails = EmailCheck()
        self.assertEqual(len(found_emails), 1)
        self.assertIn("test@example.com", PhoneEmailExtraction.matches)

        self.assertEqual(len(PhoneEmailExtraction.matches), 2)

        # PrintMatches should run cleanly without throwing
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            PrintMatches()
        output = buf.getvalue()
        self.assertIn("Found matches: 2", output)


if __name__ == "__main__":
    unittest.main()
