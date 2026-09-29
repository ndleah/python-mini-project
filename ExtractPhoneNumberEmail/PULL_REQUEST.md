# Description

This Pull Request addresses critical regex bugs, architectural issues, and feature limitations in the `ExtractPhoneNumberEmail` project:

1. **Fix Phone Number Regex & Multi-line Data Corruption**:
   - Resolved the mandatory 4-group constraint that previously prevented standard 10-digit North American phone numbers (e.g. `415-863-9900` or `(541) 754-3017`) and 7-digit local numbers from matching.
   - Fixed the multiline greedy mismatch on `Input-Data.txt` that skipped `415-863-9900` and corrupted the trailing digits into `(900)415-863-9950`.
   - Added support for international numbers (`+1`, `+44`, `+91`, `(001)`), extensions (`ext. 123`, `x456`), and formatting normalization.

2. **Fix Email Address Regex (TLDs, Subdomains, Plus-Addressing)**:
   - Replaced `{2,3}` TLD restriction so modern and multi-character TLDs (`.info`, `.online`, `.cloud`, `.digital`, `.tech`, `.email`, `.store`) are no longer truncated to 3 letters.
   - Added support for multi-level subdomains (`user@mail.corp.google.com`, `user@cs.stanford.edu`).
   - Added support for plus-addressing tags (`user+tag@example.com`).

3. **Decouple Clipboard & Remove Fragile Global State**:
   - Removed unconditional `pyperclip.paste()` execution at module top level, preventing fatal `PyperclipException` in headless CI/CD environments or servers without display/xclip.
   - Refactored extraction into reusable, pure functions: `extract_phone_numbers()`, `extract_emails()`, `extract_all()`, and `normalize_phone_number()`.
   - Preserved 100% backward compatibility for legacy functions (`PhoneNumCheck()`, `EmailCheck()`, `PrintMatches()`) and globals (`matches`, `text`).

4. **Add Comprehensive CLI Support (`argparse`)**:
   - Added `--file` / `-f` to extract directly from text files (e.g., `Input-Data.txt`).
   - Added `--text` / `-t` to extract directly from passed strings.
   - Added `--output` / `-o` to save results to a file.
   - Added `--copy` to copy results back to the clipboard.
   - Added `--unique` / `-u` to deduplicate results while preserving order.
   - Added `--phone-only` and `--email-only` filter flags.
   - Added `--json` for automated pipelines and structured data.
   - Added `--raw` flag to disable phone normalization.

5. **Automated Unit Testing & Dependency Specification**:
   - Added `test_PhoneEmailExtraction.py` with 15 test cases covering all phone formats, email edge cases, `Input-Data.txt` verification, deduplication, and legacy backward compatibility.
   - Added `requirements.txt` specifying `pyperclip>=1.8.0`.

6. **Documentation Overhaul**:
   - Updated `README.md` following the project template: corrected script names (`PhoneEmailExtractor.py` / `extractor.py` -> `PhoneEmailExtraction.py`), added usage instructions, CLI commands, test guide, and demo output.

Fixes #601

- [x] Issue_no: #601 (Bug & Feature(ExtractPhoneNumberEmail): Fix 10-digit phone regex failure, multi-line data corruption, email TLD truncation, add CLI & test suite)
- [ ] Not applicable 

## Type of change

- [x] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [x] Documentation Update

## Project

- #### **Your Project Name:** Extraction of Phone Number and Email Address in Python

- #### **Short Description:** A robust, cross-platform utility to extract, normalize, and export phone numbers and email addresses from clipboard text, files, or CLI arguments with support for international numbers, modern TLDs, and JSON output.

# Checklist:

- [x] I have named my files and folder, according to this project's guidelines.
- [x] My code follows the style guidelines of this project.
- [x] I have commented on my code, particularly in hard-to-understand areas.
- [x] I have created a helpful and easy to understand `README.md`, according to the given [`README_TEMPLATE.`](https://github.com/nduongthucanh/python-mini-project/blob/master/README_TEMPLATE.md)
- [x] My changes do not produce any warnings.
