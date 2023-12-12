import secrets
import string

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("No character types selected for password generation")

    password = ''.join(secrets.choice(characters) for i in range(length))
    return password
