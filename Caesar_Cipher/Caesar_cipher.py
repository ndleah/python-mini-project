# class main: 
#     def __init__(self,key:dict) -> None:
#         self.key = key

#     def get_input(self) -> None: 
#         while True:
#             blank_string = str(input("Enter string to decrypt: "))
#             if blank_string.isalpha():
#                 blank_string = blank_string.lower()
#                 self.blank_string = blank_string
#                 break
#             else:
#                 print("Input is not valid")
#                 continue

#     def encrypt_string(self) -> str:
#         output = ""
#         for c in self.blank_string:
#             for k,v in self.key.items():
#                 if k == c:
#                     output += v
#                 else:
#                     continue
#         self.decrypted_string = output
#         return(output)

#     def decrypt_string(self, string: str) -> str:
#         output = "" 
#         string = string.lower()
#         string = string.strip()
#         if string == "":
#             return(self.blank_string)
#         else: 
#             for c in string:
#                 for k,v in self.key.items():
#                     if v == c:
#                         output += k
        
#         return(output)

# if __name__ == "__main__":
#     key ={"a": "d", "b": "e", "c": "f", "d": "g", "e": "h", "f": "i", "g": "j", "h": "k", "i": "l", "j": "m", "k": "n", "l": "o", "m": "p", "n": "q", "o": "r", "p": "s", "q": "t", "r": "u", "s": "v", "t": "w", "u": "x", "v": "y", "w": "z", "x": "a", "y": "b", "z": "c"}
#     main = main(key=key)
#     main.get_input()
#     print(main.encrypt_string())


import art
from art import logo
print(logo)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def caesar(start_text, shift_amount, cipher_direction):
  end_text = ""
  if cipher_direction == "decode":
    shift_amount *= -1
  for char in start_text:
    if char in alphabet:
       position = alphabet.index(char)
       new_position = position + shift_amount
       end_text += alphabet[new_position]
    else:
      end_text += char
    
    
  print(f"Here's the {cipher_direction}d result: {end_text}")

should_continue = True
while should_continue:
  direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
  text = input("Type your message:\n").lower()
  shift = int(input("Type the shift number:\n"))
  
  shift = shift % 26
  caesar(start_text=text, shift_amount=shift, cipher_direction=direction)

  result = input("Type 'yes' if you want to go again. Otherwise type 'no'.\n")
  if result == "no":
    should_continue = False
    print("Goodbye")