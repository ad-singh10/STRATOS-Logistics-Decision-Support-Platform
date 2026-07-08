"""
=========================================================
STRATOS
Module : Warehouse Decision Engine
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

ORDERS_FILE = "data/final/orders_master.csv"
INVENTORY_FILE = "data/final/inventory_master.csv"
WAREHOUSE_FILE = "data/final/warehouses_master.csv"
CAPACITY_FILE = "data/final/warehouse_capacity.csv"
CITY_MAPPING_FILE = "data/final/city_warehouse_mapping.csv"

OUTPUT_DIR = "decision_engine/outputs"
OUTPUT_FILE = "warehouse_decision.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

UTILIZATION_LIMIT = 0.90

import pandas as pd

df = pd.read_csv("data/final/city_warehouse_mapping.csv")

print(df.columns.tolist())
# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS DECISION ENGINE")
    print("Module : Warehouse Decision")
    print("=" * 70)

    print("\nReading datasets...")

    orders = pd.read_csv(ORDERS_FILE)
    inventory = pd.read_csv(INVENTORY_FILE)
    warehouses = pd.read_csv(WAREHOUSE_FILE)
    capacity = pd.read_csv(CAPACITY_FILE)
    mapping = pd.read_csv(CITY_MAPPING_FILE)

    print("Creating lookup tables...")

    # -----------------------------------------------------
    # Inventory Lookup
    # Key :
    # (warehouse_id, sku_id)
    # -----------------------------------------------------

    inventory_lookup = {}

    for _, row in inventory.iterrows():

        inventory_lookup[(

            row["warehouse_id"],
            row["sku_id"]

        )] = {

            "stock": row["current_stock"],
            "reorder": row["reorder_level"]

        }

       
    # -----------------------------------------------------
    # Warehouse Status Lookup
    # -----------------------------------------------------

    warehouse_lookup = {}

    for _, row in warehouses.iterrows():

        warehouse_lookup[row["warehouse_id"]] = {

            "warehouse_code": row["warehouse_code"],
            "warehouse_city": row["warehouse_city"],
            "is_active": row["is_active"]

        }

    # -----------------------------------------------------
    # Backup Warehouse Lookup
    # -----------------------------------------------------

    backup_lookup = {}

    for _, row in mapping.iterrows():

        backup_lookup[row["city"]] = {

            "default": row["default_warehouse"],
            "backup": row["backup_warehouse"]

        }

    print("Lookup tables created successfully.")

    # -----------------------------------------------------
    # Decision Engine Starts Here
    # -----------------------------------------------------

    decision_rows = []

    same = 0
    changed = 0

    print("\nEvaluating warehouse decisions...")

    # =====================================================
    # Warehouse Decision Logic
    # =====================================================

    for _, order in orders.iterrows():

        order_id = order["order_id"]

        warehouse_id = order["warehouse_id"]

        sku_id = order["sku_id"]

        quantity = order["order_quantity"]

        destination_city = order["destination_city"]

        recommended_warehouse = warehouse_id

        decision_reason = "Optimal"

        # -------------------------------------------------
        # Rule 1 : Inventory Availability
        # -------------------------------------------------

        inventory_key = (warehouse_id, sku_id)

        if inventory_key in inventory_lookup:

            current_stock = inventory_lookup[inventory_key]["stock"]

            reorder_level = inventory_lookup[inventory_key]["reorder"]

            remaining_stock = current_stock - quantity

            if remaining_stock < reorder_level:

                recommended_city = backup_lookup[destination_city]["backup"]

                backup = warehouses[
                    warehouses["warehouse_city"] == recommended_city
                ]

                if not backup.empty:

                    recommended_warehouse = backup.iloc[0]["warehouse_id"]

                    decision_reason = "Low Inventory"

        else:

            recommended_city = backup_lookup[destination_city]["backup"]

            backup = warehouses[
                warehouses["warehouse_city"] == recommended_city
            ]

            if not backup.empty:

                recommended_warehouse = backup.iloc[0]["warehouse_id"]

                decision_reason = "SKU Not Available"

       

        # -------------------------------------------------
        # Rule 2 : Warehouse Active
        # -------------------------------------------------

        if not warehouse_lookup[recommended_warehouse]["is_active"]:

            recommended_city = backup_lookup[destination_city]["backup"]

            backup = warehouses[
                warehouses["warehouse_city"] == recommended_city
            ]

            if not backup.empty:

                recommended_warehouse = backup.iloc[0]["warehouse_id"]

                decision_reason = "Warehouse Inactive"

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        if recommended_warehouse == warehouse_id:

            same += 1

        else:

            changed += 1

        # -------------------------------------------------
        # Save Decision
        # -------------------------------------------------

        decision_rows.append({

            "order_id": order_id,

            "destination_city": destination_city,

            "original_warehouse": warehouse_lookup[
                warehouse_id
            ]["warehouse_code"],

            "recommended_warehouse": warehouse_lookup[
                recommended_warehouse
            ]["warehouse_code"],

            "decision_reason": decision_reason

        })

    # =====================================================
    # Create Output DataFrame
    # =====================================================

    decision_df = pd.DataFrame(decision_rows)

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    decision_df.to_csv(

        output_path,

        index=False

    )

    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("WAREHOUSE DECISION SUMMARY")
    print("=" * 70)

    print(decision_df.head())

    print()

    print(f"Orders Processed              : {len(decision_df)}")
    print(f"Original Warehouse Selected   : {same}")
    print(f"Backup Warehouse Recommended  : {changed}")

    print()

    print("Decision Reasons")

    print("-" * 70)

    print(

        decision_df["decision_reason"]

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