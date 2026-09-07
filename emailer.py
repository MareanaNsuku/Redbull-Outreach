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
DAILY_LIMIT = 100

sent_count = 0

# Load bounced domains list once at module load
BOUNCE_FILE = "bounced_domains.txt"
bounced_domains = set()
if os.path.exists(BOUNCE_FILE):
    with open(BOUNCE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                bounced_domains.add(line.lower())

def is_bounced_domain(domain):
    """Return True if domain is in bounce blocklist."""
    return domain.lower() in bounced_domains

def add_to_bounce_list(domain):
    """Add a domain to the permanent bounce list and save to file."""
    domain = domain.lower()
    if domain and domain not in bounced_domains:
        bounced_domains.add(domain)
        with open(BOUNCE_FILE, "a") as f:
            f.write(domain + "\n")
        print(f"  Added {domain} to bounce blocklist.")

def is_valid_email_format(email):
    """Strict email validation."""
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
    """Send via Brevo API. Returns (success, bounce_domain or None)."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily limit reached, skipping Brevo API.")
        return False, None

    api_key = os.environ.get("BREVO_API_KEY", "").strip()
    sender_email = SENDER_EMAIL.strip()
    cc_email = CC_EMAIL.strip()
    if not api_key:
        print("  Brevo API key missing, skipping Brevo.")
        return False, None

    body = EMAIL_BODY.format(company_name=company_name, website=website)
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
            response = requests.post("https://api.brevo.com/v3/smtp/email", json=data, headers=headers, timeout=30)
            if response.status_code in [200, 201, 202]:
                print(f"  Sent via Brevo API to {to_email}")
                sent_count += 1
                return True, None
            elif response.status_code == 400:
                # Often invalid recipient or sender; detect if recipient domain bad
                try:
                    err = response.json()
                    if "invalid" in str(err).lower() or "recipient" in str(err).lower():
                        domain = to_email.split("@")[-1]
                        return False, domain
                except:
                    pass
                print(f"  Brevo API attempt {attempt+1} failed: {response.status_code} {response.text}")
            else:
                print(f"  Brevo API attempt {attempt+1} failed: {response.status_code} {response.text}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"  Brevo API attempt {attempt+1} error: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return False, None

def send_via_gmail_smtp(to_email, company_name, website):
    """Send via Gmail SMTP. Returns (success, bounce_domain or None)."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily limit reached, skipping Gmail.")
        return False, None

    app_password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    sender_email = SENDER_EMAIL.strip()
    cc_email = CC_EMAIL.strip()
    if not app_password:
        print("  Gmail app password missing, skipping Gmail fallback.")
        return False, None

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
            return True, None
        except smtplib.SMTPRecipientsRefused as e:
            # Permanent recipient error -> bounce
            print(f"  Gmail recipient refused: {e}")
            domain = to_email.split("@")[-1]
            return False, domain
        except smtplib.SMTPResponseException as e:
            if e.smtp_code >= 500:
                print(f"  Gmail permanent error: {e}")
                domain = to_email.split("@")[-1]
                return False, domain
            else:
                print(f"  Gmail attempt {attempt+1} failed: {e}")
        except Exception as e:
            print(f"  Gmail attempt {attempt+1} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
    return False, None

def send_email(to_email, company_name, website):
    """Main send function: Brevo first, Gmail fallback. Returns status."""
    global sent_count
    if sent_count >= DAILY_LIMIT:
        print("  Daily email limit reached, skipping.")
        return "Limit reached"

    if not is_valid_email_format(to_email):
        print(f"  Invalid email format: {to_email}, skipping.")
        return "Invalid"

    to_email = to_email.strip()
    domain = to_email.split("@")[-1].lower()
    if is_bounced_domain(domain):
        print(f"  Skipping bounced domain: {domain}")
        return "Bounced"

    print(f"  Attempting to send to {to_email}...")

    # Try Brevo first
    print("  Trying Brevo API...")
    success, bounce = send_via_brevo_api(to_email, company_name, website)
    if success:
        return "Sent"
    if bounce:
        add_to_bounce_list(bounce)
        return "Bounced"

    # Fallback to Gmail
    print("  Brevo failed, falling back to Gmail...")
    success, bounce = send_via_gmail_smtp(to_email, company_name, website)
    if success:
        return "Sent"
    if bounce:
        add_to_bounce_list(bounce)
        return "Bounced"

    print(f"  All providers failed for {to_email}")
    return "Failed"
