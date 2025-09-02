import re
import sqlite3
from datetime import datetime
from urllib.parse import urlparse, urlunparse

DB_NAME = "tracker.db"

def normalize_amazon_url(url: str) -> str:
    """
    Strips unnecessary tracking parameters from an Amazon URL
    to get a clean, canonical URL for a product.
    """
    parsed_url = urlparse(url)
    
    # Find the product ID (ASIN), which is typically after '/dp/'
    match = re.search(r'/(dp|gp/product)/(\w{10})', parsed_url.path)
    if not match:
        return url # Return original URL if it's not a standard product page

    product_id = match.group(2)
    
    # Reconstruct the URL with only the essential parts
    clean_path = f'/dp/{product_id}'
    
    return urlunparse((parsed_url.scheme, parsed_url.netloc, clean_path, '', '', ''))


def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    conn.execute("PRAGMA foreign_keys = ON") # Enforce foreign key constraints
    return conn

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL UNIQUE,
            target_price REAL NOT NULL,
            title TEXT
        )
    ''')
    
    # Create price_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            price REAL NOT NULL,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def add_product(url: str, target_price: float):
    """Adds a new product to be tracked after normalizing its URL."""
    clean_url = normalize_amazon_url(url)
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("INSERT INTO products (url, target_price) VALUES (?, ?)", (clean_url, target_price))
            print(f"Added product: {clean_url}")
    except sqlite3.IntegrityError:
        print(f"Product with URL {clean_url} is already being tracked.")
    finally:
        conn.close()

def delete_product(product_id: int):
    """Deletes a product and its price history from the database."""
    conn = get_db_connection()
    try:
        with conn:
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
            print(f"Deleted product with ID: {product_id}")
    except sqlite3.Error as e:
        print(f"Database error on delete: {e}")
    finally:
        conn.close()

def get_all_products():
    """Fetches all products from the database."""
    conn = get_db_connection()
    products = conn.execute("SELECT id, url, target_price, title FROM products").fetchall()
    conn.close()
    return products

def get_all_products_with_latest_price():
    """
    Fetches all products and joins their most recent price from the history.
    """
    conn = get_db_connection()
    # This query gets each product and finds the price from the latest timestamp in the history table.
    query = """
    SELECT 
        p.id, 
        p.url, 
        p.target_price, 
        p.title,
        ph_latest.price AS latest_price
    FROM products p
    LEFT JOIN (
        SELECT 
            product_id, 
            price
        FROM price_history
        WHERE (product_id, timestamp) IN (
            SELECT 
                product_id, 
                MAX(timestamp)
            FROM price_history
            GROUP BY product_id
        )
    ) AS ph_latest ON p.id = ph_latest.product_id
    ORDER BY p.id;
    """
    products = conn.execute(query).fetchall()
    conn.close()
    return products

def get_product_price_history(product_id: int):
    """Fetches the entire price history for a single product."""
    conn = get_db_connection()
    history = conn.execute("SELECT * FROM price_history WHERE product_id = ? ORDER BY timestamp ASC", (product_id,)).fetchall()
    conn.close()
    return history

def log_price(product_id: int, price: float):
    """Logs a new price entry for a product."""
    conn = get_db_connection()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conn:
        conn.execute("INSERT INTO price_history (product_id, price, timestamp) VALUES (?, ?, ?)",
                   (product_id, price, timestamp))
    conn.close()

def update_product_title(product_id: int, title: str):
    """Updates the title of a product."""
    conn = get_db_connection()
    with conn:
        conn.execute("UPDATE products SET title = ? WHERE id = ?", (title, product_id))
    conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_db()
        elif command == "add" and len(sys.argv) == 4:
            add_product(sys.argv[2], float(sys.argv[3]))
        else:
            print("Invalid command. Use 'init' or 'add <url> <price>'.")


