"""
Synergy Client with Real Android Services.
This version prioritizes real Android services and handles import errors gracefully.
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
from kivy.metrics import dp

# Android-specific imports to prevent backgrounding
try:
    from jnius import autoclass
    
    # Android classes for keeping app active
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WindowManager = autoclass('android.view.WindowManager')
    Context = autoclass('android.content.Context')
    PowerManager = autoclass('android.os.PowerManager')
    
    ANDROID_AVAILABLE = True
    print("✅ Android APIs available")
except ImportError:
    ANDROID_AVAILABLE = False
    print("⚠️  Android APIs not available - running in desktop mode")

# Protocol definitions
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

# Service Import and Status
service_status = {
    'bluetooth': {'available': False, 'real': False, 'error': None},
    'wifi': {'available': False, 'real': False, 'error': None},
    'file': {'available': False, 'real': False, 'error': None}
}

# Try importing real services first
print("=== ATTEMPTING TO LOAD REAL ANDROID SERVICES ===")

# Bluetooth Service
try:
    if ANDROID_AVAILABLE:
        from bluetooth_service import BluetoothService
        service_status['bluetooth'] = {'available': True, 'real': True, 'error': None}
        print("✅ REAL Bluetooth service imported successfully")
    else:
        raise ImportError("Android APIs not available")
except ImportError as e:
    try:
        from bluetooth_service_mock import BluetoothService
        service_status['bluetooth'] = {'available': True, 'real': False, 'error': str(e)}
        print(f"⚠️  Fallback to MOCK Bluetooth service: {e}")
    except ImportError as e2:
        service_status['bluetooth'] = {'available': False, 'real': False, 'error': str(e2)}
        print(f"❌ No Bluetooth service available: {e2}")

# WiFi Service
try:
    if ANDROID_AVAILABLE:
        from wifi_hotspot_service import WiFiHotspotService
        service_status['wifi'] = {'available': True, 'real': True, 'error': None}
        print("✅ REAL WiFi service imported successfully")
    else:
        raise ImportError("Android APIs not available")
except ImportError as e:
    try:
        from wifi_hotspot_service_mock import WiFiHotspotService
        service_status['wifi'] = {'available': True, 'real': False, 'error': str(e)}
        print(f"⚠️  Fallback to MOCK WiFi service: {e}")
    except ImportError as e2:
        service_status['wifi'] = {'available': False, 'real': False, 'error': str(e2)}
        print(f"❌ No WiFi service available: {e2}")

# File Transfer Service
try:
    if ANDROID_AVAILABLE:
        from file_transfer_service import FileTransferService
        service_status['file'] = {'available': True, 'real': True, 'error': None}
        print("✅ REAL File Transfer service imported successfully")
    else:
        raise ImportError("Android APIs not available")
except ImportError as e:
    try:
        from file_transfer_service_mock import FileTransferService
        service_status['file'] = {'available': True, 'real': False, 'error': str(e)}
        print(f"⚠️  Fallback to MOCK File Transfer service: {e}")
    except ImportError as e2:
        service_status['file'] = {'available': False, 'real': False, 'error': str(e2)}
        print(f"❌ No File Transfer service available: {e2}")

# Determine overall service status
real_services_count = sum(1 for s in service_status.values() if s['real'])
available_services_count = sum(1 for s in service_status.values() if s['available'])

print(f"=== SERVICE STATUS SUMMARY ===")
print(f"Real services: {real_services_count}/3")
print(f"Available services: {available_services_count}/3")
print(f"Android APIs: {'Available' if ANDROID_AVAILABLE else 'Not Available'}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=== SYNERGY CLIENT STARTING WITH REAL SERVICES ===")
Logger.info("Application: Synergy Client starting with real services")

class SynergyClientApp(App):
    """Synergy Client with Real Android Services and Fixed UI Layout."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keep_alive_event = None
        self.wake_lock = None
        self.title = "Synergy Client - Real Services"
        self.button_count = 0
        self.current_color = ColorType.RED
        self.demo_devices = ["Windows_PC", "Samsung_S23", "Test_Device"]
        self.colors = [ColorType.RED, ColorType.YELLOW, ColorType.GREEN]
        
        # Initialize services
        self.bluetooth_service = None
        self.wifi_service = None
        self.file_service = None
        
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize available services."""
        print("Initializing services...")
        
        if service_status['bluetooth']['available']:
            try:
                self.bluetooth_service = BluetoothService()
                print("✅ Bluetooth service initialized")
            except Exception as e:
                print(f"❌ Bluetooth service initialization error: {e}")
        
        if service_status['wifi']['available']:
            try:
                self.wifi_service = WiFiHotspotService()
                print("✅ WiFi service initialized")
            except Exception as e:
                print(f"❌ WiFi service initialization error: {e}")
        
        if service_status['file']['available']:
            try:
                self.file_service = FileTransferService()
                print("✅ File transfer service initialized")
            except Exception as e:
                print(f"❌ File service initialization error: {e}")
    
    def build(self):
        """Build UI with proper layout to prevent text overlapping."""
        try:
            print("Building Synergy Client UI with fixed layout...")
            Logger.info("Application: Building UI with fixed layout")
            
            # Create main layout with proper spacing and sizing
            layout = BoxLayout(
                orientation='vertical',
                padding=dp(15),
                spacing=dp(8),
                size_hint=(1, 1)
            )
            
            # Title with proper sizing
            title = Label(
                text='Synergy Client - Real Services',
                size_hint_y=None,
                height=dp(40),
                font_size='18sp',
                bold=True,
                text_size=(None, None),
                halign='center'
            )
            layout.add_widget(title)
            
            # Service status with better formatting
            real_count = sum(1 for s in service_status.values() if s['real'])
            total_count = sum(1 for s in service_status.values() if s['available'])
            android_status = "Android" if ANDROID_AVAILABLE else "Desktop"
            
            status_text = f'{android_status} | Real: {real_count}/{total_count}'
            status = Label(
                text=status_text,
                size_hint_y=None,
                height=dp(30),
                font_size='14sp',
                text_size=(None, None),
                halign='center'
            )
            layout.add_widget(status)
            
            # Service details with wrapped text
            bt_status = "✅ Real" if service_status['bluetooth']['real'] else "⚠️ Mock" if service_status['bluetooth']['available'] else "❌ None"
            wifi_status = "✅ Real" if service_status['wifi']['real'] else "⚠️ Mock" if service_status['wifi']['available'] else "❌ None"
            file_status = "✅ Real" if service_status['file']['real'] else "⚠️ Mock" if service_status['file']['available'] else "❌ None"
            
            service_details = Label(
                text=f'BT: {bt_status} | WiFi: {wifi_status} | File: {file_status}',
                size_hint_y=None,
                height=dp(25),
                font_size='12sp',
                text_size=(None, None),
                halign='center'
            )
            layout.add_widget(service_details)
            
            # Add buttons with consistent sizing and spacing
            button_height = dp(45)
            button_font_size = '16sp'
            
            # Bluetooth button
            bluetooth_button = Button(
                text='Test Bluetooth Service',
                size_hint_y=None,
                height=button_height,
                font_size=button_font_size
            )
            bluetooth_button.bind(on_press=self.on_test_bluetooth)
            layout.add_widget(bluetooth_button)
            
            # WiFi button
            wifi_button = Button(
                text='Test WiFi Hotspot',
                size_hint_y=None,
                height=button_height,
                font_size=button_font_size
            )
            wifi_button.bind(on_press=self.on_test_wifi)
            layout.add_widget(wifi_button)
            
            # Color button
            color_button = Button(
                text='Send Color Command',
                size_hint_y=None,
                height=button_height,
                font_size=button_font_size
            )
            color_button.bind(on_press=self.on_test_color)
            layout.add_widget(color_button)
            
            # File transfer button
            file_button = Button(
                text='Test File Transfer',
                size_hint_y=None,
                height=button_height,
                font_size=button_font_size
            )
            file_button.bind(on_press=self.on_test_file_transfer)
            layout.add_widget(file_button)
            
            # Service details button
            details_button = Button(
                text='Show Service Details',
                size_hint_y=None,
                height=button_height,
                font_size=button_font_size
            )
            details_button.bind(on_press=self.on_show_details)
            layout.add_widget(details_button)
            
            # Info label with proper wrapping
            info_text = "Real Android services enabled" if any(s['real'] for s in service_status.values()) else "Using mock services"
            info = Label(
                text=info_text,
                size_hint_y=None,
                height=dp(25),
                font_size='12sp',
                text_size=(None, None),
                halign='center'
            )
            layout.add_widget(info)
            
            print("✅ UI built successfully with fixed layout")
            Logger.info("Application: UI built successfully with fixed layout")
            return layout
            
        except Exception as e:
            print(f"❌ ERROR building UI: {str(e)}")
            Logger.error(f"Application: Error building UI: {str(e)}")
            
            # Emergency fallback
            return Label(
                text=f'UI Error: {str(e)}',
                text_size=(dp(300), None),
                halign='center'
            )
    
    def on_test_bluetooth(self, instance):
        """Test Bluetooth functionality."""
        print("Testing Bluetooth service...")
        Logger.info("Application: Testing Bluetooth service")
        
        if self.bluetooth_service and service_status['bluetooth']['available']:
            try:
                # Test different functions based on service type
                if service_status['bluetooth']['real']:
                    # Test real Android Bluetooth
                    enabled = self.bluetooth_service.is_bluetooth_enabled()
                    devices = self.bluetooth_service.scan_for_devices()
                    self.button_count += 1
                    instance.text = f"Real BT: {len(devices)} devices, Enabled: {enabled}"
                    print(f"Real Bluetooth: {len(devices)} devices found, Enabled: {enabled}")
                else:
                    # Test mock Bluetooth
                    devices = self.bluetooth_service.scan_for_devices()
                    self.button_count += 1
                    instance.text = f"Mock BT: {len(devices)} devices"
                    print(f"Mock Bluetooth: {len(devices)} devices found")
            except Exception as e:
                instance.text = f"BT Error: {str(e)[:20]}..."
                print(f"Bluetooth service error: {e}")
        else:
            instance.text = "BT: Not Available"
            print("Bluetooth service not available")
    
    def on_test_wifi(self, instance):
        """Test WiFi functionality."""
        print("Testing WiFi service...")
        Logger.info("Application: Testing WiFi service")
        
        if self.wifi_service and service_status['wifi']['available']:
            try:
                if service_status['wifi']['real']:
                    # Test real Android WiFi
                    result = self.wifi_service.create_hotspot()
                    self.button_count += 1
                    if result.get('success'):
                        instance.text = f"Real WiFi: {result.get('ssid', 'Created')}"
                    else:
                        instance.text = f"WiFi Error: {result.get('error', 'Failed')[:15]}..."
                    print(f"Real WiFi service result: {result}")
                else:
                    # Test mock WiFi
                    result = self.wifi_service.create_hotspot()
                    self.button_count += 1
                    instance.text = f"Mock WiFi: {result.get('ssid', 'Created')}"
                    print(f"Mock WiFi service result: {result}")
            except Exception as e:
                instance.text = f"WiFi Error: {str(e)[:15]}..."
                print(f"WiFi service error: {e}")
        else:
            instance.text = "WiFi: Not Available"
            print("WiFi service not available")
    
    def on_test_color(self, instance):
        """Test color command functionality."""
        print("Testing color command...")
        Logger.info("Application: Testing color command")
        
        # Use color from list
        self.current_color = self.colors[self.button_count % len(self.colors)]
        self.button_count += 1
        
        if self.bluetooth_service and service_status['bluetooth']['available']:
            try:
                if service_status['bluetooth']['real']:
                    # Use real Bluetooth service
                    success = self.bluetooth_service.send_color_command(self.current_color)
                    instance.text = f"Real Color: {self.current_color.title()}"
                    print(f"Real Bluetooth color command: {success}")
                else:
                    # Use mock Bluetooth service
                    success = self.bluetooth_service.send_color_command(self.current_color)
                    instance.text = f"Mock Color: {self.current_color.title()}"
                    print(f"Mock Bluetooth color command: {success}")
            except Exception as e:
                instance.text = f"Color Error: {str(e)[:15]}..."
                print(f"Color command error: {e}")
        else:
            instance.text = f"No BT: {self.current_color.title()}"
            print(f"Color command without Bluetooth: {self.current_color}")
    
    def on_test_file_transfer(self, instance):
        """Test file transfer functionality."""
        print("Testing file transfer...")
        Logger.info("Application: Testing file transfer")
        
        if self.file_service and service_status['file']['available']:
            try:
                size_mb = PRESET_FILE_SIZES.get("medium", 25)
                if service_status['file']['real']:
                    # Test real file service
                    # (Real file service implementation would vary)
                    self.button_count += 1
                    instance.text = f"Real Transfer: {size_mb}MB"
                    print(f"Real file transfer request: {size_mb}MB")
                else:
                    # Test mock file service
                    success = self.file_service.generate_test_file(size_mb * 1024 * 1024, f"test_{size_mb}MB.bin")
                    self.button_count += 1
                    instance.text = f"Mock Transfer: {size_mb}MB"
                    print(f"Mock file transfer: {success}")
            except Exception as e:
                instance.text = f"File Error: {str(e)[:15]}..."
                print(f"File transfer error: {e}")
        else:
            self.button_count += 1
            size_mb = PRESET_FILE_SIZES.get("medium", 25)
            instance.text = f"No File: {size_mb}MB"
            print(f"File transfer simulation: {size_mb}MB")
    
    def on_show_details(self, instance):
        """Show detailed service information."""
        print("=== DETAILED SERVICE STATUS ===")
        
        details = []
        details.append(f"Android APIs: {ANDROID_AVAILABLE}")
        
        for service_name, status in service_status.items():
            real_text = "Real" if status['real'] else "Mock" if status['available'] else "None"
            details.append(f"{service_name.title()}: {real_text}")
            if status['error']:
                print(f"{service_name.title()} Error: {status['error']}")
        
        # Update button text with summary
        real_count = sum(1 for s in service_status.values() if s['real'])
        total_count = sum(1 for s in service_status.values() if s['available'])
        instance.text = f"Details: {real_count}R/{total_count}T"
        
        # Print full details to console
        for detail in details:
            print(f"DETAIL: {detail}")
    
    def on_start(self):
        """Called when app starts."""
        print("=== SYNERGY CLIENT STARTED WITH REAL SERVICES ===")
        Logger.info("Application: Synergy Client started with real services")
        
        # Prevent app from going to background
        self.prevent_backgrounding()
        
        # Keep app active with periodic updates
        self.keep_alive_event = Clock.schedule_interval(self.keep_alive, 3.0)
        
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
                print("✅ WakeLock acquired")
                
                # Try to keep app in foreground
                activity.moveTaskToFront(activity.getTaskId(), 0)
                
                print("✅ Android foreground setup complete")
                
            except Exception as e:
                print(f"⚠️  Android setup error: {e}")
        else:
            print("ℹ️  Android APIs not available - skipping foreground setup")
    
    def keep_alive(self, dt):
        """Keep app alive and prevent backgrounding."""
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
            print("✅ WakeLock released")

# Main entry point
if __name__ == '__main__':
    try:
        print("Creating Synergy Client app with real services...")
        app = SynergyClientApp()
        print("Running Synergy Client with real services...")
        app.run()
    except Exception as e:
        print(f"FATAL ERROR: {str(e)}")
        Logger.error(f"Application: Fatal error: {str(e)}")
        sys.exit(1)