from flask import Flask, jsonify, redirect, render_template, request, url_for

import database

app = Flask(__name__)

# Ensure the database is initialized when the app starts
database.init_db()

@app.route('/')
def index():
    """Main dashboard page."""
    products_rows = database.get_all_products_with_latest_price()
    
    # *** FIX: Convert list of Row objects to a list of dictionaries ***
    # This makes the data JSON serializable for the template.
    products = [dict(row) for row in products_rows]
    
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    """Handles the form submission for adding a new product."""
    url = request.form.get('url')
    target_price_str = request.form.get('target_price')

    if not url or not target_price_str:
        # Basic validation
        return redirect(url_for('index'))

    try:
        target_price = float(target_price_str)
        database.add_product(url, target_price)
    except ValueError:
        # Handle cases where target_price is not a valid number
        print(f"Invalid target price received: {target_price_str}")
    
    return redirect(url_for('index'))

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """Deletes a product from the database."""
    database.delete_product(product_id)
    return redirect(url_for('index'))

@app.route('/api/product_history/<int:product_id>')
def product_history_api(product_id):
    """API endpoint to return price history data for charting."""
    history = database.get_product_price_history(product_id)
    
    # --- FIX ---
    # Use column names ('timestamp', 'price') instead of numeric indexes.
    # This is much safer and more readable.
    labels = [row['timestamp'] for row in history]
    prices = [row['price'] for row in history]

    return jsonify({'labels': labels, 'prices': prices})

if __name__ == '__main__':
    app.run(debug=True, port=5001)



