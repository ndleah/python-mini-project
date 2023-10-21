class SubstitutionCipher:
    def __init__(self, key: dict):
        self.key = key

    def get_input(self):
        while True:
            # Prompt the user for input and convert it to lowercase
            blank_string = input("Enter a string to decrypt: ").lower()
            if blank_string.isalpha():
                self.blank_string = blank_string
                break
            else:
                print("Input is not valid")

    def encrypt_string(self):
        # Use a list comprehension to apply the substitution cipher
        encrypted_string = ''.join(self.key[c] if c in self.key else c for c in self.blank_string)
        self.encrypted_string = encrypted_string
        return encrypted_string

    def decrypt_string(self, string):
        # Use a list comprehension to reverse the substitution cipher
        decrypted_string = ''.join(self.key[c] if c in self.key else c for c in string)
        return decrypted_string

if __name__ == "__main__":
    key = {
        "a": "d", "b": "e", "c": "f", "d": "g", "e": "h", "f": "i",
        "g": "j", "h": "k", "i": "l", "j": "m", "k": "n", "l": "o",
        "m": "p", "n": "q", "o": "r", "p": "s", "q": "t", "r": "u",
        "s": "v", "t": "w", "u": "x", "v": "y", "w": "z", "x": "a",
        "y": "b", "z": "c"
    }

    # Create an instance of the SubstitutionCipher class
    substitution_cipher = SubstitutionCipher(key)

    # Get user input and store it in the instance
    substitution_cipher.get_input()

    # Encrypt the input string and print the result
    encrypted = substitution_cipher.encrypt_string()
    print(f"Encrypted string: {encrypted}")

    # Decrypt the encrypted string and print the result
    decrypted = substitution_cipher.decrypt_string(encrypted)
    print(f"Decrypted string: {decrypted}")
