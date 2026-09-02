import sys

def encrypt(text: str, shift: int = 3) -> str:
    """Encrypt input text using Caesar cipher with given shift."""
    result = ""
    shift = shift % 26
    for char in text:
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result

def decrypt(text: str, shift: int = 3) -> str:
    """Decrypt cipher text using Caesar cipher with given shift."""
    result = ""
    shift = shift % 26
    for char in text:
        if char.isupper():
            result += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            result += char
    return result

def main():
    print("=== Text Encryptor (Caesar Cipher) ===")
    print("1. Encrypt text")
    print("2. Decrypt text")

    try:
        raw_choice = input("Enter choice (1 or 2): ").strip()
        choice = int(raw_choice)
    except ValueError:
        print("Invalid choice! Defaulting to Option 1 (Encrypt).")
        choice = 1

    if choice == 1:
        text = input("Enter text to encrypt: ")
        try:
            key = int(input("Enter numeric shift key (e.g. 3): "))
        except ValueError:
            key = 3
        res = encrypt(text, key)
        print(f"\nEncrypted Text: {res}")
    elif choice == 2:
        text = input("Enter text to decrypt: ")
        try:
            key = int(input("Enter numeric shift key (e.g. 3): "))
        except ValueError:
            key = 3
        res = decrypt(text, key)
        print(f"\nDecrypted Text: {res}")
    else:
        print("Invalid option selected.")

if __name__ == '__main__':
    main()

