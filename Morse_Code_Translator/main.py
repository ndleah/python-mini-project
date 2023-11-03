# Define a dictionary for English alphabet to Morse code conversion
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': ' '  # Space between words
}

def text_to_morse(text):
    morse_code = ''
    for char in text:
        if char.upper() in morse_code_dict:
            morse_code += morse_code_dict[char.upper()] + ' '  # Add space between letters
        else:
            morse_code += ' '  # Space for characters not in the dictionary
    return morse_code

while True:
    print("Welcome to the English to Morse Code Translator")
    text = input("Enter a message to translate to Morse code: ")
    
    morse_code = text_to_morse(text)
    print("Morse Code:", morse_code)

    another_translation = input("Translate another word? (y/n): ")
    if another_translation.lower() != 'y':
        print("Goodbye!")
        break
