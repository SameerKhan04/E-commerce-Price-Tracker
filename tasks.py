from celery import Celery
from scraper import scrape_product_info

import database
import mailer
from config import CELERY_BROKER_URL

# Initialize Celery and configure it using the broker URL from our config
celery_app = Celery('tasks', broker=CELERY_BROKER_URL)

@celery_app.task
def scrape_and_notify(product_id: int):
    """
    A Celery task to scrape a product's info, update the database,
    and send a notification if the price has dropped below the target.
    
    Args:
        product_id: The ID of the product to check.
    """
    print(f"Executing task for product_id: {product_id}")
    
    # Fetch product details from the database
    product = database.get_product_by_id(product_id)
    if not product:
        print(f"Product with ID {product_id} not found in database.")
        return

    # Scrape the product page for the latest information
    scraped_data = scrape_product_info(product['url'])
    current_price = scraped_data.get('price')
    
    if current_price is None:
        print(f"Could not retrieve price for {product['title']}. Skipping.")
        return

    # Add the new price to the history
    database.add_price_history(product_id, current_price)
    print(f"Updated price for {product['title']} to ${current_price:.2f}")

    # Check if the price has dropped below the target and if an alert is needed
    if current_price < product['target_price']:
        print(f"Price alert! {product['title']} is now ${current_price:.2f}, which is below the target of ${product['target_price']:.2f}.")
        mailer.send_price_alert(
            product_title=product['title'],
            product_url=product['url'],
            new_price=current_price,
            target_price=product['target_price']
        )


