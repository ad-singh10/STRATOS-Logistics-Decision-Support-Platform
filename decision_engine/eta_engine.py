"""
=========================================================
STRATOS
Module : ETA Engine
=========================================================
"""

import os
import time
from datetime import timedelta
import pandas as pd

# =========================================================
# Configuration
# =========================================================

SHIPMENT_FILE = "data/final/shipments_master.csv"
VEHICLE_DECISION_FILE = "decision_engine/outputs/vehicle_decision.csv"

OUTPUT_DIR = "decision_engine/outputs"
OUTPUT_FILE = "eta_engine.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Vehicle Average Speed (km/hr)
# =========================================================

SPEED = {

    "Mini Truck":60,

    "Medium Truck":50,

    "Heavy Truck":40

}

# =========================================================
# Distance Generator
# =========================================================

def estimate_distance(city):

    value = abs(hash(city)) % 100

    if value < 30:

        return 40

    elif value < 60:

        return 180

    elif value < 80:

        return 450

    elif value < 95:

        return 900

    else:

        return 1500


# =========================================================
# Main
# =========================================================

def main():

    start=time.time()

    print("="*70)
    print("STRATOS DECISION ENGINE")
    print("Module : ETA Engine")
    print("="*70)

    print("\nReading datasets...")

    shipments=pd.read_csv(SHIPMENT_FILE)

    vehicle=pd.read_csv(VEHICLE_DECISION_FILE)

    vehicle_lookup={}

    for _,row in vehicle.iterrows():

        vehicle_lookup[row["shipment_id"]]={

            "vehicle_type":row["vehicle_type"]

        }

    rows=[]

    print("\nCalculating ETA...")

    for _,ship in shipments.iterrows():

        shipment_id=ship["shipment_id"]

        destination=ship["destination_city"]

        dispatch=pd.to_datetime(ship["dispatch_date"])

        vehicle_type=vehicle_lookup[shipment_id]["vehicle_type"]

        if vehicle_type=="No Vehicle":

            rows.append({

                "shipment_id":shipment_id,

                "destination_city":destination,

                "vehicle_type":"No Vehicle",

                "distance_km":None,

                "speed_kmph":None,

                "estimated_hours":None,

                "estimated_delivery":None,

                "eta_status":"Unavailable"

            })

            continue

        distance=estimate_distance(destination)

        speed=SPEED[vehicle_type]

        hours=round(distance/speed,2)

        eta=dispatch+timedelta(hours=hours)


                # -------------------------------------------------
        # ETA Status
        # -------------------------------------------------

        if hours <= 4:

            status = "On Time"

        elif hours <= 12:

            status = "In Transit"

        else:

            status = "Long Distance"

        rows.append({

            "shipment_id": shipment_id,

            "destination_city": destination,

            "vehicle_type": vehicle_type,

            "distance_km": distance,

            "speed_kmph": speed,

            "estimated_hours": hours,

            "estimated_delivery": eta.strftime("%Y-%m-%d %H:%M"),

            "eta_status": status

        })

    # =====================================================
    # Save Output
    # =====================================================

    eta_df = pd.DataFrame(rows)

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    eta_df.to_csv(

        output_path,

        index=False

    )

    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)

    print("ETA ENGINE SUMMARY")

    print("=" * 70)

    print(eta_df.head())

    print()

    print(f"Shipments Processed : {len(eta_df)}")

    print(f"Average ETA (hrs)  : {round(eta_df['estimated_hours'].mean(),2)}")

    print()

    print("ETA Status")

    print("-" * 70)

    print(

        eta_df["eta_status"]

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