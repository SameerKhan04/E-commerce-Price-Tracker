import os

from dotenv import load_dotenv

# Find the absolute path of the directory containing this script
basedir = os.path.abspath(os.path.dirname(__file__))
# Load environment variables from a .env file located in the same directory
load_dotenv(os.path.join(basedir, '.env'))

# --- Email Configuration ---
# Fetches the sender's email address from environment variables.
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
# Fetches the sender's email password (or App Password) from environment variables.
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
# Fetches the recipient's email address from environment variables.
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')


# --- Celery Configuration ---
# Fetches the Redis URL for Celery to use as a message broker.
# Defaults to the standard local Redis instance if not set in .env
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')


