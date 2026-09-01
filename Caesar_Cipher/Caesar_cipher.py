import sys

class CaesarCipher:
    """Caesar Cipher encoder/decoder supporting configurable alphabet shifts."""
    def __init__(self, shift: int = 3):
        self.shift = shift % 26

    def encrypt(self, text: str) -> str:
        """Encrypt plain text with Caesar Cipher shift."""
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = chr((ord(char) - base + self.shift) % 26 + base)
                result.append(shifted)
            else:
                result.append(char)
        return "".join(result)

    def decrypt(self, text: str) -> str:
        """Decrypt cipher text with Caesar Cipher shift."""
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = chr((ord(char) - base - self.shift) % 26 + base)
                result.append(shifted)
            else:
                result.append(char)
        return "".join(result)

def main():
    if len(sys.argv) > 1:
        user_text = " ".join(sys.argv[1:])
        shift_val = 3
    else:
        user_text = input("Enter text to encrypt: ").strip()
        if not user_text:
            user_text = "Hello, World! 123"
        try:
            raw_shift = input("Enter shift key (default 3): ").strip()
            shift_val = int(raw_shift) if raw_shift else 3
        except ValueError:
            shift_val = 3

    cipher = CaesarCipher(shift=shift_val)
    encrypted = cipher.encrypt(user_text)
    decrypted = cipher.decrypt(encrypted)

    print(f"\n🔐 Caesar Cipher (Shift={shift_val})")
    print(f"  • Original:  {user_text}")
    print(f"  • Encrypted: {encrypted}")
    print(f"  • Decrypted: {decrypted}")

if __name__ == "__main__":
    main()

