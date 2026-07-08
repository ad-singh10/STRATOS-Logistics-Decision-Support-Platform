
"""
=========================================================
STRATOS
Module : Shipment Generator
=========================================================
"""

import os
import random
import time
from datetime import datetime, timedelta
import pandas as pd

ORDERS_FILE = "data/final/orders_master.csv"

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "shipments_master.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

STATUS = ["Ready"]*15 + ["In Transit"]*30 + ["Delivered"]*55

def dispatch_date(order_date):
    d = datetime.strptime(order_date,"%Y-%m-%d")
    return d + timedelta(days=random.randint(0,2))

def eta(dispatch, priority):
    days = random.randint(1,2) if priority=="Express" else random.randint(3,7)
    return dispatch + timedelta(days=days)

def main():

    start=time.time()

    print("="*70)
    print("STRATOS EXECUTION LAYER")
    print("Module : Shipment Generator")
    print("="*70)

    orders=pd.read_csv(ORDERS_FILE)

    rows=[]

    for i,order in orders.iterrows():

        disp=dispatch_date(order["order_date"])
        est=eta(disp, order["priority"])

        today = datetime(2025, 12, 31)
        
    
         #Shipment Status

        if disp > today:
         shipment_status = "Ready"

        elif est > today:
          shipment_status = "In Transit"

        else:
         shipment_status = "Delivered"

        rows.append({

            "shipment_id":f"SHP{i+1:06d}",
            "order_id":order["order_id"],

            "warehouse_id":order["warehouse_id"],
            "warehouse_code":order["warehouse_code"],

            "destination_city":order["destination_city"],

            "sku_id":order["sku_id"],
            "sku_code":order["sku_code"],

            "shipment_quantity":order["order_quantity"],

            "dispatch_date":disp.strftime("%Y-%m-%d"),
            "estimated_delivery":est.strftime("%Y-%m-%d"),

            "shipment_status":shipment_status

        })

    df=pd.DataFrame(rows)

    out=os.path.join(OUTPUT_DIR,OUTPUT_FILE)
    df.to_csv(out,index=False)

    print(df.head())
    print(f"\nShipments Generated : {len(df)}")
    print(f"Warehouses Used     : {df['warehouse_id'].nunique()}")
    print(f"Destination Cities  : {df['destination_city'].nunique()}")
    print(f"Products Shipped    : {df['sku_id'].nunique()}")
    print(f"\nSaved To : {out}")
    print(f"\nExecution Time : {round(time.time()-start,2)} sec")

if __name__=="__main__":
    main()
