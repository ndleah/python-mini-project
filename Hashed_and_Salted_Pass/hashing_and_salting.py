import os
import sys
import secrets
import hashlib
import hmac

DEFAULT_ITERATIONS = 100000

def generate_salt(length: int = 16) -> str:
    """Generate a cryptographically secure random salt hex string."""
    return secrets.token_hex(length)

def hash_password(password: str, salt: str = None, iterations: int = DEFAULT_ITERATIONS) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with salt and iteration work factor."""
    if not salt:
        salt = generate_salt(16)
    
    salt_bytes = salt.encode('utf-8')
    password_bytes = password.encode('utf-8')
    
    key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, iterations)
    return f"pbkdf2_sha256${iterations}${salt}${key.hex()}"

def verify_password(stored_hash: str, candidate_password: str) -> bool:
    """Safely verify a candidate password against a stored PBKDF2 hash string."""
    try:
        parts = stored_hash.split('$')
        if len(parts) != 4 or parts[0] != "pbkdf2_sha256":
            return False
        
        _, iterations_str, salt, target_key_hex = parts
        iterations = int(iterations_str)
        
        salt_bytes = salt.encode('utf-8')
        candidate_bytes = candidate_password.encode('utf-8')
        
        candidate_key = hashlib.pbkdf2_hmac('sha256', candidate_bytes, salt_bytes, iterations)
        
        return hmac.compare_digest(candidate_key.hex(), target_key_hex)
    except Exception:
        return False

# Helper functions for backward compatibility
def hashing(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def salting(length: int = 16) -> str:
    return generate_salt(max(1, length // 2))

def main():
    print("--- Cryptographic Password Hashing & Verification ---")
    password = input("Enter your password: ").strip()
    if not password:
        print("Error: Password cannot be empty.")
        return

    secure_hash = hash_password(password)
    print(f"\nGenerated PBKDF2 Secure Hash:\n{secure_hash}")

    print("\n--- Verifying Password ---")
    verify_input = input("Re-enter password to verify: ").strip()
    if verify_password(secure_hash, verify_input):
        print("SUCCESS: Password verified successfully!")
    else:
        print("FAILURE: Invalid password!")

if __name__ == '__main__':
    main()

    