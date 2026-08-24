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
JUNK_EMAIL_DOMAINS = [
    "influasia.com",
    "sortlist.com",
    "autoyas.com",
    "hellopeter.com",
    "cybo.com",
    "elmejortrato.com",
    "netpages.co.za",
    "panelbeatersdirectory.co.za",
    "towingdirectory.co.za",
    "drivingschoolfinder.co.za",
    "quotesadvisor.com",
    "infoisinfo.co.za",
    "findglocal.com",
    "shopshours.co.za",
    "fyple.co.za",
    "brabys.com",
    "hotfrog.co.za",
    "snupit.co.za",
    "trustlink.co.za",
    "africanadvice.com",
    "d7leadfinder.com",
    "aeroleads.com",
    "lusha.com",
    "contactout.com",
    "dnb.com",
    "goodfirms.co",
    "wordpress.org",
    "outlook.com",
]


# ---------- Global constants ----------
MAX_RETRIES = 2
RETRY_DELAY = 5
DAILY_LIMIT = 450   # maximum emails per run, keeps us under Gmail's daily cap

sent_count = 0

def is_valid_email_format(email):
    """Return True if email looks valid."""
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
    if not re.match(r'^[a-z]{2,4}$', tld):
        return False
    placeholders = ['example', 'test', 'user', 'jane.doe', 'john.doe']
    for ph in placeholders:
        if ph in local:
            return False
    if re.match(r'^\d{2,}', local):
        return False
    if "u003e" in local:
        return False
    if domain in JUNK_EMAIL_DOMAINS:
        return False
    return True

def send_via_gmail_smtp(to_email, company_name, website):
    """Send email using Gmail SMTP."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily limit reached, skipping Gmail.")
        return False

    body = EMAIL_BODY.format(company_name=company_name, website=website)
    msg = MIMEMultipart()
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = SENDER_EMAIL.strip()
    msg["To"] = to_email
    msg["Cc"] = CC_EMAIL.strip()
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

    recipients = [to_email, CC_EMAIL.strip()] if CC_EMAIL else [to_email]
    recipients = list(dict.fromkeys(recipients))

    for attempt in range(MAX_RETRIES):
        try:
            with smtplib.SMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT, timeout=30) as server:
                server.starttls()
                server.login(SENDER_EMAIL.strip(), GMAIL_APP_PASSWORD.strip())
                server.sendmail(SENDER_EMAIL.strip(), recipients, msg.as_string())
            print(f"  Sent via Gmail to {to_email}")
            sent_count += 1
            return True
        except Exception as e:
            print(f"  Gmail attempt {attempt+1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return False

def send_via_brevo_api(to_email, company_name, website):
    """Send email using Brevo HTTP API (fallback)."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily limit reached, skipping Brevo API.")
        return False

    body = EMAIL_BODY.format(company_name=company_name, website=website)
    api_key = os.environ.get("BREVO_API_KEY", "").strip()
    sender_email = SENDER_EMAIL.strip()
    cc_email = CC_EMAIL.strip()

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
    if not api_key:
        print("  Brevo API key missing, skipping.")
        return False

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

def send_email(to_email, company_name, website):
    """Send email with Gmail first, Brevo API fallback."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily email limit reached, skipping.")
        return "Limit reached"

    if not to_email or not isinstance(to_email, str) or to_email.strip() == "" or not is_valid_email_format(to_email):
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
