import re

import requests
from bs4 import BeautifulSoup

import database
import mailer
from config import ACCEPT_LANGUAGE, USER_AGENT


def scrape_product_info(url: str):
    """
    Scrapes a single product page and returns its title and price.
    Returns (None, None) if scraping fails.
    """
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept-Language": ACCEPT_LANGUAGE
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract Title
        title_element = soup.find(id="productTitle")
        product_title = title_element.get_text().strip() if title_element else "Title not found"

        # Extract Price
        price_str = None
        price_whole_element = soup.select_one('.a-price-whole')
        price_fraction_element = soup.select_one('.a-price-fraction')

        if price_whole_element and price_fraction_element:
            price_str = f"{price_whole_element.get_text().strip()}{price_fraction_element.get_text().strip()}"
        else:
            price_span_element = soup.select_one('span.a-price span.a-offscreen')
            if price_span_element:
                price_str = price_span_element.get_text()

        if not price_str:
            return product_title, None

        price_cleaned = re.sub(r'[^\d.]', '', price_str)
        current_price = float(price_cleaned)
        return product_title, current_price

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred while scraping {url}: {e}")
        return None, None

def check_all_products():
    """
    Main function to orchestrate the price checking for all tracked products.
    """
    print("Starting price check for all tracked products...")
    products = database.get_all_products()
    
    if not products:
        print("No products found in the database. Add one by running: python database.py add <url> <price>")
        return

    for product in products:
        product_id, url, target_price, old_title = product
        print(f"\n--- Checking: {old_title or url} ---")

        title, price = scrape_product_info(url)

        if title and not old_title:
             database.update_product_title(product_id, title)
             print(f"Updated product title to: {title}")

        if price is None:
            print("Failed to retrieve price. Skipping.")
            continue
        
        print(f"Current Price: ${price:.2f} | Target Price: ${target_price:.2f}")
        database.log_price(product_id, price)

        if price < target_price:
            print("🎉 Price drop detected! Sending alert...")
            mailer.send_alert(
                product_title=title,
                product_url=url,
                current_price=price,
                target_price=target_price
            )
        else:
            print("Price is still above target.")
    
    print("\nPrice check complete.")

if __name__ == "__main__":
    check_all_products()

if __name__ == "__main__":
    check_all_products()

