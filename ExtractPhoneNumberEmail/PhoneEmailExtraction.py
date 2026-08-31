import os
import sys
import re

PHN_REGEX = re.compile(
    r"""
    (\(?(\+?\d{1,3})\)?  # area / country code
    [\s_.-]?)             # separator or space
    (\d{3})                # first three digits
    [\s_.-]?               # separator or space
    (\d{3})                # second three digits
    [\s_.-]?               # separator or space
    (\d{4,5})              # last four/five digits
""",
    re.VERBOSE,
)

EMAIL_REGEX = re.compile(
    r"""
    ([a-zA-Z0-9._%-]+        # username
    @                        # @ character
    [a-zA-Z0-9_-]+           # domain name
    \.                       # .(dot)
    [a-zA-Z]{2,6}            # domain TLD
    (\.[a-zA-Z]{2,3})?)      # second level domain like co.uk
""",
    re.VERBOSE,
)

def extract_phone_and_email(text_data: str) -> dict:
    """Extract phone numbers and email addresses from raw text data."""
    phones = []
    emails = []

    if not text_data:
        return {"phones": phones, "emails": emails}

    for num in PHN_REGEX.findall(text_data):
        country_code = f"({num[1]})" if num[1] else ""
        formatted_phone = f"{country_code}{num[2]}-{num[3]}-{num[4]}"
        phones.append(formatted_phone)

    for email_match in EMAIL_REGEX.findall(text_data):
        emails.append(email_match[0])

    return {"phones": sorted(list(set(phones))), "emails": sorted(list(set(emails)))}

def get_input_text(file_path: str = None) -> str:
    """Get input text from file, CLI argument, clipboard, or default file."""
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    script_dir = os.path.dirname(__file__)
    default_txt = os.path.join(script_dir, "Input-Data.txt")
    if os.path.exists(default_txt):
        with open(default_txt, 'r', encoding='utf-8') as f:
            return f.read()

    try:
        import pyperclip
        paste_text = str(pyperclip.paste())
        if paste_text.strip():
            print("Reading input text from system clipboard...")
            return paste_text
    except Exception:
        pass

    return ""

def main():
    target_file = sys.argv[1] if len(sys.argv) > 1 else None
    text_content = get_input_text(target_file)

    if not text_content:
        print("No text data found from file or clipboard.")
        return

    results = extract_phone_and_email(text_content)
    total = len(results["phones"]) + len(results["emails"])

    if total > 0:
        print(f"=== Extraction Results ({total} matches found) ===")
        if results["phones"]:
            print("\n📞 Phone Numbers:")
            for p in results["phones"]:
                print(f"  - {p}")

        if results["emails"]:
            print("\n📧 Email Addresses:")
            for e in results["emails"]:
                print(f"  - {e}")
    else:
        print("*** No Phone Number or Email Address found in text. ***")

if __name__ == "__main__":
    main()

