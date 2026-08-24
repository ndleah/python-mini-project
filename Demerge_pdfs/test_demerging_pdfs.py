"""
Unit tests for demerging_pdfs.py
"""

import os
import unittest
import tempfile
import shutil

from demerging_pdfs import (
    check_valid_filename,
    sanitize_filename,
    parse_page_ranges,
    split_by_page_counts,
    split_by_fixed_size,
    split_by_ranges,
    split_burst_all,
    PDFAdapter,
    PDF_LIB
)


class TestDemergePDFs(unittest.TestCase):

    def test_check_valid_filename(self):
        self.assertTrue(check_valid_filename("valid_filename.pdf"))
        self.assertTrue(check_valid_filename("My Document 2026"))
        self.assertFalse(check_valid_filename("invalid:name.pdf"))
        self.assertFalse(check_valid_filename("bad/file.pdf"))
        self.assertFalse(check_valid_filename("file<name>.pdf"))
        self.assertFalse(check_valid_filename("file*name?.pdf"))

    def test_sanitize_filename(self):
        self.assertEqual(sanitize_filename("my_file"), "my_file.pdf")
        self.assertEqual(sanitize_filename("my_file.pdf"), "my_file.pdf")
        self.assertEqual(sanitize_filename("bad:name/test"), "bad_name_test.pdf")
        self.assertEqual(sanitize_filename(""), "output.pdf")
        self.assertEqual(sanitize_filename("   "), "output.pdf")

    def test_parse_page_ranges_valid(self):
        # 1-5, 8, 10-12 in a 20-page document
        ranges = parse_page_ranges("1-5, 8, 10-12", 20)
        self.assertEqual(ranges, [(0, 5), (7, 8), (9, 12)])

        # Single range
        ranges = parse_page_ranges("1-10", 10)
        self.assertEqual(ranges, [(0, 10)])

        # Single page
        ranges = parse_page_ranges("5", 10)
        self.assertEqual(ranges, [(4, 5)])

    def test_parse_page_ranges_errors(self):
        # Empty range
        with self.assertRaises(ValueError):
            parse_page_ranges("", 10)

        # Page exceeding total pages
        with self.assertRaises(ValueError):
            parse_page_ranges("1-15", 10)

        # Page 0 (should be 1-indexed)
        with self.assertRaises(ValueError):
            parse_page_ranges("0-5", 10)

        # Inverted range (start > end)
        with self.assertRaises(ValueError):
            parse_page_ranges("5-2", 10)

        # Non-numeric input
        with self.assertRaises(ValueError):
            parse_page_ranges("abc-def", 10)
        with self.assertRaises(ValueError):
            parse_page_ranges("1-2-3", 10)


class TestDemergePDFsExecution(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_file_not_found_handling(self):
        non_existent = os.path.join(self.test_dir, "non_existent.pdf")
        with self.assertRaises(FileNotFoundError):
            split_by_page_counts(non_existent, [("part1", 5)], output_dir=self.test_dir)
        with self.assertRaises(FileNotFoundError):
            split_by_fixed_size(non_existent, 5, output_dir=self.test_dir)
        with self.assertRaises(FileNotFoundError):
            split_by_ranges(non_existent, "1-5", output_dir=self.test_dir)


if __name__ == '__main__':
    unittest.main()
