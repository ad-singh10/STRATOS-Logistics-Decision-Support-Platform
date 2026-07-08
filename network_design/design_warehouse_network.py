"""
=========================================================
STRATOS
Module : Warehouse Network Design
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

INPUT_FILE = "data/final/cities_master.csv"

OUTPUT_DIR = "data/final"

OUTPUT_FILE = "warehouse_network.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Strategic Warehouse Network
# =========================================================

WAREHOUSE_NETWORK = [

    {
        "warehouse_city": "Mumbai",
        "warehouse_type": "National Hub",
        "primary_region": "West",
        "backup_region": "Central",
        "selection_reason": "Financial capital, western port access and national logistics gateway."
    },

    {
        "warehouse_city": "Nagpur",
        "warehouse_type": "National Hub",
        "primary_region": "Central",
        "backup_region": "West",
        "selection_reason": "Geographic center of India enabling efficient nationwide distribution."
    },

    {
        "warehouse_city": "New Delhi",
        "warehouse_type": "Regional Distribution Center",
        "primary_region": "North",
        "backup_region": "Central",
        "selection_reason": "Largest distribution hub for North India."
    },

    {
        "warehouse_city": "Ahmedabad",
        "warehouse_type": "Regional Distribution Center",
        "primary_region": "West",
        "backup_region": "North",
        "selection_reason": "Strong industrial corridor and manufacturing ecosystem."
    },

    {
        "warehouse_city": "Bengaluru",
        "warehouse_type": "Regional Distribution Center",
        "primary_region": "South",
        "backup_region": "Hyderabad",
        "selection_reason": "High demand, technology hub and strong consumption market."
    },

    {
        "warehouse_city": "Hyderabad",
        "warehouse_type": "Regional Distribution Center",
        "primary_region": "South",
        "backup_region": "Central",
        "selection_reason": "Strategic central-south location with excellent connectivity."
    },

    {
        "warehouse_city": "Chennai",
        "warehouse_type": "Regional Distribution Center",
        "primary_region": "South",
        "backup_region": "Bengaluru",
        "selection_reason": "Port city with strong manufacturing base."
    },

    {
        "warehouse_city": "Kolkata",
        "warehouse_type": "Regional Distribution Center",
        "primary_region": "East",
        "backup_region": "North-East",
        "selection_reason": "Gateway to Eastern and North-Eastern India."
    }

]

# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS NETWORK DESIGN")
    print("Module : Warehouse Network Design")
    print("=" * 70)

    print("\nReading Cities Master...")

    cities = pd.read_csv(INPUT_FILE)

    warehouse_df = pd.DataFrame(WAREHOUSE_NETWORK)

    print("\nMapping Region Information...")

    warehouse_df = warehouse_df.merge(

        cities[["city", "city_id", "latitude", "longitude", "region"]],

        left_on="warehouse_city",

        right_on="city",

        how="left"

    )

    warehouse_df.drop(columns=["city"], inplace=True)

    warehouse_df.rename(

        columns={"region": "city_region"},

        inplace=True

    )

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    warehouse_df.to_csv(

        output_path,

        index=False

    )

    print("\n" + "=" * 70)

    print("NETWORK SUMMARY")

    print("=" * 70)

    print(warehouse_df[

        [

            "warehouse_city",

            "warehouse_type",

            "primary_region"

        ]

    ])

    print(f"\nTotal Warehouses : {len(warehouse_df)}")

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {round(time.time()-start,2)} sec")

    print("=" * 70)


if __name__ == "__main__":
    main()