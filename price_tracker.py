import re

import requests
from bs4 import BeautifulSoup

# --- Configuration ---

PRODUCT_URL = "https://www.amazon.com.au/Floating-Restaurant-75640-Adventure-Building/dp/B0DWDR21CF/?_encoding=UTF8&pd_rd_w=x7PGV&content-id=amzn1.sym.4af574da-f806-46eb-9b2a-605ade911875%3Aamzn1.symc.ba9f62aa-0e9e-47cb-ae63-bd23599fbe66&pf_rd_p=4af574da-f806-46eb-9b2a-605ade911875&pf_rd_r=YJQ9B14AYGSBG68H1MGS&pd_rd_wg=To8CR&pd_rd_r=6fb48327-7344-41c9-919d-488c4bc8bd49&ref_=pd_hp_d_atf_ci_mcx_mr_ca_hp_atf_d"

TARGET_PRICE = 400.00

# --- Web Scraping Logic ---

def check_price():
    """
    Scrapes the product page for the title and price and checks if it's below the target.
    """
    try:
        # Set headers to mimic a real browser visit
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }

        # Fetch the webpage content
        print("Fetching product page...")
        response = requests.get(PRODUCT_URL, headers=headers)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        print("Page fetched successfully.")

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Extract Product Title ---
        # Amazon uses the 'productTitle' ID for the main title.
        title_element = soup.find(id="productTitle")
        if not title_element:
            print("Could not find the product title. The page layout might have changed.")
            return
        
        product_title = title_element.get_text().strip()
        print(f"Product: {product_title}")

        # --- Extract Product Price ---
        # Price can be in various elements. We will try a few common ones.
        # 1. 'a-price-whole' and 'a-price-fraction' for standard prices
        price_whole_element = soup.select_one('.a-price-whole')
        price_fraction_element = soup.select_one('.a-price-fraction')

        if price_whole_element and price_fraction_element:
            price_str = f"{price_whole_element.get_text().strip()}{price_fraction_element.get_text().strip()}"
        else:
            # Fallback for different price layouts
            price_span_element = soup.select_one('span.a-price span.a-offscreen')
            if price_span_element:
                price_str = price_span_element.get_text()
            else:
                 print("Could not find the price. The page layout might have changed.")
                 return

        # Clean the price string (remove currency symbols, commas, etc.)
        price_cleaned = re.sub(r'[^\d.]', '', price_str)
        current_price = float(price_cleaned)

        print(f"Current Price: ${current_price:.2f}")
        print(f"Target Price:  ${TARGET_PRICE:.2f}")

        # --- Compare and Notify ---
        if current_price < TARGET_PRICE:
            print("\n🎉 Great news! The price has dropped below your target!")
            # In the future, we will send an email here.
        else:
            print("\nThe price is still above your target. We'll keep checking.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# --- Main execution ---
if __name__ == "__main__":
    check_price()
    check_price()
