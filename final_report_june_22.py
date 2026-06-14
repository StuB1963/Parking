#!/usr/bin/env python3
import pandas as pd
from datetime import datetime, date
import os
import smtplib
from email.mime.text import MIMEText

BASE = "/Users/stuartbanham/Parking"
CSV_FILE = f"{BASE}/johnson_week.csv"
REPORT_FILE = f"{BASE}/final_report.txt"
LOG_FILE = f"{BASE}/logs/final_report.log"

# Study window
START = date(2026, 6, 15)
END   = date(2026, 6, 21)

# Email settings (iCloud SMTP)
SMTP_SERVER = "smtp.mail.me.com"
SMTP_PORT = 587
FROM_EMAIL = "sbanham1@icloud.com"
TO_EMAIL = "sbanham1@icloud.com"
APP_PASSWORD = "YOUR-ICLOUD-APP-PASSWORD"   # replace with your real app password

def log(msg):
    ts = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{ts} - {msg}\n")

def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "Final Johnson Street Parking Report (June 15–21)"
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
        log("SUCCESS: Email sent.")
    except Exception as e:
        log(f"ERROR sending email: {e}")

def main():
    if not os.path.exists(CSV_FILE):
        log("ERROR: CSV file not found.")
        return

    df = pd.read_csv(CSV_FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["date"] = df["timestamp"].dt.date

    df_week = df[(df["date"] >= START) & (df["date"] <= END)]

    if df_week.empty:
        log("ERROR: No data found for June 15–21.")
        return

    valid = df_week[df_week["occupancy_rate"].notna()]
    errors = df_week[df_week["error"].notna() & (df_week["error"] != "")]

    min_occ = valid["occupancy_rate"].min()
    max_occ = valid["occupancy_rate"].max()
    avg_occ = round(valid["occupancy_rate"].mean(), 2)

    total_samples = len(df_week)
    valid_samples = len(valid)
    error_samples = len(errors)

    lines = []
    lines.append("Final Occupancy Report — Johnson Street Parkade")
    lines.append("Study Window: June 15–21, 2026\n")
    lines.append(f"Total Samples Collected: {total_samples}")
    lines.append(f"Valid Samples: {valid_samples}")
    lines.append(f"Error Samples: {error_samples}\n")
    lines.append(f"Minimum Occupancy: {min_occ}%")
    lines.append(f"Maximum Occupancy: {max_occ}%")
    lines.append(f"Average Occupancy: {avg_occ}%\n")

    report_text = "\n".join(lines)

    with open(REPORT_FILE, "w") as f:
        f.write(report_text)

    send_email(report_text)
    log("SUCCESS: Final report generated and emailed.")

if __name__ == "__main__":
    main()
