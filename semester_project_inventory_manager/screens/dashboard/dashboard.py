from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from database.database import InventoryManager
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), 'dashboard.kv'))


class DashboardScreen(Screen):
    """Main dashboard screen with navigation pop-up menu."""

    sidebar_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory_manager = InventoryManager()
        self.low_stock_threshold = 10

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    def show_menu(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        menu_items = [
            ('Add Item', 'item_add'),
            ('Manage Inventory', 'item_manager'),
            ('Reports', 'reports'),
        ]
        for label_text, route in menu_items:
            btn = Button(text=label_text, size_hint_y=None, height='50dp',
                         background_color=(0.2, 0.6, 0.8, 1))
            btn.route = route
            btn.bind(on_press=self.navigate_to)
            content.add_widget(btn)
        close_btn = Button(text='Close', size_hint_y=None, height='50dp',
                           background_color=(0.6, 0.6, 0.6, 1))
        content.add_widget(close_btn)
        popup = Popup(title='Navigation Menu', content=content, size_hint=(0.8, 0.6))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def navigate_to(self, instance):
        self.manager.current = instance.route

    def load_dashboard_data(self):
        self.refresh_low_stock()
        self.refresh_recent_activity()

    def refresh_low_stock(self):
        if 'low_stock_grid' not in self.ids:
            return
        grid = self.ids.low_stock_grid
        grid.clear_widgets()
        items = self.inventory_manager.get_low_stock(self.low_stock_threshold)
        if not items:
            grid.add_widget(Label(text='All items are well stocked', color=(0.2, 0.6, 0.2, 1),
                                  size_hint_y=None, height='36dp'))
            return
        for header in ['SKU', 'Product', 'Qty']:
            grid.add_widget(Label(text=header, bold=True, color=(0.6, 0.1, 0.1, 1),
                                  size_hint_y=None, height='32dp'))
        for sku, product, qty in items:
            grid.add_widget(Label(text=str(sku), size_hint_y=None, height='32dp', color=(0.2, 0.2, 0.2, 1)))
            grid.add_widget(Label(text=product, size_hint_y=None, height='32dp', color=(0.2, 0.2, 0.2, 1)))
            grid.add_widget(Label(text=str(qty), size_hint_y=None, height='32dp', color=(0.8, 0.1, 0.1, 1)))

    def refresh_recent_activity(self):
        if 'activity_grid' not in self.ids:
            return
        grid = self.ids.activity_grid
        grid.clear_widgets()
        activities = self.inventory_manager.get_recent_activity()
        if not activities:
            grid.add_widget(Label(text='No recent activity', color=(0.5, 0.5, 0.5, 1),
                                  size_hint_y=None, height='36dp'))
            return
        for action, sku, product, timestamp in activities:
            short_ts = timestamp[:16] if timestamp else ''
            grid.add_widget(Label(
                text=f'{action}: {product}  (SKU {sku})  [{short_ts}]',
                size_hint_y=None, height='36dp', color=(0.15, 0.15, 0.15, 1),
                text_size=(380, None), halign='left', valign='middle'
            ))

    def show_quick_add(self):
        content = BoxLayout(orientation='vertical', spacing='8dp', padding='10dp')
        sku_input = TextInput(hint_text='SKU (number)', multiline=False, size_hint_y=None, height='42dp', input_filter='int')
        product_input = TextInput(hint_text='Product Name', multiline=False, size_hint_y=None, height='42dp')
        supplier_input = TextInput(hint_text='Supplier', multiline=False, size_hint_y=None, height='42dp')
        quantity_input = TextInput(hint_text='Quantity', multiline=False, size_hint_y=None, height='42dp', input_filter='int')
        ppu_input = TextInput(hint_text='Price Per Unit', multiline=False, size_hint_y=None, height='42dp', input_filter='float')
        status_label = Label(text='', size_hint_y=None, height='28dp', color=(0.8, 0.1, 0.1, 1))
        for w in [sku_input, product_input, supplier_input, quantity_input, ppu_input, status_label]:
            content.add_widget(w)
        popup = Popup(title='Quick Add Item', content=content, size_hint=(0.92, 0.85))

        def do_add(instance):
            try:
                sku = int(sku_input.text)
                product = product_input.text.strip()
                supplier = supplier_input.text.strip()
                quantity = int(quantity_input.text)
                ppu = float(ppu_input.text)
            except ValueError:
                status_label.text = 'Enter valid numbers for SKU, quantity, and price'
                return
            if not product or not supplier:
                status_label.text = 'Product and supplier are required'
                return
            if self.inventory_manager.add_item(sku, product, supplier, quantity, ppu):
                popup.dismiss()
                self.load_dashboard_data()
            else:
                status_label.text = 'SKU already exists or an error occurred'

        btn_row = BoxLayout(size_hint_y=None, height='44dp', spacing='8dp')
        add_btn = Button(text='Add', background_color=(0.15, 0.7, 0.35, 1))
        cancel_btn = Button(text='Cancel', background_color=(0.55, 0.55, 0.55, 1))
        add_btn.bind(on_press=do_add)
        cancel_btn.bind(on_press=popup.dismiss)
        btn_row.add_widget(add_btn)
        btn_row.add_widget(cancel_btn)
        content.add_widget(btn_row)
        popup.open()

    def show_settings(self):
        content = BoxLayout(orientation='vertical', spacing='10dp', padding='12dp')
        content.add_widget(Label(text='User Profile & Settings', font_size='17sp', bold=True,
                                 size_hint_y=None, height='36dp', color=(0.1, 0.3, 0.6, 1)))
        content.add_widget(Label(text='Display Name:', size_hint_y=None, height='26dp', color=(0.2, 0.2, 0.2, 1)))
        username_input = TextInput(text='Admin', multiline=False, size_hint_y=None, height='40dp')
        content.add_widget(username_input)
        content.add_widget(Label(text='Low Stock Threshold:', size_hint_y=None, height='26dp', color=(0.2, 0.2, 0.2, 1)))
        threshold_input = TextInput(text=str(self.low_stock_threshold), multiline=False,
                                    input_filter='int', size_hint_y=None, height='40dp')
        content.add_widget(threshold_input)
        status_label = Label(text='', size_hint_y=None, height='28dp')
        content.add_widget(status_label)
        popup = Popup(title='Settings', content=content, size_hint=(0.88, 0.78))

        def save_settings(instance):
            try:
                self.low_stock_threshold = int(threshold_input.text)
                self.load_dashboard_data()
                status_label.text = 'Settings saved!'
                status_label.color = (0.1, 0.6, 0.2, 1)
            except ValueError:
                status_label.text = 'Invalid threshold value'
                status_label.color = (0.8, 0.1, 0.1, 1)

        btn_row = BoxLayout(size_hint_y=None, height='44dp', spacing='8dp')
        save_btn = Button(text='Save', background_color=(0.2, 0.6, 0.8, 1))
        close_btn = Button(text='Close', background_color=(0.55, 0.55, 0.55, 1))
        save_btn.bind(on_press=save_settings)
        close_btn.bind(on_press=popup.dismiss)
        btn_row.add_widget(save_btn)
        btn_row.add_widget(close_btn)
        content.add_widget(btn_row)
        popup.open()

    def set_dashboard(self):
        self.load_dashboard_data()

    def on_enter(self):
        self.load_dashboard_data()

    def on_leave(self):
        pass
