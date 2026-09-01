import sys
from datetime import datetime

def check_pywhatkit():
    try:
        import pywhatkit
        return pywhatkit
    except ImportError:
        print("Error: 'pywhatkit' package is required. Install it via 'pip install pywhatkit'.")
        return None

def validate_phone(phone_number: str) -> bool:
    """Check if phone number starts with + and contains valid digits."""
    cleaned = phone_number.strip()
    return cleaned.startswith("+") and cleaned[1:].isdigit() and len(cleaned) >= 8

def send_instant_message():
    pwk = check_pywhatkit()
    if not pwk:
        return

    phone = input("Enter Phone Number (with +country code, e.g., +1234567890): ").strip()
    if not validate_phone(phone):
        print("Error: Invalid phone number format! Must start with '+' followed by country code and digits.")
        return

    message = input("Enter Message: ").strip()
    if not message:
        print("Error: Message cannot be empty.")
        return

    print("Sending instant message via WhatsApp Web...")
    try:
        pwk.sendwhatmsg_instantly(phone, message, tab_close=True)
        print("Instant message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")

def send_scheduled_message():
    pwk = check_pywhatkit()
    if not pwk:
        return

    phone = input("Enter Phone Number (with +country code, e.g., +1234567890): ").strip()
    if not validate_phone(phone):
        print("Error: Invalid phone number format! Must start with '+' followed by country code and digits.")
        return

    message = input("Enter Message: ").strip()
    if not message:
        print("Error: Message cannot be empty.")
        return

    try:
        hr = int(input("Enter Hour (0-23, 24-hour format): "))
        mins = int(input("Enter Minutes (0-59): "))
        if not (0 <= hr <= 23 and 0 <= mins <= 59):
            print("Error: Invalid hour or minute range.")
            return
    except ValueError:
        print("Error: Hour and minutes must be numbers.")
        return

    print(f"Scheduling WhatsApp message to {phone} at {hr:02d}:{mins:02d}...")
    try:
        pwk.sendwhatmsg(phone, message, hr, mins)
        print("Scheduled message set successfully!")
    except Exception as e:
        print(f"Error scheduling message: {e}")

def convert_image_to_ascii():
    pwk = check_pywhatkit()
    if not pwk:
        return

    img_path = input("Enter path to image file (.jpg / .png): ").strip()
    out_path = input("Enter output ASCII art filename (default: ascii_art): ").strip() or "ascii_art"

    try:
        pwk.image_to_ascii_art(img_path, out_path)
        print(f"ASCII art created successfully at '{out_path}'!")
    except Exception as e:
        print(f"Error converting image: {e}")

def main():
    print("=== WhatsApp Automation Bot ===")
    print("1. Send Instant WhatsApp Message")
    print("2. Schedule WhatsApp Message")
    print("3. Convert Image to ASCII Art")
    print("4. Exit")

    choice = input("Select option (1-4): ").strip()
    if choice == "1":
        send_instant_message()
    elif choice == "2":
        send_scheduled_message()
    elif choice == "3":
        convert_image_to_ascii()
    elif choice == "4":
        print("Exiting WhatsApp Bot.")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()