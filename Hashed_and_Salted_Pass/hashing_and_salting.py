import string
import random 
import hashlib


def hashing(password):
    byte_string = password.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(byte_string)
    
    hashed_password = hash_object.hexdigest()
    
    return hashed_password

def salting(length:int):
    salt = ''
    salt = salt.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    return salt

if __name__ ==  '__main__':
    salt = salting(4)
    password = input("Enter your password\n")
    
    hashed_password = hashing(password)
    hashed_salt = hashing(salt)
    secure_password = f"{hashed_salt}${hashed_password}"
    
    print(secure_password)
    