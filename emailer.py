import smtplib
import time
import requests
import os
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import *

# ---------- Global constants ----------
MAX_RETRIES = 3
RETRY_DELAY = 10
DAILY_LIMIT = 100   # safe limit for Brevo free tier / Gmail

sent_count = 0

def is_valid_email_format(email):
    """Return True if email looks valid and unlikely to bounce."""
    if not email or not isinstance(email, str):
        return False
    email = email.strip().lower()
    if ' ' in email or email.count('@') != 1:
        return False
    local, domain = email.split('@')
    if not local or not domain or '.' not in domain:
        return False
    if '%' in email:
        return False
    tld = domain.split('.')[-1]
    if not re.match(r'^[a-z]{2,10}$', tld):
        return False
    # Reject placeholder common junk
    placeholders = ['example', 'test', 'user', 'jane.doe', 'john.doe', 'info', 'support', 'contact', 'admin']
    if local in placeholders:
        return False
    if re.match(r'^\d{2,}', local) or len(re.findall(r'\d', local)) > 3:
        return False
    suspicious = ['wixsite', 'wordpress', 'weebly', 'blogspot', 'tumblr', 'site123', 'webnode']
    for kw in suspicious:
        if kw in domain or kw in local:
            return False
    return True

def send_via_brevo_api(to_email, company_name, website):
    """Send email via Brevo HTTP API. Returns True on success."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily limit reached, skipping Brevo API.")
        return False

    body = EMAIL_BODY.format(company_name=company_name, website=website)
    api_key = os.environ.get("BREVO_API_KEY", "").strip()
    sender_email = SENDER_EMAIL.strip()
    cc_email = CC_EMAIL.strip()

    if not api_key:
        print("  Brevo API key missing, skipping Brevo.")
        return False

    data = {
        "sender": {"email": sender_email},
        "to": [{"email": to_email}],
        "cc": [{"email": cc_email}] if cc_email else [],
        "subject": EMAIL_SUBJECT,
        "htmlContent": body.replace("\n", "<br>")
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(
                "https://api.brevo.com/v3/smtp/email",
                json=data,
                headers=headers,
                timeout=30
            )
            if response.status_code in [200, 201, 202]:
                print(f"  Sent via Brevo API to {to_email}")
                sent_count += 1
                return True
            else:
                print(f"  Brevo API attempt {attempt+1} failed: {response.status_code} {response.text}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"  Brevo API attempt {attempt+1} error: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return False

def send_via_gmail_smtp(to_email, company_name, website):
    """Send email via Gmail SMTP. Only called if credentials are present."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily limit reached, skipping Gmail.")
        return False

    app_password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    sender_email = SENDER_EMAIL.strip()
    cc_email = CC_EMAIL.strip()

    if not app_password:
        print("  Gmail app password missing, skipping Gmail fallback.")
        return False

    body = EMAIL_BODY.format(company_name=company_name, website=website)
    msg = MIMEMultipart()
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = sender_email
    msg["To"] = to_email
    if cc_email:
        msg["Cc"] = cc_email
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

    recipients = [to_email, cc_email] if cc_email else [to_email]
    recipients = list(dict.fromkeys(recipients))

    for attempt in range(MAX_RETRIES):
        try:
            with smtplib.SMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT, timeout=30) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, recipients, msg.as_string())
            print(f"  Sent via Gmail to {to_email}")
            sent_count += 1
            return True
        except Exception as e:
            print(f"  Gmail attempt {attempt+1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return False

def send_email(to_email, company_name, website):
    """Main send function: Brevo first, then Gmail fallback if needed."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily email limit reached, skipping.")
        return "Limit reached"

    if not is_valid_email_format(to_email):
        print(f"  Invalid email format: {to_email}, skipping.")
        return "Invalid"

    to_email = to_email.strip()
    print(f"  Attempting to send to {to_email}...")

    # Try Brevo API first
    print("  Trying Brevo API...")
    if send_via_brevo_api(to_email, company_name, website):
        return "Sent"

    # Fallback to Gmail SMTP if Brevo fails
    print("  Brevo failed, falling back to Gmail...")
    if send_via_gmail_smtp(to_email, company_name, website):
        return "Sent"

    print(f"  All providers failed for {to_email}")
    return "Failed"
