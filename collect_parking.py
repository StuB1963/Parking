#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
import pandas as pd

# -----------------------------
# CONFIGURATION
# -----------------------------
PARKING_API_URL = "https://www.victoria.ca/api/parking/parkades"
TARGET_PARKADE = "Johnson Street Parkade"
TOTAL_SPACES = 310

BASE_DIR = "/Users/stuartbanham/Parking"
DATA_DIR = f"{BASE_DIR}/data"
LOG_FILE = f"{BASE_DIR}/logs/parking.log"
EXCEL_FILE = f"{BASE_DIR}/parking_history.xlsx"
JSON_SNAPSHOT = f"{DATA_DIR}/latest.json"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(f"{BASE_DIR}/logs", exist_ok=True)

# -----------------------------
# LOGGING
# -----------------------------
def log(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")

# -----------------------------
# DATA COLLECTION
# -----------------------------
def collect_parking_data():
    try:
        response = requests.get(PARKING_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        parkade = next((p for p in data if p.get("name") == TARGET_PARKADE), None)
        if not parkade:
            raise ValueError(f"{TARGET_PARKADE} not found in API response")

        available = parkade.get("available")
        if available is None:
            raise ValueError("API returned no 'available' field")

        pct = round((available / TOTAL_SPACES) * 100, 2)

        return {
            "timestamp": datetime.now().isoformat(),
            "available": available,
            "pct": pct,
            "location": TARGET_PARKADE,
            "total_spaces": TOTAL_SPACES,
            "error": ""
        }

    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "available": None,
            "pct": None,
            "location": TARGET_PARKADE,
            "total_spaces": TOTAL_SPACES,
            "error": str(e)
        }

# -----------------------------
# SAVE JSON SNAPSHOT
# -----------------------------
def save_json(data):
    with open(JSON_SNAPSHOT, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# UPDATE EXCEL HISTORY
# -----------------------------
def update_excel(data):
    df_new = pd.DataFrame([data])

    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(EXCEL_FILE, index=False)

# -----------------------------
# MAIN WORKFLOW
# -----------------------------
def main():
    data = collect_parking_data()
    save_json(data)
    update_excel(data)

    if data["error"]:
        log(f"ERROR: {data['error']}")
    else:
        log(f"SUCCESS: {data['available']} spaces available")

if __name__ == "__main__":
    main()


