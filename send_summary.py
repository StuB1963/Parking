import smtplib
from email.mime.text import MIMEText
from openpyxl import load_workbook
from datetime import datetime

EXCEL_PATH = "/Users/stuart/Documents/parking_data.xlsx"
ICLOUD_EMAIL = "sbanham1@icloud.com"
ICLOUD_APP_PASSWORD = "Imel-cshu-wąca-rhir"

def generate_summary():
    wb = load_workbook(EXCEL_PATH)
    ws = wb.active

    spaces = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        timestamp, available, pct = row
        date_str = timestamp.split(" ")[0]
        if date_str == datetime.now().strftime("%Y-%m-%d"):
            spaces.append((available, pct))

    if not spaces:
        return "No data collected today."

    avail_values = [s[0] for s in spaces]
    pct_values = [s[1] for s in spaces]

    summary = f"""
Daily Parking Summary — Johnson Street Parkade
Date: {datetime.now().strftime("%Y-%m-%d")}

Total Readings: {len(spaces)}
Minimum Available: {min(avail_values)}
Maximum Available: {max(avail_values)}
Average Available: {sum(avail_values)/len(avail_values):.2f}
Average Capacity %: {sum(pct_values)/len(pct_values):.2f}%
"""

    return summary

def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "Daily Parking Summary — Johnson Street Parkade"
    msg["From"] = ICLOUD_EMAIL
    msg["To"] = ICLOUD_EMAIL

    with smtplib.SMTP("smtp.mail.me.com", 587) as server:
        server.starttls()
        server.login(ICLOUD_EMAIL, ICLOUD_APP_PASSWORD)
        server.send_message(msg)

def main():
    summary = generate_summary()
    send_email(summary)
    print("Summary email sent.")

if __name__ == "__main__":
    main()
