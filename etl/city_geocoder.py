"""
=========================================================
STRATOS
Module : City Geocoder
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

CITY_MASTER_FILE = "data/final/cities_master.csv"
CITY_MAPPING_FILE = "data/final/city_warehouse_mapping.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "city_coordinates.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS ETL LAYER")
    print("Module : City Geocoder")
    print("=" * 70)

    print("\nReading datasets...")

    cities = pd.read_csv(CITY_MASTER_FILE)
    mapping = pd.read_csv(CITY_MAPPING_FILE)

    # -----------------------------------------------------
    # Standardize city names
    # -----------------------------------------------------

    cities["city"] = (
        cities["city"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    mapping["city"] = (
        mapping["city"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # -----------------------------------------------------
    # Merge Coordinates
    # -----------------------------------------------------

    merged = mapping.merge(

        cities[["city", "latitude", "longitude"]],

        on="city",

        how="left"

    )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    merged.to_csv(

        output_path,

        index=False

    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    matched = merged["latitude"].notna().sum()

    unmatched = len(merged) - matched

    print("\n" + "=" * 70)
    print("CITY GEOCODER SUMMARY")
    print("=" * 70)

    print(merged.head())

    print()

    print(f"Cities Processed : {len(merged)}")
    print(f"Matched          : {matched}")
    print(f"Unmatched        : {unmatched}")

    print()

    print(f"Saved To : {output_path}")

    print()

    print(f"Execution Time : {round(time.time()-start,2)} sec")

    print("=" * 70)


# =========================================================
# Driver
# =========================================================

if __name__ == "__main__":

    main()