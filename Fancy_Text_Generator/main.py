import sys

# Unicode Character Mapping Dictionaries for Fancy Text Styles
BOLD_MAP = {c: chr(0x1D400 + ord(c) - ord('A')) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
BOLD_MAP.update({c: chr(0x1D41A + ord(c) - ord('a')) for c in "abcdefghijklmnopqrstuvwxyz"})
BOLD_MAP.update({c: chr(0x1D7CE + ord(c) - ord('0')) for c in "0123456789"})

SCRIPT_MAP = {c: chr(0x1D49C + ord(c) - ord('A')) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
SCRIPT_MAP.update({c: chr(0x1D4B6 + ord(c) - ord('a')) for c in "abcdefghijklmnopqrstuvwxyz"})

BUBBLE_MAP = {c: chr(0x24B6 + ord(c) - ord('A')) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
BUBBLE_MAP.update({c: chr(0x24D0 + ord(c) - ord('a')) for c in "abcdefghijklmnopqrstuvwxyz"})
BUBBLE_MAP.update({c: chr(0x2460 + ord(c) - ord('1')) for c in "123456789"})
BUBBLE_MAP['0'] = '⓪'

FULLWIDTH_MAP = {c: chr(0xFF01 + ord(c) - ord('!')) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"}

def transform_text_unicode(text: str, style: str = "bold") -> str:
    """Transform input text into styled Unicode font characters."""
    style_key = style.lower().strip()
    if style_key == "bold":
        return "".join(BOLD_MAP.get(c, c) for c in text)
    elif style_key == "script":
        return "".join(SCRIPT_MAP.get(c, c) for c in text)
    elif style_key == "bubble":
        return "".join(BUBBLE_MAP.get(c, c) for c in text)
    elif style_key == "fullwidth":
        return "".join(FULLWIDTH_MAP.get(c, c) for c in text)
    return text

def ascii_maker(text: str = None) -> str:
    """Generate ASCII figlet banner or fancy Unicode text styles."""
    print('-' * 70)
    print("✨ FANCY TEXT & ASCII BANNER GENERATOR ✨")
    print('-' * 70)

    if text is None:
        text = input("\nEnter Your Text: ").strip()

    if not text:
        text = "HELLOMORNING"

    print("\n--- 1. ASCII Figlet Banner ---")
    try:
        import pyfiglet
        banner = pyfiglet.figlet_format(text).upper()
        print(banner)
    except Exception:
        print(f"[{text.upper()}] (pyfiglet library not installed)")

    print("--- 2. Bold Unicode Style ---")
    print(transform_text_unicode(text, "bold"))

    print("\n--- 3. Script / Cursive Style ---")
    print(transform_text_unicode(text, "script"))

    print("\n--- 4. Bubble / Enclosed Circle Style ---")
    print(transform_text_unicode(text, "bubble"))

    print("\n--- 5. Fullwidth Style ---")
    print(transform_text_unicode(text, "fullwidth"))
    print('-' * 70)
    return text

def ending() -> bool:
    """Prompt user to replay program without terminating Python process."""
    ans = input("\nDo you want to generate another text? (y/N): ").strip().lower()
    return ans == 'y'

def run_loop():
    """Main interactive loop."""
    if len(sys.argv) > 1:
        text_arg = " ".join(sys.argv[1:])
        ascii_maker(text_arg)
        return

    while True:
        ascii_maker()
        if not ending():
            print("\nThanks for using Fancy Text Generator! Goodbye! :)\n")
            break

def main():
    run_loop()

if __name__ == '__main__':
    main()

