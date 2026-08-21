from scraper import scrape_companies
from emailer import send_email
import pandas as pd
from config import CSV_FILE

def main():
    print("Starting company outreach...")
    df = scrape_companies()

    new_df = df[df["emailed"] == "No"]
    for idx, row in new_df.iterrows():
        email = row.get("email", "")
        company = row.get("company_name", "Unknown")
        website = row.get("website", "")

        if pd.isna(email) or not isinstance(email, str) or email.strip() == "":
            df.at[idx, "emailed"] = "No email"
            print(f"No email for {company}, marking as 'No email'.")
            continue

        success = send_email(email, company, website)
        if success:
            df.at[idx, "emailed"] = "Yes"

    df.to_csv(CSV_FILE, index=False)
    print("Outreach finished.")

if __name__ == "__main__":
    main()
