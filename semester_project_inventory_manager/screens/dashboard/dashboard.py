from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), 'dashboard.kv'))


class DashboardScreen(Screen):
    """Main dashboard screen with navigation pop-up menu."""
    
    from kivy.properties import BooleanProperty
    sidebar_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_sidebar(self):
        """Toggle the sidebar open/close state."""
        self.sidebar_open = not self.sidebar_open
    
    def show_menu(self):
        """Display the navigation menu pop-up."""
        # Create content for popup
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Menu items
        menu_items = [
            ('Add Item', 'item_add'),
            ('Manage Inventory', 'item_manager'),
            ('Reports', 'reports'),
        ]
        
        for label_text, route in menu_items:
            btn = Button(
                text=label_text,
                size_hint_y=None,
                height='50dp',
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.route = route
            btn.bind(on_press=self.navigate_to)
            content.add_widget(btn)
        
        # Close button
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height='50dp',
            background_color=(0.6, 0.6, 0.6, 1)
        )
        content.add_widget(close_btn)
        
        # Create and show popup
        popup = Popup(
            title='Navigation Menu',
            content=content,
            size_hint=(0.8, 0.6)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def navigate_to(self, instance):
        """Navigate to selected screen."""
        route = instance.route
        # Access the screen manager from the app
        screen_manager = self.manager
        screen_manager.current = route
    
    def set_dashboard(self):
        """Called when dashboard is initialized."""
        # Placeholder for any dashboard setup
        pass
    
    def on_enter(self):
        """Called when entering the screen."""
        pass
    
    def on_leave(self):
        """Called when leaving the screen."""
        pass
