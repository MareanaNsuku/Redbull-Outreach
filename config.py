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

# ---------- Scraping Settings ----------
SEARCH_QUERIES = [
    # Automotive Dealerships & Sales
    "car dealership Cape Town",
    "car dealership Bellville",
    "car dealership Parow",
    "car dealership Durbanville",
    "used car dealer Cape Town",
    "used car dealer Bellville",
    "bakkie dealer Cape Town",
    "truck dealer Cape Town",
    "motorcycle dealer Cape Town",
    "car sales Cape Town",
    "car sales Bellville",
    "car sales Somerset West",
    "car sales Stellenbosch",
    "car sales Brackenfell",
    # Car Services & Maintenance
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
    # Car Parts & Accessories
    "car parts Cape Town",
    "car parts Bellville",
    "car parts Parow",
    "auto parts supplier Cape Town",
    "performance parts Cape Town",
    "car accessories Cape Town",
    "car audio Cape Town",
    "car audio Bellville",
    "car alarm Cape Town",
    "car tracking Cape Town",
    "car tracking Bellville",
    # Vehicle Branding & Wraps
    "vehicle branding Cape Town",
    "vehicle branding Bellville",
    "car wrap Cape Town",
    "car wrap Bellville",
    "car wrap Durbanville",
    "sign writing Cape Town",
    "vehicle graphics Cape Town",
    # Logistics & Transport
    "logistics company Cape Town",
    "logistics company Bellville",
    "courier company Cape Town",
    "courier company Bellville",
    "delivery company Cape Town",
    "trucking company Cape Town",
    "fleet management Cape Town",
    "vehicle logistics Cape Town",
    "car transport Cape Town",
    "car carrier Cape Town",
    # Motorsport & Driving
    "motorsport Cape Town",
    "racing team Cape Town",
    "karting track Cape Town",
    "karting track Bellville",
    "driving school Cape Town",
    "driving school Bellville",
    "driving school Durbanville",
    "car club Cape Town",
    "car club Bellville",
    "motorsport club Cape Town",
    # Sports & Sponsorship
    "sports marketing agency Cape Town",
    "sports sponsorship Cape Town",
    "event sponsorship Cape Town",
    "sports sponsorship Bellville",
    # Workshop & Safety
    "workshop equipment supplier Cape Town",
    "workshop equipment supplier Bellville",
    "safety gear supplier Cape Town",
    "safety gear supplier Bellville",
    "tool supplier Cape Town",
    "tool supplier Bellville",
    # Additional Cape Town suburbs
    "car dealership Goodwood",
    "car dealership Table View",
    "car dealership Milnerton",
    "car dealership Brackenfell",
    "car dealership Kuils River",
    "car dealership Claremont",
    "car dealership Wynberg"
]

MAX_COMPANIES_PER_RUN = 120
REQUEST_TIMEOUT = 12
DELAY_BETWEEN_REQUESTS = 3

# ---------- Output File ----------
CSV_FILE = "companies.csv"

# ---------- Email Template ----------
EMAIL_SUBJECT = "Partnership with Team Kwik Kwik Nawu Nawu – Red Bull Box Cart Race 2026"

EMAIL_BODY = """\
Dear {company_name} team,

We are Team Kwik Kwik Nawu Nawu, selected to compete in the Red Bull Box Cart Race 2026 in Sandton, Johannesburg, on 4 October 2026.

We currently have a partnership in place with Takealot, who have committed R70,000 towards the project. This funding will primarily cover the materials, components, and tools required to design and build our cart.

Our total project budget is approximately R121,000, leaving us with a R51,000 shortfall. We are therefore seeking an additional partner to assist us with the remaining project and logistical costs.

Due to the tight deadline leading up to the race, we have also added two additional team members, with approval from Red Bull, to assist with the construction and development of the cart. This additional support will allow us to complete the build within the limited timeframe.

The additional funding would primarily assist with the logistics of getting our team and cart from Cape Town to Johannesburg/Sandton for the race weekend, including transportation, accommodation, meals, and other operational costs.

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
    "attachments/RBBCR TEAM DETAILS.pdf",
]

# ---------- CC Recipient ----------
CC_EMAIL = "katlegomalogadithare@gmail.com"

# ---------- Seed Companies ----------
SEED_COMPANIES = [
    "https://www.cars.co.za",
    "https://www.autotrader.co.za",
    "https://www.motus.co.za",
    "https://www.barloworld.com",
    "https://www.imperial.co.za",
    "https://www.supaquick.com",
    "https://www.hiq.co.za",
    "https://www.bestdrive.co.za",
    "https://www.twt.co.za",
    "https://www.netstar.co.za",
    "https://www.tracker.co.za",
    "https://www.cartrack.co.za",
    "https://www.cds.co.za",
    "https://www.fastway.co.za",
    "https://www.thecourierguy.co.za",
    "https://www.dawnwing.co.za",
    "https://www.dpd.com/za",
    "https://www.dsv.com/en-za",
    "https://www.dhl.com/za-en",
    "https://www.bidvest.co.za",
    "https://collivery.net",
    "https://www.bex.co.za",
    "https://www.aerospeed.co.za",
    "https://www.citisprint.co.za",
    "https://www.intertown.co.za",
    "https://www.kempston.co.za",
    "https://www.millstockcars.co.za",
    "https://www.avautos.co.za",
    "https://www.pioneerfreight.co.za",
    "https://www.liebenlogistics.co.za",
    "https://www.sekologistics.com",
    "https://www.gracecouriers.co.za",
    "https://www.tlc-logistics.co.za",
    "https://www.ontrackautoservices.co.za",
    "https://www.smikemotors.co.za",
    "https://www.automotivex.co.za"
]

# ---------- Manual Recipients (always emailed) ----------
MANUAL_RECIPIENTS = [
    ("carol@mscsports.co.za", "MSC Sports", "https://mscsports.co.za")
]
