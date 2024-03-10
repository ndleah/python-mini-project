import os

if __name__ == '__main__':
  print("Welcome to RoboSpeaker Created by Mustafa")
  while True:
    x = input("Enter what you want me to Speak: ")
    command = f"say {x}"
    os.system(command)
