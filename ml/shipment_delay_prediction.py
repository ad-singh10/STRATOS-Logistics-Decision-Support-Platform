"""
=========================================================
STRATOS
Module : Shipment Delay Prediction
=========================================================
"""

import os
import time
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# =========================================================
# Configuration
# =========================================================

MASTER_FILE = "decision_engine/outputs/master_decision.csv"

SPATIAL_FILE = "spatial/outputs/spatial_analysis.csv"

SUSTAINABILITY_FILE = "sustainability/outputs/sustainability_analysis.csv"

MODEL_DIR = "ml/models"

OUTPUT_DIR = "ml/outputs"

MODEL_FILE = "delay_prediction_model.pkl"

OUTPUT_FILE = "shipment_delay_predictions.csv"

os.makedirs(MODEL_DIR, exist_ok=True)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("="*70)
    print("STRATOS MACHINE LEARNING")
    print("Module : Shipment Delay Prediction")
    print("="*70)

    print("\nReading datasets...")

    master = pd.read_csv(MASTER_FILE)

    spatial = pd.read_csv(SPATIAL_FILE)

    sustainability = pd.read_csv(SUSTAINABILITY_FILE)

    print("Preparing ML Dataset...")

    df = master.merge(

        spatial[

            [

                "shipment_id",

                "distance_km",

                "distance_category",

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

                "sustainability_score"

            ]

        ],

        on="shipment_id",

        how="left"

    )

    df = df.drop_duplicates(

        subset="shipment_id"

    )

    print(f"Records : {len(df)}")

    print("\nEngineering Features...")


       # =====================================================
    # Business Target Creation
    # =====================================================

    delay_risk = []

    for _, row in df.iterrows():

        risk = 0

        # Distance

        if row["distance_category"] == "Long Distance":

            risk += 3

        elif row["distance_category"] == "Regional":

            risk += 2

        else:

            risk += 1

        # Priority

        if row["priority"] == "Express":

            risk += 2

        else:

            risk += 1

        # ETA

        if row["eta_status"] == "Long Distance":

            risk += 3

        elif row["eta_status"] == "In Transit":

            risk += 2

        else:

            risk += 1

        # Sustainability

        if row["sustainability_score"] <= 50:

            risk += 2

        elif row["sustainability_score"] <= 70:

            risk += 1

        # Coverage

        if row["coverage_status"] == "Secondary":

            risk += 1

        # Vehicle

        if row["vehicle_type"] == "Heavy Truck":

            risk += 1

        # Final Risk

        if risk >= 10:

            delay_risk.append("High")

        elif risk >= 7:

            delay_risk.append("Medium")

        else:

            delay_risk.append("Low")

    df["delay_risk"] = delay_risk

    # =====================================================
    # Feature Selection
    # =====================================================

    features = [

        "priority",

        "vehicle_type",

        "eta_status",

        "distance_category",

        "coverage_status",

        "sustainability_score"

    ]

    X = df[features].copy()

    y = df["delay_risk"]



    # =====================================================
    # Label Encoding
    # =====================================================

    encoders = {}

    categorical = [

        "priority",

        "vehicle_type",

        "eta_status",

        "distance_category",

        "coverage_status"

    ]

    for col in categorical:

        encoder = LabelEncoder()

        X[col] = encoder.fit_transform(

            X[col]

        )

        encoders[col] = encoder

    target_encoder = LabelEncoder()

    y = target_encoder.fit_transform(

        y

    )

    # =====================================================
    # Train Test Split
    # =====================================================

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=42,

        stratify=y

    )

    print(f"Training Samples : {len(X_train)}")

    print(f"Testing Samples  : {len(X_test)}")

    print("\nTraining Model...")


        # =====================================================
    # Random Forest Model
    # =====================================================

    model = RandomForestClassifier(

        n_estimators=200,

        max_depth=10,

        random_state=42

    )

    model.fit(

        X_train,

        y_train

    )

    # =====================================================
    # Predictions
    # =====================================================

    y_pred = model.predict(

        X_test

    )

    # =====================================================
    # Metrics
    # =====================================================

    accuracy = accuracy_score(

        y_test,

        y_pred

    )

    precision = precision_score(

        y_test,

        y_pred,

        average="weighted"

    )

    recall = recall_score(

        y_test,

        y_pred,

        average="weighted"

    )

    f1 = f1_score(

        y_test,

        y_pred,

        average="weighted"

    )

    cm = confusion_matrix(

        y_test,

        y_pred

    )

    report = classification_report(

        y_test,

        y_pred,

        target_names=target_encoder.classes_

    )

    # =====================================================
    # Feature Importance
    # =====================================================

    feature_importance = pd.DataFrame(

        {

            "Feature": features,

            "Importance": model.feature_importances_

        }

    )

    feature_importance = feature_importance.sort_values(

        by="Importance",

        ascending=False

    )

    print("\nModel Evaluation Complete.")


        # =====================================================
    # Predict Entire Dataset
    # =====================================================

    predictions = model.predict(X)

    prediction_labels = target_encoder.inverse_transform(

        predictions

    )

    df["predicted_delay_risk"] = prediction_labels

    # =====================================================
    # Save Model
    # =====================================================

    model_path = os.path.join(

        MODEL_DIR,

        MODEL_FILE

    )

    joblib.dump(

        model,

        model_path

    )

    # =====================================================
    # Save Predictions
    # =====================================================

    output = df[

        [

            "shipment_id",

            "order_id",

            "priority",

            "vehicle_type",

            "eta_status",

            "distance_category",

            "coverage_status",

            "sustainability_score",

            "predicted_delay_risk"

        ]

    ]

    output_path = os.path.join(

        OUTPUT_DIR,

        OUTPUT_FILE

    )

    output.to_csv(

        output_path,

        index=False

    )


    # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("SHIPMENT DELAY PREDICTION SUMMARY")
    print("=" * 70)

    print(output.head())

    print()

    print(f"Shipments Processed : {len(output)}")

    print(f"Training Dataset    : {len(X_train)} shipments")

    print(f"Validation Dataset  : {len(X_test)} shipments")

    print()

    print("Predicted Delay Risk")
    print("-" * 70)

    print(

        output["predicted_delay_risk"]

        .value_counts()

    )

    print()

    print(

        "High Risk Percentage :",

        round(

            (

                output["predicted_delay_risk"] == "High"

            ).mean() * 100,

            2

        ),

        "%"

    )

    print(

        "Medium Risk Percentage :",

        round(

            (

                output["predicted_delay_risk"] == "Medium"

            ).mean() * 100,

            2

        ),

        "%"

    )

    print(

        "Low Risk Percentage :",

        round(

            (

                output["predicted_delay_risk"] == "Low"

            ).mean() * 100,

            2

        ),

        "%"

    )

    print()

    print(f"Model Saved : {model_path}")

    print(f"Predictions : {output_path}")

    print()

    print(f"Execution Time : {round(time.time()-start,2)} sec")

    print("=" * 70)


# =========================================================
# Driver
# =========================================================

if __name__ == "__main__":

    main()
    