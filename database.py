import sqlite3
from datetime import datetime

DB_NAME = "tracker.db"

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
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
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def add_product(url: str, target_price: float):
    """Adds a new product to be tracked."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO products (url, target_price) VALUES (?, ?)", (url, target_price))
        conn.commit()
        print(f"Added product: {url}")
    except sqlite3.IntegrityError:
        print(f"Product with URL {url} is already being tracked.")
    finally:
        conn.close()

def get_all_products():
    """Fetches all products from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, target_price, title FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def log_price(product_id: int, price: float):
    """Logs a new price entry for a product."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO price_history (product_id, price, timestamp) VALUES (?, ?, ?)",
                   (product_id, price, timestamp))
    conn.commit()
    conn.close()

def update_product_title(product_id: int, title: str):
    """Updates the title of a product."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET title = ? WHERE id = ?", (title, product_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # This allows you to set up the database and add products from the command line
    # Example: python database.py init
    # Example: python database.py add "https://your.product/url" 150.00
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_db()
        elif command == "add" and len(sys.argv) == 4:
            add_product(sys.argv[2], float(sys.argv[3]))
        else:
            print("Invalid command. Use 'init' or 'add <url> <price>'.")
