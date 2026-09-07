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
    "car dealership Goodwood",
    "car dealership Table View",
    "car dealership Milnerton",
    "car dealership Brackenfell",
    "car dealership Kuils River",
    "car dealership Claremont",
    "car dealership Wynberg",
    "used car dealer Cape Town",
    "bakkie dealer Cape Town",
    "truck dealer Cape Town",
    "motorcycle dealer Cape Town",
    "car sales Cape Town",
    "car sales Bellville",
    "car sales Somerset West",
    "car service Cape Town",
    "car service Bellville",
    "car service Durbanville",
    "car service Milnerton",
    "car service Somerset West",
    "tyre fitment Cape Town",
    "tyre fitment Bellville",
    "tyre fitment Parow",
    "wheel alignment Cape Town",
    "suspension specialist Cape Town",
    "brake repair Cape Town",
    "clutch repair Cape Town",
    "gearbox repair Cape Town",
    "engine reconditioning Cape Town",
    "auto electrician Cape Town",
    "auto electrician Bellville",
    "panel beater Cape Town",
    "panel beater Bellville",
    "panel beater Durbanville",
    "auto body repair Cape Town",
    "auto body repair Bellville",
    "car aircon repair Cape Town",
    "car battery Cape Town",
    "car wash Cape Town",
    "auto glass Cape Town",
    "car audio Cape Town",
    "car alarm Cape Town",
    "vehicle tracking Cape Town",
    "car parts Cape Town",
    "car parts Bellville",
    "car parts Parow",
    "auto parts supplier Cape Town",
    "performance parts Cape Town",
    "car accessories Cape Town",
    "vehicle branding Cape Town",
    "vehicle branding Bellville",
    "car wrap Cape Town",
    "car wrap Bellville",
    "car wrap Durbanville",
    "sign writing Cape Town",
    "vehicle graphics Cape Town",
    "vehicle logistics Cape Town",
    "car transport Cape Town",
    "fleet management Cape Town",
    "courier company Cape Town",
    "delivery company Cape Town",
    "engineering company Cape Town",
    "workshop equipment Cape Town",
    "safety gear supplier Cape Town",
    "tool supplier Cape Town",
    "metal fabrication Cape Town",
    "sports sponsorship Cape Town",
    "motorsport sponsorship Cape Town",
    "event sponsorship Cape Town",
    "sports marketing Cape Town",
    "brand sponsorship Cape Town"
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

# ---------- Manual Recipients (empty) ----------
MANUAL_RECIPIENTS = []

# ---------- Seed Companies (fresh local list) ----------
SEED_COMPANIES = [
    "https://www.capetownautoclinic.co.za",
    "https://www.tableviewauto.co.za",
    "https://www.durbanvillecarservice.co.za",
    "https://www.bellvilleautocentre.co.za",
    "https://www.parowmotors.co.za",
    "https://www.milnertonauto.co.za",
    "https://www.brackenfellcarrepair.co.za",
    "https://www.kuilsriverauto.co.za",
    "https://www.claremontcarclinic.co.za",
    "https://www.wynbergauto.co.za",
    "https://www.fishhoekmotors.co.za",
    "https://www.mitchellsplainautos.co.za",
    "https://www.khayelitshacarparts.co.za",
    "https://www.eppingautoelectrical.co.za",
    "https://www.montaguegardensauto.co.za",
    "https://www.goodwoodcarwash.co.za",
    "https://www.somersetwestpanelbeaters.co.za",
    "https://www.stellenboschautobody.co.za",
    "https://www.durbanvilletowing.co.za",
    "https://www.capetownautoglass.co.za",
    "https://www.bellvilletyres.co.za",
    "https://www.parowbrake.co.za",
    "https://www.milnertonbatteries.co.za",
    "https://www.tableviewcarwash.co.za",
    "https://www.brackenfellcaravans.co.za",
    "https://www.kuilsrivertrailers.co.za",
    "https://www.claremontperformance.co.za",
    "https://www.wynbergcarradio.co.za",
    "https://www.fishhoekautoaircon.co.za",
    "https://www.mitchellsplaintyres.co.za"
]
