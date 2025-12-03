class Cipher:
    def __init__(self, key: dict) -> None:
        self.key = key
        self.rev_key = {v: k for k, v in key.items()}  # reverse mapping
    
    def get_input(self) -> None:
        while True:
            text = input("Enter string to encrypt: ").strip()
            if text.isalpha():
                self.blank_string = text.lower()
                break
            else:
                print("Input is not valid! Only alphabets allowed.")
    
    def encrypt_string(self) -> str:
        output = ""
        for c in self.blank_string:
            output += self.key.get(c, c)
        return output
    
    def decrypt_string(self, string: str) -> str:
        string = string.strip().lower()
        if string == "":
            return self.blank_string
        output = ""
        for c in string:
            output += self.rev_key.get(c, c)
        return output

if __name__ == "__main__":
    # Fixed: Caesar cipher with shift of 3 (properly wrapping around)
    key = {
        "a": "d", "b": "e", "c": "f", "d": "g", "e": "h", "f": "i", "g": "j",
        "h": "k", "i": "l", "j": "m", "k": "n", "l": "o", "m": "p", "n": "q",
        "o": "r", "p": "s", "q": "t", "r": "u", "s": "v", "t": "w", "u": "x",
        "v": "y", "w": "z", "x": "a", "y": "b", "z": "c"
    }
    
    cipher = Cipher(key)
    cipher.get_input()
    encrypted = cipher.encrypt_string()
    print("Encrypted:", encrypted)
    print("Decrypted:", cipher.decrypt_string(encrypted))