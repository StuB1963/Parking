#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
import pandas as pd

API_URL = "https://www.victoria.ca/api/parking/parkades"
TARGET = "Johnson Street Parkade"
TOTAL = 310

BASE = "/Users/stuartbanham/Parking"
DATA = f"{BASE}/johnson_week.xlsx"
LOG = f"{BASE}/logs/johnson_week.log"

os.makedirs(f"{BASE}/logs", exist_ok=True)

def log(msg):
    ts = datetime.now().isoformat()
    with open(LOG, "a") as f:
        f.write(f"{ts} - {msg}\n")

def collect():
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        data = r.json()

        p = next((x for x in data if x["name"] == TARGET), None)
        if not p:
            raise ValueError("Johnson Street not found")

        available = p["available"]
        occ = round(((TOTAL - available) / TOTAL) * 100, 2)

        return {
            "timestamp": datetime.now().isoformat(),
            "available": available,
            "total_spaces": TOTAL,
            "occupancy_rate": occ,
            "error": ""
        }

    except Exception as e:
        return {
            "timestamp": datetime.now().isoformat(),
            "available": None,
            "total_spaces": TOTAL,
            "occupancy_rate": None,
            "error": str(e)
        }

def update_excel(row):
    df_new = pd.DataFrame([row])

    if os.path.exists(DATA):
        df_old = pd.read_excel(DATA)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(DATA, index=False)

def main():
    row = collect()
    update_excel(row)

    if row["error"]:
        log(f"ERROR: {row['error']}")
    else:
        log(f"OK: {row['available']} spaces")

if __name__ == "__main__":
    main()

