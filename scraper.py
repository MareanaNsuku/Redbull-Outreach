# scraper.py
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import re
import time
import os
import pandas as pd
from config import SEARCH_QUERIES, MAX_COMPANIES_PER_RUN, REQUEST_TIMEOUT, DELAY_BETWEEN_REQUESTS, CSV_FILE

# Additional patterns to block low-quality domains
BLOCKED_DOMAINS = [
    "bing.com", "lusha.com", "aeroleads.com", "dnb.com", "contactout.com",
    "goodfirms.co", "infobelpro.com", "buzzsouthafrica.com",
    "capetownbestplaces.com", "fiata.org", "d7leadfinder.com",
    "yellowpages.net.za", "infoisinfo.co.za", "cybo.com", "yellosa.com",
    "hotfrog.co.za", "snupit.co.za", "trustlink.co.za"
]
BLOCKED_PATTERNS = [re.compile(d) for d in BLOCKED_DOMAINS]

def is_blocked(url):
    for pat in BLOCKED_PATTERNS:
        if pat.search(url):
            return True
    return False

def find_company_websites():
    domains = set()
    with DDGS() as ddgs:
        for query in SEARCH_QUERIES:
            print(f"Searching: {query}")
            try:
                results = ddgs.text(query, max_results=20)
                for res in results:
                    url = res.get("href")
                    if url and not is_blocked(url):
                        if any(x in url for x in [".co.za", ".com", ".org", ".net"]) and "search" not in url:
                            domains.add(url)
            except Exception as e:
                print(f"Search error: {e}")
            time.sleep(2)
    return list(domains)[:MAX_COMPANIES_PER_RUN]

def extract_emails_phones(url):
    emails = set()
    phones = set()

    urls_to_visit = [url]
    base_url = url.rstrip('/')
    for path in ["/contact", "/contact-us", "/about", "/about-us"]:
        urls_to_visit.append(base_url + path)

    for page_url in urls_to_visit:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            resp = requests.get(page_url, timeout=REQUEST_TIMEOUT, headers=headers)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.find_all("a", href=True):
                if a["href"].startswith("mailto:"):
                    email = a["href"].replace("mailto:", "").split("?")[0].strip()
                    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        emails.add(email)

            text = soup.get_text()
            email_re = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
            emails.update(re.findall(email_re, text))

            phone_re = r"\+?27[0-9]{9}|0[0-9]{9}"
            phones.update(re.findall(phone_re, text))

            for script in soup.find_all("script"):
                if script.string:
                    emails.update(re.findall(email_re, script.string))

        except Exception as e:
            print(f"Error scraping {page_url}: {e}")

        time.sleep(1)

    return emails, phones

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

        email = ""
        if emails:
            email = next(iter(emails))
        else:
            domain = url.split("//")[-1].split("/")[0].replace("www.", "")
            for prefix in ["info", "hello", "contact", "admin", "enquiries"]:
                guessed = f"{prefix}@{domain}"
                if re.match(r"[^@]+@[^@]+\.[^@]+", guessed):
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
