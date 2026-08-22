import smtplib
import time
import requests
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import *

MAX_RETRIES = 2
RETRY_DELAY = 5
DAILY_LIMIT = 450  # keep below Gmail's daily cap

sent_count = 0

def send_via_gmail_smtp(to_email, company_name, website):
    """Send email using Gmail SMTP."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily limit reached, skipping Gmail.")
        return False

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
                    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
                    msg.attach(part)
            except Exception as e:
                print(f"  Failed to attach {filename}: {e}")

    recipients = [to_email, CC_EMAIL] if CC_EMAIL else [to_email]
    recipients = list(dict.fromkeys(recipients))

    for attempt in range(MAX_RETRIES):
        try:
            with smtplib.SMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT, timeout=30) as server:
                server.starttls()
                server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
                server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
            print(f"  Sent via Gmail to {to_email}")
            sent_count += 1
            return True
        except Exception as e:
            print(f"  Gmail attempt {attempt+1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return False

def send_via_brevo_api(to_email, company_name, website):
    """Send email using Brevo HTTP API (not IP-restricted)."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily limit reached, skipping Brevo API.")
        return False

    body = EMAIL_BODY.format(company_name=company_name, website=website)
    data = {
        "sender": {"email": SENDER_EMAIL},
        "to": [{"email": to_email}],
        "cc": [{"email": CC_EMAIL}] if CC_EMAIL else [],
        "subject": EMAIL_SUBJECT,
        "htmlContent": body.replace("\n", "<br>")
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": os.environ.get("BREVO_API_KEY", "")
    }
    if not headers["api-key"]:
        print("  Brevo API key missing, skipping Brevo API.")
        return False

    try:
        response = requests.post("https://api.brevo.com/v3/smtp/email", json=data, headers=headers, timeout=30)
        if response.status_code in [200, 201, 202]:
            print(f"  Sent via Brevo API to {to_email}")
            sent_count += 1
            return True
        else:
            print(f"  Brevo API failed: {response.status_code} {response.text}")
            return False
    except Exception as e:
        print(f"  Brevo API error: {e}")
        return False

def send_email(to_email, company_name, website):
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily email limit reached, skipping.")
        return "Limit reached"

    if not to_email or not isinstance(to_email, str) or to_email.strip() == "":
        print(f"No valid email for {company_name}, skipping.")
        return "No email"

    to_email = to_email.strip()
    print(f"  Trying Gmail first for {to_email}...")
    if send_via_gmail_smtp(to_email, company_name, website):
        return "Sent"

    print(f"  Gmail failed, falling back to Brevo API for {to_email}...")
    if send_via_brevo_api(to_email, company_name, website):
        return "Sent"

    print(f"  All providers failed for {to_email}")
    return "Failed"
