import sys

CHAR_TO_DOTS = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', ' ': ' ', '0': '-----',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '&': '.-...', "'": '.----.', '@': '.--.-.', ')': '-.--.-', '(': '-.--.',
    ':': '---...', ',': '--..--', '=': '-...-', '!': '-.-.--', '.': '.-.-.-',
    '-': '-....-', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.'
}

DOTS_TO_CHAR = {v: k for k, v in CHAR_TO_DOTS.items() if k != ' '}

def encode_morse(message: str) -> str:
    """Encode plain text string into Morse code representation."""
    if not message:
        return ""
    result_parts = []
    for x in message:
        upper_x = x.upper()
        if upper_x == ' ':
            result_parts.append(' ')
        else:
            result_parts.append(CHAR_TO_DOTS.get(upper_x, upper_x))
    return " ".join(result_parts).strip()

def decode_morse(morse_code: str) -> str:
    """Decode Morse code representation back into plain text string."""
    if not morse_code:
        return ""
    words = morse_code.split('   ')
    decoded_words = []

    for word in words:
        chars = word.split(' ')
        decoded_chars = [DOTS_TO_CHAR.get(c, c) for c in chars if c]
        decoded_words.append("".join(decoded_chars))

    return " ".join(decoded_words)

def main():
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
    else:
        msg = "Hello World!"

    encoded = encode_morse(msg)
    decoded = decode_morse(encoded)

    print(f"Original Text: {msg}")
    print(f"Morse Code:    {encoded}")
    print(f"Decoded Back:  {decoded}")

if __name__ == '__main__':
    main()