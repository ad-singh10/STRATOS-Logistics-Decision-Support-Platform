"""
=========================================================
STRATOS
Module : Recommendation Engine
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

MASTER_FILE = "decision_engine/outputs/master_decision.csv"
DISRUPTION_FILE = "simulation/outputs/disruption_events.csv"

WAREHOUSE_FILE = "decision_engine/outputs/warehouse_decision.csv"
VEHICLE_FILE = "decision_engine/outputs/vehicle_decision.csv"
DRIVER_FILE = "decision_engine/outputs/driver_decision.csv"
ETA_FILE = "decision_engine/outputs/eta_engine.csv"

OUTPUT_DIR = "simulation/outputs"
OUTPUT_FILE = "recommendation_engine.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("="*70)
    print("STRATOS AI CONTROL TOWER")
    print("Module : Recommendation Engine")
    print("="*70)

    print("\nReading datasets...")

    master = pd.read_csv(MASTER_FILE)
    disruptions = pd.read_csv(DISRUPTION_FILE)

    warehouse = pd.read_csv(WAREHOUSE_FILE)
    vehicle = pd.read_csv(VEHICLE_FILE)
    driver = pd.read_csv(DRIVER_FILE)
    eta = pd.read_csv(ETA_FILE)

    warehouse_lookup = warehouse.set_index("order_id")

    vehicle_lookup = vehicle.set_index("shipment_id")

    driver_lookup = driver.set_index("shipment_id")

    eta_lookup = eta.set_index("shipment_id")

    recommendations = []

    print("\nGenerating Recommendations...")

    for _, event in disruptions.iterrows():

        shipment = event["shipment_id"]

        order = event["order_id"]

        event_type = event["event_type"]

        warehouse_row = warehouse_lookup.loc[order]

        vehicle_row = vehicle_lookup.loc[shipment]

        driver_row = driver_lookup.loc[shipment]

        eta_row = eta_lookup.loc[shipment]

        warehouse_code = warehouse_row["recommended_warehouse"]

        vehicle_id = vehicle_row["vehicle_id"]

        vehicle_type = vehicle_row["vehicle_type"]

        driver_id = driver_row["driver_id"]

        driver_name = driver_row["driver_name"]

        eta_value = eta_row["estimated_delivery"]



                # =====================================================
        # Recommendation Logic
        # =====================================================

        if event_type == "Vehicle Breakdown":

            recommendation = (
                "Assign alternate available vehicle from same warehouse."
            )

            action = "Vehicle Reassigned"

        elif event_type == "Driver Absence":

            recommendation = (
                "Assign alternate licensed driver from same warehouse."
            )

            action = "Driver Reassigned"

        elif event_type == "Warehouse Shutdown":

            recommendation = (
                "Move shipment to backup warehouse."
            )

            action = "Warehouse Changed"

        elif event_type == "Inventory Shortage":

            recommendation = (
                "Allocate inventory from nearest warehouse with stock."
            )

            action = "Inventory Reallocated"

        else:

            recommendation = (
                "Recalculate ETA using alternate route."
            )

            action = "ETA Updated"

        # =====================================================
        # AI Business Explanation
        # =====================================================

        explanation = (

            f"{event_type} detected. "

            f"Recommended action: {recommendation}"

        )

        recommendations.append({

            "disruption_id": event["disruption_id"],

            "shipment_id": shipment,

            "order_id": order,

            "event_type": event_type,

            "recommended_warehouse": warehouse_code,

            "recommended_vehicle": vehicle_id,

            "vehicle_type": vehicle_type,

            "recommended_driver": driver_id,

            "driver_name": driver_name,

            "estimated_delivery": eta_value,

            "recommended_action": action,

            "business_explanation": explanation

        })

    # =====================================================
    # Save Output
    # =====================================================

    recommendation_df = pd.DataFrame(recommendations)

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    recommendation_df.to_csv(
        output_path,
        index=False
    )

    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("RECOMMENDATION ENGINE SUMMARY")
    print("=" * 70)

    print(recommendation_df.head())

    print()

    print(f"Recommendations Generated : {len(recommendation_df)}")

    print(f"Affected Shipments         : {recommendation_df['shipment_id'].nunique()}")

    print()

    print("Recommended Actions")

    print("-" * 70)

    print(
        recommendation_df["recommended_action"]
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