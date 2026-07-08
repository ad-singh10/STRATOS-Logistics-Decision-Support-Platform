"""
=========================================================
STRATOS
Module : Vehicle Decision Engine
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

SHIPMENT_FILE = "data/final/shipments_master.csv"
FLEET_FILE = "data/final/fleet_master.csv"
WAREHOUSE_DECISION_FILE = "decision_engine/outputs/warehouse_decision.csv"

OUTPUT_DIR = "decision_engine/outputs"
OUTPUT_FILE = "vehicle_decision.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Vehicle Capacity Mapping
# =========================================================

CAPACITY = {
    "Mini Truck": 2000,
    "Medium Truck": 7500,
    "Heavy Truck": 16000
}

# =========================================================
# Vehicle Selection Function
# =========================================================

def select_vehicle(qty, vehicles):

    # Required vehicle type

    if qty <= 2000:

        preferred = [
            "Mini Truck",
            "Medium Truck",
            "Heavy Truck"
        ]

    elif qty <= 7500:

        preferred = [
            "Medium Truck",
            "Heavy Truck"
        ]

    else:

        preferred = [
            "Heavy Truck"
        ]

    # Search in order of preference

    for vehicle_type in preferred:

        available = vehicles[

            (vehicles["vehicle_type"] == vehicle_type)

            &

            (vehicles["vehicle_status"] == "Available")

        ]

        if not available.empty:

            return available.iloc[0]

    return None


# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS DECISION ENGINE")
    print("Module : Vehicle Decision")
    print("=" * 70)

    print("\nReading datasets...")

    shipments = pd.read_csv(SHIPMENT_FILE)

    fleet = pd.read_csv(FLEET_FILE)

    warehouse_decision = pd.read_csv(
        WAREHOUSE_DECISION_FILE
    )

    # -----------------------------------------------------
    # Warehouse Recommendation Lookup
    # -----------------------------------------------------

    warehouse_lookup = {}

    for _, row in warehouse_decision.iterrows():

        warehouse_lookup[

            row["order_id"]

        ] = row["recommended_warehouse"]

    rows = []

    assigned = 0

    unavailable = 0

    print("\nEvaluating vehicle decisions...")

    for _, shipment in shipments.iterrows():

        shipment_id = shipment["shipment_id"]

        order_id = shipment["order_id"]

        qty = shipment["shipment_quantity"]

        warehouse_code = warehouse_lookup.get(
            order_id,
            shipment["warehouse_code"]
        )

        warehouse_fleet = fleet[

            fleet["warehouse_code"] == warehouse_code

        ]

        vehicle = select_vehicle(

            qty,

            warehouse_fleet

        )

                # -------------------------------------------------
        # Decision
        # -------------------------------------------------

        if vehicle is not None:

            assigned += 1

            if vehicle["vehicle_type"] == "Mini Truck":

                reason = "Optimal"

            elif vehicle["vehicle_type"] == "Medium Truck":

                if qty <= 2000:

                    reason = "Upgraded Capacity"

                else:

                    reason = "Optimal"

            else:

                if qty <= 7500:

                    reason = "Upgraded Capacity"

                else:

                    reason = "Optimal"

            rows.append({

                "shipment_id": shipment_id,

                "order_id": order_id,

                "warehouse_code": warehouse_code,

                "vehicle_id": vehicle["vehicle_id"],

                "vehicle_number": vehicle["vehicle_number"],

                "vehicle_type": vehicle["vehicle_type"],

                "payload_capacity_kg": vehicle["payload_capacity_kg"],

                "shipment_quantity": qty,

                "decision_reason": reason

            })

        else:

            unavailable += 1

            rows.append({

                "shipment_id": shipment_id,

                "order_id": order_id,

                "warehouse_code": warehouse_code,

                "vehicle_id": None,

                "vehicle_number": None,

                "vehicle_type": "No Vehicle",

                "payload_capacity_kg": 0,

                "shipment_quantity": qty,

                "decision_reason": "No Vehicle Available"

            })

    # =====================================================
    # Save Output
    # =====================================================

    vehicle_df = pd.DataFrame(rows)

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    vehicle_df.to_csv(

        output_path,

        index=False

    )

    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)

    print("VEHICLE DECISION SUMMARY")

    print("=" * 70)

    print(vehicle_df.head())

    print()

    print(f"Shipments Processed : {len(vehicle_df)}")

    print(f"Vehicles Assigned   : {assigned}")

    print(f"No Vehicle Found    : {unavailable}")

    print()

    print("Decision Reasons")

    print("-" * 70)

    print(

        vehicle_df["decision_reason"]

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