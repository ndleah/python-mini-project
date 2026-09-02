import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_batch_emails(
    csv_path: str = None,
    sender_email: str = None,
    sender_password: str = None,
    smtp_host: str = "smtp.gmail.com",
    smtp_port: int = 587,
    dry_run: bool = False
) -> int:
    """Send batch emails efficiently reusing a single SMTP connection."""
    script_dir = os.path.dirname(__file__)
    if csv_path is None:
        csv_path = os.path.join(script_dir, "abc.csv")

    if not os.path.exists(csv_path):
        print(f"Notice: CSV dataset not found at '{csv_path}'. Running in simulation mode.")
        recipients = [("Alice", "alice@example.com"), ("Bob", "bob@example.com")]
    else:
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            recipients = list(zip(df['name'].tolist(), df['email'].tolist()))
        except Exception as e:
            print(f"Error reading CSV '{csv_path}': {e}")
            return 0

    sender_email = sender_email or os.environ.get("SMTP_EMAIL", "sender@example.com")
    sender_password = sender_password or os.environ.get("SMTP_PASSWORD", "")

    if dry_run or not sender_password:
        print(f"\n[DRY RUN] Simulating batch email delivery to {len(recipients)} recipient(s)...")
        for name, to_addr in recipients:
            print(f"  • Simulated email to {name} <{to_addr}> from {sender_email}")
        return len(recipients)

    try:
        import smtplib
        print(f"Connecting to SMTP server {smtp_host}:{smtp_port}...")
        mail_server = smtplib.SMTP(smtp_host, smtp_port)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.login(sender_email, sender_password)

        sent_count = 0
        for name, to_addr in recipients:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_addr
            msg['Subject'] = 'Automated Notification'

            body = f"Hello {name},\n\nThis is an automated notification message.\n\nBest regards,\nAutomated System"
            msg.attach(MIMEText(body, 'plain'))

            mail_server.sendmail(sender_email, to_addr, msg.as_string())
            sent_count += 1
            print(f"✅ Email sent successfully to {name} <{to_addr}>")

        mail_server.quit()
        return sent_count
    except Exception as e:
        print(f"Error during SMTP email delivery: {e}")
        return 0

def main():
    dry_mode = "--dry-run" in sys.argv or True
    send_batch_emails(dry_run=dry_mode)

if __name__ == '__main__':
    main()