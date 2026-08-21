import smtplib
from email.mime.text import MIMEText
from config import *

def send_email(to_email, company_name, website):
    if not to_email:
        print(f"No email for {company_name}, skipping.")
        return False

    body = EMAIL_BODY.format(company_name=company_name, website=website)
    msg = MIMEText(body)
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    # Try Brevo SMTP
    try:
        with smtplib.SMTP(BREVO_SMTP_HOST, BREVO_SMTP_PORT) as server:
            server.starttls()
            server.login(BREVO_SMTP_USER, BREVO_SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, [to_email], msg.as_string())
        print(f"Sent via Brevo to {to_email}")
        return True
    except Exception as e:
        print(f"Brevo failed: {e}")

    # Fallback to Gmail SMTP
    try:
        with smtplib.SMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, [to_email], msg.as_string())
        print(f"Sent via Gmail to {to_email}")
        return True
    except Exception as e:
        print(f"Gmail failed: {e}")

    return False
