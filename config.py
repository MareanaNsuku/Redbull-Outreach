import os

# ---------- Email Credentials (set as GitHub Secrets) ----------
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
BREVO_SMTP_USER = os.environ.get("BREVO_SMTP_USER")
BREVO_SMTP_PASSWORD = os.environ.get("BREVO_SMTP_PASSWORD")
BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

# ---------- SMTP Settings ----------
BREVO_SMTP_HOST = "smtp-relay.brevo.com"
BREVO_SMTP_PORT = 587
GMAIL_SMTP_HOST = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

# ---------- Scraping Settings (Cape Town automotive focus) ----------
SEARCH_QUERIES = [
    # Automotive & Racing (Cape Town focused)
    "motorsport Cape Town",
    "racing team Cape Town",
    "karting Cape Town",
    "go kart Cape Town",
    "car racing sponsorship Cape Town",
    "automotive sponsorship Cape Town",
    "car dealership Cape Town",
    "car dealership Bellville",
    "car dealership Durbanville",
    "car dealership Parow",
    "car dealership Somerset West",
    "car parts Cape Town",
    "performance parts Cape Town",
    "automotive accessories Cape Town",
    "vehicle branding Cape Town",
    "car wrap Cape Town",
    # Logistics & Transport (vehicle-related)
    "vehicle logistics Cape Town",
    "car transport Cape Town",
    "fleet management Cape Town",
    "vehicle tracking Cape Town",
    "courier company Cape Town",
    # Engineering & Workshop
    "engineering company Cape Town",
    "workshop equipment Cape Town",
    "safety gear supplier Cape Town",
    "tool supplier Cape Town",
    "metal fabrication Cape Town",
    # Sports & Sponsorship (motorsport/automotive-related)
    "sports sponsorship Cape Town",
    "motorsport sponsorship Cape Town",
    "event sponsorship Cape Town",
    "sports marketing Cape Town"
]

MAX_COMPANIES_PER_RUN = 50
REQUEST_TIMEOUT = 12
DELAY_BETWEEN_REQUESTS = 3

# ---------- Output File ----------
CSV_FILE = "companies.csv"

# ---------- Email Template ----------
EMAIL_SUBJECT = "Partnership with Team Kwik Kwik Nawu Nawu – Red Bull Box Cart Race 2026"

EMAIL_BODY = """\
Dear {company_name} team,

We are Team Kwik Kwik Nawu Nawu, selected to compete in the Red Bull Box Cart Race 2026 in Sandton, Johannesburg, on 4 October 2026.

We have already purchased our go-kart, and we are excited to share that Takealot has come on board as a partner. Takealot has committed R70,000 towards the project and has also agreed to cover the freight costs to transport the go-kart to Johannesburg.

Our total project budget is approximately R121,000, leaving us with a R51,000 shortfall. We are therefore seeking an additional partner to assist us with the remaining costs, which will be used for additional materials, accommodation, and other necessary race weekend expenses.

Due to the tight deadline leading up to the race, we have also added two additional team members, with approval from Red Bull, to assist with the construction and development of the cart. This additional support will allow us to complete the build within the limited timeframe.

The additional funding would primarily assist with accommodation, meals, extra materials, and other operational costs for our team in Johannesburg.

We have attached the proposal that we presented to Takealot, which provides a detailed overview of the project, our cart concept, the team, and the proposed partnership.

As part of their partnership, Takealot will have their media team involved in capturing photos and video content throughout the build and around race weekend for their social media and marketing platforms. We see this as an excellent opportunity to incorporate {company_name} into this content and provide meaningful brand visibility.

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
    "attachments/RBBCR TEAM DETAILS.pdf"
]

# ---------- CC Recipient ----------
CC_EMAIL = "katlegomalogadithare@gmail.com"

# ---------- Manual Recipients (always emailed) ----------
MANUAL_RECIPIENTS = [
    ("carol@mscsports.co.za", "MSC Sports", "https://mscsports.co.za")
]

# ---------- Seed Companies (empty – use search only) ----------
SEED_COMPANIES = []
