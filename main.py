import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL (without the page number)
BASE_URL = "https://www.jumia.com.ng/flash-sales/?page={}"

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

products = []

# Loop through pages 1 to 5
for page in range(1, 6):  
    url = BASE_URL.format(page)  
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        continue
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract product details
    for item in soup.find_all("article", class_="prd _fb _p col c-prd"):
        a_tag = item.find("a", class_="core")
        div_tag = item.find("div", class_="info") 

        if not a_tag or not div_tag:
            continue  

        name = div_tag.find("h3", class_="name")
        price = div_tag.find("div", class_="prc")

        link = a_tag["href"] if a_tag else None  # Extract the link safely

        if name and price:
            products.append({
                "Product Name": name.get_text(strip=True),
                "Price": price.get_text(strip=True),
                "Link": f"https://www.jumia.com.ng{link}" if link else None
            })

    print(f"Scraped page {page}")

# Save data to CSV
df = pd.DataFrame(products)
df.to_csv("products.csv", index=False)

print("Scraping complete! Data saved to products.csv")
