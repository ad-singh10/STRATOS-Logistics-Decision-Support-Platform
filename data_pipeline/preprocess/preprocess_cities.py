"""
============================================================
STRATOS - Strategic Operations Intelligence Platform
Module : Cities Preprocessing
Author : Aditya Singh
============================================================
"""

import os
import time
import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = "data/external/cities/cities_raw.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_FILE = "cities_clean.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# Main
# ==========================================================

def main():

    start_time = time.time()

    print("=" * 65)
    print("STRATOS DATA PIPELINE")
    print("Module : Cities Preprocessing")
    print("=" * 65)

    # ------------------------------------------------------
    # Read Dataset
    # ------------------------------------------------------

    print("\nReading dataset...")

    df = pd.read_csv(INPUT_FILE)

    original_rows = len(df)

    print("Columns Found :", df.columns.tolist())
    print(f"Rows Loaded : {original_rows}")
    print(f"Columns     : {len(df.columns)}")

    # ------------------------------------------------------
    # Standardize Column Names
    # ------------------------------------------------------

    print("\nStandardizing column names...")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # ------------------------------------------------------
    # Clean City Names
    # ------------------------------------------------------

    print("\nCleaning city names...")

    df["location"] = (
        df["location"]
        .str.replace(" Latitude and Longitude", "", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.title()
    )

    # ------------------------------------------------------
    # Missing Values
    # ------------------------------------------------------

    print("\nChecking missing values...")

    missing = df.isnull().sum()

    print(missing)

    # ------------------------------------------------------
    # Remove Duplicates
    # ------------------------------------------------------

    print("\nRemoving duplicates...")

    duplicates = df.duplicated().sum()

    df = df.drop_duplicates()

    # ------------------------------------------------------
    # Validate Coordinates
    # ------------------------------------------------------

    print("\nValidating coordinates...")

    latitude_column = None
    longitude_column = None

    for column in df.columns:

        if "lat" in column:
            latitude_column = column

        if "lon" in column:
            longitude_column = column

    invalid_coordinates = 0

    if latitude_column and longitude_column:

        mask = (
            (df[latitude_column] >= -90)
            & (df[latitude_column] <= 90)
            & (df[longitude_column] >= -180)
            & (df[longitude_column] <= 180)
        )

        invalid_coordinates = (~mask).sum()

        df = df[mask]

    # ------------------------------------------------------
    # Save Clean Dataset
    # ------------------------------------------------------

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    df.to_csv(output_path, index=False)

    elapsed = round(time.time() - start_time, 2)

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    print("\n" + "=" * 65)
    print("PREPROCESSING SUMMARY")
    print("=" * 65)

    print(f"Original Rows        : {original_rows}")
    print(f"Duplicate Rows       : {duplicates}")
    print(f"Invalid Coordinates  : {invalid_coordinates}")
    print(f"Final Rows           : {len(df)}")

    print(f"\nSaved To : {output_path}")

    print(f"\nExecution Time : {elapsed} seconds")

    print("=" * 65)


# ==========================================================

if __name__ == "__main__":
    main()