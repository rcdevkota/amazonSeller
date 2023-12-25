import requests
from bs4 import BeautifulSoup

def scrape_amazon_product(url):
    headers = {
        'User-Agent': 'Your User Agent'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Scrape the product title
    title = soup.find(id='productTitle').get_text().strip()

    return {
        'title': title,
        # Extract other data you need
    }

# Example URL
url = 'https://www.amazon.com/dp/product_id'
product_data = scrape_amazon_product(url)
print(product_data)
