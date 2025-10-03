def validate_email(email: str) -> bool:
    email = email.strip().lower()  

    if '@' not in email or "." not in email:
        print("You must include \"@\" and \".\" in your email!")
        return False

    try:
        email, domain = email.split('@', 1)   
    except ValueError:
        print("Email must contain exactly one \"@\" symbol")
        return False
    if not email:
        print("You have nothing before the '@'!")
        return False

    if "." not in domain:
        print("You are mising the '.'!")
        return False

    if domain.startswith('.') or domain.endswith('.'):
        return False

    split_domain = domain.split(".")
    if any(not part for part in split_domain):
        return False

    if len(split_domain[-1]) < 2: 
        return False

    return True


test_emails = [
    "john.doe@example.com",
    "  Jane@domain.org  ",
    "noatsymbol.com",
    "@missinglocal.com",
    "missingdot@domain",
    "dot..error@domain.com",
    "wrongend@domain.",
    "short@domain.c"
]

for email in test_emails:
    print(f"{email} -> {validate_email(email)}")