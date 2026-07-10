"""
=========================================================
STRATOS
 Logistics Decision Suppport Platform
=========================================================
"""

import os

import pandas as pd

import geopandas as gpd

import streamlit as st

import plotly.express as px

import folium

from streamlit_folium import st_folium

from folium.plugins import Fullscreen, MiniMap, MousePosition

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(

    page_title="STRATOS  Logistics Decision Support Platform",

    layout="wide",

    initial_sidebar_state="expanded"

)

# =========================================================
# Data Paths
# =========================================================

MASTER_FILE = "decision_engine/outputs/master_decision.csv"

AI_FILE = "decision_engine/outputs/ai_decision_engine.csv"

SPATIAL_FILE = "spatial/outputs/spatial_analysis.csv"

SUSTAINABILITY_FILE = "sustainability/outputs/sustainability_analysis.csv"

ML_FILE = "ml/outputs/shipment_delay_predictions.csv"

# =========================================================
# Load Data
# =========================================================

@st.cache_data

def load_data():

    master = pd.read_csv(MASTER_FILE)

    ai = pd.read_csv(AI_FILE)

    spatial = pd.read_csv(SPATIAL_FILE)

    sustainability = pd.read_csv(SUSTAINABILITY_FILE)

    ml = pd.read_csv(ML_FILE)

    return (

        master,

        ai,

        spatial,

        sustainability,

        ml

    )

master, ai, spatial, sustainability, ml = load_data()

# =========================================================
# Sidebar
# =========================================================

st.sidebar.title("STRATOS")

st.sidebar.markdown("---")

page = st.sidebar.radio(

    "Navigation",

    [

        "Home",

        "Shipment Explorer",

        "Decision Engine",

        "Spatial Intelligence",

        "Sustainability",

        "Machine Learning",

        "Simulation"

    ]

)

st.sidebar.markdown("---")

st.sidebar.write("Version 1.0")

# =========================================================
# HOME
# =========================================================

if page == "Home":

    st.title("STRATOS Logistics Decision Support Platform")

    st.caption(

        "Enterprise Operations Intelligence Platform"

    )

    st.markdown("---")


    # =====================================================
    # KPI Calculations
    # =====================================================

    total_shipments = len(ai)

    critical = (
        ai["operational_priority"] == "Critical"
    ).sum()

    high = (
        ai["operational_priority"] == "High"
    ).sum()

    green = (
        sustainability["green_shipment"] == "Yes"
    ).sum()

    avg_score = round(
        ai["operational_priority_score"].mean(),
        2
    )

    # =====================================================
    # KPI Cards
    # =====================================================

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Shipments",
        f"{total_shipments:,}"
    )

    c2.metric(
        "Critical",
        critical
    )

    c3.metric(
        "High Priority",
        high
    )

    c4.metric(
        "Green Shipments",
        green
    )

    c5.metric(
        "Avg OPS",
        avg_score
    )

    st.markdown("---")

    # =====================================================
    # Operational Priority Distribution
    # =====================================================

    st.subheader("Operational Priority Distribution")

    priority = (
        ai["operational_priority"]
        .value_counts()
        .reset_index()
    )

    priority.columns = [
        "Priority",
        "Shipments"
    ]

    fig = px.bar(
        priority,
        x="Priority",
        y="Shipments",
        color="Priority",
        text="Shipments"
    )

    fig.update_layout(
        height=450,
        xaxis_title="",
        yaxis_title="Shipments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # Recommendation & Delay Risk
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("AI Recommendations")

        rec = (
            ai["recommended_action"]
            .value_counts()
            .reset_index()
        )

        rec.columns = [
            "Recommendation",
            "Count"
        ]

        fig = px.pie(
            rec,
            names="Recommendation",
            values="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Delay Risk")

        delay = (
            ml["predicted_delay_risk"]
            .value_counts()
            .reset_index()
        )

        delay.columns = [
            "Risk",
            "Shipments"
        ]

        fig = px.bar(
            delay,
            x="Risk",
            y="Shipments",
            color="Risk",
            text="Shipments"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # Recent AI Decisions
    # =====================================================

    st.markdown("---")

    st.subheader("Recent AI Decisions")

    st.dataframe(
        ai.head(20),
        use_container_width=True
    )

# =========================================================
# SHIPMENT EXPLORER
# =========================================================

elif page == "Shipment Explorer":

    st.title("Shipment Explorer")

    st.caption(
        "Search and inspect individual shipment decisions."
    )

    st.markdown("---")

    shipment_id = st.text_input(

        "Enter Shipment ID",

        placeholder="Example : SHP000001"

    )

    if shipment_id == "":

        st.info(
            "Enter a Shipment ID to begin."
        )

        st.stop()

    shipment = ai[
        ai["shipment_id"] == shipment_id
    ]

    if shipment.empty:

        st.error("Shipment not found.")

        st.stop()

    shipment = shipment.iloc[0] 

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Shipment",
        shipment["shipment_id"]
    )

    c2.metric(
        "Priority",
        shipment["priority"]
    )

    c3.metric(
        "OPS",
        shipment["operational_priority_score"]
    )

    c4.metric(
        "Delay Risk",
        shipment["predicted_delay_risk"]
    )         

    st.markdown("---")

    st.subheader("AI Decision Summary")

    left, right = st.columns(2)

    with left:

        st.write("**Recommended Action**")

        st.success(

            shipment["recommended_action"]

        )

        st.write("**Operational Priority**")

        st.info(

            shipment["operational_priority"]

        )

    with right:

        st.write("**Business Explanation**")

        st.write(

            shipment["business_explanation"]

        )


    st.markdown("---")

    st.subheader("Operational Details")

    details = pd.DataFrame({

        "Field":[

            "Route Priority",

            "Coverage",

            "Green Shipment",

            "Event",

            "Severity"

        ],

        "Value":[

            shipment["route_priority"],

            shipment["coverage_status"],

            shipment["green_shipment"],

            shipment["event_type"],

            shipment["severity"]

        ]

    })

    st.dataframe(

        details,

        use_container_width=True,

        hide_index=True

    ) 

    st.markdown("---")

    st.subheader("Complete Shipment Record")

    st.dataframe(

        shipment.to_frame().T,

        use_container_width=True

    )  

# =========================================================
# AI DECISION ENGINE PAGE
# =========================================================

elif page == "Decision Engine":

    st.title("Decision Engine")

    st.caption(
        "Enterprise  Decision Support Dashboard"
    )

    st.markdown("---")    

# =========================================================
# KPI SECTION
# =========================================================

    total = len(ai)

    critical = (
        ai["operational_priority"] == "Critical"
    ).sum()

    avg_ops = round(
        ai["operational_priority_score"].mean(),
        2
    )

    recommendations = ai[
        "recommended_action"
    ].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Shipments",
        total
    )

    c2.metric(
        "Critical",
        critical
    )

    c3.metric(
        "Average OPS",
        avg_ops
    )

    c4.metric(
        "Recommendation Types",
        recommendations
    )

    st.markdown("---")    

# =========================================================
# OPERATIONAL PRIORITY CHART
# =========================================================

    st.subheader(
        "Operational Priority Distribution"
    )

    priority = (
        ai["operational_priority"]
        .value_counts()
        .reset_index()
    )

    priority.columns = [
        "Priority",
        "Shipments"
    ]

    fig = px.bar(

        priority,

        x="Priority",

        y="Shipments",

        color="Priority",

        text="Shipments"

    )

    fig.update_layout(

        height=450

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# =========================================================
# RECOMMENDATION DISTRIBUTION
# =========================================================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "Recommended Actions"
        )

        recommendation = (

            ai["recommended_action"]

            .value_counts()

            .reset_index()

        )

        recommendation.columns = [

            "Recommendation",

            "Shipments"

        ]

        fig = px.pie(

            recommendation,

            names="Recommendation",

            values="Shipments"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        st.subheader(
            "Delay Risk Distribution"
        )

        risk = (

            ai["predicted_delay_risk"]

            .value_counts()

            .reset_index()

        )

        risk.columns = [

            "Risk",

            "Shipments"

        ]

        fig = px.bar(

            risk,

            x="Risk",

            y="Shipments",

            color="Risk",

            text="Shipments"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )  

# =========================================================
#  DECISION TABLE
# =========================================================

    st.markdown("---")

    st.subheader(
        "Decision Summary"
    )

    st.dataframe(

        ai[

            [

                "shipment_id",

                "priority",

                "predicted_delay_risk",

                "operational_priority",

                "operational_priority_score",

                "recommended_action"

            ]

        ],

        use_container_width=True

    )      


# =========================================================
# OPERATIONAL PRIORITY SCORE DISTRIBUTION
# =========================================================

    st.markdown("---")

    st.subheader(
        "Operational Priority Score Distribution"
    )

    fig = px.histogram(

        ai,

        x="operational_priority_score",

        nbins=20

    )

    fig.update_layout(

        height=450,

        xaxis_title="Operational Priority Score",

        yaxis_title="Shipments"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    ) 
    
# =========================================================
# SPATIAL INTELLIGENCE
# =========================================================

elif page == "Spatial Intelligence":

    st.title("Spatial Intelligence")

    st.caption(
        "Enterprise GeoSpatial Logistics Network"
    )

    st.markdown("---")

    # =====================================================
    # LOAD DATASETS
    # =====================================================

    spatial = pd.read_csv(
        "spatial/outputs/spatial_analysis.csv"
    )

    warehouses_gdf = gpd.read_file(
        "spatial/outputs/warehouse_points.geojson"
    )

    routes_gdf = gpd.read_file(
        "spatial/outputs/shipment_routes.geojson"
    )

    coverage_gdf = gpd.read_file(
        "spatial/outputs/warehouse_coverage.geojson"
    )

    # =====================================================
    # CLEAN DATETIME COLUMNS
    # =====================================================

    for gdf in [

        warehouses_gdf,

        routes_gdf,

        coverage_gdf

    ]:

        for col in gdf.columns:

            if str(gdf[col].dtype).startswith("datetime"):

                gdf[col] = gdf[col].astype(str)

    # =====================================================
    # PERFORMANCE
    # =====================================================

    ROUTE_SAMPLE = 400

    if len(routes_gdf) > ROUTE_SAMPLE:

        routes_display = routes_gdf.sample(

            ROUTE_SAMPLE,

            random_state=42

        )

    else:

        routes_display = routes_gdf.copy()

    # =====================================================
    # MAP CENTER
    # =====================================================

    center_lat = warehouses_gdf.geometry.y.mean()

    center_lon = warehouses_gdf.geometry.x.mean()

    # =====================================================
    # KPI VALUES
    # =====================================================

    total_routes = len(routes_gdf)

    total_warehouses = len(warehouses_gdf)

    total_coverage = len(coverage_gdf)

    avg_distance = round(

        spatial["distance_km"].mean(),

        2

    )

    max_distance = round(

        spatial["distance_km"].max(),

        2

    )

    # =====================================================
    # KPI CARDS
    # =====================================================

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Warehouses",
        total_warehouses
    )

    c2.metric(
        "Routes",
        f"{total_routes:,}"
    )

    c3.metric(
        "Coverage Points",
        f"{total_coverage:,}"
    )

    c4.metric(
        "Avg Distance",
        f"{avg_distance} km"
    )

    c5.metric(
        "Max Distance",
        f"{max_distance} km"
    )

    st.markdown("---")

    # =====================================================
    # ANALYTICS
    # =====================================================

    left, right = st.columns(2)

    # =====================================================
    # DISTANCE CATEGORY
    # =====================================================

    with left:

        st.subheader(
            "Distance Category"
        )

        distance = (
            spatial["distance_category"]
            .value_counts()
            .reset_index()
        )

        distance.columns = [
            "Category",
            "Shipments"
        ]

        fig = px.bar(
            distance,
            x="Category",
            y="Shipments",
            color="Category",
            text="Shipments"
        )

        fig.update_layout(
            height=400,
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =====================================================
    # ROUTE PRIORITY
    # =====================================================

    with right:

        st.subheader(
            "Route Priority"
        )

        priority = (
            spatial["route_priority"]
            .value_counts()
            .reset_index()
        )

        priority.columns = [
            "Priority",
            "Shipments"
        ]

        fig = px.pie(
            priority,
            names="Priority",
            values="Shipments",
            hole=0.45
        )

        fig.update_layout(
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    # =====================================================
    # COVERAGE STATUS
    # =====================================================

    st.subheader(
        "Coverage Status"
    )

    coverage = (
        spatial["coverage_status"]
        .value_counts()
        .reset_index()
    )

    coverage.columns = [
        "Coverage",
        "Shipments"
    ]

    fig = px.bar(
        coverage,
        x="Coverage",
        y="Shipments",
        color="Coverage",
        text="Shipments"
    )

    fig.update_layout(
        height=400,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # =====================================================
    # ENTERPRISE LOGISTICS MAP
    # =====================================================

    st.subheader("Enterprise Logistics Network")

    m = folium.Map(

        location=[center_lat, center_lon],

        zoom_start=5,

        tiles="CartoDB Positron",

        control_scale=True

    )

    # =====================================================
    # MAP PLUGINS
    # =====================================================

    Fullscreen().add_to(m)

    MiniMap(toggle_display=True).add_to(m)

    MousePosition().add_to(m)

    # =====================================================
    # WAREHOUSE LAYER
    # =====================================================

    warehouse_layer = folium.FeatureGroup(
        name="Warehouses"
    )

    for _, row in warehouses_gdf.iterrows():

        popup = folium.Popup(

            f"""
            <b>{row['warehouse_code']}</b><br>
            City : {row['warehouse_city']}<br>
            Type : {row['warehouse_type']}
            """,

            max_width=250

        )

        folium.CircleMarker(

            location=[

                row.geometry.y,

                row.geometry.x

            ],

            radius=8,

            color="green",

            fill=True,

            fill_color="green",

            fill_opacity=1,

            popup=popup

        ).add_to(warehouse_layer)

    warehouse_layer.add_to(m)

    # =====================================================
    # SHIPMENT ROUTES
    # =====================================================

    route_layer = folium.FeatureGroup(
        name="Shipment Routes (Sample)"
    )

    folium.GeoJson(

        routes_display.to_json(),

        style_function=lambda feature: {

            "color": "#2563eb",

            "weight": 2,

            "opacity": 0.35

        }

    ).add_to(route_layer)

    route_layer.add_to(m)

    # =====================================================
    # COVERAGE LAYER
    # =====================================================

    coverage_layer = folium.FeatureGroup(
        name="Warehouse Coverage"
    )

    folium.GeoJson(

        coverage_gdf.to_json(),

        style_function=lambda feature: {

            "color": "#f59e0b",

            "fillColor": "#f59e0b",

            "weight": 1,

            "fillOpacity": 0.15

        }

    ).add_to(coverage_layer)

    coverage_layer.add_to(m)

    # =====================================================
    # LAYER CONTROL
    # =====================================================

    folium.LayerControl(
        collapsed=False
    ).add_to(m)

    st_folium(

        m,

        width=None,

        height=700,

        returned_objects=[]

    )

    st.caption(
        f"Displaying {len(routes_display):,} sampled routes out of {len(routes_gdf):,} total shipment routes for optimal dashboard performance."
    )

    st.markdown("---")

    # =====================================================
    # ROUTE ANALYTICS
    # =====================================================

    st.subheader("Route Analytics")

    c1, c2 = st.columns(2)

    with c1:

        warehouse_distribution = (

            spatial["warehouse_city"]

            .value_counts()

            .reset_index()

        )

        warehouse_distribution.columns = [

            "Warehouse",

            "Shipments"

        ]

        fig = px.bar(

            warehouse_distribution,

            x="Warehouse",

            y="Shipments",

            color="Warehouse",

            text="Shipments"

        )

        fig.update_layout(

            height=450,

            showlegend=False,

            xaxis_title="Warehouse",

            yaxis_title="Shipments"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with c2:

        destination_distribution = (

            spatial["destination_region"]

            .value_counts()

            .reset_index()

        )

        destination_distribution.columns = [

            "Region",

            "Shipments"

        ]

        fig = px.pie(

            destination_distribution,

            names="Region",

            values="Shipments",

            hole=0.45

        )

        fig.update_layout(

            height=450

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.markdown("---")

    # =====================================================
    # DISTANCE ANALYSIS
    # =====================================================

    st.subheader("Shipment Distance Distribution")

    fig = px.histogram(

        spatial,

        x="distance_km",

        nbins=30,

        color_discrete_sequence=["#2563eb"]

    )

    fig.update_layout(

        height=450,

        xaxis_title="Distance (km)",

        yaxis_title="Number of Shipments"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.markdown("---")

    # =====================================================
    # ROUTE DATA
    # =====================================================

    st.subheader("Route Dataset")

    display_columns = [

        "shipment_id",

        "warehouse_code",

        "warehouse_city",

        "destination_city",

        "destination_state",

        "distance_km",

        "distance_category",

        "coverage_status",

        "route_priority"

    ]

    st.dataframe(

        spatial[display_columns],

        use_container_width=True,

        height=450

    )

    st.caption(

        f"Showing {len(spatial):,} shipment routes generated by the GeoPandas spatial analytics pipeline."

    )

    st.markdown("---")

    # =====================================================
    # SHIPMENT ROUTE EXPLORER
    # =====================================================

    st.subheader("Shipment Route Explorer")

    shipment_options = sorted(
        spatial["shipment_id"].unique()
    )

    selected_shipment = st.selectbox(
        "Select Shipment",
        shipment_options
    )

    shipment = spatial[
        spatial["shipment_id"] == selected_shipment
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Warehouse",
        shipment["warehouse_code"]
    )

    c2.metric(
        "Destination",
        shipment["destination_city"]
    )

    c3.metric(
        "Distance",
        f"{shipment['distance_km']:.2f} km"
    )

    st.dataframe(
        shipment.to_frame().T,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # =====================================================
    # SPATIAL NETWORK SUMMARY
    # =====================================================

    st.subheader("Spatial Network Summary")

    summary = pd.DataFrame({

        "Metric":[

            "Total Warehouses",

            "Total Routes",

            "Coverage Records",

            "Average Distance (km)",

            "Maximum Distance (km)",

            "Distance Categories",

            "Coverage Categories"

        ],

        "Value":[

            total_warehouses,

            total_routes,

            total_coverage,

            avg_distance,

            max_distance,

            spatial["distance_category"].nunique(),

            spatial["coverage_status"].nunique()

        ]

    })

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    st.markdown("---")

    # =====================================================
    # BUSINESS INSIGHTS
    # =====================================================

    st.subheader("Key Business Insights")

    st.info(

        f"""
• GeoPandas generated **{total_routes:,} shipment routes**.

• Logistics network consists of **{total_warehouses} strategic warehouses**.

• Average shipment distance is **{avg_distance} km**.

• Maximum shipment distance observed is **{max_distance} km**.

• Interactive GIS visualization is powered using **GeoPandas + Folium**.

• Route geometries are exported as GeoJSON and rendered inside Streamlit.

• Only a representative sample of shipment routes is displayed to ensure smooth dashboard performance.
"""

    )

    st.markdown("---")

# =========================================================
# SUSTAINABILITY & MACHINE LEARNING
# =========================================================

elif page == "Sustainability":

    st.title("Sustainability Analytics")

    st.caption("Environmental Performance of Logistics Network")

    st.markdown("---")

    # =====================================================
    # KPI CARDS
    # =====================================================

    avg_fuel = round(
        sustainability["fuel_consumption_l"].mean(),
        2
    )

    avg_co2 = round(
        sustainability["co2_emission_kg"].mean(),
        2
    )

    green_shipments = (
        sustainability["green_shipment"] == "Yes"
    ).sum()

    avg_score = round(
        sustainability["sustainability_score"].mean(),
        2
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average Fuel",
        f"{avg_fuel} L"
    )

    c2.metric(
        "Average CO₂",
        f"{avg_co2} kg"
    )

    c3.metric(
        "Green Shipments",
        green_shipments
    )

    c4.metric(
        "Average Score",
        avg_score
    )

    st.markdown("---")

    # =====================================================
    # GREEN SHIPMENT DISTRIBUTION
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("Green Shipment Distribution")

        green = (
            sustainability["green_shipment"]
            .value_counts()
            .reset_index()
        )

        green.columns = [
            "Shipment",
            "Count"
        ]

        fig = px.pie(
            green,
            names="Shipment",
            values="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Sustainability Score")

        score = (
            sustainability["sustainability_score"]
            .value_counts()
            .reset_index()
        )

        score.columns = [
            "Score",
            "Shipments"
        ]

        fig = px.bar(
            score,
            x="Score",
            y="Shipments",
            color="Score",
            text="Shipments"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    # =====================================================
    # SUSTAINABILITY TABLE
    # =====================================================

    st.subheader("Shipment Sustainability")

    st.dataframe(
        sustainability.head(50),
        use_container_width=True
    )

# =========================================================
# MACHINE LEARNING
# =========================================================

elif page == "Machine Learning":

    st.title("Machine Learning Analytics")

    st.caption("Shipment Delay Prediction Dashboard")

    st.markdown("---")

    # =====================================================
    # KPI CARDS
    # =====================================================

    total = len(ml)

    high = (
        ml["predicted_delay_risk"] == "High"
    ).sum()

    medium = (
        ml["predicted_delay_risk"] == "Medium"
    ).sum()

    low = (
        ml["predicted_delay_risk"] == "Low"
    ).sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Predictions",
        total
    )

    c2.metric(
        "High Risk",
        high
    )

    c3.metric(
        "Medium Risk",
        medium
    )

    c4.metric(
        "Low Risk",
        low
    )

    st.markdown("---")

    # =====================================================
    # DELAY RISK DISTRIBUTION
    # =====================================================

    st.subheader("Delay Risk Distribution")

    risk = (
        ml["predicted_delay_risk"]
        .value_counts()
        .reset_index()
    )

    risk.columns = [
        "Risk",
        "Shipments"
    ]

    fig = px.bar(
        risk,
        x="Risk",
        y="Shipments",
        color="Risk",
        text="Shipments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # =====================================================
    # ML DATASET
    # =====================================================

    st.subheader("Prediction Results")

    st.dataframe(
        ml.head(50),
        use_container_width=True
    )   


# =========================================================
# SIMULATION
# =========================================================

elif page == "Simulation":

    st.title("Simulation Dashboard")

    st.caption("Operational Disruption Analysis")

    st.markdown("---")

    # =====================================================
    # LOAD SIMULATION DATA
    # =====================================================

    simulation = pd.read_csv(
        "simulation/outputs/disruption_events.csv"
    )

    # =====================================================
    # KPI CARDS
    # =====================================================

    total_events = len(simulation)

    critical = (
        simulation["severity"] == "Critical"
    ).sum()

    high = (
        simulation["severity"] == "High"
    ).sum()

    event_types = simulation["event_type"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Disruptions",
        total_events
    )

    c2.metric(
        "Critical",
        critical
    )

    c3.metric(
        "High Severity",
        high
    )

    c4.metric(
        "Event Types",
        event_types
    )

    st.markdown("---")

    # =====================================================
    # SEVERITY DISTRIBUTION
    # =====================================================

    left, right = st.columns(2)

    with left:

        st.subheader("Severity Distribution")

        severity = (
            simulation["severity"]
            .value_counts()
            .reset_index()
        )

        severity.columns = [
            "Severity",
            "Events"
        ]

        fig = px.bar(
            severity,
            x="Severity",
            y="Events",
            color="Severity",
            text="Events"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Event Types")

        events = (
            simulation["event_type"]
            .value_counts()
            .reset_index()
        )

        events.columns = [
            "Event",
            "Count"
        ]

        fig = px.pie(
            events,
            names="Event",
            values="Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    # =====================================================
    # SIMULATION TABLE
    # =====================================================

    st.subheader("Disruption Events")

    st.dataframe(
        simulation.head(50),
        use_container_width=True
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "STRATOS v1.0 | AI Logistics Control Tower | Developed using Python, Streamlit, Plotly and GeoPandas"
)