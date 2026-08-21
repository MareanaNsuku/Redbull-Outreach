import os

# ---------- Email Credentials (set as GitHub Secrets) ----------
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
BREVO_SMTP_USER = os.environ.get("BREVO_SMTP_USER")
BREVO_SMTP_PASSWORD = os.environ.get("BREVO_SMTP_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")   # e.g., yourgmail@gmail.com or your Brevo verified sender

# ---------- SMTP Settings ----------
BREVO_SMTP_HOST = "smtp-relay.brevo.com"
BREVO_SMTP_PORT = 587
GMAIL_SMTP_HOST = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

# ---------- Scraping Settings ----------
SEARCH_QUERIES = [
    "automotive companies South Africa contact",
    "car dealership South Africa contact email",
    "delivery companies South Africa contact",
    "logistics companies South Africa email",
    "courier services South Africa contact"
]
MAX_COMPANIES_PER_RUN = 20
REQUEST_TIMEOUT = 15
DELAY_BETWEEN_REQUESTS = 2

# ---------- Output File ----------
CSV_FILE = "companies.csv"

# ---------- Email Template ----------
EMAIL_SUBJECT = "Partnership Opportunity with [Your Brand]"

EMAIL_BODY = """\
Dear {company_name} team,

I hope this message finds you well.

We are reaching out to introduce a potential partnership opportunity that could benefit both {company_name} and our organisation.

We specialise in [brief description of your product/service]. We believe a collaboration with {company_name} would create mutual value.

Would you be open to a short call to discuss this further?

Looking forward to hearing from you.

Best regards,
[Your Name]
[Your Title]
[Your Website]
"""

# ---------- Attachments ----------
ATTACHMENTS = [
    "attachments/RedBull Proposal.pdf",
    "attachments/RBBCR TEAM DETAILS.pdf",
    "attachments/Delivering-More-Than-Packages-Delivering-Innovation.pptx"
]
