"""
=========================================================
STRATOS - Warehouse Service Rules
=========================================================
"""

WAREHOUSE_SERVICE_REGIONS = {

    "Mumbai": [
        "Maharashtra"
    ],

    "Ahmedabad": [
        "Gujarat",
        "Goa",
        "Dadra and Nagar Haveli and Daman and Diu",
         "Rajasthan"
    ],

    "New Delhi": [
        "Delhi",
        "Haryana",
        "Punjab",
        "Himachal Pradesh",
        "Uttarakhand",
        "Chandigarh",
        "Uttar Pradesh",
        "Jammu and Kashmir",
        "Ladakh"
    ],

    "Nagpur": [
        "Madhya Pradesh",
        "Chhattisgarh"
    ],

    "Bengaluru": [
        "Karnataka"
    ],

    "Hyderabad": [
        "Telangana",
        "Andhra Pradesh"
    ],

    "Chennai": [
        "Tamil Nadu",
        "Puducherry",
        "Kerala",
        "Lakshadweep"
    ],

    "Kolkata": [
        "West Bengal",
        "Odisha",
        "Bihar",
        "Jharkhand",
        "Sikkim",
        "Assam",
        "Arunachal Pradesh",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Tripura",
        "Andaman and Nicobar Islands"
    ]
}

BACKUP_WAREHOUSE = {

    "Mumbai": "Nagpur",
    "Ahmedabad": "Mumbai",
    "New Delhi": "Nagpur",
    "Nagpur": "Mumbai",
    "Bengaluru": "Hyderabad",
    "Hyderabad": "Nagpur",
    "Chennai": "Bengaluru",
    "Kolkata": "Nagpur"

}