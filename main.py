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
from kivy.clock import Clock

# Android-specific imports to prevent backgrounding
try:
    from jnius import autoclass
    
    # Android classes for keeping app active
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WindowManager = autoclass('android.view.WindowManager')
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')
    
    ANDROID_AVAILABLE = True
    print("Android APIs available")
except ImportError:
    ANDROID_AVAILABLE = False
    print("Android APIs not available - running in desktop mode")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=== MINIMAL SYNERGY CLIENT STARTING ===")
Logger.info("Application: Minimal Synergy Client starting")

class MinimalApp(App):
    """Minimal application for testing."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keep_alive_event = None
        self.wake_lock = None
        self.title = "Synergy Client"
    
    def build(self):
        """Build minimal UI."""
        try:
            print("Building minimal UI...")
            Logger.info("Application: Building UI")
            
            # Create simple layout
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Add title
            title = Label(
                text='Synergy Client - Minimal Version\nShould stay in foreground!',
                size_hint_y=None,
                height=80,
                text_size=(None, None)
            )
            layout.add_widget(title)
            
            # Add status
            android_status = "Android APIs Available" if ANDROID_AVAILABLE else "Desktop Mode"
            status = Label(
                text=f'App started successfully!\n{android_status}\nNo complex services loaded.',
                size_hint_y=None,
                height=120,
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
                text='If you see this UI and can tap the button,\nthe basic app is working correctly.\nNext step: add back features gradually.',
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
        instance.text = "Button Pressed! ✓ App is working!"
    
    def on_start(self):
        """Called when app starts."""
        print("=== APP STARTED SUCCESSFULLY ===")
        Logger.info("Application: Started successfully")
        
        # Prevent app from going to background
        self.prevent_backgrounding()
        
        # Keep app active with periodic updates
        self.keep_alive_event = Clock.schedule_interval(self.keep_alive, 2.0)
        
        print("Keep-alive timer started")
    
    def prevent_backgrounding(self):
        """Prevent app from automatically going to background."""
        if ANDROID_AVAILABLE:
            try:
                print("Setting up Android foreground behavior...")
                activity = PythonActivity.mActivity
                
                # Keep screen on
                activity.getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                
                # Acquire wake lock to prevent backgrounding
                power_manager = activity.getSystemService(Context.POWER_SERVICE)
                self.wake_lock = power_manager.newWakeLock(
                    PowerManager.PARTIAL_WAKE_LOCK,
                    "SynergyClient::KeepAwake"
                )
                self.wake_lock.acquire()
                print("WakeLock acquired")
                
                # Try to keep app in foreground
                activity.moveTaskToFront(activity.getTaskId(), 0)
                
                print("Android foreground setup complete")
                
            except Exception as e:
                print(f"Android setup error: {e}")
        else:
            print("Android APIs not available - skipping foreground setup")
    
    def keep_alive(self, dt):
        """Keep app alive and prevent backgrounding."""
        print("Keep-alive tick...")
        
        if ANDROID_AVAILABLE:
            try:
                # Keep bringing app to foreground
                activity = PythonActivity.mActivity
                activity.moveTaskToFront(activity.getTaskId(), 0)
            except Exception as e:
                print(f"Keep-alive error: {e}")
        
        return True  # Continue scheduling
    
    def on_stop(self):
        """Called when app stops."""
        print("=== APP STOPPING ===")
        Logger.info("Application: Stopping")
        
        # Clean up keep-alive timer
        if self.keep_alive_event:
            self.keep_alive_event.cancel()
        
        # Release wake lock
        if self.wake_lock and self.wake_lock.isHeld():
            self.wake_lock.release()
            print("WakeLock released")

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
