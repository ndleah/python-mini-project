def addressVal(address:str)-> str:
    """
    Takes an Email address string returning a valid or inavlid string output.

    Args:
        address: Email Address string
    """
    dot = address.find(".")
    at = address.find("@")
    if (dot < 0) and (at != 1): # An email address can have more than one (.) but only one (@)
        return f"Invalid Email Address: {address}"
    return f"Valid Email Address: {address}"
    

print("This program checks whether an Email Address is valid.")
while True:
    
    email = str(input("Please Enter An Email Address or (q) to quit: ")).strip()
    if email.lower() == "q":
        print("Exiting...")
        break
    addressVal(email)
"""
NOTE: This a beginner -- beginner email validator A more robust/ complex validator would use tools like
regex(re) to fine tune the validation process further.

Beginner: You colud Also check if the inputed email has upper case or lower case as a validator factor.
"""
