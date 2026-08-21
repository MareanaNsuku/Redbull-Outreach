import smtplib
import time
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import *

MAX_RETRIES = 2
RETRY_DELAY = 5  # seconds

def send_via_smtp(host, port, user, password, sender, recipients, msg):
    for attempt in range(MAX_RETRIES):
        try:
            with smtplib.SMTP(host, port, timeout=30) as server:
                server.starttls()
                server.login(user, password)
                server.sendmail(sender, recipients, msg.as_string())
            return True, "sent"
        except Exception as e:
            print(f"  Attempt {attempt+1} via {host} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return False, "failed"

def send_email(to_email, company_name, website):
    if not to_email or not isinstance(to_email, str) or to_email.strip() == "":
        print(f"No valid email for {company_name}, skipping.")
        return "No email"

    to_email = to_email.strip()
    body = EMAIL_BODY.format(company_name=company_name, website=website)

    msg = MIMEMultipart()
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Cc"] = CC_EMAIL
    msg["X-Priority"] = "1"
    msg["Importance"] = "High"

    msg.attach(MIMEText(body, "plain"))

    for filepath in ATTACHMENTS:
        if os.path.exists(filepath):
            filename = os.path.basename(filepath)
            try:
                with open(filepath, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                    )
                    msg.attach(part)
            except Exception as e:
                print(f"  Failed to attach {filename}: {e}")
        else:
            print(f"  Warning: Attachment not found: {filepath}")

    recipients = [to_email, CC_EMAIL] if CC_EMAIL else [to_email]
    recipients = list(dict.fromkeys(recipients))

    providers = [
        ("Brevo", BREVO_SMTP_HOST, BREVO_SMTP_PORT, BREVO_SMTP_USER, BREVO_SMTP_PASSWORD),
        ("Gmail", GMAIL_SMTP_HOST, GMAIL_SMTP_PORT, SENDER_EMAIL, GMAIL_APP_PASSWORD),
    ]

    for name, host, port, user, pwd in providers:
        if not user or not pwd:
            print(f"  {name} credentials missing, skipping.")
            continue
        print(f"  Trying {name}...")
        success, _ = send_via_smtp(host, port, user, pwd, SENDER_EMAIL, recipients, msg)
        if success:
            print(f"  Sent via {name} to {to_email} (CC: {CC_EMAIL})")
            return "Sent"
        else:
            print(f"  {name} failed.")

    print(f"  All providers failed for {to_email}")
    return "Failed"
