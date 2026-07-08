"""
=========================================================
STRATOS
Module : AI Decision Engine
=========================================================
"""

import os
import time

import pandas as pd

# =========================================================
# Configuration
# =========================================================

MASTER_FILE = "decision_engine/outputs/master_decision.csv"

SPATIAL_FILE = "spatial/outputs/spatial_analysis.csv"

SUSTAINABILITY_FILE = "sustainability/outputs/sustainability_analysis.csv"

ML_FILE = "ml/outputs/shipment_delay_predictions.csv"

DISRUPTION_FILE = "simulation/outputs/disruption_events.csv"

OUTPUT_DIR = "decision_engine/outputs"

OUTPUT_FILE = "ai_decision_engine.csv"

os.makedirs(

    OUTPUT_DIR,

    exist_ok=True

)

# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS AI DECISION ENGINE")
    print("Module : Intelligent Decision Support")
    print("=" * 70)

    print("\nReading datasets...")

    master = pd.read_csv(MASTER_FILE)

    spatial = pd.read_csv(SPATIAL_FILE)

    sustainability = pd.read_csv(SUSTAINABILITY_FILE)

    ml = pd.read_csv(ML_FILE)

    disruptions = pd.read_csv(DISRUPTION_FILE)

    print("Preparing Enterprise Decision Dataset...")

    df = master.merge(

        spatial[

            [

                "shipment_id",

                "distance_category",

                "route_priority",

                "coverage_status"

            ]

        ],

        on="shipment_id",

        how="left"

    )

    df = df.merge(

        sustainability[

            [

                "shipment_id",

                "sustainability_score",

                "green_shipment"

            ]

        ],

        on="shipment_id",

        how="left"

    )

    df = df.merge(

        ml[

            [

                "shipment_id",

                "predicted_delay_risk"

            ]

        ],

        on="shipment_id",

        how="left"

    )

    df = df.merge(

        disruptions[

            [

                "shipment_id",

                "event_type",

                "severity"

            ]

        ],

        on="shipment_id",

        how="left"

    )

    df = df.drop_duplicates(
        subset="shipment_id",
        keep="first"
    )

    df = df.fillna(

        {

            "event_type": "No Disruption",

            "severity": "None"

        }

    )

    print(f"Integrated Shipments : {len(df)}")

    rows = []

    print("\nRunning AI Decision Engine...")


       # =====================================================
    # AI Decision Logic
    # =====================================================

    for _, row in df.iterrows():

        ops = 0

        # ---------------------------------------------
        # Shipment Priority
        # ---------------------------------------------

        if row["priority"] == "Express":

            ops += 25

        else:

            ops += 10

        # ---------------------------------------------
        # Delay Risk (Machine Learning)
        # ---------------------------------------------

        if row["predicted_delay_risk"] == "High":

            ops += 30

        elif row["predicted_delay_risk"] == "Medium":

            ops += 20

        else:

            ops += 10

        # ---------------------------------------------
        # Route Priority
        # ---------------------------------------------

        if row["route_priority"] == "High":

            ops += 20

        elif row["route_priority"] == "Medium":

            ops += 12

        else:

            ops += 6

        # ---------------------------------------------
        # Sustainability
        # ---------------------------------------------

        if row["green_shipment"] == "Yes":

            ops += 5

        else:

            ops += 10

        # ---------------------------------------------
        # Coverage
        # ---------------------------------------------

        if row["coverage_status"] == "Secondary":

            ops += 5

        # ---------------------------------------------
        # Disruption Severity
        # ---------------------------------------------

        if row["severity"] == "Critical":

            ops += 25

        elif row["severity"] == "High":

            ops += 18

        elif row["severity"] == "Medium":

            ops += 10

        # ---------------------------------------------
        # Normalize Score
        # ---------------------------------------------

        ops = min(100, ops)

        # =====================================================
        # Operational Priority
        # =====================================================

        if ops >= 85:

            operational_priority = "Critical"

        elif ops >= 70:

            operational_priority = "High"

        elif ops >= 50:

            operational_priority = "Medium"

        else:

            operational_priority = "Low"

        # =====================================================
        # Containers
        # =====================================================

        rows.append({

            "shipment_id": row["shipment_id"],

            "order_id": row["order_id"],

            "priority": row["priority"],

            "predicted_delay_risk": row["predicted_delay_risk"],

            "route_priority": row["route_priority"],

            "coverage_status": row["coverage_status"],

            "green_shipment": row["green_shipment"],

            "event_type": row["event_type"],

            "severity": row["severity"],

            "operational_priority_score": ops,

            "operational_priority": operational_priority

        })

    # =====================================================
    # Create Output
    # =====================================================

    decision_df = pd.DataFrame(rows)

    # =====================================================
    # AI Recommendation
    # =====================================================

    recommendations = []

    explanations = []

    for _, row in decision_df.iterrows():

        if row["severity"] == "Critical":

            recommendation = "Emergency Escalation"

            explanation = (
                "Critical operational disruption detected. "
                "Immediate intervention required."
            )

        elif row["predicted_delay_risk"] == "High":

            recommendation = "Prioritize Dispatch"

            explanation = (
                "Shipment has high delay risk. "
                "Prioritize dispatch to reduce service impact."
            )

        elif row["event_type"] != "No Disruption":

            recommendation = "Mitigate Disruption"

            explanation = (
                "Active disruption detected. "
                "Apply contingency plan."
            )

        elif row["green_shipment"] == "No":

            recommendation = "Recommend Green Fleet"

            explanation = (
                "Shipment sustainability score is low. "
                "Consider greener fleet allocation."
            )

        elif row["coverage_status"] == "Secondary":

            recommendation = "Review Warehouse Assignment"

            explanation = (
                "Shipment is assigned through a secondary warehouse. "
                "Review routing efficiency."
            )

        else:

            recommendation = "Proceed with Dispatch"

            explanation = (
                "Shipment is operationally ready. "
                "No intervention required."
            )

        recommendations.append(recommendation)

        explanations.append(explanation)

    decision_df["recommended_action"] = recommendations

    decision_df["business_explanation"] = explanations

    # =====================================================
    # Save Output
    # =====================================================

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    decision_df.to_csv(

        output_path,

        index=False

    )

    print("\nAI Decisions Generated.")


        # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("AI DECISION ENGINE SUMMARY")
    print("=" * 70)

    print(decision_df.head())

    print()

    print(f"Shipments Analysed : {len(decision_df)}")

    print()

    print("Operational Priority")
    print("-" * 70)

    print(

        decision_df["operational_priority"]

        .value_counts()

    )

    print()

    print("Recommended Actions")
    print("-" * 70)

    print(

        decision_df["recommended_action"]

        .value_counts()

    )

    print()

    print("Average Operational Priority Score :",

          round(

              decision_df["operational_priority_score"].mean(),

              2

          )

    )

    print()

    print(

        "Critical Shipments :",

        round(

            (

                decision_df["operational_priority"] == "Critical"

            ).mean() * 100,

            2

        ),

        "%"

    )

    print(

        "High Priority Shipments :",

        round(

            (

                decision_df["operational_priority"] == "High"

            ).mean() * 100,

            2

        ),

        "%"

    )

    print(

        "Medium Priority Shipments :",

        round(

            (

                decision_df["operational_priority"] == "Medium"

            ).mean() * 100,

            2

        ),

        "%"

    )

    print(

        "Low Priority Shipments :",

        round(

            (

                decision_df["operational_priority"] == "Low"

            ).mean() * 100,

            2

        ),

        "%"

    )

    print()

    print(f"Saved To : {output_path}")

    print()

    print(f"Execution Time : {round(time.time()-start,2)} sec")

    print("=" * 70)


# =========================================================
# Driver
# =========================================================

if __name__ == "__main__":

    main()