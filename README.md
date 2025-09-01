# E-commerce Price Tracker
## Project Overview
This is a Python-based application designed to track the prices of products on e-commerce websites. It started as a simple web scraping script and is being developed into a full-featured web application that sends email notifications when a product's price drops below a user-defined target.

This project is built to be scalable, demonstrating skills in web scraping, data management, backend development, and automation.

## Phase 1: Core Scraping Script
Status: Completed

The initial version of the project is a standalone Python script (price_tracker.py) that performs the following actions:

- Scrapes a hardcoded product URL from Amazon.

- Extracts the product title and its current price.

- Compares the current price against a predefined target price.

- Prints the result to the console.

## Phase 2: Database Integration and Email Alerts
Status: Completed

This phase refactors the project into a modular application with a persistent database and automated email notifications.

- Database Storage: Uses SQLite to store and manage multiple products to track. It also logs a history of price changes for each product.

- Email Notifications: Sends an email alert when a product's price drops below the user's target.

- Secure Credential Management: Uses a .env file to store sensitive information like email credentials, which are kept out of version control via .gitignore.

- Modular Code: The logic is split into separate modules for scraping, database interaction, and email sending, which is a best practice for maintainability.

### Technologies Used
- Python 3

- Requests

- Beautiful Soup 4

- SQLite3 (via Python's standard library)

- smtplib (for sending emails)

- python-dotenv (for managing environment variables)

### How to Run
1. Clone the repository (if you haven't already):

```
git clone [https://github.com/your-username/price-tracker.git](https://github.com/your-username/price-tracker.git)
cd price-tracker
```

2. Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install the required libraries:

```
pip install -r requirements.txt
```

4. Create your environment file:

- Create a new file named .env in the project's root directory.

- Add the following lines to it, replacing the values with your own credentials:

SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=email_to_receive_alerts@example.com

- IMPORTANT: For SENDER_PASSWORD, if you use Gmail, you must generate an "App Password". You cannot use your regular Gmail password.

5. Initialize the database:

- Run-  the database script to create the tracker.db file and tables.

```
python3 database.py init
```

6. Add a product to track:

- Use the database script to add your first product.

```
python3 database.py add "[https://www.amazon.com.au/Logitech-Wireless-Keyboard-Receiver-Control/dp/B07W6J8L4G/](https://www.amazon.com.au/Logitech-Wireless-Keyboard-Receiver-Control/dp/B07W6J8L4G/)" 100.00
```

- Replace the URL and target price with your desired product. You can add as many as you like.

7. Run the tracker:

```
python3 price_tracker.py
```

- The script will now check all products stored in your database!