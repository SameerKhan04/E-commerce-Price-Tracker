from flask import Flask, jsonify, redirect, render_template, request, url_for

import database
from tasks import scrape_and_notify  # Import the Celery task

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main dashboard page."""
    # Convert sqlite3.Row objects to standard dictionaries for JSON serialization
    products_rows = database.get_all_products_with_latest_price()
    products = [dict(row) for row in products_rows]
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    """Handles the submission of the 'add product' form."""
    url = request.form.get('url')
    target_price_str = request.form.get('target_price')

    if not url or not target_price_str:
        # Basic validation
        return redirect(url_for('index'))

    try:
        target_price = float(target_price_str)
        # Add the product to the database
        product_id = database.add_product(url, target_price)

        if product_id:
            # --- PHASE 4 CHANGE ---
            # Instead of scraping directly, we trigger the background task.
            # .delay() sends the job to the Celery worker.
            print(f"Product added with ID: {product_id}. Triggering background scrape task.")
            scrape_and_notify.delay(product_id)

    except (ValueError, TypeError):
        # Handle cases where target_price is not a valid number
        print("Error: Invalid target price submitted.")
        pass

    return redirect(url_for('index'))

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """Deletes a product from the database."""
    database.delete_product(product_id)
    return redirect(url_for('index'))

@app.route('/api/price_history/<int:product_id>')
def price_history(product_id):
    """API endpoint to provide price history data for charts."""
    history_rows = database.get_price_history(product_id)
    # Convert data for JSON response, ensuring dates are in a standard format
    history = [
        {"timestamp": row['timestamp'], "price": row['price']}
        for row in history_rows
    ]
    return jsonify(history)

if __name__ == '__main__':
    # Note: For development, Celery worker needs to be run in a separate terminal.
    # The debug mode reloader can cause issues with Celery, so it's often disabled
    # when testing background tasks.
    app.run(debug=True, port=5001)
    app.run(debug=True, port=5001)
