"""
=========================================================
STRATOS
Module : Driver Decision Engine
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

VEHICLE_DECISION_FILE = "decision_engine/outputs/vehicle_decision.csv"
DRIVERS_FILE = "data/final/drivers_master.csv"
FLEET_FILE = "data/final/fleet_master.csv"

OUTPUT_DIR = "decision_engine/outputs"
OUTPUT_FILE = "driver_decision.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS DECISION ENGINE")
    print("Module : Driver Decision")
    print("=" * 70)

    print("\nReading datasets...")

    vehicle_decision = pd.read_csv(VEHICLE_DECISION_FILE)
    drivers = pd.read_csv(DRIVERS_FILE)
    fleet = pd.read_csv(FLEET_FILE)

    # -----------------------------------------------------
    # Vehicle Lookup
    # -----------------------------------------------------

    vehicle_lookup = {}

    for _, row in fleet.iterrows():

        vehicle_lookup[row["vehicle_id"]] = {

            "warehouse": row["home_warehouse"],
            "vehicle_type": row["vehicle_type"]

        }

    rows = []

    assigned = 0
    unavailable = 0

    print("\nEvaluating driver decisions...")

    for _, shipment in vehicle_decision.iterrows():

        shipment_id = shipment["shipment_id"]

        vehicle_id = shipment["vehicle_id"]

        if pd.isna(vehicle_id):

            rows.append({

                "shipment_id": shipment_id,

                "vehicle_id": None,

                "driver_id": None,

                "driver_name": None,

                "driver_rating": None,

                "license_type": None,

                "decision_reason": "No Vehicle Available"

            })

            unavailable += 1
            continue

        vehicle = vehicle_lookup[vehicle_id]

        warehouse = vehicle["warehouse"]

        vehicle_type = vehicle["vehicle_type"]

        # -------------------------------------------------
        # Required License
        # -------------------------------------------------

        if vehicle_type == "Mini Truck":

            required_license = "LMV"

        else:

            required_license = "HMV"

        # -------------------------------------------------
        # Filter Drivers
        # -------------------------------------------------

        eligible = drivers[

            (drivers["home_warehouse"] == warehouse)

            &

            (drivers["availability"] == "Available")

            &

            (drivers["license_type"] == required_license)

        ]


                # -------------------------------------------------
        # Driver Selection
        # -------------------------------------------------

        if not eligible.empty:

            # Select highest rated available driver
            driver = eligible.sort_values(
                by="driver_rating",
                ascending=False
            ).iloc[0]

            assigned += 1

            # Check whether highest rated or only option
            if len(eligible) > 1:

                reason = "Highest Rated Driver"

            else:

                reason = "Optimal"

            rows.append({

                "shipment_id": shipment_id,

                "vehicle_id": vehicle_id,

                "driver_id": driver["driver_id"],

                "driver_name": driver["driver_name"],

                "driver_rating": driver["driver_rating"],

                "license_type": driver["license_type"],

                "decision_reason": reason

            })

        else:

            unavailable += 1

            rows.append({

                "shipment_id": shipment_id,

                "vehicle_id": vehicle_id,

                "driver_id": None,

                "driver_name": None,

                "driver_rating": None,

                "license_type": required_license,

                "decision_reason": "No Driver Available"

            })

    # =====================================================
    # Save Output
    # =====================================================

    driver_df = pd.DataFrame(rows)

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    driver_df.to_csv(
        output_path,
        index=False
    )

    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("DRIVER DECISION SUMMARY")
    print("=" * 70)

    print(driver_df.head())

    print()

    print(f"Shipments Processed : {len(driver_df)}")
    print(f"Drivers Assigned   : {assigned}")
    print(f"No Driver Found    : {unavailable}")

    print()

    print("Decision Reasons")
    print("-" * 70)

    print(
        driver_df["decision_reason"]
        .value_counts()
    )

    print()

    print(f"Saved To : {output_path}")

    print()

    print(
        f"Execution Time : {round(time.time()-start,2)} sec"
    )

    print("=" * 70)


# =========================================================
# Driver
# =========================================================

if __name__ == "__main__":

    main()