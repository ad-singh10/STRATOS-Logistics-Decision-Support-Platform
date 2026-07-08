"""
=========================================================
STRATOS
Module : Master Decision Engine
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

WAREHOUSE_FILE="decision_engine/outputs/warehouse_decision.csv"
VEHICLE_FILE="decision_engine/outputs/vehicle_decision.csv"
DRIVER_FILE="decision_engine/outputs/driver_decision.csv"
ETA_FILE="decision_engine/outputs/eta_engine.csv"
ORDERS_FILE="data/final/orders_master.csv"

OUTPUT_DIR="decision_engine/outputs"
OUTPUT_FILE="master_decision.csv"

os.makedirs(OUTPUT_DIR,exist_ok=True)

# =========================================================
# Main
# =========================================================

def main():

    start=time.time()

    print("="*70)
    print("STRATOS DECISION ENGINE")
    print("Module : Master Decision Engine")
    print("="*70)

    print("\nReading datasets...")

    warehouse=pd.read_csv(WAREHOUSE_FILE)
    vehicle=pd.read_csv(VEHICLE_FILE)
    driver=pd.read_csv(DRIVER_FILE)
    eta=pd.read_csv(ETA_FILE)
    orders=pd.read_csv(ORDERS_FILE)

    warehouse_lookup=dict(zip(
        warehouse["order_id"],
        warehouse["recommended_warehouse"]
    ))

    order_lookup=orders.set_index("order_id")

    vehicle_lookup=vehicle.set_index("shipment_id")

    driver_lookup=driver.set_index("shipment_id")

    rows=[]

    ready=0
    action=0

    print("\nGenerating Master Decisions...")

    for _,row in eta.iterrows():

        shipment=row["shipment_id"]

        eta_status=row["eta_status"]

        vehicle_row=vehicle_lookup.loc[shipment]

        driver_row=driver_lookup.loc[shipment]

        order_id=vehicle_row["order_id"]

        warehouse_code=warehouse_lookup[order_id]

        order=order_lookup.loc[order_id]

        priority=order["priority"]


                # -------------------------------------------------
        # Decision Status
        # -------------------------------------------------

        if (
            pd.notna(vehicle_row["vehicle_id"])
            and
            pd.notna(driver_row["driver_id"])
            and
            eta_status != "Unavailable"
        ):

            decision_status = "Operational Ready"

            ready += 1

            explanation = (
                f"Shipment is ready for dispatch. "
                f"Warehouse {warehouse_code} assigned. "
                f"Vehicle {vehicle_row['vehicle_type']} allocated. "
                f"Driver assigned successfully. "
                f"ETA status: {eta_status}."
            )

        else:

            decision_status = "Action Required"

            action += 1

            explanation = (
                "Shipment requires operational attention before dispatch."
            )

        rows.append({

            "shipment_id": shipment,

            "order_id": order_id,

            "priority": priority,

            "warehouse_code": warehouse_code,

            "vehicle_id": vehicle_row["vehicle_id"],

            "vehicle_type": vehicle_row["vehicle_type"],

            "driver_id": driver_row["driver_id"],

            "driver_name": driver_row["driver_name"],

            "estimated_delivery": row["estimated_delivery"],

            "eta_status": eta_status,

            "decision_status": decision_status,

            "business_explanation": explanation

        })

    # =====================================================
    # Save Output
    # =====================================================

    master_df = pd.DataFrame(rows)

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    master_df.to_csv(
        output_path,
        index=False
    )

    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("MASTER DECISION SUMMARY")
    print("=" * 70)

    print(master_df.head())

    print()

    print(f"Shipments Processed : {len(master_df)}")

    print(f"Operational Ready  : {ready}")

    print(f"Action Required    : {action}")

    print()

    print("Decision Status")

    print("-" * 70)

    print(
        master_df["decision_status"]
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