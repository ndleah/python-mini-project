import os
import sys
import json
import re
import requests
import subprocess
import platform

def print_banner(text: str):
    """Print ASCII banner using pyfiglet or simple fallback."""
    try:
        import pyfiglet
        print(pyfiglet.figlet_format(text))
    except Exception:
        print(f"\n=== {text} ===\n")

def clear_screen():
    """Clear terminal screen cross-platform."""
    cmd = "cls" if platform.system().lower() == 'windows' else "clear"
    try:
        subprocess.call(cmd, shell=True)
    except Exception:
        pass

def locate_ip(ip_address: str = None) -> dict:
    """Locate an IP address using ip-api.com and save data to files."""
    clear_screen()
    print_banner("IP LOCATER")

    IP_PATTERN = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

    if ip_address is None:
        while True:
            ip_address = input("\nEnter a valid IP address (or 'q' to quit): ").strip()
            if ip_address.lower() == 'q':
                return None
            if not re.match(IP_PATTERN, ip_address):
                print("Invalid IP address format. Example: 8.8.8.8")
            else:
                break

    script_dir = os.path.dirname(__file__)
    filename_json = os.path.join(script_dir, "ip_data.json")
    filename_text = os.path.join(script_dir, "ip_data.txt")

    fields = "status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,currency,isp,org,as,mobile,proxy,hosting,query"
    url = f"http://ip-api.com/json/{ip_address}?fields={fields}"

    print(f"Fetching IP data for '{ip_address}'...")
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        with open(filename_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        with open(filename_text, 'w', encoding='utf-8') as f:
            f.write(response.text)

        print(f"Success! Data saved to:\n  JSON: {filename_json}\n  Text: {filename_text}")
        print(f"Country: {data.get('country')}, City: {data.get('city')}, ISP: {data.get('isp')}")
        return data
    except Exception as e:
        print(f"Error querying IP location API: {e}")
        return None

def get_ip(domain_name: str = None):
    """Get IP of a domain name using nslookup."""
    clear_screen()
    print_banner("IP FINDER")

    if domain_name is None:
        domain_name = input("Enter a domain name (e.g. google.com or 'q' to quit): ").strip()

    if domain_name.lower() == 'q':
        return

    print(f"Looking up IP for domain '{domain_name}'...")
    try:
        command = f"nslookup {domain_name}"
        subprocess.call(command, shell=True)
    except Exception as e:
        print(f"Error running nslookup: {e}")

