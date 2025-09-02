# E-commerce Price Tracker
## Project Overview
This is a Python-based application designed to track the prices of products on e-commerce websites. It started as a simple web scraping script and has been developed into a full-featured web application that runs automated background checks and sends email notifications when a product's price drops below a user-defined target.

This project is built to be scalable, demonstrating skills in web scraping, database management, asynchronous task processing, and web development.

## Phase 1 & 2: Backend Scripting
Status: Completed

- Established the core backend logic, including a modular structure for scraping, database management (SQLite), and email alerts.

## Phase 3: Web Interface with Flask
Status: Completed

- Introduced a web-based user interface using the Flask framework. This included a dashboard for adding/deleting products and interactive charts (using Chart.js) to visualize price history.

## Phase 4: Asynchronous Task Processing with Celery & Redis
Status: Completed

- This phase re-architected the application to use a professional-grade background task queue. This makes the system more robust, scalable, and non-blocking.

- Background Jobs: Web scraping and email notifications are now handled by Celery, a powerful distributed task queue. This means the web application remains fast and responsive, as long-running scraping tasks don't block it.

- Message Broker: Redis is used as the message broker, which manages the queue of scraping jobs for Celery.

- Automated Scraping: When a new product is added via the web interface, a scraping task is immediately dispatched to the background worker.

- Scheduled Checks: The price_tracker.py script now functions as a scheduler, which can be run periodically (e.g., via a cron job) to trigger price checks for all tracked products.

- Refactored Code: The core scraping logic was moved to a dedicated scraper.py module to improve code organization and resolve circular dependencies.

### Final Technology Stack
- Backend: Python, Flask, Celery

- Database: SQLite

- Message Broker: Redis

- Frontend: HTML, Tailwind CSS, Chart.js

- Web Scraping: requests, Beautiful Soup

### How to Run the Final Application
The application now consists of three main components that need to be run in separate terminals.

1. Install Redis (if you haven't already):
- The easiest method is using Docker. Make sure Docker Desktop is running, then execute:
```
docker run -d -p 6379:6379 redis
```
2. Install Dependencies:
- Make sure your virtual environment is active and run:
```
pip install -r requirements.txt
```
3. Run the System (in 3 separate terminals):

Terminal 1 — Start the Celery Worker:
- This process listens for and executes background scraping jobs.
```
celery -A tasks.celery_app worker --loglevel=info
```
Terminal 2 — Start the Flask Web App:
- This serves the website.
```
python app.py
```
Terminal 3 — Run the Scheduler (to check all products):
- This will dispatch a background job for every product in your database. You only need to run this when you want to trigger a full update.
```
python price_tracker.py
```
4.  Access the Dashboard:
- Open your browser and navigate to http://127.0.0.1:5001 to view and manage your products.