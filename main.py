import pandas as pd
from scraper import scrape_companies
from emailer import send_email
from config import CSV_FILE

MAX_ATTEMPTS = 3

def get_attempts(row):
    """Safely get attempts as integer."""
    try:
        val = row.get('attempts', 0)
        if pd.isna(val):
            return 0
        return int(val)
    except (ValueError, TypeError):
        return 0

def main():
    print("Starting company outreach...")
    df = scrape_companies()

    if 'attempts' not in df.columns:
        df['attempts'] = 0

    pending = df[~df['emailed'].isin(['Sent', 'Permanent Failed', 'Bounced'])]
    print(f"Pending emails to process: {len(pending)}")

    for idx, row in pending.iterrows():
        email = row.get('email', '')
        company = row.get('company_name', 'Unknown')
        website = row.get('website', '')
        attempts = get_attempts(row)

        if attempts >= MAX_ATTEMPTS:
            df.at[idx, 'emailed'] = 'Permanent Failed'
            print(f"Permanent fail for {company} after {MAX_ATTEMPTS} attempts.")
            df.to_csv(CSV_FILE, index=False)
            continue

        if pd.isna(email) or not isinstance(email, str) or email.strip() == '':
            df.at[idx, 'emailed'] = 'No email'
            print(f"No email for {company}, marking as 'No email'.")
            df.to_csv(CSV_FILE, index=False)
            continue

        status = send_email(email, company, website)
        df.at[idx, 'attempts'] = attempts + 1
        df.at[idx, 'emailed'] = status
        df.to_csv(CSV_FILE, index=False)
        print(f"Status for {company}: {status} (attempt {attempts+1})")

    print("Outreach finished.")

if __name__ == "__main__":
    main()
