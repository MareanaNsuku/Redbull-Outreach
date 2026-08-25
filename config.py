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

# ---------- Scraping Settings (Cape Town focused, NO food/beverage) ----------
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
]
MAX_COMPANIES_PER_RUN = 400
REQUEST_TIMEOUT = 10
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

# ---------- Seed Companies (optional) ----------
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
