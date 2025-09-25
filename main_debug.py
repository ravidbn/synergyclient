"""
Debug version of main.py that shows exactly what files are available in the APK.
This will help us understand why service imports are failing.
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

print("=== SYNERGY CLIENT DEBUG VERSION ===")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print("")

# Run the debug import tests
print("=== RUNNING DEBUG IMPORT TESTS ===")

# List all Python files in current directory
print("=== FILES IN CURRENT DIRECTORY ===")
try:
    files = [f for f in os.listdir('.') if f.endswith('.py')]
    for f in sorted(files):
        print(f"Found: {f}")
    print("")
except Exception as e:
    print(f"Error listing files: {e}")

# Test individual imports with detailed error info
print("=== TESTING SERVICE IMPORTS ===")

# Test bluetooth_service_mock import
print("1. Testing bluetooth_service_mock import...")
bluetooth_service_mock_available = False
try:
    import bluetooth_service_mock
    print("✅ bluetooth_service_mock imported successfully")
    bluetooth_service_mock_available = True
except ImportError as e:
    print(f"❌ bluetooth_service_mock import failed: {e}")
except Exception as e:
    print(f"❌ bluetooth_service_mock other error: {e}")

# Test other imports
wifi_service_mock_available = False
try:
    import wifi_hotspot_service_mock
    print("✅ wifi_hotspot_service_mock imported successfully")
    wifi_service_mock_available = True
except ImportError as e:
    print(f"❌ wifi_hotspot_service_mock import failed: {e}")

file_service_mock_available = False
try:
    import file_transfer_service_mock
    print("✅ file_transfer_service_mock imported successfully")
    file_service_mock_available = True
except ImportError as e:
    print(f"❌ file_transfer_service_mock import failed: {e}")

# Test real services
bluetooth_service_available = False
try:
    import bluetooth_service
    print("✅ bluetooth_service imported successfully")
    bluetooth_service_available = True
except ImportError as e:
    print(f"❌ bluetooth_service import failed: {e}")

# Test Android APIs
android_available = False
try:
    from jnius import autoclass
    print("✅ jnius imported successfully")
    android_available = True
except ImportError as e:
    print(f"❌ jnius import failed: {e}")

print("")
print("=== IMPORT SUMMARY ===")
print(f"Bluetooth Mock: {'✅' if bluetooth_service_mock_available else '❌'}")
print(f"WiFi Mock: {'✅' if wifi_service_mock_available else '❌'}")
print(f"File Mock: {'✅' if file_service_mock_available else '❌'}")
print(f"Bluetooth Real: {'✅' if bluetooth_service_available else '❌'}")
print(f"Android APIs: {'✅' if android_available else '❌'}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DebugApp(App):
    """Debug app to show import status."""
    
    def build(self):
        """Build debug UI."""
        try:
            layout = BoxLayout(
                orientation='vertical',
                padding=dp(15),
                spacing=dp(8),
                size_hint=(1, 1)
            )
            
            # Title
            title = Label(
                text='Synergy Client - Debug Version',
                size_hint_y=None,
                height=dp(40),
                font_size='18sp',
                bold=True,
                text_size=(None, None),
                halign='center'
            )
            layout.add_widget(title)
            
            # Import status
            mock_count = sum([bluetooth_service_mock_available, wifi_service_mock_available, file_service_mock_available])
            status = Label(
                text=f'Mock Services: {mock_count}/3 | Android: {"Yes" if android_available else "No"}',
                size_hint_y=None,
                height=dp(30),
                font_size='14sp',
                text_size=(None, None),
                halign='center'
            )
            layout.add_widget(status)
            
            # Service details
            bt_status = "✅" if bluetooth_service_mock_available else "❌"
            wifi_status = "✅" if wifi_service_mock_available else "❌"
            file_status = "✅" if file_service_mock_available else "❌"
            
            service_details = Label(
                text=f'BT: {bt_status} | WiFi: {wifi_status} | File: {file_status}',
                size_hint_y=None,
                height=dp(25),
                font_size='12sp',
                text_size=(None, None),
                halign='center'
            )
            layout.add_widget(service_details)
            
            # Test button
            test_button = Button(
                text='Test Service Import',
                size_hint_y=None,
                height=dp(45),
                font_size='16sp'
            )
            test_button.bind(on_press=self.on_test_import)
            layout.add_widget(test_button)
            
            # Show files button
            files_button = Button(
                text='Show Available Files',
                size_hint_y=None,
                height=dp(45),
                font_size='16sp'
            )
            files_button.bind(on_press=self.on_show_files)
            layout.add_widget(files_button)
            
            # Import details button
            details_button = Button(
                text='Show Import Details',
                size_hint_y=None,
                height=dp(45),
                font_size='16sp'
            )
            details_button.bind(on_press=self.on_show_details)
            layout.add_widget(details_button)
            
            # Result info
            if mock_count > 0:
                result_text = f"SUCCESS: {mock_count}/3 mock services found"
            else:
                result_text = "PROBLEM: No service files found in APK"
            
            result = Label(
                text=result_text,
                size_hint_y=None,
                height=dp(25),
                font_size='12sp',
                text_size=(None, None),
                halign='center'
            )
            layout.add_widget(result)
            
            print("✅ Debug UI built successfully")
            return layout
            
        except Exception as e:
            print(f"❌ ERROR building debug UI: {str(e)}")
            return Label(
                text=f'Debug UI Error: {str(e)}',
                text_size=(dp(300), None),
                halign='center'
            )
    
    def on_test_import(self, instance):
        """Test importing services."""
        print("=== TESTING IMPORTS AGAIN ===")
        try:
            if bluetooth_service_mock_available:
                from bluetooth_service_mock import BluetoothService
                service = BluetoothService()
                devices = service.scan_for_devices()
                instance.text = f"BT Mock: {len(devices)} devices"
                print(f"Bluetooth mock test: {len(devices)} devices found")
            else:
                instance.text = "BT Mock: Not Available"
                print("Bluetooth mock service not available")
        except Exception as e:
            instance.text = f"BT Error: {str(e)[:20]}..."
            print(f"Bluetooth test error: {e}")
    
    def on_show_files(self, instance):
        """Show available files."""
        print("=== FILES IN APK ===")
        try:
            files = [f for f in os.listdir('.') if f.endswith('.py')]
            instance.text = f"Files: {len(files)} .py files"
            for f in sorted(files):
                print(f"Available: {f}")
        except Exception as e:
            instance.text = f"File Error: {str(e)[:20]}..."
            print(f"File listing error: {e}")
    
    def on_show_details(self, instance):
        """Show detailed import information."""
        print("=== DETAILED IMPORT INFO ===")
        details = []
        details.append(f"Python: {sys.version[:10]}")
        details.append(f"BT Mock: {'Yes' if bluetooth_service_mock_available else 'No'}")
        details.append(f"WiFi Mock: {'Yes' if wifi_service_mock_available else 'No'}")
        details.append(f"File Mock: {'Yes' if file_service_mock_available else 'No'}")
        details.append(f"Android: {'Yes' if android_available else 'No'}")
        
        available_count = sum([bluetooth_service_mock_available, wifi_service_mock_available, file_service_mock_available])
        instance.text = f"Details: {available_count}/3 available"
        
        for detail in details:
            print(f"DETAIL: {detail}")

# Main entry point
if __name__ == '__main__':
    try:
        print("Creating debug app...")
        app = DebugApp()
        print("Running debug app...")
        app.run()
    except Exception as e:
        print(f"FATAL ERROR: {str(e)}")
        Logger.error(f"Application: Fatal error: {str(e)}")
        sys.exit(1)