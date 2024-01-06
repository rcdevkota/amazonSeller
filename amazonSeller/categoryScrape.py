# # Description: This file scrapes the Amazon Best Sellers page and extracts the categories and their URLs.
# # The categories are stored in database in Category model with name and URL
# # the subcategories are stored in database in Subcategory model with name and URL ( only the child categories are stored )

# import requests
# from bs4 import BeautifulSoup
# import random
# import string
# from selectorlib import Extractor
# import requests, functools 
# import json 
# import re, logging
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# import time
# from fake_useragent import UserAgent
# import sys
# import testproxy
# import urllib.parse


# def get_text_via_scrapingbee(url):
#     country_code = get_url_argument("country_code", "us") #"de"
#     render_js = get_url_argument("render_js", "false")
#     premium = get_url_argument("premium_proxy", "true")
#     encoded_url = get_url_argument("url", urllib.parse.quote(url))
#     complete_url = "https://app.scrapingbee.com/api/v1/?api_key=RVHWA75QSDH3YVIF3GGQ9G8PPS7SY6YCBZN2402YQ7G63638AK3W1Q4TQ00AYQ4JGSNARY4ARNF87EFL" + premium + country_code + render_js + encoded_url
#     return get_text_via_requests_lib(complete_url, False, False, None)

# def send_request(url):
#     response = requests.get(
#         url='https://app.scrapingbee.com/api/v1/',
#         params={
#             'api_key': 'H6U4CNF21J3B83L0CZL0RLFM0GE7T9PZ9S6DTUT60EOPL7YZB0YSAHVO3XHM5SB6VAHBFFIZDUKKDN9S',
#             'url': url,  
#         },
        
#     )
#     print('Response HTTP Status Code: ', response.status_code)
#     print('Response HTTP Response Body: ', response.content)
#     return response.content 
# #send_request()

# def get_url_argument(key, value):
#     return "&{}={}".format(key, value)
    
# def get_text_via_requests_lib(url, use_headers, rotate_proxy, proxies):
#     ua = UserAgent()
#     uag_random = ua.random  
    
#     if use_headers:
#         headers = {
#             'dnt': '1',
#             'upgrade-insecure-requests': '1',
#             'User-Agent': uag_random,
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'sec-fetch-site': 'same-origin',
#             'sec-fetch-mode': 'navigate',
#             'sec-fetch-user': '?1',
#             'sec-fetch-dest': 'document',
#             'referer': 'https://www.amazon.com/',
#             'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#         }
#     else:
#         headers = None

#     # Download the page using requests
#     logging.info("# Downloading %s"%url)
    
#     result = None
#     tries = 0
    
#     while not result:
#         tries = tries + 1
#         seconds = (tries - 1) * 1
#         if seconds > 0:
#             logging.info("## Sleep before next try: " + str(seconds) + " seconds.")
#             time.sleep(seconds)
#         if tries > 10:
#             if rotate_proxy:
#                 testproxy.rotate_proxy() 
#                 tries = 0
#             else:
#                 logging.error("## Too many errors downloading %s"%url)
#                 return None
#         try:
#             r = requests.get(url, headers=headers, proxies=proxies, timeout=120)
#             logging.info("## " + str(r))
#             if 'captcha' in str(r.text):
#                 uag_random = ua.random
#                 logging.info('## Bot has been detected... retrying ... use new identity: ' + str(uag_random) + '. Try again! (' + str(tries) + ' tries)')
#                 continue        
#             # Simple check to check if page was blocked (Usually 503)
#             elif r.status_code > 500:
#                 if "To discuss automated access to Amazon data please contact" in r.text:
#                     logging.info("## Page %s was blocked by Amazon. Please try using better proxies. Try again (%d tries)"%(url,tries))
#                 else:
#                     logging.info("## Page %s must have been blocked by Amazon as the status code was %d. Try again (%d tries)"%(url,r.status_code,tries))
#                 continue      
#             else:
#                 logging.debug('## Bot bypassed')
#                 if not r:
#                     logging.info('## Error! Result is None! (' + str(tries) + ' tries)')
#                 result = r
#         except requests.exceptions.ProxyError:
#             logging.info('## Proxy Error! Run into timeout. Try again! (' + str(tries) + ' tries)')
#         except requests.exceptions.ReadTimeout:
#             logging.info('## ReadTimeout! Run into timeout. Try again! (' + str(tries) + ' tries)')
#         except requests.exceptions.SSLError:
#             logging.info('## SSLError! Run into timeout. Try again! (' + str(tries) + ' tries)')
#         except requests.exceptions.ConnectTimeout:
#             logging.info('## ConnectTimeout! Run into timeout. Try again! (' + str(tries) + ' tries)')
#         except requests.exceptions.ConnectionError:
#             logging.info('## ConnectionError! Run into timeout. Try again! (' + str(tries) + ' tries)')  
            
#     return result.text

# if __name__ == "__main__":
#     logging.info(f"Arguments count: {len(sys.argv)}") 
#     result = get_text_via_scrapingbee("https://amazon.de/-/de/Jura-71794-Claris-Smart-Filterpatrone-3er-Pack/dp/B00VF9BJBE/ref=zg_bs_kitchen_sccl_1/262-1621054-9226751?pd_rd_i=B00VF9BJBE&psc=1")
#     logging.info(result)
    

# def fetch_amazon_best_sellers_main_category():
#     # URL of the Amazon best sellers page
#     url = "https://www.amazon.com/gp/bestsellers/"
    
#     # Set headers to mimic a web browser
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

#     # Send a GET request to the URL
#     response = requests.get(url, headers=headers)
#     categories_data = []
#     if response.status_code == 200:
#         # Parse the HTML content of the response
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Find the div element with id "zg_left_col2" which contains the categories
#         categories = soup.find_all("div", {"id": "zg_left_col2"})

#         if categories:
#             # Find all the <a> tags within the categories div
#             category_links = categories[0].find_all("a")
            
#             # Iterate over the category links
#             for link in category_links:
#                 # Extract the category name and URL
#                 category_name = link.get_text().strip()
#                 category_url = link['href'].split('/ref')[0]  # Remove everything from /ref in the URL
#                 categories_data.append({'name': category_name, 'url': category_url})
#             return categories_data       
#         else:
#             print("No categories found.")
#             return ({"error": "No categories found."})
#     else:
#         print("Failed to fetch the page.")
#         return ({"error": "Failed to fetch the page."})


# category = [
#     {
#         "name": "Amazon Devices & Accessories",
#         "url": "/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices"
#     },
#     {
#         "name": "Amazon Renewed",
#         "url": "/Best-Sellers-Amazon-Renewed/zgbs/amazon-renewed"
#     },
#     {
#         "name": "Appliances",
#         "url": "/Best-Sellers-Appliances/zgbs/appliances"
#     },
#     {
#         "name": "Apps & Games",
#         "url": "/Best-Sellers-Apps-Games/zgbs/mobile-apps"
#     },
#     {
#         "name": "Arts, Crafts & Sewing",
#         "url": "/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts"
#     },
#     {
#         "name": "Audible Books & Originals",
#         "url": "/Best-Sellers-Audible-Books-Originals/zgbs/audible"
#     },
#     {
#         "name": "Automotive",
#         "url": "/Best-Sellers-Automotive/zgbs/automotive"
#     },
#     {
#         "name": "Baby",
#         "url": "/Best-Sellers-Baby/zgbs/baby-products"
#     },
#     {
#         "name": "Beauty & Personal Care",
#         "url": "/Best-Sellers-Beauty-Personal-Care/zgbs/beauty"
#     },
#     {
#         "name": "Books",
#         "url": "/best-sellers-books-Amazon/zgbs/books"
#     },
#     {
#         "name": "Camera & Photo Products",
#         "url": "/best-sellers-camera-photo/zgbs/photo"
#     },
#     {
#         "name": "CDs & Vinyl",
#         "url": "/best-sellers-music-albums/zgbs/music"
#     },
#     {
#         "name": "Cell Phones & Accessories",
#         "url": "/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless"
#     },
#     {
#         "name": "Climate Pledge Friendly",
#         "url": "/Best-Sellers-Climate-Pledge-Friendly/zgbs/climate-pledge"
#     },
#     {
#         "name": "Clothing, Shoes & Jewelry",
#         "url": "/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion"
#     },
#     {
#         "name": "Collectible Coins",
#         "url": "/Best-Sellers-Collectible-Coins/zgbs/coins"
#     },
#     {
#         "name": "Computers & Accessories",
#         "url": "/Best-Sellers-Computers-Accessories/zgbs/pc"
#     },
#     {
#         "name": "Digital Educational Resources",
#         "url": "/Best-Sellers-Digital-Educational-Resources/zgbs/digital-educational-resources"
#     },
#     {
#         "name": "Digital Music",
#         "url": "/Best-Sellers-Digital-Music/zgbs/dmusic"
#     },
#     {
#         "name": "Electronics",
#         "url": "/Best-Sellers-Electronics/zgbs/electronics"
#     },
#     {
#         "name": "Entertainment Collectibles",
#         "url": "/Best-Sellers-Entertainment-Collectibles/zgbs/entertainment-collectibles"
#     },
#     {
#         "name": "Gift Cards",
#         "url": "/Best-Sellers-Gift-Cards/zgbs/gift-cards"
#     },
#     {
#         "name": "Grocery & Gourmet Food",
#         "url": "/Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery"
#     },
#     {
#         "name": "Handmade Products",
#         "url": "/Best-Sellers-Handmade-Products/zgbs/handmade"
#     },
#     {
#         "name": "Health & Household",
#         "url": "/Best-Sellers-Health-Household/zgbs/hpc"
#     },
#     {
#         "name": "Home & Kitchen",
#         "url": "/Best-Sellers-Home-Kitchen/zgbs/home-garden"
#     },
#     {
#         "name": "Industrial & Scientific",
#         "url": "/Best-Sellers-Industrial-Scientific/zgbs/industrial"
#     },
#     {
#         "name": "Kindle Store",
#         "url": "/Best-Sellers-Kindle-Store/zgbs/digital-text"
#     },
#     {
#         "name": "Kitchen & Dining",
#         "url": "/Best-Sellers-Kitchen-Dining/zgbs/kitchen"
#     },
#     {
#         "name": "Movies & TV",
#         "url": "/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv"
#     },
#     {
#         "name": "Musical Instruments",
#         "url": "/Best-Sellers-Musical-Instruments/zgbs/musical-instruments"
#     },
#     {
#         "name": "Office Products",
#         "url": "/Best-Sellers-Office-Products/zgbs/office-products"
#     },
#     {
#         "name": "Patio, Lawn & Garden",
#         "url": "/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden"
#     },
#     {
#         "name": "Pet Supplies",
#         "url": "/Best-Sellers-Pet-Supplies/zgbs/pet-supplies"
#     },
#     {
#         "name": "Software",
#         "url": "/best-sellers-software/zgbs/software"
#     },
#     {
#         "name": "Sports & Outdoors",
#         "url": "/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods"
#     },
#     {
#         "name": "Sports Collectibles",
#         "url": "/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles"
#     },
#     {
#         "name": "Tools & Home Improvement",
#         "url": "/Best-Sellers-Tools-Home-Improvement/zgbs/hi"
#     },
#     {
#         "name": "Toys & Games",
#         "url": "/Best-Sellers-Toys-Games/zgbs/toys-and-games"
#     },
#     {
#         "name": "Unique Finds",
#         "url": "/Best-Sellers-Unique-Finds/zgbs/boost"
#     },
#     {
#         "name": "Video Games",
#         "url": "/best-sellers-video-games/zgbs/videogames"
#     }
# ]

# def fetch_amazon_best_sellers_sub_category(category_url):
#     # Set headers to mimic a web browser
#     # Generate a random string of length 10
#     random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

#     headers = {
#         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3 {random_string}"
#     }
#     #url = "https://www.amazon.com/" + category_url
#     url = "https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/"
#     print(url)
#     # Send a GET request to the URL
#     response = send_request(url)    
#     sub_categories_data = []
#     if response.status_code == 200:
#         # Parse the HTML content of the response
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         # Find the div elements with class "_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf"
#         categories = soup.find_all("div", {"class": "_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf"})

#         if categories:
#             # Find all the <a> tags within the categories div
#             category_links = categories[0].find_all("a")
            
#             # Iterate over the category links
#             for link in category_links:
#                 # Extract the category name and URL
#                 category_name = link.get_text().strip()
#                 category_url = link['href'].split('/ref')[0]  # Remove everything from /ref in the URL
#                 sub_categories_data.append({'name': category_name, 'url': category_url})
#                 print(category_name, category_url)
#                 print()
#             return sub_categories_data       
#         else:
#             print("No categories found.")
#             return ({"error": "No categories found."})
#     else:
#         print("Failed to fetch the page.")
#         return ({"error": "Failed to fetch the page."})
    
# fetch_amazon_best_sellers_sub_category("/Best-Sellers-Appliances/zgbs/appliances")