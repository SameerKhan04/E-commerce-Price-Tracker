import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Email Configuration ---
# Your email address from which alerts will be sent
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

# The password for your sender email account.
# For Gmail, this should be an "App Password".
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# The email address that will receive the price alerts.
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# --- Scraper Configuration ---
# User-Agent to mimic a real browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
ACCEPT_LANGUAGE = "en-US,en;q=0.9"
ACCEPT_LANGUAGE = "en-US,en;q=0.9"
