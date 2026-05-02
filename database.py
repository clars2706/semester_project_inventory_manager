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
            self.connection.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error: SKU already exists or constraint violation - {e}")
            return False
        except Exception as e:
            print(f"Error adding item: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

