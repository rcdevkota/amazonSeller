# This script gets all the ASIN of the Best Seller products from the database
# It takes best seller category as input and saves the ASIN of the products of that category
# the ASIN are saved in database in product table

import random
import requests
from bs4 import BeautifulSoup
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()
AMAZON_BASE_URL = "https://www.amazon.com/"
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
class Product:
    """Product class."""
    def __init__(self, value):  # Constructor
        self.my_attribute = value
    def my_method(self):
        return f"Value is {self.my_attribute}"
    def send_request(url):
        #print("+++++++++++++++++++++++++++++++++Sending request+++++++++++++++++++++++++++++++++")
        full_url= "https://www.amazon.com" + url
        #print(full_url)
        response = requests.get(
            url='https://app.scrapingbee.com/api/v1/',
            params={
                'api_key': 'N38XB8KVB7DUA7XS5K084RADZA0DRXL0J1T2G6GUSEZZE808U1J2U098DOAQ6CK9SQNMLIJC2BZRHTW8',
                'url': full_url,
                'render_js': 'false',
            },
            timeout=60
        )
        print(full_url,'Response HTTP Status Code: ', response.status_code)
        #print('Response HTTP Response Body: ', response.content)
        return response
    
    def extract_ids(data):
        ids = []
        for item in data:
            if 'id' in item:
             ids.append(item['id'])
        return ids

def get_product_asin(url):
    try:
        response = Product.send_request(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize an empty list to store product data
        products_data = []
        product_info = None
        # Iterate over each product div and extract required information

        grid = soup.find('div', {'class': 'p13n-gridRow'})
        gridItems = grid.find_all('div', {'class': '_cDEzb_grid-column_2hIsc'})  # {id:'gridItemRoot'})

        retryBackOff = 1
        while len(gridItems) == 0:
            response = Product.send_request(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            grid = soup.find('div', {'class': 'p13n-gridRow'})
            gridItems = grid.find_all('div', {'class': '_cDEzb_grid-column_2hIsc'})  # {id:'gridItemRoot'})
            if retryBackOff > 3:
                break
            time.sleep(retryBackOff)
            retryBackOff = retryBackOff + 1
        ids = []
        asinList = soup.find('div', {'class': 'p13n-desktop-grid'})
        ids += Product.extract_ids(json.loads(asinList.get('data-client-recs-list')))
        #print("second page outcome..................")
        #print(ids)
        #print(json.loads(asinList.get('data-client-recs-list')))

        second_page_link = soup.find('li', {'class': 'a-normal'}).find('a')
        if second_page_link:
            second_page_url = second_page_link['href']
            #print(second_page_url)
            response = Product.send_request(second_page_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            asinList = soup.find('div', {'class': 'p13n-desktop-grid'})
            ids += Product.extract_ids(json.loads(asinList.get('data-client-recs-list')))
            #print(second_page_link)
            print(second_page_url)
            #print("first and second page outcome..................")
        print(ids)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        ids = []  # Return default ids if an error occurs
    return ids

def get_missing_asin_from_sub_category():
    file_path = os.path.join(os.path.dirname(__file__), "asins.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        for item in data:
            if "url" in item and ("asins" not in item or not item["asins"]):
                asins = get_product_asin(item["url"].split("ref")[0])
                item["asins"] = asins
                #print(item)
        
        with open(file_path, "w") as file:
            json.dump(data, file)

get_missing_asin_from_sub_category()


