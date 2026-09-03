import sys
import time
import platform

# Morse code dictionary
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
    ' ': '/'
}

# Reverse dictionary for Morse to Text conversion
reverse_morse_dict = {val: key for key, val in morse_code_dict.items()}

def play_sound(duration: int):
    """Play beep sound on Windows or print visual audio representation on Linux/macOS."""
    if platform.system() == 'Windows':
        try:
            import winsound
            winsound.Beep(1000, duration)
        except Exception:
            time.sleep(duration / 1000.0)
    else:
        # For Linux/macOS
        sys.stdout.write('\a')
        sys.stdout.flush()
        time.sleep(duration / 1000.0)

def text_to_morse(text: str) -> str:
    """Convert text string into Morse code representation."""
    morse_code = []
    for char in text.upper():
        if char in morse_code_dict:
            morse_code.append(morse_code_dict[char])
        else:
            morse_code.append('/')
    return ' '.join(morse_code)

def morse_to_text(morse_code: str) -> str:
    """Convert Morse code string back into plain text."""
    words = morse_code.strip().split('/')
    decoded_words = []

    for word in words:
        chars = word.strip().split()
        decoded_chars = [reverse_morse_dict.get(c, '?') for c in chars]
        decoded_words.append(''.join(decoded_chars))

    return ' '.join(decoded_words)

def morse_to_sound(morse_code: str):
    """Play audio beeps for Morse code symbols."""
    print("Playing Morse Code Audio: ", end="", flush=True)
    for symbol in morse_code:
        if symbol == '.':
            print(".", end="", flush=True)
            play_sound(100)
        elif symbol == '-':
            print("-", end="", flush=True)
            play_sound(300)
        elif symbol == ' ':
            time.sleep(0.2)
        elif symbol == '/':
            print(" / ", end="", flush=True)
            time.sleep(0.5)
    print("\nAudio playback complete!")

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text to convert to Morse code: ").strip()

    if text:
        morse = text_to_morse(text)
        print("Morse Code Output:", morse)

        # Reverse test
        decoded = morse_to_text(morse)
        print("Decoded Back Text :", decoded)

        # Play sound
        morse_to_sound(morse)

if __name__ == '__main__':
    main()

