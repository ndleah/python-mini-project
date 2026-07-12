def validate_email(email):
    email = email.strip().lower()

    if email.count("@") != 1:
        return False

    username, domain = email.split("@")

    if not username or not domain:
        return False

    if "." not in domain:
        return False

    if ".." in email:
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    return True


email = input("Enter email: ")

if validate_email(email):
    print("Valid email")
else:
    print("Invalid email")