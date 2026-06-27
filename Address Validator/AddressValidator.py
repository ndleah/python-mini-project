def addressVal(address):
    address = address.strip()

    if " " in address:
        return False

    if "@" not in address:
        return False

    if "." not in address:
        return False

    at = address.find("@")
    dot = address.find(".")

    # @ should come before .
    if at > dot:
        return False

    # Something should exist before @ and after .
    if at == 0 or dot == len(address) - 1:
        return False

    return True


print("This program will decide if your input is a valid email address")

while True:
    print("\nA valid email address needs an '@' symbol and a '.'")
    x = input("Input your email address (or type 'quit' to exit): ")

    if x.lower() == "quit":
        print("Goodbye!")
        break

    if addressVal(x):
        print("Valid email address")
    else:
        print("Invalid email address")
#end