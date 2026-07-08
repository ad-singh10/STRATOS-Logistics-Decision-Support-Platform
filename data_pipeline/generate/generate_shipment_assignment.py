"""
=========================================================
STRATOS
Module : Shipment Assignment Generator
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

SHIPMENTS_FILE = "data/final/shipments_master.csv"
FLEET_FILE = "data/final/fleet_master.csv"
DRIVERS_FILE = "data/final/drivers_master.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "shipment_assignment.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS EXECUTION LAYER")
    print("Module : Shipment Assignment Generator")
    print("=" * 70)

    print("\nReading datasets...")

    shipments = pd.read_csv(SHIPMENTS_FILE)
    fleet = pd.read_csv(FLEET_FILE)
    drivers = pd.read_csv(DRIVERS_FILE)

    rows = []

    fleet_size = len(fleet)

    for i, ship in shipments.iterrows():

        idx = i % fleet_size

        vehicle = fleet.iloc[idx]
        driver = drivers.iloc[idx]

        # -----------------------------------------------------
        # Assignment Time
        # -----------------------------------------------------

        dispatch = pd.to_datetime(ship["dispatch_date"])

        assignment_time = dispatch.replace(

            hour=random.randint(6, 20),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)

        )

        rows.append({

            "assignment_id": f"ASN{i+1:06d}",

            "shipment_id": ship["shipment_id"],

            "vehicle_id": vehicle["vehicle_id"],

            "driver_id": driver["driver_id"],

            "assignment_time": assignment_time.strftime("%Y-%m-%d %H:%M:%S"),

            "assignment_status": "Assigned"

        })

    df = pd.DataFrame(rows)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    df.to_csv(output_path, index=False)

    print("\n" + "=" * 70)
    print("SHIPMENT ASSIGNMENT SUMMARY")
    print("=" * 70)

    print(df.head())

    print(f"\nAssignments Created : {len(df)}")
    print(f"Unique Shipments    : {df['shipment_id'].nunique()}")
    print(f"Vehicles Used       : {df['vehicle_id'].nunique()}")
    print(f"Drivers Used        : {df['driver_id'].nunique()}")

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {round(time.time() - start, 2)} sec")

    print("=" * 70)

# =========================================================

if __name__ == "__main__":
    main()