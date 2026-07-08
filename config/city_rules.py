"""
=========================================================
STRATOS - City Business Rules
=========================================================
"""

# =========================================================
# REGION MAPPING
# =========================================================

STATE_TO_REGION = {

    # ---------------- NORTH ----------------
    "Delhi": "North",
    "Haryana": "North",
    "Punjab": "North",
    "Himachal Pradesh": "North",
    "Jammu and Kashmir": "North",
    "Ladakh": "North",
    "Uttarakhand": "North",
    "Chandigarh": "North",
    "Uttar Pradesh": "North",

    # ---------------- WEST ----------------
    "Maharashtra": "West",
    "Gujarat": "West",
    "Goa": "West",
    "Rajasthan": "West",
    "Dadra and Nagar Haveli and Daman and Diu": "West",

    # ---------------- SOUTH ----------------
    "Karnataka": "South",
    "Kerala": "South",
    "Tamil Nadu": "South",
    "Telangana": "South",
    "Andhra Pradesh": "South",
    "Puducherry": "South",
    "Lakshadweep": "South",

    # ---------------- EAST ----------------
    "West Bengal": "East",
    "Odisha": "East",
    "Bihar": "East",
    "Jharkhand": "East",

    # ---------------- CENTRAL ----------------
    "Madhya Pradesh": "Central",
    "Chhattisgarh": "Central",

    # ---------------- NORTH-EAST ----------------
    "Assam": "North-East",
    "Arunachal Pradesh": "North-East",
    "Manipur": "North-East",
    "Meghalaya": "North-East",
    "Mizoram": "North-East",
    "Nagaland": "North-East",
    "Tripura": "North-East",
    "Sikkim": "North-East",

    # ---------------- ISLANDS ----------------
    "Andaman and Nicobar Islands": "East"
}

# =========================================================
# TIER 1 CITIES
# =========================================================

TIER_1_CITIES = [

    "Mumbai",
    "New Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Ahmedabad"

]

# =========================================================
# TIER 2 CITIES
# =========================================================

TIER_2_CITIES = [

    "Nagpur",
    "Lucknow",
    "Jaipur",
    "Indore",
    "Bhopal",
    "Patna",
    "Surat",
    "Kanpur",
    "Visakhapatnam",
    "Coimbatore",
    "Vadodara",
    "Ludhiana",
    "Agra",
    "Nashik",
    "Ranchi",
    "Raipur",
    "Jamshedpur",
    "Mysuru",
    "Vijayawada",
    "Kochi",
    "Guwahati",
    "Noida",
    "Ghaziabad",
    "Faridabad",
    "Aurangabad",
    "Hubballi",
    "Mangalore",
    "Tiruchirappalli",
    "Varanasi"

]

# =========================================================
# DEMAND WEIGHTS
# =========================================================

LOGISTICS_DEMAND_WEIGHT = {

    "Tier 1": 1.00,
    "Tier 2": 0.60,
    "Tier 3": 0.20

}

# =========================================================
# POTENTIAL WAREHOUSE CITIES
# =========================================================

POTENTIAL_WAREHOUSE_CITIES = [

    "Mumbai",
    "Pune",
    "Nagpur",
    "Ahmedabad",
    "New Delhi",
    "Lucknow",
    "Jaipur",
    "Indore",
    "Hyderabad",
    "Bengaluru",
    "Chennai",
    "Kolkata"

]