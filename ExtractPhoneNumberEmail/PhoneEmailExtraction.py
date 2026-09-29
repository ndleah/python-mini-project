#!/usr/bin/env python3
"""
Phone and Email Extraction Tool.

Extracts phone numbers and email addresses from clipboard text, files,
command-line arguments, or standard input with support for international
formats, normalization, deduplication, JSON output, and file exporting.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Optional

# Regular expression for matching phone numbers
PHONE_REGEX = re.compile(
    r"""
    (?<!\w)
    (?:
        # Country code: +1, (+1), +91, (001), 001
        (?P<country>(?:\+\d{1,3}|\(\+?\d{1,3}\)|(?<!\d)00\d{1,3}|\(00\d{1,3}\)))
        [\s_.-]*
    )?
    (?:
        # Standard separated: (415) 863-9900, 415-863-9900, 415 863 9950, 415.863.9900, +44 20 7946 0958
        (?:(?:\((?P<area1>\d{2,4})\)|(?P<area2>\d{2,4}))[\s_.-]+(?P<exch1>\d{3,4})[\s_.-]+(?P<line1>\d{4}))
        |
        # Continuous or 5+5 format: (001) 8004207240, (+1)541-754-3017, +91 98765 43210, +91-9876543210
        (?:(?:\((?P<area3>\d{2,4})\)|(?P<area4>\d{2,4}))?[\s_.-]*(?P<first5>\d{3,5})[\s_.-]*(?P<second5>\d{4,5}))
    )
    (?:
        \s*(?:ext|x|ext\.)\s*(?P<ext>\d{2,5})
    )?
    (?!\d)
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Regular expression for matching email addresses
EMAIL_REGEX = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

# Global variables maintained for backward compatibility with legacy scripts
matches: List[str] = []
text: str = ""


def get_clipboard_text() -> str:
    """
    Safely retrieve text from the system clipboard.
    
    Returns:
        The clipboard text string, or an empty string if unavailable.
    """
    try:
        import pyperclip
        return pyperclip.paste() or ""
    except ImportError:
        print(
            "Notice: 'pyperclip' is not installed. To enable clipboard support, "
            "run: pip install pyperclip (or use --file / --text instead).",
            file=sys.stderr,
        )
        return ""
    except Exception as exc:
        print(f"Warning: Could not access clipboard: {exc}", file=sys.stderr)
        return ""


def copy_to_clipboard(content: str) -> bool:
    """
    Safely copy text to the system clipboard.
    
    Args:
        content: The text content to copy.
        
    Returns:
        True if copied successfully, False otherwise.
    """
    try:
        import pyperclip
        pyperclip.copy(content)
        return True
    except ImportError:
        print("Notice: 'pyperclip' is not installed. Install with: pip install pyperclip", file=sys.stderr)
        return False
    except Exception as exc:
        print(f"Warning: Could not copy to clipboard: {exc}", file=sys.stderr)
        return False


def deduplicate_list(items: List[str]) -> List[str]:
    """Remove duplicate items while preserving insertion order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def normalize_phone_number(raw_phone: str) -> str:
    """
    Normalize an extracted phone number string into a clean readable format.
    
    Args:
        raw_phone: The raw matched phone string.
        
    Returns:
        A standardized phone string.
    """
    raw_phone = raw_phone.strip()
    if not raw_phone:
        return ""

    # Extract extension if present
    ext_match = re.search(r"(?:ext|x|ext\.)\s*(\d{2,6})", raw_phone, re.IGNORECASE)
    ext_suffix = f" ext. {ext_match.group(1)}" if ext_match else ""
    core = re.sub(r"(?:ext|x|ext\.)\s*\d{2,6}", "", raw_phone, flags=re.IGNORECASE).strip()

    # Preserve country code in parens like (+1) or (001)
    country_paren_match = re.match(r"^\((?:\+?\d{1,4}|00\d{1,4})\)", core)
    prefix = ""
    if country_paren_match:
        prefix = country_paren_match.group(0) + " "
        core = core[len(country_paren_match.group(0)):].strip()
    elif core.startswith("+"):
        plus_match = re.match(r"^\+\d{1,3}[\s.-]?", core)
        if plus_match:
            prefix = plus_match.group(0).rstrip(" -.") + "-"
            core = core[len(plus_match.group(0)):].strip()

    # Preserve (Area) Local format if explicitly parenthesized
    area_paren = re.match(r"^\((\d{2,4})\)\s*(\d{3,4})[\s.-]?(\d{4})", core)
    if area_paren:
        return f"{prefix}({area_paren.group(1)}) {area_paren.group(2)}-{area_paren.group(3)}{ext_suffix}".strip()

    digits = re.sub(r"\D", "", core)
    if len(digits) == 10:
        formatted_core = f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"
        return f"{prefix}{formatted_core}{ext_suffix}".strip()
    elif len(digits) == 7:
        formatted_core = f"{digits[0:3]}-{digits[3:7]}"
        return f"{prefix}{formatted_core}{ext_suffix}".strip()
    else:
        cleaned_core = re.sub(r"\s+", " ", core)
        return f"{prefix}{cleaned_core}{ext_suffix}".strip()


def extract_phone_numbers(
    input_text: str,
    formatted: bool = True,
    deduplicate: bool = False,
) -> List[str]:
    """
    Extract all phone numbers from a text string.
    
    Args:
        input_text: The text to search.
        formatted: If True, normalize phone numbers; otherwise return raw matches.
        deduplicate: If True, remove duplicate occurrences.
        
    Returns:
        List of extracted phone number strings.
    """
    if not input_text:
        return []

    results: List[str] = []
    for match in PHONE_REGEX.finditer(input_text):
        raw = match.group(0).strip()
        if raw:
            results.append(normalize_phone_number(raw) if formatted else raw)

    return deduplicate_list(results) if deduplicate else results


def extract_emails(
    input_text: str,
    deduplicate: bool = False,
) -> List[str]:
    """
    Extract all email addresses from a text string.
    
    Args:
        input_text: The text to search.
        deduplicate: If True, remove duplicate occurrences.
        
    Returns:
        List of extracted email address strings.
    """
    if not input_text:
        return []

    results = [m.group(0).strip() for m in EMAIL_REGEX.finditer(input_text)]
    return deduplicate_list(results) if deduplicate else results


def extract_all(
    input_text: str,
    deduplicate: bool = False,
    formatted: bool = True,
) -> Dict[str, List[str]]:
    """
    Extract both phone numbers and email addresses from a text string.
    
    Args:
        input_text: The text to search.
        deduplicate: If True, remove duplicate occurrences.
        formatted: If True, normalize phone numbers.
        
    Returns:
        A dictionary with 'phone_numbers' and 'emails' lists.
    """
    return {
        "phone_numbers": extract_phone_numbers(input_text, formatted=formatted, deduplicate=deduplicate),
        "emails": extract_emails(input_text, deduplicate=deduplicate),
    }


# ==============================================================================
# Backward Compatibility Wrappers (for legacy imports and function calls)
# ==============================================================================

def PhoneNumCheck() -> List[str]:
    """Legacy function to extract phone numbers into the global 'matches' list."""
    global matches, text
    if not text:
        text = get_clipboard_text()
    found = extract_phone_numbers(text, formatted=True)
    matches.extend(found)
    return found


def EmailCheck() -> List[str]:
    """Legacy function to extract email addresses into the global 'matches' list."""
    global matches, text
    if not text:
        text = get_clipboard_text()
    found = extract_emails(text)
    matches.extend(found)
    return found


def PrintMatches() -> None:
    """Legacy function to print the current global 'matches' list."""
    if len(matches) > 0:
        print(f"Found matches: {len(matches)}")
        for match in matches:
            print(match)
    else:
        print("***No Phone Number or Email Address found.***")


# ==============================================================================
# CLI and Entry Point
# ==============================================================================

def parse_args() -> argparse.Namespace:
    """Configure and parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract phone numbers and email addresses from text, files, or clipboard.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python PhoneEmailExtraction.py --file Input-Data.txt
  python PhoneEmailExtraction.py --text "Call 415-863-9900 or email info@nostarch.com"
  python PhoneEmailExtraction.py --clipboard
  python PhoneEmailExtraction.py --file Input-Data.txt --json
  python PhoneEmailExtraction.py --file Input-Data.txt --output results.txt --copy
        """,
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "-f", "--file",
        type=str,
        help="Path to an input text file to extract from.",
    )
    input_group.add_argument(
        "-t", "--text",
        type=str,
        help="Direct text string to extract from.",
    )
    input_group.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help="Extract text from system clipboard (default behavior if no file/text provided).",
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Save extracted matches to the specified output file.",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy extracted matches back to the system clipboard.",
    )
    parser.add_argument(
        "-u", "--unique",
        action="store_true",
        help="Deduplicate results while preserving original order.",
    )
    parser.add_argument(
        "--phone-only",
        action="store_true",
        help="Extract only phone numbers.",
    )
    parser.add_argument(
        "--email-only",
        action="store_true",
        help="Extract only email addresses.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Display raw phone number matches without normalization.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format.",
    )

    return parser.parse_args()


def main() -> None:
    """Main CLI execution flow."""
    args = parse_args()

    # Determine input text source
    source_text = ""
    source_name = "clipboard"

    if args.file:
        source_name = f"file '{args.file}'"
        if not os.path.exists(args.file):
            print(f"Error: Input file '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        try:
            with open(args.file, "r", encoding="utf-8", errors="replace") as f:
                source_text = f.read()
        except Exception as exc:
            print(f"Error reading file '{args.file}': {exc}", file=sys.stderr)
            sys.exit(1)
    elif args.text is not None:
        source_name = "provided text argument"
        source_text = args.text
    else:
        # Default to clipboard
        source_name = "clipboard"
        source_text = get_clipboard_text()
        if not source_text.strip():
            print(
                "Notice: Clipboard is empty or contains no readable text.\n"
                "Tip: Copy text with Ctrl+C first, or pass a file using:\n"
                "     python PhoneEmailExtraction.py --file Input-Data.txt\n"
                "     python PhoneEmailExtraction.py --text \"Call 415-863-9900\"\n"
            )

    # Perform extraction based on flags
    formatted_phones = not args.raw
    dedup = args.unique

    phones: List[str] = []
    emails: List[str] = []

    if not args.email_only:
        phones = extract_phone_numbers(source_text, formatted=formatted_phones, deduplicate=dedup)
    if not args.phone_only:
        emails = extract_emails(source_text, deduplicate=dedup)

    total_matches = len(phones) + len(emails)

    # JSON Output Mode
    if args.json:
        payload = {}
        if not args.email_only:
            payload["phone_numbers"] = phones
        if not args.phone_only:
            payload["emails"] = emails
        payload["total_matches"] = total_matches
        output_str = json.dumps(payload, indent=2)
        print(output_str)
    else:
        # Standard Formatted Terminal Output
        lines = []
        if total_matches == 0:
            output_str = "***No Phone Number or Email Address found.***"
            print(output_str)
        else:
            header = f"=== Extracted from {source_name} (Total: {total_matches}) ==="
            print(header)
            lines.append(header)

            if phones:
                sub_header = f"\n[ Phone Numbers ({len(phones)}) ]"
                print(sub_header)
                lines.append(sub_header)
                for p in phones:
                    print(f"  - {p}")
                    lines.append(p)

            if emails:
                sub_header = f"\n[ Email Addresses ({len(emails)}) ]"
                print(sub_header)
                lines.append(sub_header)
                for e in emails:
                    print(f"  - {e}")
                    lines.append(e)

            output_str = "\n".join(phones + emails)

    # Optional: Save to file
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as out_f:
                if args.json:
                    out_f.write(output_str)
                else:
                    out_f.write("\n".join(phones + emails) + "\n")
            print(f"\n[+] Results successfully saved to '{args.output}'.")
        except Exception as exc:
            print(f"Error saving to '{args.output}': {exc}", file=sys.stderr)

    # Optional: Copy to clipboard
    if args.copy:
        to_copy = output_str if args.json else "\n".join(phones + emails)
        if copy_to_clipboard(to_copy):
            print("[+] Results copied to system clipboard.")


if __name__ == "__main__":
    main()
