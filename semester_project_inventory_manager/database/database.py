import sqlite3

connection = sqlite3.connect('inventory.db')
cursor = connection.cursor()
        
cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                    SKU INTEGER PRIMARY KEY,
                    product TEXT NOT NULL,
                    supplier TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    ppu REAL NOT NULL
                    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    sku INTEGER,
                    product TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

connection.commit()
connection.close()


class InventoryManager:
    """Class to manage inventory database operations"""
    
    def __init__(self, db_name='inventory.db'):
        """Initialize database connection"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def add_item(self, sku, product, supplier, quantity, ppu):
        """
        Add a new item to the inventory
        
        Args:
            sku (int): SKU number
            product (str): Product name
            supplier (str): Supplier name
            quantity (int): Quantity in stock
            ppu (float): Price per unit
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cursor.execute('''INSERT INTO inventory (SKU, product, supplier, quantity, ppu)
                                   VALUES (?, ?, ?, ?, ?)''',
                                (sku, product, supplier, quantity, ppu))
            self.cursor.execute('INSERT INTO activity_log (action, sku, product) VALUES (?, ?, ?)',
                                ('Added', sku, product))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error: SKU already exists or constraint violation - {e}")
            return False
        except Exception as e:
            print(f"Error adding item: {e}")
            return False
    
    def get_recent_activity(self, limit=5):
        try:
            self.cursor.execute(
                'SELECT action, sku, product, timestamp FROM activity_log ORDER BY id DESC LIMIT ?',
                (limit,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching recent activity: {e}")
            return []

    def get_low_stock(self, threshold=10):
        try:
            self.cursor.execute(
                'SELECT SKU, product, quantity FROM inventory WHERE quantity < ? ORDER BY quantity ASC',
                (threshold,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching low stock: {e}")
            return []

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

