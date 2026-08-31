import sys
import re

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

def is_valid_email(email: str) -> bool:
    """Validate email address using regex."""
    email = email.strip()
    return bool(re.fullmatch(EMAIL_REGEX, email))

def slice_email(email: str) -> dict:
    """Slice email address into username and domain components."""
    email = email.strip()
    if not is_valid_email(email):
        return {"username": None, "domain": None, "is_valid": False}

    at_idx = email.index('@')
    username = email[:at_idx]
    domain = email[at_idx + 1:]
    return {"username": username, "domain": domain, "is_valid": True}

def main():
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        user_input = input("Enter your email id: ").strip()

    res = slice_email(user_input)
    if res["is_valid"]:
        print(f"\n✅ Valid Email Address: '{user_input}'")
        print(f"  • Username: {res['username']}")
        print(f"  • Domain:   {res['domain']}")
    else:
        print(f"\n❌ Error: '{user_input}' is not a valid email address.")

if __name__ == '__main__':
    main()