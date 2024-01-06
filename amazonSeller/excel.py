#This script creates a new excel file and writes the data from the database into it
#the excel file contains seller information

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import json


# Use webdriver-manager to handle the Firefox driver installation
driver_path = '/Applications/chromedriver-mac-arm64/chromedriver'
service = Service(driver_path)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
    
driver = webdriver.Chrome(service=service, options=options)


# Open the Amazon website
driver.get("https://www.amazon.com")

# Optionally, add some code here to interact with the website
# e.g., find elements, click buttons, etc.

# Check if the title contains "Amazon"
if "Amazon" in driver.title:
    print("Successfully opened Amazon.com and found 'Amazon' in the title.")
else:
    print("Amazon.com was not opened correctly.")

# Close the browser window
driver.quit()
