"""
=========================================================
STRATOS
Module : Regional Demand Analysis
=========================================================
"""

import os
import sys
import time
import pandas as pd

# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------
# Business Rules
# ---------------------------------------------------------

from config.network_rules import (
    DEMAND_WEIGHTS,
    RLI_WEIGHTS
)

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

INPUT_FILE = "data/final/cities_master.csv"

OUTPUT_DIR = "data/final"

OUTPUT_FILE = "regional_demand.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Main
# =========================================================

def main():

    start_time = time.time()

    print("=" * 70)
    print("STRATOS NETWORK DESIGN")
    print("Module : Regional Demand Analysis")
    print("=" * 70)

    # -----------------------------------------------------

    print("\nReading Cities Master Dataset...")

    df = pd.read_csv(INPUT_FILE)

    # -----------------------------------------------------

    print("Grouping by Region...")

    summary = []

    regions = sorted(df["region"].unique())

    for region in regions:

        temp = df[df["region"] == region]

        total_cities = len(temp)

        tier1 = (temp["logistics_tier"] == "Tier 1").sum()

        tier2 = (temp["logistics_tier"] == "Tier 2").sum()

        tier3 = (temp["logistics_tier"] == "Tier 3").sum()

        warehouse_candidates = temp["warehouse_candidate"].sum()

        demand_score = (

            tier1 * DEMAND_WEIGHTS["Tier 1"]

            +

            tier2 * DEMAND_WEIGHTS["Tier 2"]

            +

            tier3 * DEMAND_WEIGHTS["Tier 3"]

        )

        logistics_density = demand_score / total_cities

        summary.append({

            "region": region,

            "total_cities": total_cities,

            "tier1": tier1,

            "tier2": tier2,

            "tier3": tier3,

            "warehouse_candidates": warehouse_candidates,

            "demand_score": round(demand_score,2),

            "logistics_density": round(logistics_density,4)

        })

    regional_df = pd.DataFrame(summary)

    # -----------------------------------------------------
    # Demand Share
    # -----------------------------------------------------

    national_demand = regional_df["demand_score"].sum()

    regional_df["demand_share"] = (

        regional_df["demand_score"]

        /

        national_demand

    )

    # -----------------------------------------------------
    # Ratios
    # -----------------------------------------------------

    total_tier1 = regional_df["tier1"].sum()

    total_candidates = regional_df["warehouse_candidates"].sum()

    regional_df["tier1_ratio"] = regional_df["tier1"] / total_tier1

    regional_df["candidate_ratio"] = (

        regional_df["warehouse_candidates"]

        /

        total_candidates

    )

    # -----------------------------------------------------
    # Normalize Logistics Density
    # -----------------------------------------------------

    max_density = regional_df["logistics_density"].max()

    regional_df["density_ratio"] = (

        regional_df["logistics_density"]

        /

        max_density

    )

    # -----------------------------------------------------
    # Regional Logistics Index
    # -----------------------------------------------------

    regional_df["RLI"] = (

        regional_df["demand_share"]

        * RLI_WEIGHTS["demand_share"]

        +

        regional_df["tier1_ratio"]

        * RLI_WEIGHTS["tier1_ratio"]

        +

        regional_df["candidate_ratio"]

        * RLI_WEIGHTS["warehouse_candidate_ratio"]

        +

        regional_df["density_ratio"]

        * RLI_WEIGHTS["logistics_density"]

    )

    regional_df["RLI"] = regional_df["RLI"].round(4)

    regional_df["demand_share"] = (

        regional_df["demand_share"]

        * 100

    ).round(2)

    # -----------------------------------------------------
    # Sort
    # -----------------------------------------------------

    regional_df = regional_df.sort_values(

        by="RLI",

        ascending=False

    )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    regional_df.to_csv(

        output_path,

        index=False

    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    elapsed = round(

        time.time() - start_time,

        2

    )

    print("\n" + "=" * 70)

    print("REGIONAL DEMAND SUMMARY")

    print("=" * 70)

    print(regional_df[

        [

            "region",

            "total_cities",

            "demand_score",

            "demand_share",

            "RLI"

        ]

    ])

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {elapsed} seconds")

    print("=" * 70)


# =========================================================

if __name__ == "__main__":

    main()