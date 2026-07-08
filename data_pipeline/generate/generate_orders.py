
"""
=========================================================
STRATOS
Module : Orders Generator
=========================================================
"""

import os
import random
import time
from datetime import datetime, timedelta
import pandas as pd

# =========================================================
# Configuration
# =========================================================

WAREHOUSE_FILE = "data/final/warehouses_master.csv"
INVENTORY_FILE = "data/final/inventory_master.csv"
CITIES_FILE = "data/final/cities_master.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "orders_master.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_ORDERS = 10000

random.seed(42)

PRIORITY = ["Standard"] * 80 + ["Express"] * 20
STATUS = ["Pending", "Allocated", "Dispatched"]

# =========================================================

def random_date():

    start = datetime(2025, 1, 1)
    end = datetime(2025, 12, 31)

    return (
        start +
        timedelta(days=random.randint(0, (end - start).days))
    ).strftime("%Y-%m-%d")

# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS EXECUTION LAYER")
    print("Module : Orders Generator")
    print("=" * 70)

    print("\nReading datasets...")

    warehouses = pd.read_csv(WAREHOUSE_FILE)
    inventory = pd.read_csv(INVENTORY_FILE)
    cities = pd.read_csv(CITIES_FILE)

    wh_lookup = warehouses.set_index("warehouse_id")

    rows = []

    for i in range(1, NUM_ORDERS + 1):

        # Random product from inventory
        item = inventory.sample(1).iloc[0]

        # Warehouse fulfilling the order
        wh = wh_lookup.loc[item["warehouse_id"]]

        # Random destination city
        city = cities.sample(1,random_state=None).iloc[0]

        # Order quantity
        qty = random.randint(
            1,
            max(5, int(item["current_stock"] * 0.05))
        )

        rows.append({

            "order_id": f"ORD{i:06d}",

            "order_date": random_date(),

            "customer_id": f"CUST{random.randint(1,3000):05d}",

            "destination_city": city["city"],

            "warehouse_id": item["warehouse_id"],

            "warehouse_code": item["warehouse_code"],

            "sku_id": item["sku_id"],

            "sku_code": item["sku_code"],

            "product_name": item["product_name"],

            "category": item["category"],

            "order_quantity": qty,

            "priority": random.choice(PRIORITY),

            "order_status": random.choice(STATUS)

        })

    df = pd.DataFrame(rows)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    df.to_csv(output_path, index=False)

    print("\n" + "=" * 70)
    print("ORDERS SUMMARY")
    print("=" * 70)

    print(df.head())

    print(f"\nOrders Generated : {len(df)}")
    print(f"Unique Customers : {df['customer_id'].nunique()}")
    print(f"Unique Products  : {df['sku_id'].nunique()}")
    print(f"Warehouses Used  : {df['warehouse_id'].nunique()}")

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {round(time.time() - start, 2)} sec")

    print("=" * 70)

# =========================================================

if __name__ == "__main__":
    main()
