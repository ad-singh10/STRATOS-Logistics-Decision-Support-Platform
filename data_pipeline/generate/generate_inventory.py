"""
=========================================================
STRATOS
Module : Inventory Master Generator
=========================================================
"""

import os
import time
from datetime import datetime
import pandas as pd
import random

# =========================================================
# Configuration
# =========================================================

WAREHOUSE_FILE = "data/final/warehouses_master.csv"
PRODUCT_FILE = "data/final/products_master.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "inventory_master.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

CATEGORY_MULTIPLIER = {
    "FMCG": 1.60,
    "Grocery": 1.50,
    "Apparel": 0.90,
    "Healthcare": 0.80,
    "Home & Kitchen": 0.70,
    "Electronics": 0.60,
    "Automotive": 0.50
}

SKU_LIMIT = {
    "Critical": 75,
    "High": 65,
    "Medium": 50
}

random.seed(42)

# =========================================================
# Inventory Status
# =========================================================

def status(stock, reorder):

    if stock == 0:
        return "Out of Stock"

    elif stock <= reorder:
        return "Low Stock"

    else:
        return "Normal"

# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS EXECUTION LAYER")
    print("Module : Inventory Master Generator")
    print("=" * 70)

    warehouses = pd.read_csv(WAREHOUSE_FILE)
    products = pd.read_csv(PRODUCT_FILE)

    rows = []

    inv = 1

    today = datetime.today().strftime("%Y-%m-%d")

    for _, wh in warehouses.iterrows():

        limit = SKU_LIMIT[wh["warehouse_priority"]]

        subset = products.sample(
            n=min(limit, len(products)),
            random_state=int(wh.name) + 10
        )

        capacity_per_sku = max(
            wh["operating_capacity"] / limit,
            50
        )

        for _, p in subset.iterrows():

            category_multiplier = CATEGORY_MULTIPLIER[p["category"]]
            velocity_multiplier = p["velocity_multiplier"]

            # -------------------------------------------------
            # Base Stock
            # -------------------------------------------------

            base_stock = int(

                capacity_per_sku
                * category_multiplier
                * velocity_multiplier

            )

            # -------------------------------------------------
            # Inventory Simulation
            # -------------------------------------------------

            scenario = random.random()

            # 90% Normal Stock
            if scenario < 0.90:

                stock = int(
                    base_stock *
                    random.uniform(0.85, 1.15)
                )

            # 8% Low Stock
            elif scenario < 0.98:

                stock = int(
                    base_stock *
                    random.uniform(0.15, 0.40)
                )

            # 2% Out of Stock
            else:

                stock = random.randint(0, 5)

            # -------------------------------------------------
            # Reorder Level
            # -------------------------------------------------

            reorder = max(

                int(base_stock * 0.25),

                10

            )

            value = stock * p["unit_price"]

            rows.append({

                "inventory_id": f"INV{inv:06d}",

                "warehouse_id": wh["warehouse_id"],

                "warehouse_code": wh["warehouse_code"],

                "sku_id": p["sku_id"],

                "sku_code": p["sku_code"],

                "product_name": p["product_name"],

                "category": p["category"],

                "current_stock": stock,

                "reorder_level": reorder,

                "inventory_value": value,

                "inventory_status": status(stock, reorder),

                "last_updated": today

            })

            inv += 1

    df = pd.DataFrame(rows)

    output = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    df.to_csv(output, index=False)

    print("\n" + "=" * 70)
    print("INVENTORY MASTER SUMMARY")
    print("=" * 70)

    print(df.head())

    print(f"\nInventory Records : {len(df)}")
    print(f"Warehouses        : {df['warehouse_id'].nunique()}")
    print(f"Unique Products   : {df['sku_id'].nunique()}")
    print(f"Total Stock       : {df['current_stock'].sum():,}")
    print(f"Inventory Value   : ₹{df['inventory_value'].sum():,.0f}")

    print("\nInventory Status Distribution")
    print("-" * 70)
    print(df["inventory_status"].value_counts())

    print(f"\nSaved To : {output}")

    print(f"\nExecution Time : {round(time.time() - start, 2)} sec")

    print("=" * 70)


# =========================================================
# Driver
# =========================================================

if __name__ == "__main__":

    main()