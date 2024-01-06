


def fetch_amazon_best_sellers_main_category():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    
    url = "https://www.amazon.com/gp/bestsellers/"
    driver.get(url)
    
    time.sleep(2)  # Wait for the page to load
    
    categories_data = []
    
    category_elements = driver.find_elements_by_css_selector("#zg_left_col2 a")
    
    for element in category_elements:
        category_name = element.text.strip()
        category_url = element.get_attribute("href")
        
        categories_data.append({"name": category_name, "url": category_url})
    
    driver.quit()
    
    return categories_data

categories = fetch_amazon_best_sellers_main_category()
for category in categories:
    print(category["name"], category["url"])


    def fetch_amazon_best_sellers_main_category():
    # Fetch the Amazon Best Sellers page
    driver.get('https://www.amazon.com/Best-Sellers/zgbs')
    # Wait for the page to load
    time.sleep(5)
    # Get the page source
    page_source = driver.page_source
    # Create a BeautifulSoup object
    soup = BeautifulSoup(page_source, 'html.parser')
    # Find the div with id zg_browseRoot
    div = soup.find('div', {'id': 'zg_browseRoot'})
    # Find all the anchor tags inside the div
    a_tags = div.find_all('a')
    # Create an empty list to store the categories
    categories = []
    # Iterate over the anchor tags
    for a_tag in a_tags:
        # Create a dictionary to store the category name and URL
        category = {}
        # Get the category name
        category['name'] = a_tag.text
        # Get the category URL
        category['url'] = web + a_tag['href']
        # Append the dictionary to the categories list
        categories.append(category)
    # Return the categories list
    return categories

fetch_amazon_best_sellers_main_category()


_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz selectorgadget_suggested
_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz
_p13n-zg-nav-tree-all_style_zg-browse-root__-jwNv