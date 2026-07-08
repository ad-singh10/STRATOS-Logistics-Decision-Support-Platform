
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
import time
import pandas as pd

from config.city_rules import (
    STATE_TO_REGION,
    TIER_1_CITIES,
    TIER_2_CITIES,
    LOGISTICS_DEMAND_WEIGHT,
    POTENTIAL_WAREHOUSE_CITIES
)

# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = "data/processed/cities_clean.csv"
OUTPUT_DIR = "data/final"
OUTPUT_FILE = "cities_master.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# Main
# ==========================================================

def main():

    start_time = time.time()

    print("=" * 65)
    print("STRATOS DATA PIPELINE")
    print("Module : Cities Enrichment")
    print("=" * 65)

    print("\nReading cleaned dataset...")

    df = pd.read_csv(INPUT_FILE)

    # ------------------------------------------------------
    # Rename Columns
    # ------------------------------------------------------

    print("Renaming columns...")

    df.rename(
        columns={
            "location": "city"
        },
        inplace=True
    )

    # ------------------------------------------------------
    # Generate City ID
    # ------------------------------------------------------

    print("Generating City IDs...")

    df.insert(
        0,
        "city_id",
        [f"C{str(i+1).zfill(5)}" for i in range(len(df))]
    )

    # ------------------------------------------------------
    # Region
    # ------------------------------------------------------

    print("Assigning Regions...")

    df["region"] = df["state"].map(STATE_TO_REGION)

    df["region"] = df["region"].fillna("Unknown")

    # ------------------------------------------------------
    # Logistics Tier
    # ------------------------------------------------------

    print("Assigning Logistics Tier...")

    def assign_tier(city):

        if city in TIER_1_CITIES:
            return "Tier 1"

        elif city in TIER_2_CITIES:
            return "Tier 2"

        else:
            return "Tier 3"

    df["logistics_tier"] = df["city"].apply(assign_tier)

    # ------------------------------------------------------
    # Demand Weight
    # ------------------------------------------------------

    print("Assigning Demand Weights...")

    df["demand_weight"] = df["logistics_tier"].map(
        LOGISTICS_DEMAND_WEIGHT
    )

    # ------------------------------------------------------
    # Warehouse Candidate
    # ------------------------------------------------------

    print("Assigning Warehouse Candidates...")

    df["warehouse_candidate"] = df["city"].isin(
        POTENTIAL_WAREHOUSE_CITIES
    )

    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    df.to_csv(
        output_path,
        index=False
    )

    elapsed = round(
        time.time() - start_time,
        2
    )

    print("\n" + "=" * 65)
    print("ENRICHMENT SUMMARY")
    print("=" * 65)

    print(f"Total Cities           : {len(df)}")
    print(f"Tier 1 Cities          : {(df['logistics_tier'] == 'Tier 1').sum()}")
    print(f"Tier 2 Cities          : {(df['logistics_tier'] == 'Tier 2').sum()}")
    print(f"Tier 3 Cities          : {(df['logistics_tier'] == 'Tier 3').sum()}")
    print(f"Warehouse Candidates   : {df['warehouse_candidate'].sum()}")

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {elapsed} seconds")

    print("=" * 65)


# ==========================================================

if __name__ == "__main__":
    main()


import pandas as pd

df = pd.read_csv("data/final/cities_master.csv")

print(df[df["city"].isin([
    "Mumbai",
    "Delhi",
    "New Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Ahmedabad"
])][["city", "logistics_tier"]])