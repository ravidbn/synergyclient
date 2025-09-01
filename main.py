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

# Service imports - using mock versions for stability
try:
    # Try to import Android-specific services
    from bluetooth_service import BluetoothService
    from wifi_hotspot_service import WiFiHotspotService
    from file_transfer_service import FileTransferService
    USING_MOCKS = False
    print("SUCCESS: Using real Android services")
except ImportError as e:
    # Fall back to mock services if Android imports fail
    print(f"FALLBACK: Android services failed ({e}), using mock services")
    from bluetooth_service_mock import BluetoothService
    from wifi_hotspot_service_mock import WiFiHotspotService
    from file_transfer_service_mock import FileTransferService
    USING_MOCKS = True

try:
    from utils.protocol import ColorType, ActionType, MessageType
    from utils.file_generator import PRESET_FILE_SIZES, FileGenerator
except ImportError as e:
    print(f"Protocol imports failed: {e} - creating minimal alternatives")
    # Create minimal alternatives for missing imports
    class ColorType:
        RED = "red"
        YELLOW = "yellow"
        GREEN = "green"
    
    PRESET_FILE_SIZES = {"small": 10, "medium": 25, "large": 50}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=== SYNERGY CLIENT STARTING ===")
Logger.info("Application: Synergy Client starting")

class SynergyClientApp(App):
    """SynergyClient application with stable foreground handling."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keep_alive_event = None
        self.wake_lock = None
        self.title = "Synergy Client"
        
        # Initialize services with error handling
        self.bluetooth_service = None
        self.wifi_service = None
        self.file_service = None
        self.available_devices = []
        self._init_services()
    
    def _init_services(self):
        """Initialize services with error handling."""
        try:
            self.bluetooth_service = BluetoothService()
            self.wifi_service = WiFiHotspotService()
            self.file_service = FileTransferService()
            print("Services initialized successfully")
        except Exception as e:
            print(f"Service initialization error: {e}")
    
    def build(self):
        """Build minimal UI."""
        try:
            print("Building minimal UI...")
            Logger.info("Application: Building UI")
            
            # Create main layout
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Add title
            title = Label(
                text='Synergy Client\nStays in foreground!',
                size_hint_y=None,
                height=80,
                text_size=(None, None)
            )
            layout.add_widget(title)
            
            # Add status
            android_status = "Android APIs Available" if ANDROID_AVAILABLE else "Desktop Mode"
            service_status = "Mock Services" if USING_MOCKS else "Real Services"
            status = Label(
                text=f'Status: {android_status}\nServices: {service_status}\nReady for Bluetooth pairing',
                size_hint_y=None,
                height=100,
                text_size=(None, None)
            )
            layout.add_widget(status)
            
            # Add Bluetooth button
            bt_button = Button(
                text='Scan & Connect Bluetooth',
                size_hint_y=None,
                height=60
            )
            bt_button.bind(on_press=self.on_bluetooth_scan)
            layout.add_widget(bt_button)
            
            # Add WiFi button
            wifi_button = Button(
                text='Create WiFi Hotspot',
                size_hint_y=None,
                height=60
            )
            wifi_button.bind(on_press=self.on_wifi_hotspot)
            layout.add_widget(wifi_button)
            
            # Add color control buttons
            color_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
            
            red_btn = Button(text='Red')
            red_btn.bind(on_press=lambda x: self.send_color_command('red'))
            color_layout.add_widget(red_btn)
            
            yellow_btn = Button(text='Yellow')
            yellow_btn.bind(on_press=lambda x: self.send_color_command('yellow'))
            color_layout.add_widget(yellow_btn)
            
            green_btn = Button(text='Green')
            green_btn.bind(on_press=lambda x: self.send_color_command('green'))
            color_layout.add_widget(green_btn)
            
            layout.add_widget(color_layout)
            
            # Add file transfer button
            file_button = Button(
                text='Request File Transfer (25MB)',
                size_hint_y=None,
                height=60
            )
            file_button.bind(on_press=self.on_file_transfer)
            layout.add_widget(file_button)
            
            # Add info
            info = Label(
                text='All buttons functional with mock services.\nUses stable foreground handling.',
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
    
    def on_bluetooth_scan(self, instance):
        """Handle Bluetooth scan and connect."""
        print("Bluetooth scan requested!")
        Logger.info("Application: Bluetooth scan")
        
        if self.bluetooth_service:
            try:
                devices = self.bluetooth_service.scan_for_devices()
                instance.text = f"Found {len(devices)} devices"
                print(f"Bluetooth scan found {len(devices)} devices")
            except Exception as e:
                instance.text = f"Scan error: {e}"
                print(f"Bluetooth scan error: {e}")
        else:
            instance.text = "Bluetooth service not available"
    
    def on_wifi_hotspot(self, instance):
        """Handle WiFi hotspot creation."""
        print("WiFi hotspot requested!")
        Logger.info("Application: WiFi hotspot")
        
        if self.wifi_service:
            try:
                result = self.wifi_service.create_hotspot()
                if result.get('success'):
                    instance.text = f"Hotspot: {result.get('ssid', 'Created')}"
                    print(f"WiFi hotspot created: {result}")
                else:
                    instance.text = "Hotspot failed"
                    print(f"WiFi hotspot failed: {result}")
            except Exception as e:
                instance.text = f"WiFi error: {e}"
                print(f"WiFi error: {e}")
        else:
            instance.text = "WiFi service not available"
    
    def send_color_command(self, color):
        """Send color command."""
        print(f"Color command: {color}")
        Logger.info(f"Application: Color command {color}")
        
        if self.bluetooth_service:
            try:
                success = self.bluetooth_service.send_color_command(getattr(ColorType, color.upper(), color))
                print(f"Color command {color} sent: {success}")
            except Exception as e:
                print(f"Color command error: {e}")
        else:
            print("Bluetooth service not available for color command")
    
    def on_file_transfer(self, instance):
        """Handle file transfer request."""
        print("File transfer requested!")
        Logger.info("Application: File transfer")
        
        if self.bluetooth_service and self.file_service:
            try:
                size_mb = PRESET_FILE_SIZES.get("medium", 25)
                success = self.bluetooth_service.send_file_transfer_request(
                    size_mb * 1024 * 1024,
                    f"test_file_{size_mb}MB.bin",
                    "android_to_windows"
                )
                instance.text = f"Transfer request: {success}"
                print(f"File transfer request sent: {success}")
            except Exception as e:
                instance.text = f"Transfer error: {e}"
                print(f"File transfer error: {e}")
        else:
            instance.text = "Services not available"
    
    def on_start(self):
        """Called when app starts."""
        print("=== SYNERGY CLIENT STARTED SUCCESSFULLY ===")
        Logger.info("Application: Synergy Client started successfully")
        
        # Initialize service callbacks if available
        self._setup_service_callbacks()
        
        # Prevent app from going to background
        self.prevent_backgrounding()
        
        # Keep app active with periodic updates
        self.keep_alive_event = Clock.schedule_interval(self.keep_alive, 2.0)
        
        print("Keep-alive timer started")
    
    def _setup_service_callbacks(self):
        """Setup service callbacks with error handling."""
        try:
            if self.bluetooth_service and hasattr(self.bluetooth_service, 'start_server'):
                self.bluetooth_service.start_server("SynergyClient")
                print("Bluetooth server started")
        except Exception as e:
            print(f"Service callback setup error: {e}")
    
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
        print("Creating Synergy Client app...")
        app = SynergyClientApp()
        print("Running Synergy Client...")
        app.run()
    except Exception as e:
        print(f"FATAL ERROR: {str(e)}")
        Logger.error(f"Application: Fatal error: {str(e)}")
        sys.exit(1)
