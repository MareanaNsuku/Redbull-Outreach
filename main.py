from scraper import scrape_companies
from emailer import send_email
import pandas as pd
from config import CSV_FILE

def main():
    print("Starting company outreach...")
    df = scrape_companies()

    new_df = df[df["emailed"] == "No"]
    for idx, row in new_df.iterrows():
        success = send_email(row["email"], row["company_name"], row["website"])
        if success:
            df.at[idx, "emailed"] = "Yes"

    df.to_csv(CSV_FILE, index=False)
    print("Outreach finished.")

if __name__ == "__main__":
    main()
