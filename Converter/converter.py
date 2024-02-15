from converter_values import *  # import required files

def main():
    print(options["help"])  # prints help menu
    res = input("Response: ")

    while res.lower() != "q":  # program loop
        try:
            res = res.strip().split(" ")

            if len(res) == 1:
                display_help(res[0])  # display help menu
            elif len(res) == 4:
                perform_conversion(res)  # perform unit conversion
            else:
                print("Invalid command")

        except Exception as e:
            print("Error:", e)

        res = input("\nResponse: ")

def display_help(command):
    """Display help menu."""
    print(options[command])

def perform_conversion(res):
    """Perform unit conversion."""
    for i in res[3].split(','):
        value = round(eval("{} * {}['{}'] / {}['{}']".format(res[2], res[0], i, res[0], res[1])), 6)  # calculating
        print("{} \t : {}".format(i, value))  # displaying

if __name__ == "__main__":
    main()


