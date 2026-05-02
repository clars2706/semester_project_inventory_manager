from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.popup import Popup
from database.database import InventoryManager
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), 'item_manager.kv'))


class ItemManagerScreen(Screen):
    """Screen for viewing and managing existing inventory items."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory_manager = InventoryManager()
        self.items = []
    
    def load_items(self):
        """Load all items from the database and display them."""
        try:
            # Query all items from database
            self.inventory_manager.cursor.execute('SELECT * FROM inventory')
            self.items = self.inventory_manager.cursor.fetchall()
            self.refresh_display()
        except Exception as e:
            print(f"Error loading items: {e}")
    
    def refresh_display(self):
        """Refresh the display with current items."""
        if hasattr(self, 'ids') and 'items_grid' in self.ids:
            items_grid = self.ids.items_grid
            items_grid.clear_widgets()
            
            # Add header
            header_labels = ['SKU', 'Product', 'Supplier', 'Quantity', 'Price/Unit', 'Actions']
            for label_text in header_labels:
                items_grid.add_widget(Label(text=label_text, bold=True, size_hint_y=None, height='40dp'))
            
            # Add items
            for item in self.items:
                sku, product, supplier, quantity, ppu = item
                
                items_grid.add_widget(Label(text=str(sku), size_hint_y=None, height='40dp'))
                items_grid.add_widget(Label(text=product, size_hint_y=None, height='40dp'))
                items_grid.add_widget(Label(text=supplier, size_hint_y=None, height='40dp'))
                items_grid.add_widget(Label(text=str(quantity), size_hint_y=None, height='40dp'))
                items_grid.add_widget(Label(text=f'${ppu:.2f}', size_hint_y=None, height='40dp'))
                
                # Actions button
                delete_btn = Button(
                    text='Delete',
                    size_hint_y=None,
                    height='40dp',
                    background_color=(0.8, 0.2, 0.2, 1)
                )
                delete_btn.sku = sku  # Store SKU for deletion
                delete_btn.bind(on_press=self.delete_item)
                items_grid.add_widget(delete_btn)
    
    def delete_item(self, instance):
        """Delete an item from inventory."""
        sku = instance.sku
        try:
            self.inventory_manager.cursor.execute('DELETE FROM inventory WHERE SKU = ?', (sku,))
            self.inventory_manager.connection.commit()
            self.load_items()  # Refresh display
            print(f"Item {sku} deleted successfully")
        except Exception as e:
            print(f"Error deleting item: {e}")
    
    def search_items(self, search_text):
        """Search items by product name or supplier."""
        try:
            query = '''SELECT * FROM inventory WHERE product LIKE ? OR supplier LIKE ?'''
            search_pattern = f'%{search_text}%'
            self.inventory_manager.cursor.execute(query, (search_pattern, search_pattern))
            self.items = self.inventory_manager.cursor.fetchall()
            self.refresh_display()
        except Exception as e:
            print(f"Error searching items: {e}")
    
    def on_enter(self):
        """Called when entering the screen."""
        self.load_items()
    
    def on_leave(self):
        """Called when leaving the screen."""
        pass
