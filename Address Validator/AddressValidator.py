
def addressVal(address):

    address = address.strip()

    if " " in address:
        print("Invalid: Email should not contain spaces")

    elif address.count("@") != 1:
        print("Invalid: Email must contain exactly one @")

    elif "." not in address:
        print("Invalid: Email must contain a dot")

    else:
        username, domain = address.split("@")

        if username == "":
            print("Invalid: Username cannot be empty")

        elif domain == "":
            print("Invalid: Domain cannot be empty")

        elif domain.startswith(".") or domain.endswith("."):
            print("Invalid: Incorrect dot position")

        elif "." not in domain:
            print("Invalid: Domain must contain a dot")

        else:
            print("Valid Email Address")


print("Email Validation Program")

while True:

    print("\nEnter your email address")
    print("Type exit to stop")

    x = input("Email: ")

    if x.lower() == "exit":
        print("Program Ended")
        break

    addressVal(x)

