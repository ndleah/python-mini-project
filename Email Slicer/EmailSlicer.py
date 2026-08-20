import re

def is_valid_email(email: str) -> bool:
    """Validates an email address using regex."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.fullmatch(regex, email.strip()))

def slice_email(email: str) -> dict:
    """Slices an email address into username, domain, domain name, and TLD."""
    email = email.strip()
    username, domain = email.split('@', 1)
    
    domain_parts = domain.rsplit('.', 1)
    domain_name = domain_parts[0]
    tld = domain_parts[1] if len(domain_parts) > 1 else ''
    
    return {
        "username": username,
        "domain": domain,
        "domain_name": domain_name,
        "tld": tld
    }

def main():
    print("=" * 45)
    print("           📧 EMAIL SLICER TOOL 📧           ")
    print("=" * 45)
    print("Type 'exit' or 'q' to quit the program.\n")
    
    while True:
        user_input = input("Enter your email address: ").strip()
        
        if user_input.lower() in ['exit', 'q']:
            print("Exiting Email Slicer. Goodbye! 👋")
            break
            
        if not user_input:
            print("⚠️ Email input cannot be empty. Please try again.\n")
            continue
            
        if is_valid_email(user_input):
            details = slice_email(user_input)
            print("\n" + "-" * 35)
            print(f"  Username    : {details['username']}")
            print(f"  Domain      : {details['domain']}")
            print(f"  Domain Name : {details['domain_name']}")
            print(f"  TLD         : .{details['tld']}")
            print("-" * 35 + "\n")
        else:
            print("❌ Invalid Email format! Example of valid email: user@example.com\n")

if __name__ == "__main__":
    main()