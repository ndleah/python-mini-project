import sys
import pyfiglet

# Banner maker
def ascii_maker():
    print('-' * 70)
    ascii_banner = pyfiglet.figlet_format("A C I I banner").upper()
    print(ascii_banner)
    print('-' * 70)
    
    text = input("\nEnter Your Text: ")
    banner = pyfiglet.figlet_format(f"{text}").upper()
    print(banner)

# Ending message
def ending():
    print("\n\nThanks for using the code :)\n")
    a = input("Do you want to run the program again? (y for yes) (any key for no): ")
    if a.lower() == 'y':
        return True
    else:
        sys.exit()

# Main loop
def run_loop():
    while True:
        ascii_maker()
        if not ending():
            break

run_loop()
