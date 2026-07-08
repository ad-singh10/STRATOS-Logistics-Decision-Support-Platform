"""
=========================================================
STRATOS
Module : Network Validator
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

DEMAND_FILE = "data/final/regional_demand.csv"
NETWORK_FILE = "data/final/warehouse_network.csv"
MAPPING_FILE = "data/final/city_warehouse_mapping.csv"
CAPACITY_FILE = "data/final/warehouse_capacity.csv"

# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS NETWORK DESIGN")
    print("Module : Network Validator")
    print("=" * 70)

    # -----------------------------------------------------

    print("\nReading datasets...")

    demand = pd.read_csv(DEMAND_FILE)
    network = pd.read_csv(NETWORK_FILE)
    mapping = pd.read_csv(MAPPING_FILE)
    capacity = pd.read_csv(CAPACITY_FILE)

    # =====================================================
    # Validation 1
    # =====================================================

    print("\nChecking Warehouse Count...")

    warehouse_count = len(network)

    # =====================================================
    # Validation 2
    # =====================================================

    print("Checking City Mapping...")

    total_cities = len(mapping)

    mapped_cities = mapping["default_warehouse"].notna().sum()

    unmapped = total_cities - mapped_cities

    # =====================================================
    # Validation 3
    # =====================================================

    print("Checking Duplicate Warehouses...")

    duplicate_warehouses = (
        network["warehouse_city"]
        .duplicated()
        .sum()
    )

    # =====================================================
    # Validation 4
    # =====================================================

    print("Checking Capacity Hierarchy...")

    invalid_capacity = (
        capacity["operating_capacity"]
        >
        capacity["design_capacity"]
    ).sum()

    # =====================================================
    # Validation 5
    # =====================================================

    print("Checking Warehouse Coverage...")

    served = (
        mapping
        .groupby("default_warehouse")
        .size()
    )

    warehouses_without_cities = 0

    for warehouse in network["warehouse_city"]:

        if warehouse not in served.index:

            warehouses_without_cities += 1

    # =====================================================
    # Validation 6
    # =====================================================

    print("Checking Regional Coverage...")

    expected_regions = {

        "North",
        "South",
        "West",
        "East",
        "Central"

    }

    actual_regions = set(
        network["primary_region"]
    )

    missing_regions = expected_regions - actual_regions

    # =====================================================
    # Final Report
    # =====================================================

    elapsed = round(
        time.time() - start,
        2
    )

    print("\n" + "=" * 70)
    print("NETWORK VALIDATION REPORT")
    print("=" * 70)

    print(f"Warehouses Designed        : {warehouse_count}")

    print(f"Cities Mapped              : {mapped_cities}/{total_cities}")

    print(f"Unmapped Cities            : {unmapped}")

    print(f"Duplicate Warehouses       : {duplicate_warehouses}")

    print(f"Invalid Capacities         : {invalid_capacity}")

    print(f"Warehouses Without Cities  : {warehouses_without_cities}")

    print(f"Missing Regions            : {len(missing_regions)}")

    # -----------------------------------------------------

    if (
        unmapped == 0
        and duplicate_warehouses == 0
        and invalid_capacity == 0
        and warehouses_without_cities == 0
        and len(missing_regions) == 0
    ):

        print("\nNETWORK STATUS : PASSED ✅")

    else:

        print("\nNETWORK STATUS : FAILED ❌")

    print(f"\nExecution Time : {elapsed} sec")

    print("=" * 70)


# =========================================================

if __name__ == "__main__":

    main()