"""
Minimal Android application for debugging startup issues.
Just shows a basic UI without any complex imports.
"""

import os
import sys
import logging

# Only basic Kivy imports
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=== MINIMAL SYNERGY CLIENT STARTING ===")
Logger.info("Application: Minimal Synergy Client starting")

class MinimalApp(App):
    """Minimal application for testing."""
    
    def build(self):
        """Build minimal UI."""
        try:
            print("Building minimal UI...")
            Logger.info("Application: Building UI")
            
            # Create simple layout
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Add title
            title = Label(
                text='Synergy Client - Minimal Version',
                size_hint_y=None,
                height=50,
                text_size=(None, None)
            )
            layout.add_widget(title)
            
            # Add status
            status = Label(
                text='App started successfully!\nNo complex services loaded.',
                size_hint_y=None,
                height=100,
                text_size=(None, None)
            )
            layout.add_widget(status)
            
            # Add test button
            button = Button(
                text='Test Button - Tap Me!',
                size_hint_y=None,
                height=60
            )
            button.bind(on_press=self.on_button_press)
            layout.add_widget(button)
            
            # Add info
            info = Label(
                text='If you see this, the basic app is working.\nNext step: gradually add back features.',
                text_size=(None, None)
            )
            layout.add_widget(info)
            
            print("UI built successfully")
            Logger.info("Application: UI built successfully")
            return layout
            
        except Exception as e:
            print(f"ERROR building UI: {str(e)}")
            Logger.error(f"Application: Error building UI: {str(e)}")
            
            # Emergency fallback
            return Label(text=f'Error: {str(e)}')
    
    def on_button_press(self, instance):
        """Handle button press."""
        print("Button pressed!")
        Logger.info("Application: Button pressed")
        instance.text = "Button Pressed! ✓"
    
    def on_start(self):
        """Called when app starts."""
        print("=== APP STARTED SUCCESSFULLY ===")
        Logger.info("Application: Started successfully")
    
    def on_stop(self):
        """Called when app stops."""
        print("=== APP STOPPING ===")
        Logger.info("Application: Stopping")

# Main entry point
if __name__ == '__main__':
    try:
        print("Creating minimal app...")
        app = MinimalApp()
        print("Running app...")
        app.run()
    except Exception as e:
        print(f"FATAL ERROR: {str(e)}")
        Logger.error(f"Application: Fatal error: {str(e)}")
        sys.exit(1)