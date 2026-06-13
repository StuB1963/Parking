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
    """
    Fetch real-time parking availability for Johnson Street Parkade.
    """

    try:
        response = requests.get(PARKING_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        parkade = next(
            (p for p in data if p.get("name") == TARGET_PARKADE),
            None
        )

        if not parkade:
            raise ValueError(f"{TARGET_PARKADE} not found in API response")

        available = parkade.get("available", None)

        if available is None:
            raise ValueError("API returned no 'available' field")

        capacity_percent = round((available / TOTAL_SPACES) * 100, 2)

        result = {
            "location": TARGET_PARKADE,
            "timestamp": datetime.now().isoformat(),
            "available_spaces": available,
            "total_spaces": TOTAL_SPACES,
            "capacity_percent": capacity_percent
        }

        return result

    except Exception as e:
        return {
            "location": TARGET_PARKADE,
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "available_spaces": None,
            "total_spaces": TOTAL_SPACES,
            "capacity_percent": None
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

    if "error" in data:
        log(f"ERROR: {data['error']}")
    else:
        log(f"SUCCESS: {data['available_spaces']} spaces available")

if __name__ == "__main__":
    main()


