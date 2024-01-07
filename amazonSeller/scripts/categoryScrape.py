import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


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


index = 0

def send_request(url):
    """Send a GET request to the specified URL using the ScrapingBee API."""
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': 'H6U4CNF21J3B83L0CZL0RLFM0GE7T9PZ9S6DTUT60EOPL7YZB0YSAHVO3XHM5SB6VAHBFFIZDUKKDN9S',
            'url': url,  
        },
    )
    print('Response HTTP Status Code: ', response.status_code)
    return response 

def get_subcategories(category_url, id):
    """Fetch and parse subcategories using requests and BeautifulSoup."""
    userAgentIndex = random.randint(0, len(USER_AGENTS) - 1)  
    user = USER_AGENTS[userAgentIndex]
    headers = {
        "user-agent": user,
        "Cookie": "",
        "Referer": "https://www.google.de/",
    }           
    full_url = "https://www.amazon.com"+ category_url
    response = requests.get(full_url, headers=headers)
    #response = send_request(full_url)
    subcategories_data = []

    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        subcategory_elements = soup.find("div", {'class': '_p13n-zg-nav-tree-all_style_zg-browse-root__-jwNv'})
        if subcategory_elements is None:
            return subcategories_data
        subcategory_elements = (subcategory_elements.find("div", {"role": "group"})).find_all("div", {"role": "treeitem"})
        for elementDiv in subcategory_elements:
            element = elementDiv.find("a")
            if element is None: 
                return []
            subcategory_name = element.get_text().strip()
            subcategory_url = element['href']
            if subcategory_name:
                id = id + 1
                subcategories_data.append({"id": id, "name": subcategory_name, "url": subcategory_url})
    else:
        print(f"Failed to fetch the subcategory page for {full_url}")
    return subcategories_data

# Example usage
all_categories = [
    {
        "id": index,
        "name": "Any Department",
        "url": "/Best-Sellers-Video-Games-Mac-Game-Flight-Controls/zgbs/videogames/",
    },
]

def get_lowest_child_categories(parent_categories):
    """Loop through all parent categories and get lowest child categories."""
    global all_categories

    for category in parent_categories:
        subcategories = get_subcategories(category['url'], index)
        if len(subcategories) == 0:
            all_categories.append(category)
        else:
            get_lowest_child_categories(subcategories)


get_lowest_child_categories(all_categories)
print(all_categories)
