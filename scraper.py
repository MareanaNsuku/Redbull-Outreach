import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from googlesearch import search as google_search
import re
import time
import random
import os
import pandas as pd
import urllib3
from config import SEARCH_QUERIES, MAX_COMPANIES_PER_RUN, REQUEST_TIMEOUT, DELAY_BETWEEN_REQUESTS, CSV_FILE, SEED_COMPANIES

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Directories and low-quality domains to skip
BLOCKED_DOMAINS = [
    "facebook.com", "linkedin.com", "youtube.com", "wikipedia.org", "tiktok.com",
    "instagram.com", "twitter.com", "pissedconsumer.com", "yelp.com",
    "yellowpages", "yellosa", "infobel", "cylex", "netpages", "fyple",
    "brabys", "hotfrog", "snupit", "trustlink", "africanadvice",
    "findglocal", "shopshours", "capetourism", "autoyas", "infoisinfo",
    "d7leadfinder", "aeroleads", "lusha", "contactout", "dnb.com",
    "bing.com", "goodfirms", "fiata.org", "cargoyellowpages", "buzzsouthafrica"
]
BLOCKED_PATTERNS = [re.compile(d, re.IGNORECASE) for d in BLOCKED_DOMAINS]

JUNK_EMAIL_DOMAINS = [
    "example.com", "email.com", "mail.com", "facebook.com", "google.com",
    "wikipedia.org", "youtube.com", "linkedin.com", "twitter.com",
    "sentry.io", "wixpress.com", "shopify.com", "wordpress.com",
    "godaddy.com", "domain.com", "webmaster.com", "mysite.com",
    "test.com", "sample.com", "mailinator.com", "10minutemail.com",
    "guerrillamail.com", "temp-mail.org", "throwawaymail.com",
    "dispostable.com", "yopmail.com", "getnada.com", "sharklasers.com"
]
JUNK_EMAIL_PATTERNS = [re.compile(d, re.IGNORECASE) for d in JUNK_EMAIL_DOMAINS]

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

def is_valid_email_format(email):
    if not email or not isinstance(email, str):
        return False
    email = email.strip().lower()
    if " " in email or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        return False
    if len(domain.split(".")[-1]) < 2:
        return False
    placeholders = ["example", "test", "user", "jane.doe", "john.doe"]
    for ph in placeholders:
        if ph in local:
            return False
    return True

def find_company_websites():
    domains = set()
    # Add seed companies first
    for url in SEED_COMPANIES:
        if url and not is_blocked(url):
            domains.add(url)
    with DDGS() as ddgs:
        for query in SEARCH_QUERIES:
            print(f"Searching: {query}")
            try:
                results = list(ddgs.text(query, max_results=8))
                if results:
                    for res in results:
                        url = res.get("href")
                        if url and not is_blocked(url):
                            if any(x in url for x in [".co.za", ".com", ".org", ".net"]) and "search" not in url:
                                domains.add(url)
                else:
                    print("  DDG no results, trying Google...")
                    try:
                        gresults = list(google_search(query, num_results=5, sleep_interval=1))
                        for url in gresults:
                            if url and not is_blocked(url):
                                if any(x in url for x in [".co.za", ".com", ".org", ".net"]) and "search" not in url:
                                    domains.add(url)
                    except Exception as e:
                        print(f"  Google fallback error: {e}")
            except Exception as e:
                print(f"  DDG error: {e}, trying Google...")
                try:
                    gresults = list(google_search(query, num_results=5, sleep_interval=1))
                    for url in gresults:
                        if url and not is_blocked(url):
                            if any(x in url for x in [".co.za", ".com", ".org", ".net"]) and "search" not in url:
                                domains.add(url)
                except Exception as e:
                    print(f"  Google fallback error: {e}")
            time.sleep(5 + random.uniform(0, 3))
    return list(domains)[:MAX_COMPANIES_PER_RUN]

def extract_emails_phones(url):
    emails = set()
    phones = set()
    pages_to_visit = [url]
    try:
        # Fetch homepage
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
        resp = requests.get(url, timeout=10, headers=headers, verify=False)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # Look for contact page links
            for a in soup.find_all("a", href=True):
                text = a.get_text().lower()
                if any(kw in text for kw in ["contact", "about", "reach", "enquir"]):
                    href = a["href"]
                    if href.startswith("http") and not is_blocked(href):
                        pages_to_visit.append(href)
                        break
            # Extract emails and phones from homepage
            _extract_from_soup(soup, emails, phones)
    except Exception:
        pass

    # Visit one contact page if found
    if len(pages_to_visit) > 1:
        try:
            resp = requests.get(pages_to_visit[1], timeout=10, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                _extract_from_soup(soup, emails, phones)
        except Exception:
            pass

    return emails, phones

def _extract_from_soup(soup, emails, phones):
    email_re = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    # mailto links
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("mailto:"):
            email = a["href"].replace("mailto:", "").split("?")[0].strip()
            if is_valid_email_format(email) and not is_junk_email(email):
                emails.add(email.lower())
    # visible text
    text = soup.get_text()
    for email in re.findall(email_re, text):
        if is_valid_email_format(email) and not is_junk_email(email):
            emails.add(email.lower())
    # script tags
    for script in soup.find_all("script"):
        if script.string:
            for email in re.findall(email_re, script.string):
                if is_valid_email_format(email) and not is_junk_email(email):
                    emails.add(email.lower())
    # phone numbers
    phone_re = r"(?:\+27|0)(?:[ \-]?\d){9,11}"
    phones.update(re.findall(phone_re, text))

def search_email_with_google(company_name):
    emails = set()
    query = f"{company_name} email"
    try:
        results = list(google_search(query, num_results=3, sleep_interval=1))
        for res in results:
            snippet = res
            email_re = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
            for email in re.findall(email_re, snippet):
                if is_valid_email_format(email) and not is_junk_email(email):
                    emails.add(email.lower())
    except Exception as e:
        print(f"  Google email search error: {e}")
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
            print(f"  No email on website, trying Google search...")
            emails = search_email_with_google(company_name)
        email = ""
        if emails:
            email = next(iter(emails))
        else:
            domain = url.split("//")[-1].split("/")[0].replace("www.", "")
            for prefix in ["info", "hello", "contact", "admin", "enquiries"]:
                guessed = f"{prefix}@{domain}"
                if is_valid_email_format(guessed) and not is_junk_email(guessed):
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
