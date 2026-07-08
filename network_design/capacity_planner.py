"""
=========================================================
STRATOS
Module : Warehouse Capacity Planner
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

REGIONAL_FILE = "data/final/regional_demand.csv"
NETWORK_FILE = "data/final/warehouse_network.csv"
MAPPING_FILE = "data/final/city_warehouse_mapping.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "warehouse_capacity.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Constants
# =========================================================

TYPE_WEIGHT = {
    "National Hub": 1.40,
    "Regional Distribution Center": 1.00
}


def round_capacity(value):
    return int(round(value / 5000) * 5000)


# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS NETWORK DESIGN")
    print("Module : Warehouse Capacity Planner")
    print("=" * 70)

    # -----------------------------------------------------

    print("\nReading datasets...")

    regional = pd.read_csv(REGIONAL_FILE)
    network = pd.read_csv(NETWORK_FILE)
    mapping = pd.read_csv(MAPPING_FILE)

    # -----------------------------------------------------

    print("Calculating Cities Served...")

    cities_served = (
        mapping
        .groupby("default_warehouse")
        .size()
        .reset_index(name="cities_served")
    )

    network = network.merge(
        cities_served,
        left_on="warehouse_city",
        right_on="default_warehouse",
        how="left"
    )

    network.drop(columns=["default_warehouse"], inplace=True)

    # -----------------------------------------------------

    regional_lookup = regional.set_index("region")["demand_share"].to_dict()

    network["regional_demand_share"] = (
        network["primary_region"].map(regional_lookup)
    )

    # -----------------------------------------------------

    total_cities = network["cities_served"].sum()

    network["city_share"] = (
        network["cities_served"] / total_cities
    )

    # -----------------------------------------------------

    network["type_weight"] = (
        network["warehouse_type"].map(TYPE_WEIGHT)
    )

    # -----------------------------------------------------

    print("Calculating Planning Score...")

    network["planning_score"] = (
        0.45 * (network["regional_demand_share"] / 100)
        + 0.40 * network["city_share"]
        + 0.15 * (network["type_weight"] / 1.40)
    )

    # =====================================================
    # Capacity Planning
    # =====================================================

    print("Calculating Warehouse Capacities...")

    # ---------------- National Hubs ----------------

    hub = network[
        network["warehouse_type"] == "National Hub"
    ].copy()

    hub_min = hub["planning_score"].min()
    hub_max = hub["planning_score"].max()

    for idx, row in hub.iterrows():

        if hub_max == hub_min:
            norm = 1.0
        else:
            norm = (
                row["planning_score"] - hub_min
            ) / (
                hub_max - hub_min
            )

        capacity = 100000 + norm * 20000

        network.loc[idx, "design_capacity"] = round_capacity(capacity)

    # ---------------- RDC ----------------

    rdc = network[
        network["warehouse_type"] == "Regional Distribution Center"
    ].copy()

    min_cities = rdc["cities_served"].min()
    max_cities = rdc["cities_served"].max()

    for idx, row in rdc.iterrows():

        if max_cities == min_cities:
            norm = 1.0
        else:
            norm = (
                row["cities_served"] - min_cities
            ) / (
                max_cities - min_cities
            )

        capacity = 45000 + norm * 35000

        network.loc[idx, "design_capacity"] = round_capacity(capacity)

    # -----------------------------------------------------

    network["design_capacity"] = (
        network["design_capacity"]
        .astype(int)
    )

    network["operating_capacity"] = (
        network["design_capacity"] * 0.80
    ).astype(int)

    # -----------------------------------------------------

    output = network[
        [
            "warehouse_city",
            "warehouse_type",
            "primary_region",
            "cities_served",
            "regional_demand_share",
            "planning_score",
            "design_capacity",
            "operating_capacity"
        ]
    ]

    # -----------------------------------------------------

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    output.to_csv(
        output_path,
        index=False
    )

    # -----------------------------------------------------

    elapsed = round(time.time() - start, 2)

    print("\n" + "=" * 70)
    print("CAPACITY SUMMARY")
    print("=" * 70)

    print(output)

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {elapsed} sec")

    print("=" * 70)


# =========================================================

if __name__ == "__main__":
    main()