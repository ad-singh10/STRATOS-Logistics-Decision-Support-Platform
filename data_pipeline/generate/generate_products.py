
"""
=========================================================
STRATOS
Module : Product Master Generator
=========================================================
"""

import os
import time
from datetime import datetime
import pandas as pd

OUTPUT_DIR = "data/final"
OUTPUT_FILE = "products_master.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# Product Catalog
# name, price, weight, fragile, shelf_life,
# velocity, supplier_id, supplier_name, lead_time
# =========================================================

PRODUCTS = {
    "Electronics":[
        ("Laptop",65000,2.2,True,None,"Medium","SUP001","Dell India",10),
        ("Smartphone",35000,0.2,True,None,"Fast","SUP002","Samsung India",7),
        ("Tablet",28000,0.5,True,None,"Medium","SUP001","Dell India",9),
        ("Monitor",15000,4.5,True,None,"Medium","SUP003","LG Electronics",8),
        ("Keyboard",1200,0.7,False,None,"Fast","SUP004","Logitech",5),
        ("Mouse",700,0.2,False,None,"Fast","SUP004","Logitech",5),
        ("Printer",9000,8.0,True,None,"Slow","SUP005","HP India",12),
        ("Router",2500,0.4,False,None,"Medium","SUP006","TP-Link",6),
        ("SSD",4500,0.1,True,None,"Medium","SUP007","Western Digital",7),
        ("Hard Drive",6000,0.3,True,None,"Medium","SUP007","Western Digital",7),
        ("Smartwatch",12000,0.1,True,None,"Fast","SUP002","Samsung India",7),
        ("Power Bank",1800,0.4,False,None,"Fast","SUP008","Ambrane",5)
    ],
    "FMCG":[
        ("Shampoo",350,0.5,False,730,"Fast","SUP009","Hindustan Unilever",4),
        ("Soap",45,0.1,False,1095,"Fast","SUP009","Hindustan Unilever",4),
        ("Toothpaste",120,0.2,False,730,"Fast","SUP010","Colgate",4),
        ("Detergent",450,2.0,False,1095,"Fast","SUP011","Surf Excel",5),
        ("Face Wash",220,0.2,False,730,"Medium","SUP009","Hindustan Unilever",4),
        ("Hair Oil",180,0.3,False,730,"Medium","SUP012","Parachute",5),
        ("Deodorant",250,0.2,False,730,"Medium","SUP013","Nivea",6),
        ("Body Lotion",300,0.4,False,730,"Medium","SUP013","Nivea",6),
        ("Dishwash Liquid",180,0.5,False,730,"Fast","SUP014","Vim",4),
        ("Floor Cleaner",250,1.0,False,730,"Fast","SUP015","Lizol",4),
        ("Hand Wash",150,0.3,False,730,"Fast","SUP014","Lifebuoy",4),
        ("Tissue Pack",90,0.2,False,1095,"Fast","SUP016","Origami",3)
    ],
    "Grocery":[
        ("Rice",800,5.0,False,365,"Fast","SUP017","ITC Foods",5),
        ("Wheat Flour",250,5.0,False,180,"Fast","SUP018","Aashirvaad",5),
        ("Sugar",280,5.0,False,365,"Fast","SUP019","Dhampur Sugar",5),
        ("Salt",120,1.0,False,730,"Fast","SUP020","Tata Salt",4),
        ("Cooking Oil",900,5.0,False,365,"Fast","SUP021","Fortune",5),
        ("Tea",450,1.0,False,365,"Medium","SUP022","Tata Tea",5),
        ("Coffee",650,0.5,False,365,"Medium","SUP023","Nescafe",5),
        ("Pulses",700,2.0,False,365,"Fast","SUP024","24 Mantra",5),
        ("Biscuits",50,0.2,False,180,"Fast","SUP025","Parle",3),
        ("Noodles",90,0.4,False,270,"Fast","SUP026","Maggi",3),
        ("Spices",350,0.5,False,365,"Medium","SUP027","MDH",5),
        ("Oats",220,1.0,False,365,"Medium","SUP028","Quaker",5)
    ],
    "Apparel":[
        ("T-Shirt",700,0.3,False,None,"Fast","SUP029","Aditya Birla Fashion",7),
        ("Jeans",1800,0.8,False,None,"Medium","SUP029","Aditya Birla Fashion",7),
        ("Shirt",1200,0.4,False,None,"Medium","SUP029","Aditya Birla Fashion",7),
        ("Jacket",3500,1.2,False,None,"Slow","SUP030","Woodland",10),
        ("Hoodie",2200,0.8,False,None,"Medium","SUP031","Puma",8),
        ("Shoes",2800,1.0,False,None,"Fast","SUP031","Puma",8),
        ("Socks",250,0.1,False,None,"Fast","SUP032","Jockey",5),
        ("Cap",400,0.2,False,None,"Medium","SUP031","Puma",6),
        ("Shorts",900,0.3,False,None,"Medium","SUP029","Aditya Birla Fashion",7),
        ("Track Pants",1400,0.5,False,None,"Medium","SUP031","Puma",7),
        ("Belt",650,0.3,False,None,"Slow","SUP033","Levi's",7),
        ("Backpack",2500,0.8,False,None,"Fast","SUP034","American Tourister",8)
    ],
    "Healthcare":[
        ("Face Mask",250,0.2,False,1825,"Fast","SUP035","3M India",4),
        ("Hand Gloves",350,0.2,False,1825,"Fast","SUP035","3M India",4),
        ("Sanitizer",180,0.5,False,730,"Fast","SUP036","Dettol",4),
        ("Thermometer",450,0.2,True,None,"Medium","SUP037","Omron",6),
        ("Blood Pressure Monitor",2200,0.8,True,None,"Slow","SUP037","Omron",8),
        ("Vitamin Tablets",600,0.3,False,730,"Medium","SUP038","Himalaya",6),
        ("First Aid Kit",850,1.0,False,None,"Medium","SUP039","Johnson & Johnson",6),
        ("Bandages",120,0.2,False,1825,"Fast","SUP039","Johnson & Johnson",4),
        ("Pain Relief Spray",300,0.4,False,730,"Medium","SUP040","Volini",5)
    ],
    "Automotive":[
        ("Engine Oil",1200,4.0,False,1095,"Fast","SUP041","Castrol",6),
        ("Brake Pads",1800,2.0,False,None,"Medium","SUP042","Bosch",7),
        ("Car Battery",6500,12.0,True,None,"Slow","SUP043","Exide",10),
        ("Spark Plug",450,0.2,False,None,"Medium","SUP042","Bosch",6),
        ("Air Filter",650,0.4,False,None,"Medium","SUP042","Bosch",6),
        ("Coolant",900,5.0,False,1095,"Medium","SUP044","Prestone",6),
        ("Tyre Inflator",2200,2.5,True,None,"Slow","SUP045","Michelin",8),
        ("Wiper Blade",500,0.5,False,None,"Fast","SUP042","Bosch",5),
        ("Lubricant",350,1.0,False,1095,"Medium","SUP041","Castrol",5)
    ],
    "Home & Kitchen":[
        ("LED Bulb",180,0.2,True,None,"Fast","SUP046","Philips",4),
        ("Ceiling Fan",2800,6.0,True,None,"Medium","SUP047","Havells",8),
        ("Mixer Grinder",3500,4.0,True,None,"Medium","SUP048","Prestige",7),
        ("Electric Kettle",1800,1.5,True,None,"Medium","SUP048","Prestige",7),
        ("Cookware Set",4200,6.0,False,None,"Slow","SUP048","Prestige",8),
        ("Plastic Chair",900,2.5,False,None,"Medium","SUP049","Nilkamal",6),
        ("Storage Box",650,1.0,False,None,"Fast","SUP049","Nilkamal",5),
        ("Water Bottle",350,0.4,False,None,"Fast","SUP050","Milton",4),
        ("Dustbin",500,1.5,False,None,"Medium","SUP049","Nilkamal",5)
    ]
}

PREFIX={"Electronics":"ELE","FMCG":"FMC","Grocery":"GRO","Apparel":"APP","Healthcare":"HEA","Automotive":"AUT","Home & Kitchen":"HOM"}
VELOCITY_MULTIPLIER={"Fast":1.50,"Medium":1.00,"Slow":0.60}

def abc(price):
    if price>=10000: return "A"
    elif price>=1000: return "B"
    return "C"

def main():
    start=time.time()
    today=datetime.today().strftime("%Y-%m-%d")
    rows=[]
    sku=1

    print("="*70)
    print("STRATOS EXECUTION LAYER")
    print("Module : Product Master Generator")
    print("="*70)

    for category,items in PRODUCTS.items():
        count=1
        for (name,price,wt,fragile,shelf,velocity,sup_id,sup_name,lead) in items:
            rows.append({
                "sku_id":f"SKU{sku:04d}",
                "sku_code":f"{PREFIX[category]}{count:03d}",
                "product_name":name,
                "category":category,
                "unit":"Pieces",
                "unit_price":price,
                "weight_kg":wt,
                "storage_type":"Standard",
                "shelf_life_days":shelf,
                "is_fragile":fragile,
                "abc_class":abc(price),
                "velocity_class":velocity,
                "velocity_multiplier":VELOCITY_MULTIPLIER[velocity],
                "supplier_id":sup_id,
                "supplier_name":sup_name,
                "lead_time_days":lead,
                "created_at":today,
                "updated_at":today,
                "is_active":True
            })
            sku+=1
            count+=1

    df=pd.DataFrame(rows)
    out=os.path.join(OUTPUT_DIR,OUTPUT_FILE)
    df.to_csv(out,index=False)

    print(df.head())
    print(f"\nTotal Products : {len(df)}")
    print(f"Categories     : {df['category'].nunique()}")
    print(f"Suppliers      : {df['supplier_id'].nunique()}")
    print(f"Saved To       : {out}")
    print(f"Execution Time : {round(time.time()-start,2)} sec")
    print("="*70)

if __name__=="__main__":
    main()
