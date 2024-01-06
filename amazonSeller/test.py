import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

AMAZON_BASE_URL = "https://www.amazon.com/"

def get_subcategories(category_url):
    """Fetch and parse subcategories using requests and BeautifulSoup."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    full_url = "https://www.amazon.com"+ category_url
    response = requests.get(full_url, headers=headers)

    subcategories_data = []

    if response.status_code == 200:
        print("response")
        soup = BeautifulSoup(response.content, 'html.parser')
        # Adjust the selector based on the structure of the Amazon subcategory page
        subcategory_elements = soup.select(".a-fixed-left-grid-col.a-col-left div.celwidget")
        print("subcategory_elements")
        print(subcategory_elements)
        for element in subcategory_elements:
            subcategory_name = element.get_text().strip()
            subcategory_url = element['href']
            if subcategory_name:
                subcategories_data.append({"name": subcategory_name, "url": subcategory_url})
    else:
        print(f"Failed to fetch the subcategory page for {full_url}")
    print("subcategories_data")
    print(subcategories_data)
    return subcategories_data

def get_lowest_child_categories(parent_categories):
    """Loop through all parent categories and get lowest child categories."""
    # print("parentcategories")
    # print(parent_categories)
    all_child_categories = []

    for category in parent_categories:
        subcategories = get_subcategories(category['url'])  # Get the subcategories for the current parent category
        if not subcategories:  # If there are no subcategories, add the current category to the list of lowest child categories
            all_child_categories.append(category)
        else:
            for subcategory in subcategories:
                child_subcategories = get_subcategories(subcategory['url'])  # Get the subcategories for the current subcategory
                if not child_subcategories:  # If there are no further subcategories, add the current subcategory to the list of lowest child categories
                    all_child_categories.append(subcategory)
    print(all_child_categories)
    return all_child_categories

# Example usage
parent_categories = [
    {
        "name": "Amazon Devices & Accessories",
        "url": "/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices"
    },
    {
        "name": "Amazon Renewed",
        "url": "/Best-Sellers-Amazon-Renewed/zgbs/amazon-renewed"
    },
    {
        "name": "Appliances",
        "url": "/Best-Sellers-Appliances/zgbs/appliances"
    },
    {
        "name": "Apps & Games",
        "url": "/Best-Sellers-Apps-Games/zgbs/mobile-apps"
    },
    {
        "name": "Arts, Crafts & Sewing",
        "url": "/Best-Sellers-Arts-Crafts-Sewing/zgbs/arts-crafts"
    },
    {
        "name": "Audible Books & Originals",
        "url": "/Best-Sellers-Audible-Books-Originals/zgbs/audible"
    },
    {
        "name": "Automotive",
        "url": "/Best-Sellers-Automotive/zgbs/automotive"
    },
    {
        "name": "Baby",
        "url": "/Best-Sellers-Baby/zgbs/baby-products"
    },
    {
        "name": "Beauty & Personal Care",
        "url": "/Best-Sellers-Beauty-Personal-Care/zgbs/beauty"
    },
    {
        "name": "Books",
        "url": "/best-sellers-books-Amazon/zgbs/books"
    },
    {
        "name": "Camera & Photo Products",
        "url": "/best-sellers-camera-photo/zgbs/photo"
    },
    {
        "name": "CDs & Vinyl",
        "url": "/best-sellers-music-albums/zgbs/music"
    },
    {
        "name": "Cell Phones & Accessories",
        "url": "/Best-Sellers-Cell-Phones-Accessories/zgbs/wireless"
    },
    {
        "name": "Climate Pledge Friendly",
        "url": "/Best-Sellers-Climate-Pledge-Friendly/zgbs/climate-pledge"
    },
    {
        "name": "Clothing, Shoes & Jewelry",
        "url": "/Best-Sellers-Clothing-Shoes-Jewelry/zgbs/fashion"
    },
    {
        "name": "Collectible Coins",
        "url": "/Best-Sellers-Collectible-Coins/zgbs/coins"
    },
    {
        "name": "Computers & Accessories",
        "url": "/Best-Sellers-Computers-Accessories/zgbs/pc"
    },
    {
        "name": "Digital Educational Resources",
        "url": "/Best-Sellers-Digital-Educational-Resources/zgbs/digital-educational-resources"
    },
    {
        "name": "Digital Music",
        "url": "/Best-Sellers-Digital-Music/zgbs/dmusic"
    },
    {
        "name": "Electronics",
        "url": "/Best-Sellers-Electronics/zgbs/electronics"
    },
    {
        "name": "Entertainment Collectibles",
        "url": "/Best-Sellers-Entertainment-Collectibles/zgbs/entertainment-collectibles"
    },
    {
        "name": "Gift Cards",
        "url": "/Best-Sellers-Gift-Cards/zgbs/gift-cards"
    },
    {
        "name": "Grocery & Gourmet Food",
        "url": "/Best-Sellers-Grocery-Gourmet-Food/zgbs/grocery"
    },
    {
        "name": "Handmade Products",
        "url": "/Best-Sellers-Handmade-Products/zgbs/handmade"
    },
    {
        "name": "Health & Household",
        "url": "/Best-Sellers-Health-Household/zgbs/hpc"
    },
    {
        "name": "Home & Kitchen",
        "url": "/Best-Sellers-Home-Kitchen/zgbs/home-garden"
    },
    {
        "name": "Industrial & Scientific",
        "url": "/Best-Sellers-Industrial-Scientific/zgbs/industrial"
    },
    {
        "name": "Kindle Store",
        "url": "/Best-Sellers-Kindle-Store/zgbs/digital-text"
    },
    {
        "name": "Kitchen & Dining",
        "url": "/Best-Sellers-Kitchen-Dining/zgbs/kitchen"
    },
    {
        "name": "Movies & TV",
        "url": "/best-sellers-movies-TV-DVD-Blu-ray/zgbs/movies-tv"
    },
    {
        "name": "Musical Instruments",
        "url": "/Best-Sellers-Musical-Instruments/zgbs/musical-instruments"
    },
    {
        "name": "Office Products",
        "url": "/Best-Sellers-Office-Products/zgbs/office-products"
    },
    {
        "name": "Patio, Lawn & Garden",
        "url": "/Best-Sellers-Patio-Lawn-Garden/zgbs/lawn-garden"
    },
    {
        "name": "Pet Supplies",
        "url": "/Best-Sellers-Pet-Supplies/zgbs/pet-supplies"
    },
    {
        "name": "Software",
        "url": "/best-sellers-software/zgbs/software"
    },
    {
        "name": "Sports & Outdoors",
        "url": "/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods"
    },
    {
        "name": "Sports Collectibles",
        "url": "/Best-Sellers-Sports-Collectibles/zgbs/sports-collectibles"
    },
    {
        "name": "Tools & Home Improvement",
        "url": "/Best-Sellers-Tools-Home-Improvement/zgbs/hi"
    },
    {
        "name": "Toys & Games",
        "url": "/Best-Sellers-Toys-Games/zgbs/toys-and-games"
    },
    {
        "name": "Unique Finds",
        "url": "/Best-Sellers-Unique-Finds/zgbs/boost"
    },
    {
        "name": "Video Games",
        "url": "/best-sellers-video-games/zgbs/videogames"
    }
]


#function to add amazon base url to url in parent_categories
for category in parent_categories:
    category['url'] = urljoin(AMAZON_BASE_URL, category['url'])
print(parent_categories)

# lowest_child_categories = get_lowest_child_categories(parent_categories)  # Get the lowest child categories for the given parent categories
# for category in lowest_child_categories:
#     print("..............................     .........................    ....................")  # Print the name of each lowest child category
#    # print("category")

