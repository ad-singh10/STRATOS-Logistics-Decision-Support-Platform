# STRATOS – Logistics Decision Support Platform

An end-to-end logistics analytics platform that enables data-driven operational decision making through shipment analytics, spatial intelligence, machine learning, sustainability metrics, and disruption simulation.

> Built using **Python, Streamlit, GeoPandas, Folium, Scikit-learn, Plotly, and Pandas**

---

# Dashboard Preview

## Home Dashboard

![Home Dashboard](docs/screenshots/home_1.png)

---

## Shipment Explorer

| Overview | Detailed Analytics |
|----------|--------------------|
| ![Shipment Explorer 1](docs/screenshots/shipment_explorer_1.png) | ![Shipment Explorer 2](docs/screenshots/shipment_explorer_2.png) |

---

## Decision Engine

| Operational Insights | Recommendation Engine |
|----------------------|-----------------------|
| ![Decision Engine 1](docs/screenshots/decision_engine_1.png) | ![Decision Engine 2](docs/screenshots/decision_engine_2.png) |

---

## Spatial Intelligence

| Warehouse Coverage | Interactive Logistics Map |
|--------------------|---------------------------|
| ![Spatial Intelligence 1](docs/screenshots/spatial_intelligence_1.png) | ![Spatial Intelligence 2](docs/screenshots/spatial_intelligence_2.png) |

---

## Sustainability Analytics

![Sustainability Analytics](docs/screenshots/sustainability_1.png)

---

## Machine Learning

| Model Performance | Feature Analysis |
|-------------------|------------------|
| ![Machine Learning 1](docs/screenshots/machine_learning_1.png) | ![Machine Learning 2](docs/screenshots/machine_learning_2.png) |

---

## Simulation

| Simulation Overview | Scenario Analysis |
|---------------------|-------------------|
| ![Simulation 1](docs/screenshots/simulation_1.png) | ![Simulation 2](docs/screenshots/simulation_2.png) |
---

# Project Overview

Modern logistics operations generate large volumes of shipment data across multiple locations and transportation networks. Organizations often struggle to convert this data into actionable operational insights.

STRATOS addresses this challenge by integrating logistics analytics, spatial visualization, predictive machine learning, sustainability analysis, and disruption simulation into a unified decision support platform.

The platform enables logistics managers and analysts to monitor operational performance, identify risks, analyze shipment trends, evaluate warehouse coverage, predict delivery delays, and simulate disruption scenarios through an interactive dashboard.

---

# Business Objectives

- Improve logistics visibility
- Monitor shipment performance
- Predict delivery delays
- Support operational decision making
- Analyze warehouse coverage geographically
- Track sustainability metrics
- Simulate supply chain disruptions

---

# Key Features

### Executive Dashboard

- Logistics KPIs
- Shipment statistics
- Operational overview

### Shipment Explorer

- Interactive shipment filtering
- Delivery status analysis
- Route exploration

### Decision Engine

- Operational recommendations
- Delay prioritization
- Business rule-based insights

### Spatial Intelligence

- Warehouse visualization
- Route mapping
- Geographic coverage analysis

### Sustainability Analytics

- Carbon emission metrics
- Sustainability KPIs
- Environmental performance insights

### Machine Learning

- Shipment delay prediction
- Feature importance analysis
- Model performance evaluation

### Disruption Simulation

- Supply chain disruption scenarios
- Operational impact assessment
- Risk visualization

---

# System Architecture

```
                Raw Logistics Data
                        │
                        ▼
               Data Preprocessing
                        │
                        ▼
             Feature Engineering
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
Decision Engine   Spatial Analytics   ML Pipeline
        │               │               │
        └───────────────┼───────────────┘
                        ▼
              Interactive Dashboard
```

---

# Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Dashboard | Streamlit |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Spatial Analytics | GeoPandas, Folium |
| Visualization | Plotly |
| GIS Data | GeoJSON |
| Version Control | Git, GitHub |

---

# Machine Learning Pipeline

- Data preprocessing
- Feature engineering
- Model training
- Prediction generation
- Performance evaluation
- Interactive visualization

---

# Spatial Intelligence

The platform integrates geospatial analytics using GeoPandas and Folium to provide location-based logistics insights.

Features include:

- Warehouse locations
- Shipment routes
- Geographic coverage
- Interactive logistics maps

---

# Project Structure

```
STRATOS
│
├── data/
├── docs/
│   └── screenshots/
├── ml/
├── models/
├── notebooks/
├── spatial/
├── streamlit/
├── requirements.txt
├── README.md
└── app.py
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/ad-singh10/STRATOS-Logistics-Decision-Support-Platform.git
```

Navigate into the project

```bash
cd STRATOS-Logistics-Decision-Support-Platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run streamlit/app.py
```

---

# Future Enhancements

- Live GPS integration
- Traffic API integration
- Route optimization
- Demand forecasting
- Multi-modal transportation support
- Real-time shipment monitoring

---

# Learning Outcomes

Through this project, I gained practical experience in:

- Logistics analytics
- Geospatial data analysis
- Machine learning workflows
- Interactive dashboard development
- Data visualization
- Business KPI design
- End-to-end Python project development

---

# Author

**Aditya Singh**

Engineering & Computational Mechanics  
National Institute of Technology Jamshedpur

GitHub: https://github.com/ad-singh10

---

# License

This project is intended for educational and portfolio purposes.