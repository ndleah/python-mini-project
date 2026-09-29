# Description

### Bug Summary & Feature Limitations
In `ExtractPhoneNumberEmail/PhoneEmailExtraction.py`, several critical regex bugs, architecture flaws, and feature limitations prevent the script from functioning reliably:

1. **Critical Regex Failure on Standard 10-Digit Phone Numbers & Cross-Line Data Corruption**:
   - In `PhoneNumCheck()`, the regex pattern requires 4 consecutive digit groups:
     ```python
     (\(?(\+?\d{1,3})\)?[\s_.-]?) (\d{3}) [\s_.-]? (\d{3}) [\s_.-]? (\d{4,5})
     ```
   - The first group `(\(?(\+?\d{1,3})\)?[\s_.-]?)` is **not optional**. Consequently, standard 10-digit North American phone numbers (e.g. `415-863-9900` or `(541) 754-3017`) and 7-digit local numbers completely fail to match.
   - Even worse, in multiline text (such as the provided `Input-Data.txt`), when a standard 10-digit number like `415-863-9900` is followed by another number on the next line `415 863 9950`, the regex skips the initial digits, greedily grabs the trailing `900\n` as an area code, and combines it with the next line to produce a corrupted phantom number: `(900)415-863-9950`, while completely dropping `415-863-9900`.

2. **Email Regex Truncation on Modern TLDs, Subdomains, and Plus Addressing**:
   - In `EmailCheck()`, the top-level domain (TLD) is hardcoded to `{2,3}`:
     ```python
     [a-zA-Z]{2,3}(\.[a-zA-Z]{2,3})?
     ```
   - Modern and common domains with >3 letters (e.g. `.info`, `.online`, `.cloud`, `.digital`, `.tech`, `.email`, `.store`, `.museum`) are truncated (e.g., `user@example.info` matches `user@example.inf`, chopping off the `o`).
   - Emails with multi-level subdomains (e.g., `user@mail.corp.google.com` or `dev@cs.stanford.edu`) are truncated to `user@mail.cor`.
   - Plus-addressed emails (`user+newsletter@gmail.com`) are split, dropping the user prefix and returning only `newsletter@gmail.com`.

3. **Global State Mutation and Fragile Top-Level Clipboard Execution**:
   - The script unconditionally executes `text = str(pyperclip.paste())` at the module top level upon import.
   - If imported in headless environments (e.g. CI/CD test runners, Docker containers, remote servers, or Linux systems without `xclip`/`xsel`), `pyperclip` raises a fatal `PyperclipException`.
   - The extraction functions `PhoneNumCheck()`, `EmailCheck()`, and `PrintMatches()` accept no arguments and return no values, relying entirely on mutating the global `matches` list and reading the global `text` variable, making the code untestable and impossible to reuse as a module.

4. **Lack of CLI Options, File Input, Stdin Piping, and Output Saving**:
   - Users cannot pass an input file (such as `Input-Data.txt`), pass text directly via CLI flag (`--text`), or pipe input via stdin (`cat data.txt | python PhoneEmailExtraction.py`).
   - There are no options to save results to a file (`-o` / `--output`), copy results back to the clipboard (`--copy`), extract only phone numbers (`--phone-only`), extract only emails (`--email-only`), or export structured JSON (`--json`).

5. **Inaccurate Documentation and Naming Inconsistencies**:
   - `README.md` references nonexistent files `PhoneEmailExtractor.py` and `extractor.py` instead of the actual file `PhoneEmailExtraction.py`.
   - Contains grammatical errors and incomplete instructions.

6. **Missing Automated Unit Tests and Dependency Specification**:
   - The project lacks automated unit tests to verify regex accuracy and prevent regressions.
   - Missing `requirements.txt` specifying `pyperclip`.

---

## Type of issue

- [x] Bug
- [x] Feature (Enhancement)
- [x] Documentation

---

## Checklist:

- [x] I have read the project guidelines.
- [x] I have checked previous issues to avoid duplicates.
- [x] This issue will be meaningful for the project.
- [x] I have added steps to reproduce the bug
- [x] I have proposed a possible solution for the bug

---

## Steps to Reproduce the Bug:

1. **Test Extraction on `Input-Data.txt`**:
   Execute the regex on the provided sample input:
   ```python
   import re

   regex = re.compile(r'''
       (\(?(\+?\d{1,3})\)?
       [\s_.-]?)
       (\d{3})
       [\s_.-]?
       (\d{3})
       [\s_.-]?
       (\d{4,5})
   ''', re.VERBOSE)

   with open('ExtractPhoneNumberEmail/Input-Data.txt') as f:
       text = f.read()

   print(regex.findall(text))
   ```
   **Observed Output**:
   ```python
   [('(+1)', '+1', '541', '754', '3017'), ('+19-', '+19', '541', '754', '3017'), ('(001) ', '001', '800', '420', '7240'), ('900\n', '900', '415', '863', '9950')]
   ```
   Notice that `415-863-9900` was completely missed, and instead `900\n415 863 9950` was corrupted into `(900)415-863-9950`.

2. **Test Modern Email TLDs & Plus-Addressing**:
   ```python
   import re

   email_regex = re.compile(r'''
       ([a-zA-Z0-9._%-]+
       @
       [a-zA-Z0-9_-]+
       \.
       [a-zA-Z]{2,3}
       (\.[a-zA-Z]{2,3})?)
   ''', re.VERBOSE)

   print(email_regex.findall("contact@company.info"))
   print(email_regex.findall("user+tag@gmail.com"))
   ```
   **Observed Output**:
   ```python
   [('contact@company.inf', '')]          # Truncated .info to .inf
   [('newsletter@gmail.com', '')]         # User prefix lost due to '+'
   ```

3. **Test Module Import in Headless / Non-GUI Environment**:
   ```bash
   python -c "import PhoneEmailExtraction"
   ```
   In environments without clipboard access (headless Linux/CI), this crashes immediately on import.

---

## Proposed Solution:

1. **Robust Phone Number Regex & Normalizer**:
   - Rewrite the phone regex with boundary assertions (`(?<!\w)`, `(?!\d)`) and support for:
     - Optional international country codes (`+1`, `(+1)`, `001`, `+91`, `+44`).
     - Standard 10-digit North American numbers (`415-863-9900`, `(415) 863-9900`, `415 863 9950`, `415.863.9900`).
     - Formats with extensions (`ext. 123`, `x456`).
     - Formats with 5+5 digits or 7-digit local numbers.
   - Add a `normalize_phone_number()` helper to standardize extracted phone numbers cleanly into readable formats.

2. **Comprehensive RFC-compliant Email Regex**:
   - Update the email regex to support:
     - Full usernames including `+` (e.g. `user+tag@example.com`).
     - Multi-level subdomains (e.g. `user@mail.corp.google.com`, `user@cs.stanford.edu`).
     - TLDs of any valid length (e.g. `.info`, `.cloud`, `.online`, `.education`).

3. **Decoupled Architecture & Safe Clipboard Handling**:
   - Remove top-level clipboard execution. Wrap clipboard access in defensive helper functions (`get_clipboard_text()`, `copy_to_clipboard()`) with graceful fallbacks.
   - Provide clean, pure functions:
     - `extract_phone_numbers(text: str, formatted: bool = True) -> list[str]`
     - `extract_emails(text: str) -> list[str]`
     - `extract_all(text: str, deduplicate: bool = False, formatted: bool = True) -> dict[str, list[str]]`
   - Preserve 100% backward compatibility for legacy functions (`PhoneNumCheck()`, `EmailCheck()`, `PrintMatches()`, and `matches` list).

4. **Full Command-Line Interface (`argparse`)**:
   - Support `--file` / `-f` to read directly from a file (e.g. `Input-Data.txt`).
   - Support `--text` / `-t` to extract directly from a string argument.
   - Support `--output` / `-o` to save extracted results to a file.
   - Support `--copy` to copy results back to clipboard.
   - Support `--phone-only` and `--email-only` filters.
   - Support `--unique` / `-u` for deduplication preserving order.
   - Support `--json` for automated scripting and data pipelines.
   - Support `--raw` for unformatted matched strings.

5. **Complete Test Suite & Documentation**:
   - Create `test_PhoneEmailExtraction.py` using standard `unittest` testing all phone patterns, email edge cases, file extraction, deduplication, and legacy compatibility.
   - Add `requirements.txt` with `pyperclip>=1.8.0`.
   - Update `README.md` to follow the project template with accurate instructions and examples.
