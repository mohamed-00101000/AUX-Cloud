import json
import time
import requests
from pathlib import Path

# ======================================================
# Configuration
# ======================================================

# The data.json file that the dashboard reads
DATA_FILE = Path(__file__).resolve().parent / "data" / "data.json"

# Cloud JSON URL
CLOUD_URL = "https://racingteam.rf.gd/new/data.json"

# Update interval
DELAY = 0.5  # seconds


# ======================================================
# MAIN LOOP
# ======================================================
def main():
    print("[BOOT] getFromCloud.py is running...")

    while True:
        try:
            response = requests.get(CLOUD_URL, timeout=5)

            if response.status_code == 200:
                data = response.json()

                # Write new data.json for the dashboard
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

                print("[OK] Updated data.json")

            else:
                print(f"[WARN] Cloud returned status {response.status_code}")

        except Exception as e:
            print(f"[ERROR] Failed to fetch cloud data → {e}")

        time.sleep(DELAY)


if __name__ == "__main__":
    main()
