"""
=========================================================
STRATOS
Module : Disruption Events Generator
=========================================================
"""

import os
import time
import random
from datetime import datetime

import pandas as pd

# =========================================================
# Configuration
# =========================================================

MASTER_FILE = "decision_engine/outputs/master_decision.csv"
FLEET_FILE = "data/final/fleet_master.csv"
DRIVER_FILE = "data/final/drivers_master.csv"
WAREHOUSE_FILE = "data/final/warehouses_master.csv"
INVENTORY_FILE = "data/final/inventory_master.csv"

OUTPUT_DIR = "simulation/outputs"
OUTPUT_FILE = "disruption_events.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

# =========================================================
# Event Probabilities
# =========================================================

VEHICLE_BREAKDOWN = 0.02
DRIVER_ABSENCE = 0.015
WAREHOUSE_SHUTDOWN = 0.005
INVENTORY_SHORTAGE = 0.03
WEATHER_DELAY = 0.04


# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("="*70)
    print("STRATOS SIMULATION LAYER")
    print("Module : Disruption Events Generator")
    print("="*70)

    print("\nReading datasets...")

    master = pd.read_csv(MASTER_FILE)
    fleet = pd.read_csv(FLEET_FILE)
    drivers = pd.read_csv(DRIVER_FILE)
    warehouses = pd.read_csv(WAREHOUSE_FILE)
    inventory = pd.read_csv(INVENTORY_FILE)
    shipments = pd.read_csv("data/final/shipments_master.csv")

    destination_lookup = dict(
    zip(
        shipments["shipment_id"],
        shipments["destination_city"]
    )
)

    rows = []

    disruption_id = 1

    print("\nGenerating disruptions...")

    for _, shipment in master.iterrows():

        shipment_id = shipment["shipment_id"]

        order_id = shipment["order_id"]

        warehouse = shipment["warehouse_code"]

        vehicle = shipment["vehicle_id"]

        driver = shipment["driver_id"]

        eta = shipment["estimated_delivery"]

        priority = shipment["priority"]

        # =====================================================
        # Vehicle Breakdown
        # =====================================================

        if random.random() < VEHICLE_BREAKDOWN:

            rows.append({

                "disruption_id": f"DIS{disruption_id:06d}",

                "shipment_id": shipment_id,

                "order_id": order_id,

                "event_type": "Vehicle Breakdown",

                "affected_resource": vehicle,

                "warehouse_code": warehouse,

                "severity": "High",

                "priority": priority,

                "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "impact": "Vehicle Unavailable",

                "status": "Active"

            })

            disruption_id += 1

        # =====================================================
        # Driver Absence
        # =====================================================

        if random.random() < DRIVER_ABSENCE:

            rows.append({

                "disruption_id": f"DIS{disruption_id:06d}",

                "shipment_id": shipment_id,

                "order_id": order_id,

                "event_type": "Driver Absence",

                "affected_resource": driver,

                "warehouse_code": warehouse,

                "severity": "Medium",

                "priority": priority,

                "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "impact": "Driver Unavailable",

                "status": "Active"

            })

            disruption_id += 1

        # =====================================================
        # Warehouse Shutdown
        # =====================================================

        if random.random() < WAREHOUSE_SHUTDOWN:

            rows.append({

                "disruption_id": f"DIS{disruption_id:06d}",

                "shipment_id": shipment_id,

                "order_id": order_id,

                "event_type": "Warehouse Shutdown",

                "affected_resource": warehouse,

                "warehouse_code": warehouse,

                "severity": "Critical",

                "priority": priority,

                "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "impact": "Warehouse Closed",

                "status": "Active"

            })

            disruption_id += 1


        # =====================================================
        # Inventory Shortage
        # =====================================================

        if random.random() < INVENTORY_SHORTAGE:

            rows.append({

                "disruption_id": f"DIS{disruption_id:06d}",

                "shipment_id": shipment_id,

                "order_id": order_id,

                "event_type": "Inventory Shortage",

                "affected_resource": warehouse,

                "warehouse_code": warehouse,

                "severity": "Medium",

                "priority": priority,

                "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "impact": "Low Inventory",

                "status": "Active"

            })

            disruption_id += 1

        # =====================================================
        # Weather Delay
        # =====================================================

        if random.random() < WEATHER_DELAY:

            rows.append({

                "disruption_id": f"DIS{disruption_id:06d}",

                "shipment_id": shipment_id,

                "order_id": order_id,

                "event_type": "Weather Delay",

                "affected_resource": destination_lookup[shipment_id],

                "warehouse_code": warehouse,

                "severity": "Medium",

                "priority": priority,

                "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "impact": "ETA Increased",

                "status": "Active"

            })

            disruption_id += 1

    # =====================================================
    # Save Output
    # =====================================================

    disruption_df = pd.DataFrame(rows)

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    disruption_df.to_csv(
        output_path,
        index=False
    )

    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("DISRUPTION EVENTS SUMMARY")
    print("=" * 70)

    print(disruption_df.head())

    print()

    print(f"Total Disruptions : {len(disruption_df)}")

    print(f"Affected Shipments : {disruption_df['shipment_id'].nunique()}")

    print()

    print("Event Types")

    print("-" * 70)

    print(
        disruption_df["event_type"]
        .value_counts()
    )

    print()

    print("Severity")

    print("-" * 70)

    print(
        disruption_df["severity"]
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