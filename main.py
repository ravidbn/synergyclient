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

# Phase 5: Real service integration with mock fallback
# Try real services first, fallback to mock services
USING_REAL_SERVICES = False

try:
    from bluetooth_service import BluetoothService  # Real Android service
    BLUETOOTH_SERVICE_AVAILABLE = True
    USING_REAL_SERVICES = True
    print("SUCCESS: Real Bluetooth service imported")
except ImportError as e:
    try:
        from bluetooth_service_mock import BluetoothService  # Mock fallback
        BLUETOOTH_SERVICE_AVAILABLE = True
        print(f"FALLBACK: Using mock Bluetooth service ({e})")
    except ImportError as e2:
        BLUETOOTH_SERVICE_AVAILABLE = False
        print(f"ERROR: No Bluetooth service available ({e2})")

try:
    from wifi_hotspot_service import WiFiHotspotService  # Real Android service
    WIFI_SERVICE_AVAILABLE = True
    if not USING_REAL_SERVICES:
        USING_REAL_SERVICES = True
    print("SUCCESS: Real WiFi service imported")
except ImportError as e:
    try:
        from wifi_hotspot_service_mock import WiFiHotspotService  # Mock fallback
        WIFI_SERVICE_AVAILABLE = True
        print(f"FALLBACK: Using mock WiFi service ({e})")
    except ImportError as e2:
        WIFI_SERVICE_AVAILABLE = False
        print(f"ERROR: No WiFi service available ({e2})")

try:
    from file_transfer_service import FileTransferService  # Real Android service
    FILE_SERVICE_AVAILABLE = True
    if not USING_REAL_SERVICES:
        USING_REAL_SERVICES = True
    print("SUCCESS: Real File Transfer service imported")
except ImportError as e:
    try:
        from file_transfer_service_mock import FileTransferService  # Mock fallback
        FILE_SERVICE_AVAILABLE = True
        print(f"FALLBACK: Using mock File Transfer service ({e})")
    except ImportError as e2:
        FILE_SERVICE_AVAILABLE = False
        print(f"ERROR: No File Transfer service available ({e2})")

print(f"Service Status: {'Real Android Services' if USING_REAL_SERVICES else 'Mock Services'}")

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
        
        # Phase 4: Initialize all mock services if available
        self.bluetooth_service = None
        self.wifi_service = None
        self.file_service = None
        
        if BLUETOOTH_SERVICE_AVAILABLE:
            try:
                self.bluetooth_service = BluetoothService()
                print("Bluetooth mock service initialized")
            except Exception as e:
                print(f"Bluetooth service initialization error: {e}")
        
        if WIFI_SERVICE_AVAILABLE:
            try:
                self.wifi_service = WiFiHotspotService()
                print("WiFi mock service initialized")
            except Exception as e:
                print(f"WiFi service initialization error: {e}")
        
        if FILE_SERVICE_AVAILABLE:
            try:
                self.file_service = FileTransferService()
                print("File transfer mock service initialized")
            except Exception as e:
                print(f"File service initialization error: {e}")
    
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
            service_status = "Real Android Services" if USING_REAL_SERVICES else "Mock Services"
            status = Label(
                text=f'Status: {android_status}\nServices: {service_status}\nReady for cross-platform communication',
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
            
            # Add file transfer button
            file_button = Button(
                text='Demo: File Transfer (25MB)',
                size_hint_y=None,
                height=60
            )
            file_button.bind(on_press=self.on_demo_file_transfer)
            layout.add_widget(file_button)
            
            # Add info
            info = Label(
                text='All SynergyClient functions with mock services.\nStable foreground operation maintained.\nReady for cross-platform testing.',
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
        """Demo Bluetooth functionality with real mock service."""
        print("Demo: Bluetooth scan with mock service")
        Logger.info("Application: Demo Bluetooth scan with mock service")
        
        if self.bluetooth_service and BLUETOOTH_SERVICE_AVAILABLE:
            try:
                # Use real mock service
                devices = self.bluetooth_service.scan_for_devices()
                self.button_count += 1
                instance.text = f"Mock Service: {len(devices)} devices"
                print(f"Mock Bluetooth service found {len(devices)} devices: {devices}")
            except Exception as e:
                instance.text = f"Service error: {e}"
                print(f"Mock service error: {e}")
        else:
            # Fallback to simulation
            self.button_count += 1
            device_name = self.demo_devices[self.button_count % len(self.demo_devices)]
            instance.text = f"Simulated: {device_name}"
            print(f"Simulated connection to {device_name}")
    
    def on_demo_wifi(self, instance):
        """Demo WiFi functionality with real mock service."""
        print("Demo: WiFi hotspot with mock service")
        Logger.info("Application: Demo WiFi hotspot with mock service")
        
        if self.wifi_service and WIFI_SERVICE_AVAILABLE:
            try:
                # Use real mock service
                result = self.wifi_service.create_hotspot()
                self.button_count += 1
                instance.text = f"Mock: {result.get('ssid', 'Created')}"
                print(f"Mock WiFi service result: {result}")
            except Exception as e:
                instance.text = f"WiFi error: {e}"
                print(f"Mock WiFi service error: {e}")
        else:
            # Fallback to simulation
            self.button_count += 1
            ssid = f"SynergyHotspot_{self.button_count}"
            instance.text = f"Simulated: {ssid}"
            print(f"Simulated WiFi hotspot: {ssid}")
    
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
        
        # Try to use Bluetooth service for color commands
        if self.bluetooth_service and BLUETOOTH_SERVICE_AVAILABLE:
            try:
                success = self.bluetooth_service.send_color_command(self.current_color)
                instance.text = f"Bluetooth: {self.current_color.title()}"
                print(f"Mock Bluetooth color command sent: {success}")
            except Exception as e:
                instance.text = f"BT Error: {e}"
                print(f"Bluetooth color error: {e}")
        else:
            instance.text = f"Protocol: {self.current_color.title()}"
            print(f"Sent protocol message: {color_message}")
    
    def on_demo_file_transfer(self, instance):
        """Demo file transfer with mock services."""
        print("Demo: File transfer with mock services")
        Logger.info("Application: Demo file transfer with mock services")
        
        if self.bluetooth_service and self.file_service and BLUETOOTH_SERVICE_AVAILABLE and FILE_SERVICE_AVAILABLE:
            try:
                # Use real mock services
                size_mb = PRESET_FILE_SIZES.get("medium", 25)
                success = self.bluetooth_service.send_file_transfer_request(
                    size_mb * 1024 * 1024,
                    f"test_file_{size_mb}MB.bin",
                    "android_to_windows"
                )
                self.button_count += 1
                instance.text = f"Mock Transfer: {size_mb}MB"
                print(f"Mock file transfer request: {success}")
            except Exception as e:
                instance.text = f"Transfer error: {e}"
                print(f"File transfer error: {e}")
        else:
            # Fallback to simulation
            self.button_count += 1
            size_mb = PRESET_FILE_SIZES.get("medium", 25)
            instance.text = f"Simulated: {size_mb}MB"
            print(f"Simulated file transfer: {size_mb}MB")
    
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
