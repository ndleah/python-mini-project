import os
import sys
import imaplib
import email
from email.header import decode_header

def decode_mime_header(header_value: str) -> str:
    """Decode MIME encoded email subject headers."""
    if not header_value:
        return "(No Subject)"
    decoded_fragments = decode_header(header_value)
    subject_parts = []
    for bytes_or_str, encoding in decoded_fragments:
        if isinstance(bytes_or_str, bytes):
            subject_parts.append(bytes_or_str.decode(encoding or 'utf-8', errors='replace'))
        else:
            subject_parts.append(str(bytes_or_str))
    return "".join(subject_parts)

def fetch_latest_email_subject(mail, sender_address: str) -> str:
    """Search inbox for latest email from sender_address and return decoded Subject header."""
    sender_address = sender_address.strip()
    status, data = mail.search(None, f'(FROM "{sender_address}")')

    if status != 'OK' or not data or not data[0]:
        print(f"No emails found from: {sender_address}")
        return None

    id_list = data[0].split()
    latest_email_id = id_list[-1]

    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    if status != 'OK' or not msg_data:
        print(f"Failed to fetch email ID {latest_email_id}")
        return None

    raw_email_bytes = msg_data[0][1]
    msg = email.message_from_bytes(raw_email_bytes)
    raw_subject = msg.get('Subject')
    decoded_subject = decode_mime_header(raw_subject)

    print(f"------- FROM: {sender_address} -------")
    print(f"Latest Subject: {decoded_subject}\n")
    return decoded_subject

def check_emails(user: str = None, password: str = None, list_of_mails: list = None):
    """Connect to IMAP server and fetch latest email subjects from given addresses."""
    if not user:
        user = os.getenv("IMAP_USER", "user@gmail.com")
    if not password:
        password = os.getenv("IMAP_PASSWORD", "password")
    if list_of_mails is None:
        list_of_mails = ["example1@gmail.com", "example2@gmail.com"]

    if user in ("Your Gamil address", "user@gmail.com") or password in ("Your password", "password"):
        print("Notice: Dummy credentials configured. Set IMAP_USER and IMAP_PASSWORD environment variables or arguments.")
        return

    print(f"Connecting to IMAP server (imap.gmail.com) for '{user}'...")
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(user, password)
        mail.select("inbox")

        for addr in list_of_mails:
            fetch_latest_email_subject(mail, addr)

        mail.logout()
    except Exception as e:
        print(f"IMAP Connection / Authentication error: {e}")

def main():
    target_user = sys.argv[1] if len(sys.argv) > 1 else None
    target_pass = sys.argv[2] if len(sys.argv) > 2 else None
    check_emails(target_user, target_pass)

if __name__ == '__main__':
    main()