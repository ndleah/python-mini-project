import random
import string


def main(length):
    all = []
    # getting all the types of characters from string library
    lower_case = string.ascii_lowercase
    upper_case = string.ascii_uppercase
    numbers = string.digits
    special_chars = string.punctuation
    # putting all characters in one list 'all' using extend function
    all.extend(lower_case)
    all.extend(upper_case)
    all.extend(numbers)
    all.extend(special_chars)

    ran = random.sample(all,length)
    password = "".join(ran)

    return password


if __name__ == "__main__":
    l = int(input("Enter the length of the password you want to use: \n"))
    password = main(l)
    print(password)