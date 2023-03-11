#This application uses the ceaser cipher in order to encrypt text
def encrypt(text):
    result = ""
    
    for i in range(len(text)):
        char = text[i]
        
        if char.isupper():
            result += chr((ord(char) + key - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + key - 97) % 26 + 97)
        else:
            result += char
    
    return result

def decrypt(text):
    result = ""
    
    for i in range(len(text)):
        char = text[i]
        
        if char.isupper():
            result += chr((ord(char) - decryptkey - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) - decryptkey - 97) % 26 + 97)
        else:
            result += char
    
    return result


choice = int(input("Would you like to encrypt some text or decrypt some text? Choose 1 to encrypt and 2 to decrypt "))
if choice == 1:
    text = input("Input the text you want to encrypt: \n")
    key = int(input("Input the key for the encryption *NOTE! This is using the Ceaser cipher \n"))

    result = encrypt(text)
    print(result)

elif choice == 2:
    text = input("Input the text you want to decrypt: \n")
    decryptkey = int(input("Input the key for the decryption *NOTE! This is using the Ceaser cipher \n"))

    result = decrypt(text)
    print(result)

else:
    print("idk")
