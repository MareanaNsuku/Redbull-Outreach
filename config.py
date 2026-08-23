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
    # Automotive Dealerships & Services
    "automotive companies Cape Town contact",
    "car dealership Cape Town contact email",
    "vehicle dealership Cape Town contact",
    "truck dealership Cape Town contact",
    "car rental agency Cape Town contact",
    "car service Cape Town contact",
    "tyre fitment Cape Town contact",
    "car audio Cape Town",
    "car accessories Cape Town",
    "car wash Cape Town contact",
    "auto glass Cape Town",
    "vehicle tracking Cape Town",
    "automotive finance Cape Town",
    "automotive insurance Cape Town",
    "car recovery Cape Town",
    "towing company Cape Town",
    "panel beater Cape Town",
    "auto electrician Cape Town",
    "engine rebuild Cape Town",
    "gearbox repair Cape Town",
    "suspension specialist Cape Town",
    # Logistics & Transport (vehicle-related)
    "delivery companies Cape Town contact",
    "logistics companies Cape Town email",
    "courier services Cape Town contact",
    "transport and logistics Cape Town contact",
    "vehicle logistics Cape Town",
    "fleet management Cape Town contact",
    "trucking company Cape Town contact",
    # Motorsport & Driving
    "motorsport companies Cape Town contact",
    "motorsport team Cape Town",
    "racing team Cape Town contact",
    "karting track Cape Town",
    "driving school Cape Town contact",
    "car club Cape Town contact",
    # Vehicle Customisation & Maintenance
    "vehicle branding Cape Town",
    "car wrap Cape Town contact",
    "automotive parts supplier Cape Town",
    "auto body repair Cape Town email",
    "workshop equipment supplier Cape Town",
    "safety gear supplier Cape Town",
    # Sports & Sponsorship
    "sports marketing agency Cape Town",
    "sports sponsorship Cape Town",
    "event sponsorship Cape Town"
]
MAX_COMPANIES_PER_RUN = 100
# ---------- Seed Companies (known Cape Town companies) ----------
SEED_COMPANIES = [
    "https://collivery.net",
    "https://www.bex.co.za",
    "https://www.fastway.co.za",
    "https://truckport.co.za",
    "https://www.milnertonnissan.co.za",
    "https://urgentgocourier.co.za",
    "https://www.motusselect.co.za",
    "https://gracecouriers.co.za",
    "https://www.sekologistics.com",
    "https://salogistics.co.za",
    "https://www.starwheelsct.co.za",
    "https://thecourierguy.co.za",
    "https://www.intertown.co.za",
    "https://www.citisprint.co.za",
    "https://kempston.co.za",
    "https://www.avautos.co.za",
    "https://millstockcars.co.za",
    "https://www.aerospeed.co.za",
    "https://nwlogistics.co.za",
    "https://www.pioneerfreight.co.za",
    "https://liebenlogistics.co.za",
    "https://ontrackautoservices.co.za",
    "https://smikemotors.co.za",
    "https://automotivedynamix.co.za",
    "https://synergyhaulage.co.za",
    "https://tlc-logistics.co.za",
    "https://koreanboyz.co.za",
    "https://lastmilefast.co.za",
    "https://www.shipchain-sa.com",
    "https://racingtechnik.com",
    "https://www.citisprint.co.za",
    "https://kesselmotors.co.za",
    "https://www.autoworks.co.za",
    "https://harkersauto.co.za",
    "https://frostlogistics.co.za",
    "https://c-h-logistics.com",
    "https://jacservdelivery.com",
    "https://www.trianglecouriers.co.za",
    "https://www.autoexecutive.co.za",
    "https://driving-force.co.za",
    "https://www.mycouriersa.co.za",
    "https://www.concordecars.co.za",
    "https://www.dsv.com",
    "https://www.craneww.com",
    "https://www.scangl.com",
    "https://www.happyfreight.co.za",
    "https://bridgewaterlogistics.co.za",
    "https://www.vwtableview.co.za",
    "https://www.scootercouriersza.co.za",
    "https://www.capetownmotorcycles.co.za",
    "https://bdautobodyworks.co.za",
    "https://connectlogistics.za.com",
    "https://www.mrd.com",
    "https://www.m24logistics.com",
    "https://www.motorvia.co.za",
    "https://www.autocarriers.co.za",
    "https://www.freightfactory.co.za",
    "https://www.mwezatrans.co.za",
    "https://www.titanictrucking.co.za",
    "https://www.carefulmovers.co.za",
    "https://www.leebotti.co.za",
    "https://www.steinweg.com",
    "https://www.caferemovals.co.za",
    "https://www.airportrentals.com",
    "https://www.avis.co.za",
    "https://www.hertz.co.za",
    "https://www.pacecarrental.co.za",
    "https://www.wisemove.co.za",
    "https://www.velocitycartransport.co.za",
    "https://intercityautomovers.co.za",
    "https://movemycar.co.za",
    "https://www.gogirl-logistics.com",
    "https://www.vdsgroup.co.za",
    "https://www.webfleet.com",
    "https://www.foodfitnessfactory.co.za",
    "https://www.bonappetitmeal.co.za",
    "https://www.primelog.co.za",
    "https://www.cmremovals.co.za",
    "https://www.madmacintosh.com"
]
# Additional seed companies for expanded industries
SEED_COMPANIES.extend([
    "https://www.motorsport.co.za",
    "https://www.vehiclebranding.co.za",
    "https://www.workshopequipment.co.za",
    "https://www.safetygear.co.za",
    "https://www.engineeringnews.co.za",
    "https://www.manufacturing.co.za",
    "https://www.sportsmarketing.co.za",
    "https://www.energydrink.co.za"
])


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
