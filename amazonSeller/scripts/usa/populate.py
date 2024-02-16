#this script is used to scrape all the categories from amazon
import re
import requests
from bs4 import BeautifulSoup
import json
import psycopg2
import os
from dotenv import load_dotenv
import csv
import pandas as pd



load_dotenv()

def get_asin_missing_item_from_sub_category():
    file_path = os.path.join(os.path.dirname(__file__), "list.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        missing_asin_items = []
        for item in data:
            if "asins" not in item or not item["asins"]:
                missing_asin_items.append(item)
        
        print(json.dumps(missing_asin_items))

def get_all_asins():
    # Use '__file__' to get the directory of the current script. Adjust if necessary.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "sub_cat_asin.json")
    print(file_path)    
    asin_set = set()  # Using a set to ensure uniqueness
    print(" dsadfsafile")

    # Check if the JSON file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            print("file")
            data = json.load(file)  # Load the JSON data

        # Iterate through each item in the JSON data
        for item in data:
            # Check if 'asins' key exists and has elements
            if "asins" in item and item["asins"]:
                # Extend the set with the ASINs from the current item
                asin_set.update(item["asins"])

    # Path to the output text file
    asin_file_path = os.path.join(current_dir, "wasin.txt")
    # Write all unique ASINs to the file
    with open(asin_file_path, "w") as asin_file:
        for asin in asin_set:
            asin_file.write(asin + "\n")

    return list(asin_set)  # Optionally, return the list of unique ASINs
 
def remove_duplicate_asins():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "sub_cat_asin.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        # Process each item individually to remove duplicate ASINs
        for item in data:
            if "asins" in item:
                # Convert the list of ASINs to a set to remove duplicates, then back to a list
                item["asins"] = list(set(item["asins"]))

        # Write the updated data back to the file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)  # Using indent for better readability of the JSON file
        print("Duplicate ASINs removed successfully.")

def add_asin_to_db(asins):
    try:
        # Connect to your PostgreSQL database
        with psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
        ) as conn:
            with conn.cursor() as c:
                for asin in asins:
                    print(asin)
                    try:
                        c.execute("INSERT INTO \"amazonSeller_us_productinfo\" (asin, main_category_id, sub_category_id, scraped, contacted) VALUES ( %s, %s, %s, %s, %s)", (asin, '32', '16050','False','False'))
                    except psycopg2.errors.UniqueViolation:
                        print(f"Skipping duplicate key violation:")
                        continue
            conn.commit()
            conn.close()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        print("Operation completed.")

def fix_json_formatting(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        for line in lines:
            try:
                # Try to load the JSON to see if it's already correct
                json.loads(line)
                file.write(line)  # Line is fine, write it back to the file
            except json.JSONDecodeError:
                # Attempt to fix common issues
                try:
                    # Use a recursive function to fix nested objects
                    corrected_line = fix_nested_json(line)
                    file.write(corrected_line)  # Write the corrected line back to the file
                except Exception as e:
                    # If it's still not valid or encounters an error, log the error or handle it as needed
                    print(f"Could not fix line: {line}")
                    # Optionally, write the unfixable line back to the file to not lose data
                    file.write(line)

def fix_nested_json(line):
    # Recursive function to fix nested objects in JSON line
    obj = json.loads(line)
    fixed_obj = fix_nested_object(obj)
    return json.dumps(fixed_obj)

def fix_nested_object(obj):
    # Recursive function to fix nested objects in JSON object
    if isinstance(obj, dict):
        fixed_dict = {}
        for key, value in obj.items():
            fixed_key = fix_key_quotes(key)
            fixed_value = fix_nested_object(value)
            fixed_dict[fixed_key] = fixed_value
        return fixed_dict
    elif isinstance(obj, list):
        fixed_list = []
        for item in obj:
            fixed_item = fix_nested_object(item)
            fixed_list.append(fixed_item)
        return fixed_list
    else:
        return obj

def fix_key_quotes(key):
    # Function to add quotes around keys if missing
    if not key.startswith('"') and not key.endswith('"'):
        return f'"{key}"'
    return key

def remove_asins_from_list():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "test.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        for item in data:
            if "asins" in item:
                item["asins"] = []

        with open(file_path, "w") as file:
            json.dump(data, file)
        
        print("ASINs removed successfully.")
    else:
        print("File not found.")

def extract_info_from_line(line):
    # Define regex patterns for extracting information
    patterns = {
        'asin': r'"([A-Z0-9]{10})":',
        'product_name': r'"product_name": "(.*?)"',
        'store_name': r'"store_name": "(.*?)"',
        'seller_name': r'"seller_name": "(.*?)"',
        'seller_id': r'"seller_id": "(.*?)"',
        'company_name': r'"name": "(.*?)"',  # Assuming company name is under "name"
        'email': r'"email": "(.*?)"',
        'phone_number': r'"phone_number": "(.*?)"',
        'address': r'"address": "(.*?)"',
        'about_seller': r'"about_seller": "(.*?)"',
        'seller_detailed_info': r'"detailed_seller_info": "(.*?)"',
        # 'scraped' and 'contacted' columns are not extracted from text, handle them as needed
    }
    extracted_info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, line)
        extracted_info[key] = match.group(1) if match else None
    return extracted_info

def add_product_info_to_db(file_path):

    try:
        # Connect to your PostgreSQL database
        with psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
        ) as conn:
            with conn.cursor() as c:
                with open(file_path, 'r', encoding='utf-8') as file:
                    counter = 0  # Counter variable
                    for line in file:
                        info = extract_info_from_line(line)
                        if info['asin']:
                            try:
                                c.execute("""
                                    UPDATE \"amazonSeller_us_productinfo\"
                                    SET product_name = %s, store_name = %s, seller_name = %s, seller_id = %s, 
                                        company_name = %s, email = %s, phone_number = %s, address = %s, 
                                        about_seller = %s, seller_detailed_info = %s, scraped = %s, contacted = %s
                                    WHERE asin = %s""",
                                    (info['product_name'], info['store_name'], info['seller_name'], info['seller_id'],
                                     info['company_name'], info['email'], info['phone_number'], info['address'],
                                     info['about_seller'], info['seller_detailed_info'], True, False,  # Assuming scraped=True, contacted=False
                                     info['asin']))
                            except psycopg2.errors.UniqueViolation:
                                print(f"Skipping duplicate key violation for ASIN: {info['asin']}")
                                continue
                            counter += 1  # Increment counter
                            print(f"Added product info for ASIN: {info['asin']} (Counter: {counter})")  # Print counter
                conn.commit()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
    finally:
        print("Operation completed.")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'info.txt')

#add_product_info_to_db(file_path)

def find_email_and_phone(text):
    """
    Searches for email addresses and phone numbers within a given text string.
    Returns a tuple containing the first found email and phone number, or None for each if not found.
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'  # Simplistic pattern; adjust as needed
    
    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)

    email = email_match.group(0) if email_match else None
    phone = phone_match.group(0) if phone_match else None

    return (email, phone)

def process_file(file_path):
    csv_data = []  # Store CSV data

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            email, phone = find_email_and_phone(line)
            
            # Extract product_name, store_name, and seller_name using regex
            product_name_match = re.search(r'"product_name": "(.*?)"', line)
            store_name_match = re.search(r'"store_name": "(.*?)"', line)
            seller_name_match = re.search(r'"seller_name": "(.*?)"', line)

            product_name = product_name_match.group(1) if product_name_match else ''
            store_name = store_name_match.group(1) if store_name_match else ''
            seller_name = seller_name_match.group(1) if seller_name_match else ''
            
            # Only add to CSV if email is found         
            if email:
                csv_data.append([product_name, store_name, seller_name, email])

    # Write to CSV
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name', 'Store Name', 'Seller Name', 'Email'])
        writer.writerows(csv_data)

#fix_json_formatting(file_path)
print("done formatting")
#updated_content = process_file(file_path)
print("done csv")
# Load the CSV file
csv_file = os.path.join(current_dir, 'output.csv')
df = pd.read_csv(csv_file)

# Save as an Excel file
excel_file = os.path.join(current_dir, 'output1.xlsx')
df.to_excel(excel_file, index=False)
