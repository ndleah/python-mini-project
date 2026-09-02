import secrets
import string

def generate_password(length: int = 12, use_uppercase: bool = True, use_lowercase: bool = True, use_numbers: bool = True, use_symbols: bool = True) -> str:
    """Generate a cryptographically secure random password with guaranteed character set coverage."""
    if length <= 0:
        raise ValueError("Password length must be greater than zero.")

    character_pools = []
    if use_uppercase:
        character_pools.append(string.ascii_uppercase)
    if use_lowercase:
        character_pools.append(string.ascii_lowercase)
    if use_numbers:
        character_pools.append(string.digits)
    if use_symbols:
        character_pools.append(string.punctuation)

    if not character_pools:
        raise ValueError("No character types selected for password generation")

    # Guarantee at least one character from each selected set
    password_chars = [secrets.choice(pool) for pool in character_pools]

    # Combine all selected pools for remaining characters
    all_characters = ''.join(character_pools)
    remaining_length = max(0, length - len(password_chars))

    for _ in range(remaining_length):
        password_chars.append(secrets.choice(all_characters))

    # Shuffle the characters securely
    shuffled_chars = list(password_chars)
    for i in range(len(shuffled_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        shuffled_chars[i], shuffled_chars[j] = shuffled_chars[j], shuffled_chars[i]

    return ''.join(shuffled_chars[:length])

