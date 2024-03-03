#this script is used to get the seller information from the amazon website
#It takes ASIN as input and returns the seller information
import csv
import random
import re
import time
from typing import List
import requests
from bs4 import BeautifulSoup
import os
import json
import multiprocessing
import concurrent.futures


AMAZON_BASE_URL = "https://www.amazon.de"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G985F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 10; en-us; SM-N960U Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (BB10; Touch) AppleWebKit/537.35+ (KHTML, like Gecko) Version/10.3.3.3216 Mobile Safari/537.35+",
    "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254",
    "Mozilla/5.0 (Windows NT 10.0; ARM; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254"
]
request = requests.Session()

class Seller:
    """Seller class."""
    def __init__(self):  # Constructor
        self.lock = False
        self.asins_to_txt = []
        self.counter = 0

    def my_method(self):
        return f"Value is {self.my_attribute}"
    
    
    def add_info_to_txt(self, asin, extracted_info):
        self.asins_to_txt.append((asin, extracted_info))

    def write_failed_asins_to_file(self, asins):
        with open('failed_asins.txt', 'a') as file:
            for asin in asins:
                file.write(f"{asin}\n")

    def write_to_file(self):
#        copyList = self.asins_to_txt.copy()
 #       self.asins_to_txt.clear()
        with open('info.txt', 'a') as file: 
            for asin, extracted_info in self.asins_to_txt:
                print(f"Writing to file: {self.counter} => {asin}")
                self.counter = self.counter + 1
                file.write(f'"{asin}": {extracted_info},\n')
            self.asins_to_txt = []
    #    self.lock = False

    def send_request(self, url):
        #print("+++++++++++++++++++++++++++++++++Sending request+++++++++++++++++++++++++++++++++")
        full_url= "https://www.amazon.de" + url
        #print(full_url)
        response = requests.get(
            url='https://app.scrapingbee.com/api/v1/',
            params={
                'api_key': 'RVHWA75QSDH3YVIF3GGQ9G8PPS7SY6YCBZN2402YQ7G63638AK3W1Q4TQ00AYQ4JGSNARY4ARNF87EFL',
                'url': full_url,
                'render_js': 'false',
            },
            timeout=60
        )
        print(full_url,'Response HTTP Status Code: ', response.status_code)
        #print('Response HTTP Response Body: ', response.content)
        return response

    def send_request_without_proxy(url):
        userAgentIndex = random.randint(0, len(USER_AGENTS) - 1)
        user = USER_AGENTS[userAgentIndex]
       
        headers = {
            "user-agent": user,
            "Cookie": "8rShzaMtFiBn4qZUtWPg6Ngo1sf84TCBWPLhCqqbuGwfmFstKRjjI7GyuAYHD1QZsYVXuX2nL"
            "+WFpTLONMwq4Rf5N1OAAvXKGOOd7EJT+KIx2TK+ePErJBXZEydz/vb36n/9FMuT9DyhmtT3j4OgZQTJFpTvVQYNbU2dXtbW3j7077N10ULoN+AVL89Xo"
            "+Mi4DT9IPiD5sTVYMftd0XGD+G9/ocQBArPHoqJRuN28R9AyJVbQNzetOjGt0ZRQEzKdLLGMeEKXcSGBLe5tvpw3clZW5zynRw0LwdYvtbcf"
            "+qMWPPI7HPHvWlWp2zsGAsBv6p87LpdKh4ruT1rK24bUt7b2GqVpEop",
            "Referer": "https://www.amazon.de",
            "authority": "www.amazon.de",
            "path": url,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                    "application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
        }

        full_url = AMAZON_BASE_URL + url
        print(full_url)
        request.headers.update(headers)
        retryBackOff = 1
        response = None
        while not response:
            response = request.get(full_url, headers=headers, cookies={}) 
            if retryBackOff >= 10:
                break
            time.sleep(retryBackOff)
            retryBackOff = retryBackOff + 1
        print('Response HTTP Status Code: ', response.status_code)
        return response 
    
seller = Seller()
def get_product_info_and_seller_id(asin):
    global seller
    extracted_info = {}   
    url = "/dp/" + asin
    try:
        response = seller.send_request(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the product title
        product_title_tag = soup.find('span', id='productTitle')
        if product_title_tag:
            product_name = product_title_tag.get_text(strip=True)
            extracted_info['product_name'] = product_name
        else:
            extracted_info['product_name'] = 'unknown product name'
        store_name_tag = soup.find('a', id='bylineInfo')
        store_name_div = soup.find('div', id='bylineInfo_feature_div')
        #Extract the store name
        if store_name_div:
            store_name_tag = store_name_div.find('a')
            if store_name_tag:
                store_name = store_name_tag.get_text(strip=True).replace('Visit the ', '').replace(' Store', '')
                extracted_info['store_name'] = store_name
            else:
                extracted_info['store_name'] = 'unknown'
        else:
            extracted_info['store_name'] = 'unknown'


        # Extract the seller name and seller URL from the main div id
        merchant_info_div = soup.find('div', id='merchantInfoFeature_feature_div')
        if merchant_info_div:
            seller_name_tag = merchant_info_div.find('a')
            #print(seller_name_tag)
            if seller_name_tag:
                extracted_info['seller_name'] = seller_name_tag.text.strip()
                extracted_info['seller_id'] = get_seller_id_from_url(seller_name_tag['href'])
            else:
                extracted_info['seller_name'] = 'Not Available'
                extracted_info['seller_id'] = 'Not Found'
        else:
            extracted_info['seller_name'] = 'Not Found'
            extracted_info['seller_id'] = 'Not Found'

        if extracted_info['seller_id'] == 'Not Found':
            print("********************************************No seller ID found in Product page********************************************************************")
            print(asin,extracted_info)
            seller.add_info_to_txt(asin, extracted_info)
            return extracted_info

        seller_info = get_seller_info(extracted_info['seller_id'])
        extracted_info['seller_info'] = seller_info
        print("***********************************************SellerID found in Product Page*****************************************************************")
        print(asin,extracted_info)
        seller.add_info_to_txt(asin, extracted_info)
        return extracted_info
    except Exception as e:
        print("1****************************************************************************************************************")
        print(f"An error occurred: {str(e)}")
        print(asin,extracted_info)
        seller.add_info_to_txt(asin, extracted_info)
        return extracted_info

def extract_info_from_text(text, info):
    # Search for phone number, email, and address in the given text
    phone_match = re.search(r'Telefon:\s*([\+0-9\(\) -]+)', text)
    email_match = re.search(r'E-Mail:\s*([\w\.-]+@[\w\.-]+\.\w+)', text)

    if phone_match:
        info['phone_number'] = phone_match.group(1)
    if email_match:
        info['email'] = email_match.group(1)
    # Extract business name
    name_match = re.search(r'Geschäftsname:\s*([^<]+)', text)
    if name_match:
        info['name'] = name_match.group(1).strip()
    # Extract business address
    address_match = re.findall(r'Geschäftsadresse:\s*([^<]+)', text)
    if address_match:
        info['address'] = ', '.join(address_match).strip()

def get_seller_info(seller_url):
    global seller
    info = {
        'name': None,
        'email': None,
        'phone_number': None,
        'address': None,
        'about_seller': None,
        'detailed_seller_info': None
    }
    url = '/sp?ie=UTF8&seller=' + seller_url
    try:
        # Send a request to the URL
        response = seller.send_request(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract information from the first div (About Seller) a-box-inner a-padding-medium
        about_seller_div = soup.find(id="page-section-about-seller")
        if about_seller_div:
            about_seller_text = about_seller_div.get_text(separator=' ', strip=True)
            info['about_seller'] = about_seller_text
            extract_info_from_text(about_seller_text, info)
        detailed_info_div = soup.find(id="page-section-detail-seller-info")


        if detailed_info_div:
            detailed_info_text = detailed_info_div.get_text(separator=' ', strip=True)
            info['detailed_seller_info'] = detailed_info_text
            extract_info_from_text(detailed_info_text, info)
    except Exception as e:
        print("An error occurred:", str(e))

    return info

def get_seller_id_from_url(seller_url):
    # Extract the seller ID from the seller URL
    try:
        seller_id = None
        if seller_url:
            seller_id_match = re.search(r'seller=([A-Z0-9]+)', seller_url)
            if seller_id_match:
                seller_id = seller_id_match.group(1)
        return seller_id
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def get_asins_from_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "list.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        asin_set = set()  # Create an empty set to store ASINs

        for item in data:
            asins = item.get("asins")
            if asins:
                for asin in asins:
                    if asin:  # Check if the asin is not empty
                        try:
                            asin_set.add(asin)  # Add ASIN to the set
                        except Exception as e:
                            print(f"An error occurred while getting seller info for ASIN {asin}: {str(e)}")

        # Save ASINs to a text file
        asin_txt_path = os.path.join(current_dir, "asin.txt")
        with open(asin_txt_path, "w") as file:
            for asin in asin_set:
                file.write(asin + "\n")

        return data
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {str(e)}")
        return None
    
print("Script started")

def remove_duplicate_asins_from_all_asins():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    asin_txt_path = os.path.join(current_dir, "asin.txt")
    all_asin_txt_path = os.path.join(current_dir, "all-asins.txt")
    
    # Read the ASINs from asin.txt
    with open(asin_txt_path, "r") as asin_file:
        asins = asin_file.read().splitlines()
    
    # Read the existing ASINs from all-asins.txt
    with open(all_asin_txt_path, "r") as all_asin_file:
        existing_asins = all_asin_file.read().splitlines()
    
    # Remove duplicate ASINs
    unique_asins = set(asins) - set(existing_asins)
    
    # Write the unique ASINs back to asin.txt
    with open(asin_txt_path, "w") as asin_file:
        asin_file.write("\n".join(unique_asins))

#remove_duplicate_asins_from_all_asins()



def process_asin_batch(asins, asin_to_data_map, timeout=20):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_asin = {executor.submit(get_product_info_and_seller_id, asin): asin for asin in asins}
            for future in concurrent.futures.as_completed(future_to_asin, timeout=timeout):
                asin = future_to_asin[future]
                try:
                    info = future.result(timeout=timeout)  # Set a timeout for getting the result
                    if asin in asin_to_data_map:
                        asin_to_data_map[asin]['asins'][asin] = info
                except concurrent.futures.TimeoutError:
                    print(f"Fetching data for ASIN {asin} timed out")
                except Exception as e:
                    print(f"Failed to fetch data for ASIN {asin}: {str(e)}")
    except Exception as e:
        print(f"An error occurred while processing ASIN batch: {str(e)}")

def remove_duplicate_asins():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "sub_cat_asin.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        unique_asins = set()
        for item in data:
            asins = item.get("asins")
            if asins:
                for asin in list(asins.keys()):
                    if asin in unique_asins:
                        del asins[asin]
                    else:
                        unique_asins.add(asin)

        with open(file_path, "w") as file:
            json.dump(data, file)
        
        print("Duplicate ASINs removed successfully")
    except Exception as e:
        print(f"An error occurred while removing duplicate ASINs: {str(e)}")
    
def get_asins_from_asin_txt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    asin_file_path = os.path.join(current_dir, "all-asins.txt")
    asins: List[str] = []
    with open(asin_file_path, "r") as file:
        for line in file.readlines():
            
            asins.append(line.strip())
            if len(asins) >= 30:
                yield asins
                asins = []

def process_asins_and_save_in_batches():
    global seller
    # Process ASINs in batches
    # Determine the number of workers based on available CPU cores
    
    
    counter = 0
    for asins in get_asins_from_asin_txt():
        futures = []
        num_workers = multiprocessing.cpu_count()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            for asin in asins:
                futures.append(executor.submit(get_product_info_and_seller_id, asin))
                counter = counter + 1
            if counter == 0:
                break

            try:
                for future in concurrent.futures.as_completed(futures, 120):
                    try:
                        result = future.result()
                       #print(result)
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        exception_occured = True
            except concurrent.futures.TimeoutError:
                seller.write_failed_asins_to_file(asins)
                print("Failed to process ASINs:",asins)
            #breakpoint()
            seller.write_to_file()

    if exception_occured:
        print("Some errors occurred while processing ASINs")
        return

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
    with open('output1.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name', 'Store Name', 'Seller Name', 'Email'])
        writer.writerows(csv_data)

# current_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(current_dir, 'a.txt')
# updated_content = process_file(file_path)


process_asins_and_save_in_batches()
