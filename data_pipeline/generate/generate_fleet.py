"""
=========================================================
STRATOS
Module : Fleet Master Generator
=========================================================
"""

import os
import random
import time
from datetime import datetime
import pandas as pd

# =========================================================
# Configuration
# =========================================================

WAREHOUSE_FILE = "data/final/warehouses_master.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "fleet_master.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

# =========================================================

STATUS = (
    ["Available"] * 70 +
    ["On Trip"] * 20 +
    ["Maintenance"] * 10
)

VEHICLE_INFO = {

    "Mini Truck": {
        "capacity": 2000,
        "fuel": "Diesel",
        "mileage": 12
    },

    "Medium Truck": {
        "capacity": 7500,
        "fuel": "Diesel",
        "mileage": 8
    },

    "Heavy Truck": {
        "capacity": 16000,
        "fuel": "Diesel",
        "mileage": 5

    }

}

CATEGORY_MAP = {

    "Mini Truck": "Light",
    "Medium Truck": "Medium",
    "Heavy Truck": "Heavy"

}

STATE_PREFIX = {

    "Mumbai": "MH",
    "Nagpur": "MH",
    "New Delhi": "DL",
    "Ahmedabad": "GJ",
    "Bengaluru": "KA",
    "Hyderabad": "TS",
    "Chennai": "TN",
    "Kolkata": "WB"

}

# =========================================================

def registration(city):

    state = STATE_PREFIX.get(city, "IN")

    return (
        f"{state}"
        f"{random.randint(1,99):02d}"
        f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))}"
        f"{random.randint(1000,9999)}"
    )

# =========================================================

def fleet_mix(warehouse_type):

    if warehouse_type == "National Hub":

        return [
            "Heavy Truck",
            "Heavy Truck",
            "Medium Truck",
            "Medium Truck",
            "Mini Truck"
        ]

    return [
        "Medium Truck",
        "Medium Truck",
        "Mini Truck",
        "Mini Truck",
        "Heavy Truck"
    ]

# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS EXECUTION LAYER")
    print("Module : Fleet Master Generator")
    print("=" * 70)

    warehouses = pd.read_csv(WAREHOUSE_FILE)

    rows = []

    today = datetime.today().strftime("%Y-%m-%d")

    vehicle_no = 1

    for _, wh in warehouses.iterrows():

        for vt in fleet_mix(wh["warehouse_type"]):

            info = VEHICLE_INFO[vt]

            rows.append({

                "vehicle_id": f"VEH{vehicle_no:03d}",

                "vehicle_number": registration(wh["warehouse_city"]),

                "vehicle_type": vt,

                "vehicle_category": CATEGORY_MAP[vt],

                "payload_capacity_kg": info["capacity"],

                "fuel_type": info["fuel"],

                "fuel_efficiency_kmpl": info["mileage"],

                "home_warehouse": wh["warehouse_id"],

                "warehouse_code": wh["warehouse_code"],

                "vehicle_status": random.choice(STATUS),

                "current_load_kg": 0,

                "created_at": today,

                "is_active": True

            })

            vehicle_no += 1

    df = pd.DataFrame(rows)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    df.to_csv(output_path, index=False)

    print("\n" + "=" * 70)
    print("FLEET MASTER SUMMARY")
    print("=" * 70)

    print(df.head())

    print(f"\nTotal Vehicles : {len(df)}")
    print(f"Warehouses      : {df['home_warehouse'].nunique()}")
    print(f"Vehicle Types   : {df['vehicle_type'].nunique()}")

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {round(time.time()-start,2)} sec")

    print("=" * 70)

# =========================================================

if __name__ == "__main__":
    main()