import re

def validate_email(email: str) -> dict:
    
    result = {
        "original_email": email,
        "is_valid": True,
        "errors": []
    }

    email = email.strip().lower()

    # Rule 1: Email must not be empty
    if not email:
        result["is_valid"] = False
        result["errors"].append("Email cannot be empty.")
        return result

    # Rule 2: Must contain exactly one '@'
    if email.count("@") != 1:
        result["is_valid"] = False
        result["errors"].append("Email must contain exactly one '@' symbol.")
        return result

    local_part, domain_part = email.split("@")

    # Rule 3: Local part must not be empty
    if not local_part:
        result["is_valid"] = False
        result["errors"].append("Email must contain text before '@'.")
    
    # Rule 4: Domain part must contain at least one '.'
    if "." not in domain_part:
        result["is_valid"] = False
        result["errors"].append("Email must contain at least one '.' after '@'.")
        return result

    # Rule 5: Domain extension must be present
    domain_name, *extensions = domain_part.split(".")
    if not domain_name:
        result["is_valid"] = False
        result["errors"].append("Domain name cannot start with a dot.")

    if any(ext == "" for ext in extensions):
        result["is_valid"] = False
        result["errors"].append("Email cannot end with a dot or contain empty extensions.")

    # Rule 6: Prevent consecutive dots
    if ".." in email:
        result["is_valid"] = False
        result["errors"].append("Email cannot contain consecutive dots '..'.")

    # Rule 7: Basic character whitelist
    allowed_pattern = r"^[a-z0-9._%-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    if not re.match(allowed_pattern, email):
        result["is_valid"] = False
        result["errors"].append("Email contains invalid characters or structure.")

    return result


if __name__ == "__main__":
    print("------ Improved Email Validator ------")
    user_email = input("Enter an email address: ")

    response = validate_email(user_email)

    if response["is_valid"]:
        print("\n✓ Email is valid!")
    else:
        print("\n✗ Email is invalid due to:")
        for err in response["errors"]:
            print(f" - {err}")

    
