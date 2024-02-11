import os
import django
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Connect to your PostgreSQL database
    with psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
    ) as conn:
        with conn.cursor() as c:

            # Read the categories from the JSON file

            categories = [
                {
                    "name": "Amazon Renewed",
                    "url": "/Best-Sellers-Amazon-Renewed/zgbs/amazon-renewed"
                },
                {
                    "name": "Appliances",
                    "url": "/Best-Sellers-Appliances/zgbs/appliances"
                },
                {
                    "name": "Arts, Crafts & Sewing",
                    "url": "/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts"
                },
                {
                    "name": "Automotive",
                    "url": "/Best-Sellers-Automotive/zgbs/automotive"
                },
                {
                    "name": "Baby",
                    "url": "/Best-Sellers-Baby/zgbs/baby-products"
                },
                {
                    "name": "Beauty & Personal Care",
                    "url": "/Best-Sellers-Beauty-Personal-Care/zgbs/beauty"
                },
                {
                    "name": "Camera & Photo Products",
                    "url": "/best-sellers-camera-photo/zgbs/photo"
                },
                {
                    "name": "Cell Phones & Accessories",
                    "url": "/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless"
                },
                {
                    "name": "Climate Pledge Friendly",
                    "url": "/Best-Sellers-Climate-Pledge-Friendly/zgbs/climate-pledge"
                },
                {
                    "name": "Clothing, Shoes & Jewelry",
                    "url": "/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion"
                },
                {
                    "name": "Collectible Coins",
                    "url": "/Best-Sellers-Collectible-Coins/zgbs/coins"
                },
                {
                    "name": "Computers & Accessories",
                    "url": "/Best-Sellers-Computers-Accessories/zgbs/pc"
                },
                {
                    "name": "Digital Educational Resources",
                    "url": "/Best-Sellers-Digital-Educational-Resources/zgbs/digital-educational-resources"
                },
                {
                    "name": "Electronics",
                    "url": "/Best-Sellers-Electronics/zgbs/electronics"
                },
                {
                    "name": "Entertainment Collectibles",
                    "url": "/Best-Sellers-Entertainment-Collectibles/zgbs/entertainment-collectibles"
                },
                {
                    "name": "Grocery & Gourmet Food",
                    "url": "/Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery"
                },
                {
                    "name": "Handmade Products",
                    "url": "/Best-Sellers-Handmade-Products/zgbs/handmade"
                },
                {
                    "name": "Health & Household",
                    "url": "/Best-Sellers-Health-Household/zgbs/hpc"
                },
                {
                    "name": "Home & Kitchen",
                    "url": "/Best-Sellers-Home-Kitchen/zgbs/home-garden"
                },
                {
                    "name": "Industrial & Scientific",
                    "url": "/Best-Sellers-Industrial-Scientific/zgbs/industrial"
                },
                {
                    "name": "Kitchen & Dining",
                    "url": "/Best-Sellers-Kitchen-Dining/zgbs/kitchen"
                },
                {
                    "name": "Musical Instruments",
                    "url": "/Best-Sellers-Musical-Instruments/zgbs/musical-instruments"
                },
                {
                    "name": "Office Products",
                    "url": "/Best-Sellers-Office-Products/zgbs/office-products"
                },
                {
                    "name": "Patio, Lawn & Garden",
                    "url": "/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden"
                },
                {
                    "name": "Pet Supplies",
                    "url": "/Best-Sellers-Pet-Supplies/zgbs/pet-supplies"
                },
                {
                    "name": "Software",
                    "url": "/best-sellers-software/zgbs/software"
                },
                {
                    "name": "Sports & Outdoors",
                    "url": "/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods"
                },
                {
                    "name": "Sports Collectibles",
                    "url": "/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles"
                },
                {
                    "name": "Tools & Home Improvement",
                    "url": "/Best-Sellers-Tools-Home-Improvement/zgbs/hi"
                },
                {
                    "name": "Toys & Games",
                    "url": "/Best-Sellers-Toys-Games/zgbs/toys-and-games"
                },
                {
                    "name": "Unique Finds",
                    "url": "/Best-Sellers-Unique-Finds/zgbs/boost"
                },
                {
                    "name": "unknown",
                    "url": "/unknown"
                }
            ]

            # Loop through the categories and insert them into the database

            for category in categories:
                c.execute("INSERT INTO \"amazonSeller_category\" (name, link, country_id) VALUES (%s, %s, %s)", (category['name'], category['url'], '2'))
            # Fetch all records from the table
            #c.execute("SELECT * FROM \"amazonSeller_country\"")
            #records = c.fetchall()

            # Print the records
            #for record in records:
                #print(record)

            # Insert a new record
            # Note: This will throw an error if a country with the same name/code already exists
            # due to the PRIMARY KEY or UNIQUE constraints, handle this accordingly.
           # c.execute("INSERT INTO amazonSeller_country (name, code) VALUES (%s, %s)", ('United States', 'US'))
            
        conn.commit()
        conn.close()
            # Commit is automatic with 'with' statement
except psycopg2.Error as e:
    print(f"An error occurred: {e}")
finally:
    print("Operation completed.")