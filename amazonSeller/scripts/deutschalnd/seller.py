#this script is used to get the seller information from the amazon website
#It takes ASIN as input and returns the seller information

import random
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

AMAZON_BASE_URL = "https://www.amazon.de/dp/"
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
    
    def send_request(asin):
        """Fetch and parse subcategories using requests and BeautifulSoup."""
        userAgentIndex = random.randint(0, len(USER_AGENTS) - 1)
        user = USER_AGENTS[userAgentIndex]
        if "ref" in asin:
            asin = asin.split("ref")[0]
        print(asin)
        headers = {
            "user-agent": user,
            "Cookie":os.getenv("DE_COOKIE"),
            "Referer": "https://www.amazon.de",
            "authority": "www.amazon.de",
            "path": asin,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                    "application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
        }
        time.sleep(30)
        full_url = full_url + asin
        request.headers.update(headers)
        retryBackOff = 1
        response = None
        while not response:
            response = request.get(full_url, headers=headers, cookies={})  # proxies=proxy)
            if retryBackOff >= 5:
                break
            time.sleep(retryBackOff)
            retryBackOff = retryBackOff + 1
        print('Response HTTP Status Code: ', response.status_code)
        return response 
    
eller = Seller()
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
    name_match = re.search(r'Verkäufer:\s*([^<]+)', text)
    if name_match:
        info['name'] = name_match.group(1).strip()
    # Extract business address
    address_match = re.findall(r'Addresse:\s*([^<]+)', text)
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


 