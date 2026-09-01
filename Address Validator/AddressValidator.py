import sys
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
IPV4_REGEX = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
URL_REGEX = re.compile(r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$')

def validate_address(address: str) -> dict:
    """Validate whether input is a valid Email, IPv4 IP Address, or Web URL Address."""
    address = address.strip()

    is_email = bool(EMAIL_REGEX.match(address))
    is_ip = bool(IPV4_REGEX.match(address))
    is_url = bool(URL_REGEX.match(address))

    is_valid = is_email or is_ip or is_url
    category = "Email Address" if is_email else "IPv4 Address" if is_ip else "Web URL Address" if is_url else "Invalid Format"

    return {
        "input": address,
        "is_email": is_email,
        "is_ip": is_ip,
        "is_url": is_url,
        "is_valid": is_valid,
        "category": category
    }

def addressVal(address: str) -> str:
    """Legacy function interface preserving original return/print behavior."""
    res = validate_address(address)
    status = "Valid" if res["is_valid"] else "Invalid"
    print(status)
    return status

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
        res = validate_address(target)
        print(f"Address '{target}' -> {res['category']} ({'Valid' if res['is_valid'] else 'Invalid'})")
        return

    print("=== Address & Email Validator ===")
    print("Supports Email, IPv4 IP, and Web URL addresses. Enter 'q' to exit.")

    while True:
        user_input = input("\nEnter Address: ").strip()
        if not user_input or user_input.lower() == 'q':
            print("Exiting Address Validator.")
            break

        res = validate_address(user_input)
        if res["is_valid"]:
            print(f"✅ Valid {res['category']}!")
        else:
            print(f"❌ Invalid address or email format.")

if __name__ == "__main__":
    main()

