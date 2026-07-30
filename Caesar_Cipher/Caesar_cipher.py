class CaesarCipher: 
    """
    A class used to encrypt and decrypt strings using a substitution cipher key dictionary.
    """
    def __init__(self, key: dict) -> None:
        """
        Initializes the cipher with a key mapping dictionary.
        
        :param key: dict mapping input characters to their encrypted output characters.
        """
        self.key = key

    def get_input(self) -> None: 
        """
        Prompts the user for alphabetic text input and converts it to lowercase.
        """
        while True:
            blank_string = str(input("Enter string to encrypt/decrypt: "))
            if blank_string.isalpha():
                self.blank_string = blank_string.lower()
                break
            else:
                print("Input is not valid. Please enter alphabetic characters only.")
                continue

    def encrypt_string(self) -> str:
        """
        Encrypts self.blank_string using the instance key dictionary.
        
        :return: Encrypted string
        """
        output = ""
        for c in self.blank_string:
            if c in self.key:
                output += self.key[c]
        self.encrypted_string = output
        return output

    def decrypt_string(self, string: str = "") -> str:
        """
        Decrypts a given string (or self.blank_string) using the inverse key dictionary.
        
        :param string: Encrypted input string to decode.
        :return: Decrypted original string
        """
        output = "" 
        target_string = string.lower().strip() if string else self.blank_string
        
        # Create inverse lookup map (v -> k)
        inverse_key = {v: k for k, v in self.key.items()}
        for c in target_string:
            if c in inverse_key:
                output += inverse_key[c]
                
        return output

if __name__ == "__main__":
    key = {
        "a": "d", "b": "e", "c": "f", "d": "g", "e": "h", "f": "i", "g": "j", 
        "h": "k", "i": "l", "j": "m", "k": "n", "l": "o", "m": "p", "n": "q", 
        "o": "r", "p": "s", "q": "t", "r": "u", "s": "v", "t": "w", "u": "x", 
        "v": "y", "w": "z", "x": "a", "y": "b", "z": "c"
    }
    cipher = CaesarCipher(key=key)
    cipher.get_input()
    encrypted = cipher.encrypt_string()
    print(f"Encrypted Output: {encrypted}")