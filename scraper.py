import re

import requests
from bs4 import BeautifulSoup


def _normalize_amazon_url(url: str) -> str:
    """
    Strips unnecessary tracking parameters from an Amazon URL to get a clean, canonical URL.
    This helps prevent duplicate entries for the same product.
    """
    # Find the part of the URL that contains the Amazon Standard Identification Number (ASIN)
    match = re.search(r'(/(dp|gp/product)/)([\w\d]{10})', url)
    if match:
        # Reconstruct the URL with only the essential parts
        base_url = "https://www.amazon.com.au" # Or your local Amazon domain
        return f"{base_url}{match.group(1)}{match.group(3)}"
    return url # Return the original URL if the pattern isn't found

def scrape_product_info(url: str) -> dict:
    """
    Scrapes a given product URL to find its title and price.
    
    This function has been made more robust by checking multiple possible CSS selectors 
    for the title and price, as Amazon's layout can vary.

    Args:
        url: The URL of the product page to scrape.

    Returns:
        A dictionary containing the 'title' and 'price' of the product. 
        Returns None for a value if it cannot be found.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Connection": "keep-alive"
    }

    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return {'title': None, 'price': None}

    soup = BeautifulSoup(page.content, 'html.parser')

    # --- Find Title ---
    title = None
    # A list of possible CSS selectors for the product title
    title_selectors = [
        "span#productTitle",
        "h1#title span#productTitle"
    ]
    for selector in title_selectors:
        title_element = soup.select_one(selector)
        if title_element:
            title = title_element.get_text(strip=True)
            break
    
    # --- Find Price ---
    price = None
    # A list of possible CSS selectors for the price
    price_selectors = [
        "span.a-price-whole", # Main part of the price
        "span#priceblock_ourprice",
        "span#priceblock_dealprice",
        "span.priceToPay span.a-price-whole"
    ]
    for selector in price_selectors:
        price_element = soup.select_one(selector)
        if price_element:
            price_text = price_element.get_text(strip=True).replace(',', '').replace('$', '')
            try:
                price = float(price_text)
                break
            except (ValueError, TypeError):
                continue
    
    # If the main price part was found, look for the fractional part
    if price is not None:
        fraction_element = soup.select_one("span.a-price-fraction")
        if fraction_element:
            try:
                fraction = float(f"0.{fraction_element.get_text(strip=True)}")
                price += fraction
            except (ValueError, TypeError):
                pass # Ignore if fraction can't be converted

    return {'title': title, 'price': price}

    return {'title': title, 'price': price}
