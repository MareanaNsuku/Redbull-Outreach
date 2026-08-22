import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import re
import time
from googlesearch import search as google_search
import random
import os
import pandas as pd
import urllib3
from config import SEARCH_QUERIES, MAX_COMPANIES_PER_RUN, REQUEST_TIMEOUT, DELAY_BETWEEN_REQUESTS, CSV_FILE, SEED_COMPANIES

# Disable SSL warnings (some sites have expired certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BLOCKED_DOMAINS = [
    "bing.com", "lusha.com", "aeroleads.com", "dnb.com", "contactout.com",
    "goodfirms.co", "infobelpro.com", "buzzsouthafrica.com",
    "capetownbestplaces.com", "fiata.org", "d7leadfinder.com",
    "yellowpages.net.za", "infoisinfo.co.za", "cybo.com", "yellosa.com",
    "hotfrog.co.za", "snupit.co.za", "trustlink.co.za",
    "facebook.com", "linkedin.com", "youtube.com", "wikipedia.org",
    "tiktok.com", "instagram.com", "twitter.com", "pissedconsumer.com"
]
BLOCKED_PATTERNS = [re.compile(d) for d in BLOCKED_DOMAINS]

JUNK_EMAIL_DOMAINS = [
    "example.com", "email.com", "mail.com", "facebook.com", "google.com",
    "wikipedia.org", "youtube.com", "linkedin.com", "twitter.com",
    "sentry.io", "wixpress.com", "shopify.com", "wordpress.com",
    "godaddy.com", "domain.com", "webmaster.com", "sentry-next.wixpress.com"
]
JUNK_EMAIL_PATTERNS = [re.compile(d) for d in JUNK_EMAIL_DOMAINS]

def is_blocked(url):
    for pat in BLOCKED_PATTERNS:
        if pat.search(url):
            return True
    return False

def is_junk_email(email):
    domain = email.split("@")[-1].lower()
    for pat in JUNK_EMAIL_PATTERNS:
        if pat.search(domain):
            return True
    return False

def find_company_websites():
    domains = set()
    # Add seed companies first
    for url in SEED_COMPANIES:
        if not is_blocked(url):
            domains.add(url)
    with DDGS() as ddgs:
        for query in SEARCH_QUERIES:
            print(f"Searching: {query}")
            success = False
            # Try DuckDuckGo first
            try:
                results = list(ddgs.text(query, max_results=10))
                if results:
                    for res in results:
                        url = res.get("href")
                        if url and not is_blocked(url):
                            if any(x in url for x in [".co.za", ".com", ".org", ".net"]) and "search" not in url:
                                domains.add(url)
                    success = True
                else:
                    print(f"  DDG: No results for '{query}', trying Google fallback...")
            except Exception as e:
                print(f"  DDG error: {e}, trying Google fallback...")
            # Google fallback if DDG failed
            if not success:
                try:
                    gresults = list(google_search(query, num_results=10, sleep_interval=2))
                    for url in gresults:
                        if url and not is_blocked(url):
                            if any(x in url for x in [".co.za", ".com", ".org", ".net"]) and "search" not in url:
                                domains.add(url)
                    success = True
                except Exception as e:
                    print(f"  Google fallback error: {e}")
            # Polte delay
            time.sleep(8 + random.uniform(0, 4))
    return list(domains)[:MAX_COMPANIES_PER_RUN]

def extract_emails_phones(url):
    emails = set()
    phones = set()

    base_url = url.rstrip('/')
    pages_to_visit = [url]
    for path in ["/contact", "/contact-us", "/about", "/about-us", "/contact.html", "/contact-us.html", "/about.html"]:
        pages_to_visit.append(base_url + path)

    for page_url in pages_to_visit:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
            resp = requests.get(page_url, timeout=REQUEST_TIMEOUT, headers=headers, verify=False)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                if href.startswith("mailto:"):
                    email = href.replace("mailto:", "").split("?")[0].strip()
                    if re.match(r"[^@]+@[^@]+\.[^@]+", email) and not is_junk_email(email):
                        emails.add(email.lower())

            text = soup.get_text()
            email_re = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
            for email in re.findall(email_re, text):
                if not is_junk_email(email):
                    emails.add(email.lower())

            for script in soup.find_all("script"):
                if script.string:
                    for email in re.findall(email_re, script.string):
                        if not is_junk_email(email):
                            emails.add(email.lower())

            phone_re = r"(?:\+27|0)(?:[ \-]?\d){9,11}"
            phones.update(re.findall(phone_re, text))

        except Exception:
            pass

        time.sleep(0.5)

    return emails, phones

def search_email_with_ddg(company_name):
    emails = set()
    query = f"{company_name} email"
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)
            for res in results:
                snippet = res.get("body", "") + " " + res.get("title", "")
                email_re = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
                for email in re.findall(email_re, snippet):
                    if not is_junk_email(email):
                        emails.add(email.lower())
    except Exception as e:
        print(f"  DDG email search error: {e}")
    return emails

def scrape_companies():
    websites = find_company_websites()
    data = []
    existing_df = None
    if os.path.exists(CSV_FILE):
        existing_df = pd.read_csv(CSV_FILE)
        existing_urls = set(existing_df["website"].tolist())
    else:
        existing_urls = set()

    for url in websites:
        if url in existing_urls:
            continue
        print(f"Scraping: {url}")
        emails, phones = extract_emails_phones(url)

        if not emails:
            company_name = url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0]
            print(f"  No email on website, searching DDG for {company_name}...")
            emails = search_email_with_ddg(company_name)

        email = ""
        if emails:
            email = next(iter(emails))
        else:
            domain = url.split("//")[-1].split("/")[0].replace("www.", "")
            for prefix in ["info", "hello", "contact", "admin", "enquiries"]:
                guessed = f"{prefix}@{domain}"
                if re.match(r"[^@]+@[^@]+\.[^@]+", guessed) and not is_junk_email(guessed):
                    email = guessed
                    break

        phone = next(iter(phones), "")
        company_name = url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0]
        data.append({
            "company_name": company_name,
            "website": url,
            "email": email,
            "phone": phone,
            "date_added": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "emailed": "No"
        })
        time.sleep(DELAY_BETWEEN_REQUESTS)

    df = pd.DataFrame(data)
    if existing_df is not None and not existing_df.empty:
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    print(f"Saved {len(data)} new companies to {CSV_FILE}")
    return df
