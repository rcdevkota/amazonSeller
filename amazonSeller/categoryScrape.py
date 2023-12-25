import requests
from bs4 import BeautifulSoup
import re

def fetch_amazon_best_sellers():
    url = "https://www.amazon.com/gp/bestsellers/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        categories = soup.find_all("div", {"id": "zg_col1"})

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

# def validate_categories(data):
#     valid_entries = []
#     for line in data:
#         match = re.match(r'Category: (.*?), URL: (https?://www\.amazon\.com[\S]+)', line)
#         if match:
#             category, url = match.groups()
#             valid_entries.append({'category': category, 'url': url})
#     return valid_entries

# # Fetch categories and validate them
# fetched_data = fetch_amazon_best_sellers()
# valid_categories = validate_categories(fetched_data)

# for entry in valid_categories:
#     print(entry)