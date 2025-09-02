import re
import time

import requests
from bs4 import BeautifulSoup

import database
import mailer
from config import ACCEPT_LANGUAGE, USER_AGENT


def scrape_product_info(url: str):
    """
    Scrapes a single product page using multiple selectors for robustness.
    Returns (None, None) if scraping fails.
    """
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept-Language": ACCEPT_LANGUAGE,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1", # Do Not Track Request Header
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        time.sleep(1) # Be respectful to the server

        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Extract Title (Try multiple selectors) ---
        product_title = "Title not found"
        title_selectors = ["#productTitle", "#title", "h1.a-size-large"]
        for selector in title_selectors:
            title_element = soup.select_one(selector)
            if title_element:
                product_title = title_element.get_text(strip=True)
                break
        
        # --- Extract Price (Try multiple selectors) ---
        price_str = None
        price_selectors = [
            'span.a-price span[aria-hidden="true"]',
            'span.a-price.aok-align-center span.a-offscreen',
            '#corePrice_feature_div .a-offscreen',
            '#priceblock_ourprice',
            '.priceToPay'
        ]
        for selector in price_selectors:
            price_element = soup.select_one(selector)
            if price_element:
                price_str = price_element.get_text(strip=True)
                break
        
        if not price_str:
            print(f"Could not find price for {url}")
            return product_title, None

        price_cleaned = re.sub(r'[^\d.]', '', price_str)
        if not price_cleaned:
            print(f"Price string '{price_str}' could not be cleaned.")
            return product_title, None

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






