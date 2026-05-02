from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, BooleanProperty


class WindowManager(ScreenManager):
    """Manages the switching between different content screens."""
    pass


class AppShell(BoxLayout):
    screen_manager = ObjectProperty()
    tabs = ObjectProperty()
    sidebar_open = BooleanProperty(False)

    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    def change_screen(self, screen):
        """Change to the selected screen."""
        self.sidebar_open = False
        self.screen_manager.current = screen

        # Load screen-specific data when entering
        if self.screen_manager.current == 'dashboard':
            self.screen_manager.get_screen('dashboard').set_dashboard()
        elif self.screen_manager.current == 'item_add':
            self.screen_manager.get_screen('item_add').clear_inputs()
        elif self.screen_manager.current == 'item_manager':
            self.screen_manager.get_screen('item_manager').load_items()
        elif self.screen_manager.current == 'reports':
            self.screen_manager.get_screen('reports').load_reports()

        # Update active tab button
        for tab_button in self.tabs.children:
            if tab_button.route == screen:
                tab_button.is_active = True
            else:
                tab_button.is_active = False

    def set_dashboard(self):
        """Initialize and set the dashboard screen."""
        self.screen_manager.get_screen('dashboard').set_dashboard()
        self.change_screen('dashboard')


Builder.load_file('shell.kv')