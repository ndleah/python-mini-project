import csv
from cryptography.fernet import Fernet

passwords = []
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

def add_password():
    website = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")
    encrypted_password = encrypt_password(password)
    passwords.append({
        "website": website,
        "username": username,
        "password": encrypted_password
    })
    with open('passwords.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([website, username, encrypted_password])

def get_password(website):
    for entry in passwords:
        if entry["website"] == website:
            username = entry["username"]
            encrypted_password = entry["password"]
            decrypted_password = decrypt_password(encrypted_password)        
            print(f"Website: {website}")
            print(f"Username: {username}")
            print(f"Password: {decrypted_password}")
            return
    print("Website not found")

with open('passwords.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        passwords.append({
            "website": row[0],
            "username": row[1],
            "password": row[2]
        })

while True:
    print("\n1. Add Password")
    print("2. Get Password")
    print("3. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        add_password()
    elif choice == '2':
        website = input("Enter website: ")
        get_password(website)
    elif choice == '3':
        break
    else:
        print("Invalid choice")
