import os

# ---------- Email Credentials (set as GitHub Secrets) ----------
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
BREVO_SMTP_USER = os.environ.get("BREVO_SMTP_USER")
BREVO_SMTP_PASSWORD = os.environ.get("BREVO_SMTP_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

# ---------- SMTP Settings ----------
BREVO_SMTP_HOST = "smtp-relay.brevo.com"
BREVO_SMTP_PORT = 587
GMAIL_SMTP_HOST = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

# ---------- Scraping Settings (Cape Town focused) ----------
SEARCH_QUERIES = [
    "automotive companies Cape Town contact",
    "car dealership Cape Town contact email",
    "delivery companies Cape Town contact",
    "logistics companies Cape Town email",
    "courier services Cape Town contact",
    "courier company Cape Town email",
    "transport and logistics Cape Town contact",
    "vehicle dealership Cape Town contact",
    "automotive repair Cape Town email",
    "auto parts Cape Town contact",
    "freight forwarding Cape Town contact",
    "supply chain logistics Cape Town email",
    "last mile delivery Cape Town contact",
    "trucking companies Cape Town email",
    "fleet management Cape Town contact",
    "car transport Cape Town contact",
    "motorcycle dealer Cape Town email",
    "car rental Cape Town contact",
    "auto body repair Cape Town email",
    "truck dealership Cape Town contact",
    "vehicle logistics Cape Town",
    "moving company Cape Town contact",
    "food delivery Cape Town contact",
    "pharmaceutical logistics Cape Town",
    "warehousing Cape Town contact"
]
MAX_COMPANIES_PER_RUN = 100
REQUEST_TIMEOUT = 15
DELAY_BETWEEN_REQUESTS = 1

# ---------- Output File ----------
CSV_FILE = "companies.csv"

# ---------- Email Template ----------
EMAIL_SUBJECT = "Partnership with Team Kwik Kwik Nawu Nawu – Red Bull Box Cart Race 2026"

EMAIL_BODY = """\
Dear {company_name} team,

We are Team Kwik Kwik Nawu Nawu, selected to compete in the Red Bull Box Cart Race on 4 October 2026 in Sandton. Our cart is a tribute to South Africa's delivery heroes – a stripped-down van with a stopwatch on the roof and a grocery bag riding shotgun, celebrating the everyday drivers who keep our economy moving.

We're reaching out because we believe there is a powerful alignment between {company_name} and our project.

Logistics is the backbone of South Africa, and our cart is a direct tribute to your industry. We want to celebrate the drivers who make it all happen – and we think {company_name} would be the perfect partner to help us bring this story to life in front of thousands of spectators and media.

What we're asking:
- Financial contribution (any amount from R15,000 upwards) to cover materials and safety gear.
- Or in-kind support – workshop space, engineering advice, or materials.

What you get in return:
- Your logo prominently displayed on our cart and team uniforms.
- Social media coverage and visibility on the event's official channels.
- The satisfaction of helping a young South African team compete on a national stage.

We'd love to hop on a quick 10-minute call to explore this further. Please let me know if you're interested – I'm happy to send over our full proposal.

Kind regards,
Katlego Malogadithare
Team Captain, Kwik Kwik Nawu Nawu
📱 060 965 4322
📧 katlegomalogadithare@gmail.com
"""

# ---------- Attachments ----------
ATTACHMENTS = [
    "attachments/RedBull Proposal.pdf",
    "attachments/RBBCR TEAM DETAILS.pdf",
    "attachments/Delivering-More-Than-Packages-Delivering-Innovation.pptx"
]

# ---------- CC Recipient ----------
CC_EMAIL = "katlegomalogadithare@gmail.com"
