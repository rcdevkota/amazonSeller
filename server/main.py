#this script is used to get the seller information from the amazon website
#It takes ASIN as input and returns the seller information

import os
import random
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time

AMAZON_BASE_URL = "https://www.amazon.com"
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

    def __init__(self, value):  # Constructor
        self.my_attribute = value

    def my_method(self):
        return f"Value is {self.my_attribute}"
    
    def send_request(url):
        userAgentIndex = random.randint(0, len(USER_AGENTS) - 1)
        user = USER_AGENTS[userAgentIndex]
       
        headers = {
            "user-agent": user,
            "Cookie": "uQEO+0qKCQfzI7nHWfd1pdzL2v8lKZmhW0OGIzAUjSH8ZESnSiO2TD58r8IuZ6xw8sJn1ve"
            "/Ndf/cjciqUYzg5K14tNT1RbavpKNWxmHDYfL7pPp+SkvXMD1qFEF7BaAWWJuypaTFEddGKwl8SgIaqQ/"
            "iZPcFFHPBfyBAEX507EAWOEUiazCsDG6aAzudHv/Lo+77wvm81x8wrko8nO2xfWP3SCdA8vKM8bP24u9uaKMVD2oxytQuCV+1Ey0TSXiJYFw9UNbfGjxQ8CF2prWanvK42m9N3+SWE2AGcBGwRapLcWhLSoQGiZdGnQYL2qNTFfNlAjI/g6XBvQ8XpMDOtNS/WJxlm7u ",

            "Referer": "https://www.amazon.com",
            "authority": "www.amazon.com",
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
    
    
def get_product_info_and_seller_id(asin):
    extracted_info = {}   
    url = "/dp/" + asin
    try:
        response = Seller.send_request(url)
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
        print("after name and store name:",extracted_info)
        # Extract the seller name and seller URL from the main div id
        merchant_info_div = soup.find('div', id='merchantInfoFeature_feature_div')
        if merchant_info_div:
            seller_name_tag = merchant_info_div.find('a')
            print(seller_name_tag)
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
            print("sellerUrl: ", extracted_info['seller_id'])
            return extracted_info

        seller_info = get_seller_info(extracted_info['seller_id'])
        extracted_info['seller_info'] = seller_info
        add_info_to_json(asin, extracted_info)
        # Return the extracted information
        print("sellerUrl: ", extracted_info['seller_id'])
        print(extracted_info)
        
        return extracted_info
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(extracted_info)
        return extracted_info

products = [ "B078GX9R5W",
            "B08PMP778K",
            "B098M47N55",
            "B0BV5PPRFM",
            "B08L5HKWFX",
            "B0BKD96YJT",
            "B08PNQTYV2",
            "B07RJZMC49",
            "B095FTDJB6",
            "B0751N2Y78",
            "B0BKTMYGTQ",
            "B08PNP5YGV",
            "B08B5MYT8T",
            "B08X1KKVCZ",
            "B09LP9TM5L"]

def add_info_to_json(asin, extracted_info):
            data = {}
            try:
                with open('info.json', 'r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                pass

            data[asin] = extracted_info

            with open('info.json', 'w') as file:
                json.dump(data, file)
def extract_info_from_text(text, info):
    # Search for phone number, email, and address in the given text
    phone_match = re.search(r'Telephone:\s*([\+0-9\(\) -]+)', text)
    email_match = re.search(r'E-Mail:\s*([\w\.-]+@[\w\.-]+\.\w+)', text)

    if phone_match:
        info['phone_number'] = phone_match.group(1)
    if email_match:
        info['email'] = email_match.group(1)
    # Assuming the business name is in the format: "Inh. [Name]"
    name_match = re.search(r'Inh.\s*([^&]+)', text)
    if name_match:
        info['name'] = name_match.group(1).strip()

def get_seller_info(seller_url):
    
    info = {
        'name': None,
        'email': None,
        'phone_number': None,
        'address': None,
        'about_seller': None,
        'detailed_seller_info': None
    }
    url = '/sp?ie=UTF8&seller=' + seller_url
    print("sellerUrl: ", seller_url)
    try:
        # Send a request to the URL
        response = Seller.send_request(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract information from the first div (About Seller) a-box-inner a-padding-medium
        about_seller_div = soup.find(id="page-section-about-seller")
        if about_seller_div:
            about_seller_text = about_seller_div.get_text(separator=' ', strip=True)
            info['about_seller'] = about_seller_text
            extract_info_from_text(about_seller_text, info)
        # Extract information from the second div (Detailed Seller Information) a-box-inner a-padding-medium
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

# Example usage
# seller_url = '/sp?ie=UTF8&seller=A3SG0AEGKJK9W3&asin=B0CP8J6KTH'
# seller_info = get_product_info_and_seller_id("B08412TYML")
# print(seller_info)

#print(get_seller_id_from_url('https://www.amazon.com/gp/help/seller/at-a-glance.html/ref=dp_merchant_link?ie=UTF8&seller=A2J9CB3QL3LKD1&asin=B07RP1YGHD&ref_=dp_merchant_link'))
# for product in products:
#      get_product_info_and_seller_id(product)
     

def make_asin_key_empty():
    file_path = "/Users/rcd/Documents/GitHub/prufengel/amazonSeller/amazonSeller/scripts/usa/list.json"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        for item in data:
            asins = item.get("asins")
            if asins:
                item["asins"] = {asin: {} for asin in asins}

        with open(file_path, "w") as file:
            json.dump(data, file)
        
        print("ASINs changed to empty objects")


def get_asins_from_json():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "list.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        for item in data:
            asins = item.get("asins")
            if asins:
                for asin, info in asins.items():
                    if not info:  # Check if the asin has an empty object
                        try:
                            seller_info = get_product_info_and_seller_id(asin)
                            #print("added to json")
                            asins[asin] = seller_info
                        except Exception as e:
                            print(f"An error occurred while getting seller info for ASIN {asin}: {str(e)}")

            with open(file_path, "w") as file:
                json.dump(data, file)
        return data
    except Exception as e:
        print(f"An error occurred while reading the JSON file: {str(e)}")
        return None

def remove_duplicate_asins():
    file_path = "/Users/rcd/Documents/GitHub/prufengel/amazonSeller/amazonSeller/scripts/usa/list.json"
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
    
#remove_duplicate_asins()
#make_asin_key_empty();
get_asins_from_json()