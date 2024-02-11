# This script gets all the ASIN of the Best Seller products from the database
# It takes best seller category as input and saves the ASIN of the products of that category
# the ASIN are saved in database in product table

import random
import requests
from bs4 import BeautifulSoup
import json
import os
import time
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

        index = 0

        """Fetch and parse subcategories using requests and BeautifulSoup."""
        userAgentIndex = random.randint(0, len(USER_AGENTS) - 1)
        user = USER_AGENTS[userAgentIndex]
        # if "ref" in url:
        #     url = url.split("ref")[0]
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

        full_url = "https://www.amazon.com" + url
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

def delete_ids_from_list():
    file_path = os.path.join(os.path.dirname(__file__), "list.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            
        for item in data:
            if "id" in item:
                del item["id"]
        
        with open(file_path, "w") as file:
            json.dump(data, file)
def delete_items_if_false_url():
    file_path = os.path.join(os.path.dirname(__file__), "list.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            
        data = [item for item in data if "url" not in item or "/zgbs/" in item.get("url", "")]
        
        with open(file_path, "w") as file:
            json.dump(data, file)            

subcategories = [{
        "name": "Appliances",
        "link": "/Best-Sellers-Appliances/zgbs/appliances/ref=zg_bs_pg_2_appliances?_encoding=UTF8&amp;pg=2"
    },
   ]


def getall_asin_from_sub_category():
    file_path = os.path.join(os.path.dirname(__file__), "list.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        for item in data:
            if "url" in item:
                asins = get_product_asin(item["url"])
                item["asins"] = asins
                print(item)
        
        with open(file_path, "w") as file:
            json.dump(data, file)

def get_missing_asin_from_sub_category():
    file_path = os.path.join(os.path.dirname(__file__), "list.json")
    
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



def get_all_unique_asins():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "list.json")
    asin_array = []

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        for item in data:
            if "asins" in item:
                if isinstance(item["asins"], dict):
                    asin_array.extend(item["asins"].keys())
                elif isinstance(item["asins"], list):
                    asin_array.extend(item["asins"])

    unique_asins = list(set(asin_array))

    # Create asin.txt file and write unique ASINs
    asin_file_path = os.path.join(current_dir, "asin.txt")
    with open(asin_file_path, "w") as asin_file:
        for asin in unique_asins:
            asin_file.write(asin + "\n")

    return unique_asins

def remove_duplicate_asins():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "test.json")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)

        for item in data:
            if "asins" in item:
                item["asins"] = list(set(item["asins"]))

        with open(file_path, "w") as file:
            json.dump(data, file)

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

get_missing_asin_from_sub_category()
remove_duplicate_asins()

# unique_asins = get_all_unique_asins()

# with open("output.txt", "w") as file:
#     file.write(str(unique_asins))

# print("Output written to output.txt")
