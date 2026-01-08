import re

def is_valid_email(email):
    """
    Checks whether the given email address is valid.
    Returns True if valid, otherwise False.
    """
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.fullmatch(regex, email) is not None


def extract_email_parts(email):
    """
    Extracts username and domain from a valid email.
    """
    return email.split('@', 1)


email = input("Enter your email id: ")

if is_valid_email(email):
    username, domain = extract_email_parts(email)
    print("Username:", username)
    print("Domain:", domain)
else:
    print("Invalid Email!")
