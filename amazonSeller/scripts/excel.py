#This script creates a new excel file and writes the data from the database into it
#the excel file contains seller information

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import json


import json

def convert_txt_to_json(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by tab
            parts = line.strip().split('\t')
            if len(parts) == 2:
                # Add a dictionary with 'name' and 'link' to the data list
                data.append({'name': parts[0], 'link': parts[1]})
    
    # Convert the list to JSON
    return json.dumps(data, indent=4)

print(convert_txt_to_json('amazonSeller/a.txt'))