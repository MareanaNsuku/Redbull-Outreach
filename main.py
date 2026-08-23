import pandas as pd
from scraper import scrape_companies
from emailer import send_email
from config import CSV_FILE

MAX_ATTEMPTS = 3   # permanent: max attempts per email

def main():
    print("Starting company outreach...")
    df = scrape_companies()

    # Add attempts column if not exists
    if 'attempts' not in df.columns:
        df['attempts'] = 0

    # Process only rows that are not already sent/permanent failed
    pending = df[~df['emailed'].isin(['Sent', 'Permanent Failed'])]
    print(f"Pending emails to process: {len(pending)}")

    for idx, row in pending.iterrows():
        email = row.get('email', '')
        company = row.get('company_name', 'Unknown')
        website = row.get('website', '')
        attempts = int(row.get('attempts', 0))

        if attempts >= MAX_ATTEMPTS:
            df.at[idx, 'emailed'] = 'Permanent Failed'
            print(f"Permanent fail for {company} after {MAX_ATTEMPTS} attempts.")
            df.to_csv(CSV_FILE, index=False)   # save progress
            continue

        if pd.isna(email) or not isinstance(email, str) or email.strip() == '':
            df.at[idx, 'emailed'] = 'No email'
            print(f"No email for {company}, marking as 'No email'.")
            df.to_csv(CSV_FILE, index=False)
            continue

        try:
            status = send_email(email, company, website)
        except Exception as e:
            print(f"ERROR sending to {email}: {e}")
            status = 'Failed'

        # Update status and attempts
        if status == 'Sent':
            df.at[idx, 'emailed'] = 'Sent'
            df.at[idx, 'attempts'] = attempts + 1
        else:
            df.at[idx, 'emailed'] = status
            df.at[idx, 'attempts'] = attempts + 1

        # Save after each email to preserve progress
        df.to_csv(CSV_FILE, index=False)
        print(f"Status for {company}: {status} (attempt {attempts+1})")

    print("Outreach finished.")

if __name__ == "__main__":
    main()
