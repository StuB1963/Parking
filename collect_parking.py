#!/usr/bin/env python3
import os
import json
import pandas as pd
from datetime import datetime

# -----------------------------
# PATH CONFIGURATION (macOS)
# -----------------------------
BASE_PATH = "/Users/stuartbanham/Parking"
JSON_DIR = os.path.join(BASE_PATH, "data/json")
EXCEL_DIR = os.path.join(BASE_PATH, "output/excel")
LOG_DIR = os.path.join(BASE_PATH, "output/logs")

os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(EXCEL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "collect_parking.log")

# -----------------------------
# LOGGING
# -----------------------------
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

# -----------------------------
# DATA COLLECTION
# -----------------------------
def collect_parking_data():
    """
    Replace this placeholder with the real API call or scraping logic.
    """
    # Example placeholder data
    return {
        "location": "Johnson Street Parkade",
        "timestamp": datetime.now().isoformat(),
        "available_spaces": 42,
        "total_spaces": 120,
        "capacity_percent": round((42 / 120) * 100, 2)
    }

# -----------------------------
# SAVE JSON
# -----------------------------
def save_json(data):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"johnson_street_{timestamp}.json"
    full_path = os.path.join(JSON_DIR, filename)

    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

    log(f"Saved JSON file: {full_path}")
    return full_path

# -----------------------------
# UPDATE EXCEL
# -----------------------------
def update_excel(data):
    excel_path = os.path.join(EXCEL_DIR, "parking_data.xlsx")

    df_new = pd.DataFrame([data])

    if os.path.exists(excel_path):
        df_existing = pd.read_excel(excel_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(excel_path, index=False)
    log(f"Updated Excel file: {excel_path}")

# -----------------------------
# MAIN
# -----------------------------
def main():
    log("Starting parking data collection")

    try:
        data = collect_parking_data()
        save_json(data)
        update_excel(data)
        log("Parking data collection completed successfully")

    except Exception as e:
        log(f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()

