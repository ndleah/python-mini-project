<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Extraction of Phone Number and Email Address

A fast, reliable Python utility to extract, normalize, and export phone numbers and email addresses. It supports extracting from the system clipboard, text files, CLI arguments, and piping, with full support for international phone numbers, extensions, modern long TLDs, subdomains, plus-addressing, deduplication, and JSON export.

---

## 🛠️ Description

Whenever you copy long articles, contacts, logs, or web pages, finding and formatting contact details manually is tedious and error-prone. This script automates that workflow:

- **Phone Number Parsing**: Accurately extracts 10-digit North American numbers (`415-863-9900`, `(415) 863-9900`), international formats (`(+1) 541-754-3017`, `+44 20 7946 0958`, `+91 98765 43210`, `(001) 800-420-7240`), and extensions (`ext. 1234`, `x567`).
- **Email Parsing**: Matches standard emails, modern and long TLDs (`.info`, `.cloud`, `.online`, `.tech`, `.digital`), multi-level subdomains (`user@mail.corp.google.com`), and plus-addressing (`user+tag@gmail.com`).
- **Safe & Decoupled Architecture**: Modular pure functions (`extract_phone_numbers()`, `extract_emails()`, `extract_all()`) with safe clipboard fallbacks, making it ready for automation, CI/CD pipelines, and script imports.
- **Multiple Input Sources**: Accepts text from system clipboard, text files (`--file`), or direct CLI string (`--text`).
- **Export & Output Modes**: Formatted terminal output, deduplicated output (`--unique`), file export (`--output`), copy results back to clipboard (`--copy`), or structured JSON (`--json`).

---

## ⚙️ Languages or Frameworks Used

- **Python 3.8+**
- **Standard Library**: `re`, `argparse`, `json`, `sys`, `os`, `unittest`
- **External Dependency**: `pyperclip>=1.8.0` (for clipboard access)

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## 🌟 How to run

### 1. Clipboard Mode (Default)
1. Copy any text containing phone numbers or email addresses (`Ctrl + C` or `Cmd + C`).
2. Run the script:
   ```bash
   python PhoneEmailExtraction.py
   ```
3. The matches will be extracted and displayed directly in your terminal.

### 2. File Mode
Extract contacts directly from a text file (such as the bundled `Input-Data.txt`):
```bash
python PhoneEmailExtraction.py --file Input-Data.txt
```

### 3. Direct String Argument Mode
```bash
python PhoneEmailExtraction.py --text "Contact support at +1-800-555-0199 or email help@startup.cloud"
```

### 4. Advanced CLI Options

| Option | Shorthand | Description |
|---|---|---|
| `--file PATH` | `-f` | Extract from a specified text file |
| `--text "STRING"` | `-t` | Extract directly from a text string |
| `--clipboard` | `-c` | Extract from system clipboard (default) |
| `--output PATH` | `-o` | Save extracted matches to a text or JSON file |
| `--copy` | | Copy extracted matches back to the system clipboard |
| `--unique` | `-u` | Remove duplicate matches while preserving original order |
| `--phone-only` | | Extract only phone numbers |
| `--email-only` | | Extract only email addresses |
| `--json` | | Output results in JSON format |
| `--raw` | | Output raw phone matches without standard normalization |

#### Example: Export Unique Matches to JSON
```bash
python PhoneEmailExtraction.py --file Input-Data.txt --unique --json
```

#### Example: Extract to File & Copy to Clipboard
```bash
python PhoneEmailExtraction.py --file Input-Data.txt -o extracted.txt --copy
```

---

## 🧪 Running the Tests

A comprehensive unit test suite is included to verify phone regex patterns, email edge cases, deduplication, and file extractions:

```bash
python test_PhoneEmailExtraction.py
```
Or using Python's test runner:
```bash
python -m unittest discover -s .
```

All 15 tests should pass with `OK`.

---

## 📺 Demo

Running against `Input-Data.txt`:

```text
$ python PhoneEmailExtraction.py --file Input-Data.txt

=== Extracted from file 'Input-Data.txt' (Total: 9) ===

[ Phone Numbers (5) ]
  - (+1) 541-754-3017
  - +19-541-754-3017
  - (001) 800-420-7240
  - 415-863-9900
  - 415-863-9950

[ Email Addresses (4) ]
  - info@nostarch.co.in
  - media@gmail.com
  - academic@nostarch.com
  - help@yahoo.com
```

JSON Output:
```json
$ python PhoneEmailExtraction.py --file Input-Data.txt --json
{
  "phone_numbers": [
    "(+1) 541-754-3017",
    "+19-541-754-3017",
    "(001) 800-420-7240",
    "415-863-9900",
    "415-863-9950"
  ],
  "emails": [
    "info@nostarch.co.in",
    "media@gmail.com",
    "academic@nostarch.com",
    "help@yahoo.com"
  ],
  "total_matches": 9
}
```

---

## 🤖 Author

- [ndleah](https://github.com/ndleah) (Original Project Repository)
- Enhanced and fixed by open-source contributor
