"""
=========================================================
STRATOS
Module : Drivers Master Generator
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

FLEET_FILE = "data/final/fleet_master.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "drivers_master.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

# =========================================================

AVAILABILITY = (
    ["Available"] * 90 +
    ["Assigned"] * 8 +
    ["On Leave"] * 2
)

NAMES = [
    "Rahul","Amit","Vikas","Sandeep","Rohit","Ajay","Sunil","Deepak","Arun","Ankit",
    "Vivek","Rakesh","Nitin","Sachin","Pankaj","Abhishek","Manoj","Prakash","Vinod","Ravi",
    "Mahesh","Suresh","Karan","Mohit","Yash","Harsh","Aditya","Shubham","Akash","Lokesh",
    "Tarun","Gaurav","Naveen","Dinesh","Mukesh","Hemant","Ashish","Sanjay","Kunal","Rajesh"
]

LAST = [
    "Sharma","Singh","Patel","Yadav","Kumar","Gupta","Verma","Jain","Joshi","Mishra",
    "Das","Naik","Reddy","Nair","Pillai","Pandey","Roy","Sahu","Kulkarni","Chauhan"
]

LICENSE = {
    "Light": "LMV",
    "Medium": "HMV",
    "Heavy": "HMV"
}

# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS EXECUTION LAYER")
    print("Module : Drivers Master Generator")
    print("=" * 70)

    print("\nReading Fleet Master...")

    fleet = pd.read_csv(FLEET_FILE)

    today = datetime.today().strftime("%Y-%m-%d")

    rows = []

    for i, veh in fleet.iterrows():

        # -----------------------------------------------------
        # Experience based on Vehicle Category
        # -----------------------------------------------------

        if veh["vehicle_category"] == "Light":
            experience = random.randint(1, 6)

        elif veh["vehicle_category"] == "Medium":
            experience = random.randint(4, 12)

        else:
            experience = random.randint(8, 20)

        rows.append({

            "driver_id": f"DRV{i+1:03d}",

            "driver_name": f"{NAMES[i % len(NAMES)]} {random.choice(LAST)}",

            "license_type": LICENSE[veh["vehicle_category"]],

            "experience_years": experience,

            "assigned_vehicle": veh["vehicle_id"],

            "home_warehouse": veh["home_warehouse"],

            "availability": random.choice(AVAILABILITY),

            "driver_rating": round(random.uniform(3.5, 5.0), 1),

            "created_at": today,

            "is_active": True

        })

    df = pd.DataFrame(rows)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    df.to_csv(output_path, index=False)

    print("\n" + "=" * 70)
    print("DRIVERS MASTER SUMMARY")
    print("=" * 70)

    print(df.head())

    print(f"\nTotal Drivers      : {len(df)}")
    print(f"Assigned Vehicles  : {df['assigned_vehicle'].nunique()}")
    print(f"Warehouses         : {df['home_warehouse'].nunique()}")

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {round(time.time() - start, 2)} sec")

    print("=" * 70)

# =========================================================

if __name__ == "__main__":
    main()