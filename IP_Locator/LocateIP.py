# Import necessary modules
import subprocess
import platform
import requests
import pyfiglet
import json
import os
import re


def locate_ip():
    """
    Locate an IP address using an API.
    """
    # Clear the terminal
    if platform.system().lower() == 'windows':
        command = "cls"
    else:
        command = "clear"
    subprocess.call(command, shell=True)

    # Banner of the tool.
    banner = pyfiglet.figlet_format("IP LOCATER")
    print(banner)

    # A pattern to validate an IP address
    IP_PATTERN = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

    # Get the IP address.
    # if it matches the IP pattern, then it is valid.
    # If not, raise an error message and try again.
    while True:
        IP_address = input("\nEnter a valid IP address: ")
        if IP_address.lower() == 'q':
            quit()
        if not re.match(IP_PATTERN, IP_address):
            print("Invalid IP address.")
        else:
            break

    # Change the current working directory to system's desktop
    os.chdir(rf"C:\Users\{os.getlogin()}\Desktop")

    # Files to save IP data
    filename_json = "ip_data.json"
    filename_text = "ip_data.txt"

    # The files containing IP data will have these fields
    fields = "status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,currency,isp,org,as,mobile,proxy,hosting,query"
    
    # Send a request to the API
    url = f"http://ip-api.com/json/{IP_address}?fields={fields}"
    response = requests.get(url)

    # Write the extracted data to files
    with open(filename_json, 'w') as ip_data_file_json:
        json.dump(response.json(), ip_data_file_json, indent=4)
    
    with open(filename_text, 'w') as ip_data_file_text:
        ip_data_file_text.write(response.text)
    
    # Let the user know that files created on the system's desktop.
    print("You got the files containing data about the given IP address.")
    print("Please check your system desktop.")
    input("\nPress any key to continue...")

def get_ip():
    """
    Get the IP of a certain domain name.
    """
    # Clear the terminal
    if platform.system().lower() == 'windows':
        command = "cls"
    else:
        command = "clear"
    subprocess.call(command, shell=True)
    
    # Banner of the tool.
    banner = pyfiglet.figlet_format("IP FINDER")
    print(banner)

    # Get the domain name
    domain_name = input("Enter a domain name: ")
    
    if domain_name.lower() == 'q':
        quit()
    else:
        command = f"nslookup {domain_name}"
    
    subprocess.call(command) == 0
    input("\nPress any key to continue...")
