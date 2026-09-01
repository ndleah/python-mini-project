import sys
import subprocess
import LocateIP

def Display_Menu():
    header = """
    __________________________
    |       IP Locater        |
    |       IP Finder         |
    |___________   ___________|
                \\  \\ 
                ^_ _^
                (o o)\\_________
                (_ _)\\         )/\\/
                  U   ||----W||
                      ||     ||
    ### Tools:
        [1] Locate an IP address
        [2] Get the IP address of a domain
        [3] Exit

    * Type <clear> to clear previous commands
    * Type <q> to abort operation of a tool
    """
    print(header)

def Home():
    """Non-recursive menu loop."""
    Display_Menu()

    while True:
        try:
            selected_option = input("\nEnter your option (1-3): ").strip()
            if selected_option.lower() == 'clear':
                subprocess.call('cls' if sys.platform == 'win32' else 'clear', shell=True)
                Display_Menu()
                continue
            if selected_option.lower() == 'q':
                print("Exiting tool.")
                break

            opt_int = int(selected_option)
            if opt_int == 1:
                LocateIP.locate_ip()
            elif opt_int == 2:
                LocateIP.get_ip()
            elif opt_int == 3:
                print("Goodbye!")
                break
            else:
                print("Option not available. Please enter 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid option number (1, 2, or 3).")

def main():
    Home()

if __name__ == '__main__':
    main()