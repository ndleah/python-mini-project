import os
import sys
import csv
from cryptography.fernet import Fernet

def get_or_create_key() -> bytes:
    """Load or generate persistent encryption key to secret.key file."""
    key_path = os.path.join(os.path.dirname(__file__), 'secret.key')
    if os.path.exists(key_path):
        with open(key_path, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
        return key

key = get_or_create_key()
cipher_suite = Fernet(key)
csv_file_path = os.path.join(os.path.dirname(__file__), 'passwords.csv')
passwords = []

def encrypt_password(password: str) -> str:
    """Encrypt plain text password string to token string."""
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    """Decrypt token string or bytes back to plain text password."""
    if isinstance(encrypted_password, str):
        encrypted_password = encrypted_password.encode()
    return cipher_suite.decrypt(encrypted_password).decode()

def load_passwords():
    """Load passwords from passwords.csv if file exists."""
    global passwords
    passwords = []
    if os.path.exists(csv_file_path):
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        passwords.append({
                            "website": row[0],
                            "username": row[1],
                            "password": row[2]
                        })
        except Exception as e:
            print(f"Error loading passwords: {e}")

def add_password():
    website = input("Website: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if not website or not password:
        print("Error: Website and password cannot be empty.")
        return

    encrypted_password = encrypt_password(password)
    passwords.append({
        "website": website,
        "username": username,
        "password": encrypted_password
    })

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([website, username, encrypted_password])
    print(f"Password for '{website}' saved successfully.")

def get_password(website: str):
    website = website.strip()
    for entry in passwords:
        if entry["website"].lower() == website.lower():
            username = entry["username"]
            encrypted_password = entry["password"]
            try:
                decrypted_password = decrypt_password(encrypted_password)
                print("\n--- Credential Details ---")
                print(f"Website : {entry['website']}")
                print(f"Username: {username}")
                print(f"Password: {decrypted_password}")
                return
            except Exception as e:
                print(f"Error decrypting password: {e}")
                return
    print(f"Website '{website}' not found.")

def main():
    load_passwords()
    while True:
        print("\n--- Password Manager ---")
        print("1. Add Password")
        print("2. Get Password")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()
        if choice == '1':
            add_password()
        elif choice == '2':
            site = input("Enter website to look up: ")
            get_password(site)
        elif choice == '3':
            print("Exiting Password Manager.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()

