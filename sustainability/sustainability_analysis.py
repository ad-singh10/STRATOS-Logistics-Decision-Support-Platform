"""
=========================================================
STRATOS
Module : Sustainability Analytics
=========================================================
"""

import os
import time
import pandas as pd

# =========================================================
# Configuration
# =========================================================

FLEET_FILE = "data/final/fleet_master.csv"

SPATIAL_FILE = "spatial/outputs/spatial_analysis.csv"

VEHICLE_FILE = "decision_engine/outputs/vehicle_decision.csv"

ETA_FILE = "decision_engine/outputs/eta_engine.csv"

OUTPUT_DIR = "sustainability/outputs"

OUTPUT_FILE = "sustainability_analysis.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

EMISSION_FACTOR = 2.68

# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS SUSTAINABILITY LAYER")
    print("Module : Sustainability Analytics")
    print("=" * 70)

    print("\nReading datasets...")

    fleet = pd.read_csv(FLEET_FILE)

    spatial = pd.read_csv(SPATIAL_FILE)

    vehicle = pd.read_csv(VEHICLE_FILE)

    eta = pd.read_csv(ETA_FILE)

    print("Creating lookup tables...")

    fleet_lookup = fleet.set_index("vehicle_id")

    spatial_lookup = spatial.set_index("shipment_id")

    eta_lookup = eta.set_index("shipment_id")

    rows = []

    print("\nCalculating Sustainability Metrics...")

    # =====================================================
    # Calculate Sustainability Metrics
    # =====================================================

    for _, row in vehicle.iterrows():

        shipment = row["shipment_id"]

        vehicle_id = row["vehicle_id"]

        fleet_row = fleet_lookup.loc[vehicle_id]

        spatial_row = spatial_lookup.loc[shipment]

        eta_row = eta_lookup.loc[shipment]

        # =====================================================
        # Distance
        # =====================================================

        distance = spatial_row["distance_km"]

        # =====================================================
        # Fuel Efficiency
        # =====================================================

        fuel_efficiency = round(

            fleet_row["fuel_efficiency_kmpl"],

            2

        )

        # =====================================================
        # Fuel Consumption
        # =====================================================

        fuel = round(

            distance / fuel_efficiency,

            2

        )

        # =====================================================
        # CO2 Emission
        # =====================================================

        co2 = round(

            fuel * EMISSION_FACTOR,

            2

        )

        # =====================================================
        # Carbon Intensity
        # =====================================================

        if distance == 0:

            carbon_intensity = 0

        else:

            carbon_intensity = round(

                co2 / distance,

                3

            )

        # =====================================================
        # Sustainability Score
        # =====================================================

        if co2 < 60:

            score = 100

            category = "Excellent"

        elif co2 < 100:

            score = 85

            category = "Good"

        elif co2 < 180:

            score = 70

            category = "Average"

        else:

            score = 50

            category = "Poor"

        # =====================================================
        # Green Shipment
        # =====================================================

        if score >= 70:

            green = "Yes"

        else:

            green = "No"

        # =====================================================
        # Store Results
        # =====================================================

        rows.append({

            "shipment_id": shipment,

            "vehicle_id": vehicle_id,

            "distance_km": round(distance, 2),

            "fuel_efficiency_kmpl": fuel_efficiency,

            "fuel_consumption_l": fuel,

            "co2_emission_kg": co2,

            "carbon_intensity": carbon_intensity,

            "estimated_delivery": eta_row["estimated_delivery"],

            "eta_status": eta_row["eta_status"],

            "sustainability_score": score,

            "green_shipment": green,

            "sustainability_category": category

        })

    # =====================================================
    # Create Output
    # =====================================================

    sustainability_df = pd.DataFrame(rows)

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    sustainability_df.to_csv(

        output_path,

        index=False

    )
    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("SUSTAINABILITY SUMMARY")
    print("=" * 70)

    print(sustainability_df.head())

    print()

    print(f"Shipments Analysed : {len(sustainability_df)}")

    print(

        f"Average Fuel Consumption : {round(sustainability_df['fuel_consumption_l'].mean(),2)} L"

    )

    print(

        f"Average CO2 Emission : {round(sustainability_df['co2_emission_kg'].mean(),2)} kg"

    )

    print()

    # =====================================================
    # Green Shipments
    # =====================================================

    print("Green Shipments")

    print("-" * 70)

    green_counts = (

        sustainability_df["green_shipment"]

        .value_counts()

    )

    green_percent = round(

        green_counts / len(sustainability_df) * 100,

        2

    )

    for label, count in green_counts.items():

        print(

            f"{label:<5}: {count:>5} ({green_percent[label]}%)"

        )

    print()

    # =====================================================
    # Sustainability Category
    # =====================================================

    print("Sustainability Category")

    print("-" * 70)

    category_counts = (

        sustainability_df["sustainability_category"]

        .value_counts()

    )

    category_percent = round(

        category_counts / len(sustainability_df) * 100,

        2

    )

    for label, count in category_counts.items():

        print(

            f"{label:<10}: {count:>5} ({category_percent[label]}%)"

        )

    print()

    # =====================================================
    # Sustainability Score
    # =====================================================

    print("Sustainability Score")

    print("-" * 70)

    score_counts = (

        sustainability_df["sustainability_score"]

        .value_counts()

        .sort_index(ascending=False)

    )

    score_percent = round(

        score_counts / len(sustainability_df) * 100,

        2

    )

    for label, count in score_counts.items():

        print(

            f"{label:<3}: {count:>5} ({score_percent[label]}%)"

        )

    print()

    print(f"Saved To : {output_path}")

    print()

    print(

        f"Execution Time : {round(time.time() - start,2)} sec"

    )

    print("=" * 70)


# =========================================================
# Driver
# =========================================================

if __name__ == "__main__":

    main()    