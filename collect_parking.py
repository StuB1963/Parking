#!/usr/bin/env python3
import os
import json
import pandas as pd
from datetime import datetime

BASE_PATH = "/Users/stuartbanham/Parking"
JSON_DIR = os.path.join(BASE_PATH, "data/json")
EXCEL_DIR = os.path.join(BASE_PATH, "output/excel")
LOG_DIR = os.path.join(BASE_PATH, "output/logs")

os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "parking.log")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def collect_parking_data():
    # Placeholder — replace with your real scraping logic
    return {
        "location": "Johnson Street",
        "timestamp": datetime.now().isoformat(),
        "available_spaces": 42,
        "total_spaces": 120
    }

def save_json(data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"parking_{timestamp}.json"
    full_path = os.path.join(JSON_DIR, filename)

    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

    log(f"Saved JSON: {full_path}")
    return full_path

def update_excel(data):
    excel_path = os.path.join(EXCEL_DIR, "parking_data.xlsx")

    df_new = pd.DataFrame([data])

    if os.path.exists(excel_path):
        df_existing = pd.read_excel(excel_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(excel_path, index=False)
    log(f"Updated Excel: {excel_path}")

def main():
    log("Starting parking data collection")
    data = collect_parking_data()
    save_json(data)
    update_excel(data)
    log("Completed parking data collection")

if __name__ == "__main__":
    main()
