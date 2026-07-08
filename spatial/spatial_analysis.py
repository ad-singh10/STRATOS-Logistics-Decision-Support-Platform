"""
=========================================================
STRATOS
Module : Spatial Intelligence using GeoPandas
=========================================================
"""

import os
import time

import pandas as pd
import geopandas as gpd

from shapely.geometry import Point
from shapely.geometry import LineString

# =========================================================
# Configuration
# =========================================================

MASTER_FILE = "decision_engine/outputs/master_decision.csv"

ORDERS_FILE = "data/final/orders_master.csv"

CITY_FILE = "data/final/city_coordinates.csv"

WAREHOUSE_FILE = "data/final/warehouses_master.csv"

OUTPUT_DIR = "spatial/outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Main
# =========================================================

def main():

    start = time.time()

    print("=" * 70)
    print("STRATOS SPATIAL INTELLIGENCE")
    print("Module : GeoPandas Spatial Analytics")
    print("=" * 70)

    print("\nReading datasets...")

    master = pd.read_csv(MASTER_FILE)

    orders = pd.read_csv(ORDERS_FILE)

    cities = pd.read_csv(CITY_FILE)

    warehouses = pd.read_csv(WAREHOUSE_FILE)

    # =====================================================
    # Standardize Text
    # =====================================================

    orders["destination_city"] = (

        orders["destination_city"]

        .astype(str)

        .str.strip()

        .str.lower()

    )

    cities["city"] = (

        cities["city"]

        .astype(str)

        .str.strip()

        .str.lower()

    )

    warehouses["warehouse_city"] = (

        warehouses["warehouse_city"]

        .astype(str)

        .str.strip()

        .str.lower()

    )

    # =====================================================
    # Merge Datasets
    # =====================================================

    print("\nPreparing Spatial Dataset...")

    spatial = (

        master

        .merge(

            orders[

                [

                    "order_id",

                    "destination_city"

                ]

            ],

            on="order_id",

            how="left"

        )

        .merge(

            cities,

            left_on="destination_city",

            right_on="city",

            how="left"

        )

        .drop_duplicates(

            subset="shipment_id"

        )

    )

    print(f"Spatial Records : {len(spatial)}")

    # =====================================================
    # Warehouse GeoDataFrame
    # =====================================================

    warehouse_gdf = gpd.GeoDataFrame(

        warehouses,

        geometry=gpd.points_from_xy(

            warehouses["longitude"],

            warehouses["latitude"]

        ),

        crs="EPSG:4326"

    )

    # =====================================================
    # Destination City GeoDataFrame
    # =====================================================

    city_gdf = gpd.GeoDataFrame(

        cities,

        geometry=gpd.points_from_xy(

            cities["longitude"],

            cities["latitude"]

        ),

        crs="EPSG:4326"

    )

    # =====================================================
    # Export Base GeoJSON Layers
    # =====================================================

    warehouse_gdf.to_file(

        f"{OUTPUT_DIR}/warehouse_points.geojson",

        driver="GeoJSON"

    )

    city_gdf.to_file(

        f"{OUTPUT_DIR}/city_points.geojson",

        driver="GeoJSON"

    )

    print("Base GeoJSON Layers Created.")

    # =====================================================
    # Containers
    # =====================================================

    rows = []

    routes = []

    print("\nRunning Spatial Intelligence...")

    # =====================================================
    # Warehouse Lookup
    # =====================================================

    warehouse_lookup = warehouse_gdf.set_index("warehouse_code")

    # =====================================================
    # Shipment Loop
    # =====================================================

    for _, row in spatial.iterrows():

        shipment_id = row["shipment_id"]

        order_id = row["order_id"]

        warehouse_code = row["warehouse_code"]

        destination_city = row["destination_city"]

        # Skip rows with missing coordinates
        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):

            continue

        if warehouse_code not in warehouse_lookup.index:

            continue

        warehouse = warehouse_lookup.loc[warehouse_code]

        # =================================================
        # Geometry Objects
        # =================================================

        warehouse_point = warehouse.geometry

        destination_point = Point(

            row["longitude"],

            row["latitude"]

        )

        # =================================================
        # Metric CRS
        # =================================================

        warehouse_metric = gpd.GeoSeries(

            [warehouse_point],

            crs="EPSG:4326"

        ).to_crs(epsg=3857)

        destination_metric = gpd.GeoSeries(

            [destination_point],

            crs="EPSG:4326"

        ).to_crs(epsg=3857)

        # =================================================
        # Distance
        # =================================================

        distance_km = round(

            warehouse_metric.distance(

                destination_metric

            ).iloc[0] / 1000,

            2

        )

        # =================================================
        # Route Geometry
        # =================================================

        route = LineString(

            [

                warehouse_point,

                destination_point

            ]

        )

        routes.append(

            {

                "shipment_id": shipment_id,

                "order_id": order_id,

                "warehouse_code": warehouse_code,

                "destination_city": destination_city,

                "geometry": route

            }

        )

        # =================================================
        # Distance Category
        # =================================================

        if distance_km <= 150:

            distance_category = "Local"

            route_priority = "High"

        elif distance_km <= 500:

            distance_category = "Regional"

            route_priority = "Medium"

        else:

            distance_category = "Long Distance"

            route_priority = "Low"

        # =================================================
        # Coverage
        # =================================================

        if row["default_warehouse"] == warehouse["warehouse_city"]:

            coverage_status = "Primary"

        else:

            coverage_status = "Secondary"

        # =================================================
        # Save Result
        # =================================================

        rows.append(

            {

                "shipment_id": shipment_id,

                "order_id": order_id,

                "warehouse_code": warehouse_code,

                "warehouse_city": warehouse["warehouse_city"],

                "destination_city": destination_city,

                "destination_state": row["state"],

                "destination_region": row["region"],

                "nearest_warehouse": row["default_warehouse"],

                "backup_warehouse": row["backup_warehouse"],

                "distance_km": distance_km,

                "distance_category": distance_category,

                "coverage_status": coverage_status,

                "route_priority": route_priority

            }

        )

            # =====================================================
    # Create Output DataFrames
    # =====================================================

    spatial_df = pd.DataFrame(rows)

    route_gdf = gpd.GeoDataFrame(

        routes,

        geometry="geometry",

        crs="EPSG:4326"

    )

    # =====================================================
    # Warehouse Coverage Buffer (300 km)
    # =====================================================

    warehouse_buffer = warehouse_gdf.to_crs(epsg=3857)

    warehouse_buffer["geometry"] = warehouse_buffer.buffer(

        300000

    )

    warehouse_buffer = warehouse_buffer.to_crs(

        epsg=4326

    )

    # =====================================================
    # Save Outputs
    # =====================================================

    print("\nSaving Outputs...")

    spatial_df.to_csv(

        f"{OUTPUT_DIR}/spatial_analysis.csv",

        index=False

    )

    route_gdf.to_file(

        f"{OUTPUT_DIR}/shipment_routes.geojson",

        driver="GeoJSON"

    )

    warehouse_buffer.to_file(

        f"{OUTPUT_DIR}/warehouse_coverage.geojson",

        driver="GeoJSON"

    )

    print("Spatial Outputs Saved Successfully.")


        # =====================================================
    # Summary
    # =====================================================

    print("\n" + "=" * 70)
    print("SPATIAL ANALYSIS SUMMARY")
    print("=" * 70)

    print(spatial_df.head())

    print()

    print(f"Shipments Analysed : {len(spatial_df)}")

    print(f"Warehouses Covered : {warehouse_gdf['warehouse_code'].nunique()}")

    print(f"Cities Covered     : {city_gdf['city'].nunique()}")

    print()

    print("Distance Statistics")
    print("-" * 70)

    print(f"Average Distance : {round(spatial_df['distance_km'].mean(),2)} km")

    print(f"Maximum Distance : {round(spatial_df['distance_km'].max(),2)} km")

    print(f"Minimum Distance : {round(spatial_df['distance_km'].min(),2)} km")

    print()

    print("Distance Categories")
    print("-" * 70)

    print(

        spatial_df["distance_category"]

        .value_counts()

    )

    print()

    print("Coverage Status")
    print("-" * 70)

    print(

        spatial_df["coverage_status"]

        .value_counts()

    )

    print()

    print("Route Priority")
    print("-" * 70)

    print(

        spatial_df["route_priority"]

        .value_counts()

    )

    print()

    print("Generated Files")
    print("-" * 70)

    print("✓ warehouse_points.geojson")

    print("✓ city_points.geojson")

    print("✓ shipment_routes.geojson")

    print("✓ warehouse_coverage.geojson")

    print("✓ spatial_analysis.csv")

    print()

    print(f"Execution Time : {round(time.time()-start,2)} sec")

    print("=" * 70)


# =========================================================
# Driver
# =========================================================

if __name__ == "__main__":

    main()