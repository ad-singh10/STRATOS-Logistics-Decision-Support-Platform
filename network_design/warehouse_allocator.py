"""
=========================================================
STRATOS
Module : City Warehouse Allocation
=========================================================
"""

import os
import sys
import time
import pandas as pd
from pathlib import Path

# =========================================================
# Project Root
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# =========================================================
# Business Rules
# =========================================================

from config.warehouse_rules import (
    WAREHOUSE_SERVICE_REGIONS,
    BACKUP_WAREHOUSE
)

# =========================================================
# Configuration
# =========================================================

INPUT_FILE = "data/final/cities_master.csv"

OUTPUT_DIR = "data/final"

OUTPUT_FILE = "city_warehouse_mapping.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("="*70)
    print("STRATOS NETWORK DESIGN")
    print("Module : City Warehouse Allocation")
    print("="*70)

    print("\nReading Cities Master...")

    df = pd.read_csv(INPUT_FILE)

    # -----------------------------------------------------

    state_to_warehouse = {}

    for warehouse, states in WAREHOUSE_SERVICE_REGIONS.items():

        for state in states:

            state_to_warehouse[state] = warehouse

    # -----------------------------------------------------

    print("Assigning Default Warehouses...")

    df["default_warehouse"] = df["state"].map(state_to_warehouse)

    # -----------------------------------------------------

    print("Assigning Backup Warehouses...")

    df["backup_warehouse"] = df["default_warehouse"].map(BACKUP_WAREHOUSE)

    # -----------------------------------------------------

    output = df[[
        "city_id",
        "city",
        "state",
        "region",
        "default_warehouse",
        "backup_warehouse"
    ]]

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    output.to_csv(
        output_path,
        index=False
    )

    # -----------------------------------------------------

    elapsed = round(time.time()-start,2)
    df["default_warehouse"] = df["state"].map(state_to_warehouse)
    print("\nUNMAPPED STATES")
    print("-" * 40)

    print(
    df[df["default_warehouse"].isna()]
    ["state"]
    .value_counts()
)
    print("\n"+"="*70)
    print("ALLOCATION SUMMARY")
    print("="*70)

    print(output["default_warehouse"].value_counts())

    print(f"\nTotal Cities : {len(output)}")

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {elapsed} sec")

    print("="*70)


if __name__ == "__main__":
    main()

    