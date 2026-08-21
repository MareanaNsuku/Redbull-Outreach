import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import re
import time
import os
import pandas as pd
from config import SEARCH_QUERIES, MAX_COMPANIES_PER_RUN, REQUEST_TIMEOUT, DELAY_BETWEEN_REQUESTS, CSV_FILE

def find_company_websites():
    domains = set()
    with DDGS() as ddgs:
        for query in SEARCH_QUERIES:
            print(f"Searching: {query}")
            try:
                results = ddgs.text(query, max_results=5)
                for res in results:
                    url = res.get("href")
                    if url and not any(x in url for x in ["facebook.com", "linkedin.com", "youtube.com", "wikipedia.org"]):
                        domains.add(url)
            except Exception as e:
                print(f"Search error: {e}")
            time.sleep(2)
    return list(domains)[:MAX_COMPANIES_PER_RUN]

def extract_emails_phones(url):
    emails = set()
    phones = set()
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers=headers)
        if resp.status_code != 200:
            return emails, phones
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()

        email_re = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
        emails.update(re.findall(email_re, text))

        phone_re = r"\+?27[0-9]{9}|0[0-9]{9}"
        phones.update(re.findall(phone_re, text))

        for a in soup.find_all("a", href=True):
            if a["href"].startswith("mailto:"):
                emails.add(a["href"].replace("mailto:", "").split("?")[0])

    except Exception as e:
        print(f"Error scraping {url}: {e}")
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
        email = next(iter(emails), "")
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
