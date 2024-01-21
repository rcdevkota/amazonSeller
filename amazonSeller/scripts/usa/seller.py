#this script is used to get the seller information from the amazon website
#It takes ASIN as input and returns the seller information

import random
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
            "Cookie": "x-main=4H4PAb9kQtk2wwvWsrYULkO2C1fc3TSisJNgJp4H9kxZPFKG9foI4SD2UGi5iiAo; "
                    "at-main=Atza"
                    "|IwEBIP9O0aNybb5YG0xUQD9mk46jqanwHrU_NluV2rRSziiyWBfvVmC2dAZbfY1rRcAWEzrdYGG0LIyR9nJ5XZOOZBpC3fIrAz6iLaNWrVhZ_SiDF0QBLTXfAbbfLYlMLdKCYuB_7_ueRyiuJZWJ5qMU0ENjAsLsLAaZNbv_FhDIAlBdVfcgscdGjbUleDiEZbpEOkVa2OsOQs0Nyvssd_tErxda; sess-at-main=\"aQTU63C+9QPTNmIFQ+jeuMMcPkdu83eO5EmAyUR1NVU=\"; ubid-main=131-3218811-7398132; aws-target-data=%7B%22support%22%3A%221%22%7D; sp-cdn=\"L5Z9:DE\"; aws-ubid-main=458-4182210-1032216; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6ImRiYWRkNTY2LWE4MjEtNGM0NC04MDhhLTFlNzE1MWFlYWM2MCJ9.eyJzdWIiOiIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiWFdvcHJGSk9WZ0xPTE93XC9WQm1UN0xiR01qQlFTSW53RVl3dDZ1VWM5d009IiwiYXJuIjoiYXJuOmF3czppYW06OjQ1MzkyMTYzMjUzOTpyb290IiwidXNlcm5hbWUiOiJBeWFzaFBNVCJ9.SyJSbYrIC0g4z-DdImqudc1ZQSzx-kEVApme-FHr0WHhKrWJHVtgn0fJi5Fji87MvQFb8HM-oXBqv_l1pbZ_uQD1xMECFAfUzp5MJqOtTU3IXD8YWHeQ_LG8G4jARyLr; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A453921632539%3Aroot%22%2C%22alias%22%3A%22%22%2C%22username%22%3A%22AyashPMT%22%2C%22keybase%22%3A%22XWoprFJOVgLOLOw%2FVBmT7LbGMjBQSInwEYwt6uUc9wM%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D; session-id=140-3119798-0790727; session-id-apay=140-3119798-0790727; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; lc-main=en_US; csm-hit=tb:GVWHP05NVKPWXYHJS781+s-GVWHP05NVKPWXYHJS781|1704659747878&t:1704659747878&adb:adblk_yes; session-token=XwKzwhcALwSUcEAjOAOraT4WgvLKkfX3zqTWw+Yo8RUTuDbKqcAyHUNNHYLmV8pNfgo9XNNhsScZvRKaC3LcYyEE70fmSPfuTJjFjDYPH7ByxKHcvoxkpOqtB3+umRxPNZztPNp8j6TymgZNJpJUP8Y0r0CCfCiLBgiza30gY7V8B9tP4XRtY8y32G2I+evSNqaHY7xjbiHXjb39Uf3Bt4PxLis52cDbicGbMSNMGE9ygV1uivid7OP6ewOe5Ke6qAeI2pAozJcoCOZPaLqtcQzWVFvwxeKIaJ1ZK+RurVBJNhCkjU+SitnLRl3x0pEw1ee9cF3KxrNaJu1ZEcitKGmkL10Ef2lh",
            "Referer": "https://www.amazon.com",
            "authority": "www.amazon.com",
            "path": url,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                    "application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
        }

        full_url = AMAZON_BASE_URL + url
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
    

    def get_seller_info(seller_url):
        info = {}
        response = Seller.send_request(seller_url)
        return info
        
    
def get_product_info_and_seller_id(asin):
    extracted_info = {}   
    url = "/dp/" + asin
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
    if store_name_tag:
        store_name = store_name_tag.get_text(strip=True).replace('Visit the ', '').replace(' Store', '')
        extracted_info['store_name'] = store_name
    else:
        extracted_info['store_name'] = 'Store name not found'
    
     # Find the span with class 'a-size-small offer-display-feature-text-message' h1.a-size-large span.a-size-large
    sold_by_name_span = soup.find('span', class_='a-size-small offer-display-feature-text-message')

    # Proceed only if the span is found
    if sold_by_name_span:
        # Find the 'a' tag within the span
        sold_by_name_tag = sold_by_name_span.find('a')

        # Extract information if the 'a' tag is found
        if sold_by_name_tag:
            extracted_info['sold_by_name'] = sold_by_name_tag.text.strip()
            extracted_info['sold_by_url'] = 'https://www.amazon.com' + sold_by_name_tag['href']
        else:
            extracted_info['sold_by_name'] = 'Not Available'
            extracted_info['sold_by_url'] = 'Not Available'
    else:
        extracted_info['sold_by_name'] = 'Not Found'
        extracted_info['sold_by_url'] = 'Not Found'
    # extracted_info = {}

    # # Extracting the title
    # title_tag = soup.select_one('h1.a-size-large span.a-size-large')
    # extracted_info['title'] = title_tag.text.strip() if title_tag else 'Not Found'

    # # Extracting the number of sellers
    # number_of_sellers_tag = soup.select_one('div.olp-text-box > span:nth-of-type(1)')
    # extracted_info['numberOfSellers'] = number_of_sellers_tag.text.strip() if number_of_sellers_tag else 'Not Found'

    # # Extracting the seller link
    # seller_link_tag = soup.select_one('div.tabular-buybox-text span.a-size-small a')
    # extracted_info['sellerLink'] = 'https://www.amazon.com' + seller_link_tag['href'] if seller_link_tag else 'Not Found'

    # # Extracting the store name
    # store_name_tag = soup.select_one('div.centerColAlign div.a-section.a-spacing-none a.a-link-normal')
    # store_name = store_name_tag.text.strip().replace('Visit the ', '').replace(' Store', '') if store_name_tag else 'Not Found'
    # extracted_info['storeName'] = store_name

    # # Extracting the alternate seller link
    # seller_link_alt_tag = soup.select_one('div.a-section div.a-section div.a-section div.offer-display-feature-text span.a-size-small a')
    # extracted_info['sellerLinkAlt'] = 'https://www.amazon.com' + seller_link_alt_tag['href'] if seller_link_alt_tag else 'Not Found'

    # Return the extracted information
    print(extracted_info)
    return extracted_info
products = ['B07MCYDD62', 'B08412TYML', 'B00L1G7K50', 'B01BYKEEFQ', 'B0C3L93F2Q', 'B01J3WQ360', 'B01BYKV8FK', 'B0722C491T', 'B08DRS8MNF', 'B00L1G7LBI', 'B000PDFQ6K']

for product in products:
    get_product_info_and_seller_id(product)



    