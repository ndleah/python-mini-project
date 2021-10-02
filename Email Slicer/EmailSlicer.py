email = input("Enter your email id - ")
username = email[0:email.index('@')]
domain = email[email.index('@')+1: ]
print("Username - ", username)
print("Domain - ", domain)
