from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.lang import Builder
from database.database import InventoryManager
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), 'reports.kv'))


class ReportsScreen(Screen):
    """Screen for viewing inventory reports and analytics."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory_manager = InventoryManager()
    
    def load_reports(self):
        """Load and display inventory reports."""
        try:
            self.update_summary()
            self.update_low_stock()
            self.update_inventory_value()
        except Exception as e:
            print(f"Error loading reports: {e}")
    
    def update_summary(self):
        """Update inventory summary statistics."""
        try:
            self.inventory_manager.cursor.execute('SELECT COUNT(*) FROM inventory')
            total_items = self.inventory_manager.cursor.fetchone()[0]
            
            self.inventory_manager.cursor.execute('SELECT SUM(quantity) FROM inventory')
            total_quantity = self.inventory_manager.cursor.fetchone()[0] or 0
            
            if hasattr(self, 'ids') and 'summary_label' in self.ids:
                self.ids.summary_label.text = f'Total Items: {total_items}\nTotal Units: {total_quantity}'
        except Exception as e:
            print(f"Error updating summary: {e}")
    
    def update_low_stock(self):
        """Display items with low stock (quantity < 10)."""
        try:
            self.inventory_manager.cursor.execute('SELECT SKU, product, quantity FROM inventory WHERE quantity < 10 ORDER BY quantity ASC')
            low_stock_items = self.inventory_manager.cursor.fetchall()
            
            if hasattr(self, 'ids') and 'low_stock_grid' in self.ids:
                grid = self.ids.low_stock_grid
                grid.clear_widgets()
                
                if not low_stock_items:
                    grid.add_widget(Label(text='No low stock items', size_hint_y=None, height='40dp'))
                else:
                    # Add header
                    for header in ['SKU', 'Product', 'Quantity']:
                        grid.add_widget(Label(text=header, bold=True, size_hint_y=None, height='40dp'))
                    
                    # Add items
                    for sku, product, quantity in low_stock_items:
                        grid.add_widget(Label(text=str(sku), size_hint_y=None, height='40dp'))
                        grid.add_widget(Label(text=product, size_hint_y=None, height='40dp'))
                        grid.add_widget(Label(text=str(quantity), color=(1, 0, 0, 1), size_hint_y=None, height='40dp'))
        except Exception as e:
            print(f"Error updating low stock: {e}")
    
    def update_inventory_value(self):
        """Calculate total inventory value."""
        try:
            self.inventory_manager.cursor.execute('SELECT SUM(quantity * ppu) FROM inventory')
            total_value = self.inventory_manager.cursor.fetchone()[0] or 0
            
            if hasattr(self, 'ids') and 'value_label' in self.ids:
                self.ids.value_label.text = f'Total Inventory Value: ${total_value:,.2f}'
        except Exception as e:
            print(f"Error updating inventory value: {e}")
    
    def on_enter(self):
        """Called when entering the screen."""
        self.load_reports()
    
    def on_leave(self):
        """Called when leaving the screen."""
        pass
