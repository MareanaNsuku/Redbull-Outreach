import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import *

def send_email(to_email, company_name, website):
    if not to_email:
        print(f"No email for {company_name}, skipping.")
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
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                    )
                    msg.attach(part)
            except Exception as e:
                print(f"Failed to attach {filename}: {e}")
        else:
            print(f"Warning: Attachment not found: {filepath}")

    recipients = [to_email, CC_EMAIL] if CC_EMAIL else [to_email]
    # Remove duplicates just in case
    recipients = list(dict.fromkeys(recipients))

    # Try Brevo SMTP
    try:
        with smtplib.SMTP(BREVO_SMTP_HOST, BREVO_SMTP_PORT) as server:
            server.starttls()
            server.login(BREVO_SMTP_USER, BREVO_SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        print(f"Sent via Brevo to {to_email} (CC: {CC_EMAIL})")
        return True
    except Exception as e:
        print(f"Brevo failed: {e}")

    # Fallback to Gmail SMTP
    try:
        with smtplib.SMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        print(f"Sent via Gmail to {to_email} (CC: {CC_EMAIL})")
        return True
    except Exception as e:
        print(f"Gmail failed: {e}")

    return False
