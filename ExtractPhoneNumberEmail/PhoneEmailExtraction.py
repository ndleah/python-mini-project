import pyperclip  # Clipboard module
import re  # Regular expression module

# Get the text from the clipboard
text = str(pyperclip.paste())

# Empty list to store matches
matches = []


def PhoneNumCheck():
    # Regular expression for matching phone numbers
    PhnNumregex = re.compile(
        r"""
        (\(?(\+?\d{1,3})\)?  # area code
        [\s_.-]?)             # separator or space
        (\d{3})                # first three digits
        [\s_.-]?               # separator or space
        (\d{3})                # second three digits
        [\s_.-]?               # separator or space
        (\d{4,5})              # last four/five digits
    """,
        re.VERBOSE,
    )  # VERBOSE is used to ignore whitespace and comments inside the regex string

    # Loop through the phone numbers found in the text
    for num in PhnNumregex.findall(text):
        if num[1] != "":
            PhoneNum = "(" + num[1] + ")"  # Add area code in brackets
        else:
            PhoneNum = ""
        PhoneNum += "-".join([num[2], num[3], num[4]])  # Join the digits with dashes
        matches.append(PhoneNum)


def EmailCheck():
    # Regular expression for matching email addresses
    emailCheck = re.compile(
        r"""
        ([a-zA-Z0-9._%-]+        # username
        @                        # @ character
        [a-zA-Z0-9_-]+           # domain name
        \.                       # .(dot)
        [a-zA-Z]{2,3}            # domain type
        (\.[a-zA-Z]{2,3})?)      # second domain type like co.in 
    """,
        re.VERBOSE,
    )

    # Loop through the email addresses found in the text
    for emails in emailCheck.findall(text):
        matches.append(emails[0])


# Print the output from matches list
def PrintMatches():
    if len(matches) > 0:
        print("Found matches: " + str(len(matches)))
        for i in range(0, len(matches)):
            print(matches[i])
    else:
        print("***No Phone Number or Email Address found.***")


def main():
    # Call functions to check for phone numbers and email addresses
    PhoneNumCheck()
    EmailCheck()

    # Print the matches
    PrintMatches()


if __name__ == "__main__":
    main()
