#this script is used to get the seller information from the amazon website
#It takes ASIN as input and returns the seller information
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
def get_request(url):
    """Make a request with a random user agent."""
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    response = requests.get(url, headers=headers)
    return response
def fetch_amazon_best_sellers():
    url = " https://www.amazon.com/best-sellers-video-games/zgbs/videogames"
    response = get_request(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        categories = soup.find_all("div", {"id": "zg_left_col"})

        if categories:
            category_links = categories[0].find_all("a")
            for link in category_links:
                category_name = link.get_text().strip()
                category_url = link['href']
                print(category_name, category_url)
        else:
            print("No categories found.")
    else:
        print("Failed to fetch the page.")

fetch_amazon_best_sellers()

def get_subcategories(category_url):
    """Fetch and parse subcategories using requests and BeautifulSoup."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    full_url = urljoin(AMAZON_BASE_URL, category_url)
    response = requests.get(full_url, headers=headers)

    subcategories_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Adjust the selector based on the structure of the Amazon subcategory page
        subcategory_elements = soup.select("_p13n-zg-nav-tree-all_style_zg-browse-root__-jwNv")

        for element in subcategory_elements:
            subcategory_name = element.get_text().strip()
            subcategory_url = element.get('href')  # Safely get the href attribute
            if subcategory_name and subcategory_url:
                subcategories_data.append({"name": subcategory_name, "url": subcategory_url})
    else:
        print(f"Failed to fetch the subcategory page for {full_url}")
    print("subcategories_data")    
    print(subcategories_data)
    return subcategories_data

def get_lowest_child_categories(parent_categories):
    all_child_categories = []

    for category in parent_categories:
        subcategories = get_subcategories(category['url'])
        if not subcategories:
            all_child_categories.append(category)
        else:
            for subcategory in subcategories:
                child_subcategories = get_subcategories(subcategory['url'])
                if not child_subcategories:
                    all_child_categories.append(subcategory)

    return all_child_categories

# Example usage
parent_categories = [
    {
        "name": "Amazon Devices & Accessories",
        "url": "/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices"
    },
    {
        "name": "Video Games",
        "url": "/best-sellers-video-games/zgbs/videogames"
    }
]

# lowest_child_categories = get_lowest_child_categories(parent_categories)
# for category in lowest_child_categories:
#     print(category)
