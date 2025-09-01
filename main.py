"""
Minimal Android application that stays in foreground.
Gradually adding SynergyClient features while maintaining stability.
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

# Lightweight protocol definitions - safe additions
class ColorType:
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"

class ActionType:
    COLOR_CHANGE = "color_change"
    WIFI_CONNECTION_STATUS = "wifi_status"
    FILE_TRANSFER_REQUEST = "file_transfer_request"

PRESET_FILE_SIZES = {
    "small": 10,
    "medium": 25,
    "large": 50,
    "xlarge": 100
}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=== SYNERGY CLIENT STARTING ===")
Logger.info("Application: Synergy Client starting")

class SynergyClientApp(App):
    """Synergy Client with proven foreground handling."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keep_alive_event = None
        self.wake_lock = None
        self.title = "Synergy Client"
        self.button_count = 0
        self.current_color = ColorType.RED
        self.demo_devices = ["Device_1", "Device_2", "Windows_PC"]
        self.colors = [ColorType.RED, ColorType.YELLOW, ColorType.GREEN]
    
    def build(self):
        """Build stable UI with SynergyClient branding."""
        try:
            print("Building Synergy Client UI...")
            Logger.info("Application: Building UI")
            
            # Create main layout
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Add title
            title = Label(
                text='Synergy Client\nDemo System - Stays in Foreground!',
                size_hint_y=None,
                height=80,
                text_size=(None, None)
            )
            layout.add_widget(title)
            
            # Add status
            android_status = "Android APIs Available" if ANDROID_AVAILABLE else "Desktop Mode"
            status = Label(
                text=f'Status: {android_status}\nReady for cross-platform communication\nBuilds successfully with stable foreground handling',
                size_hint_y=None,
                height=120,
                text_size=(None, None)
            )
            layout.add_widget(status)
            
            # Add demo button
            demo_button = Button(
                text='Demo: Simulate Bluetooth Scan',
                size_hint_y=None,
                height=60
            )
            demo_button.bind(on_press=self.on_demo_bluetooth)
            layout.add_widget(demo_button)
            
            # Add demo WiFi button
            wifi_button = Button(
                text='Demo: Simulate WiFi Hotspot',
                size_hint_y=None,
                height=60
            )
            wifi_button.bind(on_press=self.on_demo_wifi)
            layout.add_widget(wifi_button)
            
            # Add color demo
            color_button = Button(
                text='Demo: Send Color Command',
                size_hint_y=None,
                height=60
            )
            color_button.bind(on_press=self.on_demo_color)
            layout.add_widget(color_button)
            
            # Add info
            info = Label(
                text='Demo buttons show SynergyClient functionality.\nStable foundation ready for real service integration.\nForces foreground operation - no backgrounding.',
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
    
    def on_demo_bluetooth(self, instance):
        """Demo Bluetooth functionality with protocol integration."""
        print("Demo: Bluetooth scan with protocol")
        Logger.info("Application: Demo Bluetooth scan with protocol")
        self.button_count += 1
        device_name = self.demo_devices[self.button_count % len(self.demo_devices)]
        instance.text = f"Connected: {device_name}"
        print(f"Protocol: Connected to {device_name}")
    
    def on_demo_wifi(self, instance):
        """Demo WiFi functionality with protocol integration."""
        print("Demo: WiFi hotspot with protocol")
        Logger.info("Application: Demo WiFi hotspot with protocol")
        self.button_count += 1
        ssid = f"SynergyHotspot_{self.button_count}"
        
        # Simulate protocol message
        wifi_message = {
            "action": ActionType.WIFI_CONNECTION_STATUS,
            "ssid": ssid,
            "status": "active"
        }
        
        instance.text = f"Active: {ssid}"
        print(f"Protocol message: {wifi_message}")
    
    def on_demo_color(self, instance):
        """Demo color command with protocol integration."""
        print("Demo: Color command with protocol")
        Logger.info("Application: Demo color command with protocol")
        
        # Use protocol definitions
        self.current_color = self.colors[self.button_count % len(self.colors)]
        self.button_count += 1
        
        # Simulate protocol message
        color_message = {
            "action": ActionType.COLOR_CHANGE,
            "color": self.current_color,
            "timestamp": self.button_count
        }
        
        instance.text = f"Protocol: {self.current_color.title()}"
        print(f"Sent protocol message: {color_message}")
    
    def on_start(self):
        """Called when app starts."""
        print("=== SYNERGY CLIENT STARTED SUCCESSFULLY ===")
        Logger.info("Application: Synergy Client started successfully")
        
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
        print("=== SYNERGY CLIENT STOPPING ===")
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
        print("Creating Synergy Client app...")
        app = SynergyClientApp()
        print("Running Synergy Client...")
        app.run()
    except Exception as e:
        print(f"FATAL ERROR: {str(e)}")
        Logger.error(f"Application: Fatal error: {str(e)}")
        sys.exit(1)
