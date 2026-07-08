
"""
=========================================================
STRATOS
Module : Warehouse Master Generator
=========================================================
"""

import os
import time
from datetime import datetime
import pandas as pd

# =========================================================
# Configuration
# =========================================================

NETWORK_FILE = "data/final/warehouse_network.csv"
CAPACITY_FILE = "data/final/warehouse_capacity.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "warehouses_master.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Helper Functions
# =========================================================

def create_name(row):
    if row["warehouse_type"] == "National Hub":
        return f'{row["warehouse_city"]} National Hub'
    return f'{row["warehouse_city"]} Regional Distribution Center'


def create_code(city, warehouse_type):

    city_codes = {
        "Mumbai": "MUM",
        "Nagpur": "NAG",
        "New Delhi": "DEL",
        "Ahmedabad": "AMD",
        "Bengaluru": "BLR",
        "Hyderabad": "HYD",
        "Chennai": "MAA",
        "Kolkata": "CCU"
    }

    city_code = city_codes.get(city, city[:3].upper())

    suffix = "NH" if warehouse_type == "National Hub" else "RDC"

    return f"{city_code}_{suffix}"


def priority(row):

    if row["warehouse_type"] == "National Hub":
        return "Critical"
    elif row["operating_capacity"] >= 55000:
        return "High"
    else:
        return "Medium"


# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS EXECUTION LAYER")
    print("Module : Warehouse Master Generator")
    print("=" * 70)

    print("\nReading datasets...")

    network = pd.read_csv(NETWORK_FILE)
    capacity = pd.read_csv(CAPACITY_FILE)

    print("Merging datasets...")

    df = network.merge(
        capacity[
            [
                "warehouse_city",
                "design_capacity",
                "operating_capacity"
            ]
        ],
        on="warehouse_city",
        how="left"
    )

    print("Generating Warehouse IDs...")

    df.insert(
        0,
        "warehouse_id",
        [f"WH{str(i+1).zfill(3)}" for i in range(len(df))]
    )

    print("Creating Warehouse Names...")

    df["warehouse_name"] = df.apply(create_name, axis=1)

    print("Generating Warehouse Codes...")

    df["warehouse_code"] = df.apply(
        lambda row: create_code(
            row["warehouse_city"],
            row["warehouse_type"]
        ),
        axis=1
    )

    print("Assigning Warehouse Priority...")

    df["warehouse_priority"] = df.apply(priority, axis=1)

    df["warehouse_status"] = "Active"

    today = datetime.today().strftime("%Y-%m-%d")

    df["created_at"] = today
    df["updated_at"] = today
    df["is_active"] = True

    output = df[
        [
            "warehouse_id",
            "warehouse_code",
            "warehouse_name",
            "warehouse_city",
            "warehouse_type",
            "primary_region",
            "latitude",
            "longitude",
            "design_capacity",
            "operating_capacity",
            "warehouse_priority",
            "warehouse_status",
            "created_at",
            "updated_at",
            "is_active"
        ]
    ]

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    output.to_csv(output_path, index=False)

    elapsed = round(time.time() - start, 2)

    print("\n" + "=" * 70)
    print("WAREHOUSE MASTER SUMMARY")
    print("=" * 70)

    print(output)

    print(f"\nTotal Warehouses : {len(output)}")
    print(f"\nSaved To : {output_path}")
    print(f"\nExecution Time : {elapsed} sec")

    print("=" * 70)


if __name__ == "__main__":
    main()
