# E-commerce Price Tracker
## Project Overview
This is a Python-based application designed to track the prices of products on e-commerce websites. It started as a simple web scraping script and is being developed into a full-featured web application that sends email notifications when a product's price drops below a user-defined target.

This project is built to be scalable, demonstrating skills in web scraping, data management, backend development, and automation.

## Phase 1: Core Scraping Script
### Status: Completed

The initial version of the project is a standalone Python script (price_tracker.py) that performs the following actions:

- Scrapes a hardcoded product URL from Amazon.

- Extracts the product title and its current price.

- Compares the current price against a predefined target price.

- Prints the result to the console.

### Technologies Used
- Python 3

- Requests: For making HTTP requests to the product page.

- Beautiful Soup 4: For parsing HTML and extracting data.

### How to Run
1. Clone the repository:

```
git clone [https://github.com/your-username/price-tracker.git](https://github.com/your-username/price-tracker.git)
cd price-tracker
```
2. Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required libraries:

```
pip install requests beautifulsoup4
```

4. Configure the script:

- Open price_tracker.py.

Ch- ange the PRODUCT_URL variable to the Amazon product you want to track.

- Set the TARGET_PRICE to your desired notification threshold.

5. Run the script:

```
python price_tracker.py
```