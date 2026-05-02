from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from database.database import InventoryManager
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), 'item_add.kv'))


class ItemAddScreen(Screen):
    """Screen for adding new items to the inventory."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory_manager = InventoryManager()
    
    def add_item(self):
        """Handle adding a new item to inventory."""
        try:
            sku = int(self.ids.sku_input.text)
            product = self.ids.product_input.text
            supplier = self.ids.supplier_input.text
            quantity = int(self.ids.quantity_input.text)
            ppu = float(self.ids.ppu_input.text)
            
            # Validate inputs
            if not product or not supplier:
                self.show_error("Product and supplier cannot be empty")
                return
            
            if quantity < 0 or ppu < 0:
                self.show_error("Quantity and price must be non-negative")
                return
            
            # Add item to database
            if self.inventory_manager.add_item(sku, product, supplier, quantity, ppu):
                self.show_success("Item added successfully!")
                self.clear_inputs()
            else:
                self.show_error("Failed to add item")
                
        except ValueError:
            self.show_error("Please enter valid numbers for SKU, quantity, and price")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
    
    def clear_inputs(self):
        """Clear all input fields."""
        self.ids.sku_input.text = ''
        self.ids.product_input.text = ''
        self.ids.supplier_input.text = ''
        self.ids.quantity_input.text = ''
        self.ids.ppu_input.text = ''
    
    def show_success(self, message):
        """Display success message."""
        # Placeholder - implement with popup or notification
        print(f"Success: {message}")
    
    def show_error(self, message):
        """Display error message."""
        # Placeholder - implement with popup or notification
        print(f"Error: {message}")
    
    def on_leave(self):
        """Called when leaving the screen."""
        # Optional: Validate unsaved changes
        pass
