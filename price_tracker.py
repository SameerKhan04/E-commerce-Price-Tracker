import time

import database
from tasks import scrape_and_notify


def run_price_checks():
    """
    Finds all products in the database and triggers a background scraping task for each one.
    """
    print("Starting scheduled price checks for all tracked products...")
    all_products = database.get_all_products()

    if not all_products:
        print("No products in the database to checka.")
        return

    for product in all_products:
        product_id = product['id']
        product_title = product['title'] or f"Product ID {product_id}"
        print(f"--- Dispatching job for: {product_title} ---")
        
        # Trigger the background task via Celery
        scrape_and_notify.delay(product_id)
        
        # A small delay can be polite to the server and Celery broker
        time.sleep(1) 

    print("All price check jobs have been dispatched.")

if __name__ == '__main__':
    run_price_checks()

    run_price_checks()

