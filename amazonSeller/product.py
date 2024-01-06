# This script gets all the ASIN of the Best Seller products from the database
# It takes best seller category as input and saves the ASIN of the products of that category
# the ASIN are saved in database in product table

import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

def scrape_amazon(url):
    # Set up Chrome WebDriver with headless options
    # Specify the version of ChromeDriver you want to use
    driver_path = '/Applications/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    # Navigate to the provided URL
    driver.get(url)
    driver.implicitly_wait(5)

    # Lists to store scraped data
    product_data = []

    try:
        # Adjust the XPath based on the structure of the Amazon page
        items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "zg-item-immersion")]')))
        for item in items:
            # Extract product name
            name = item.find_element(By.XPATH, './/div[contains(@class, "p13n-sc-truncated")]').text

            # Extract ASIN
            data_asin = item.get_attribute("data-asin")

            # Extract product link
            link = item.find_element(By.XPATH, './/a[contains(@class, "a-link-normal")]').get_attribute("href")

            product_data.append({"name": name, "asin": data_asin, "link": link})
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the driver after scraping
        driver.quit()

    # Return data as JSON
    return json.dumps(product_data, indent=4)

# Example usage
url = 'https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261'
print(scrape_amazon(url))
