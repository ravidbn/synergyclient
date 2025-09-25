import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

# VERSION DISPLAY
APP_VERSION = "v3.0 - SINGLE FILE SOLUTION"
BUILD_DATE = "2025-09-25"

# =============================================================================
# EMBEDDED SERVICE CODE - All services embedded in main.py to bypass inclusion issues
# =============================================================================

class BluetoothServiceMock:
    """Embedded Bluetooth service mock"""
    def __init__(self):
        self.is_enabled = False
        self.connected_devices = []
    
    def test_bluetooth(self):
        return "Bluetooth service mock working from embedded code!"
    
    def enable_bluetooth(self):
        self.is_enabled = True
        return {"status": "enabled", "method": "embedded_mock"}
    
    def scan_devices(self):
        return [{"name": "Device1", "mac": "00:11:22:33:44:55"}]

class WiFiHotspotServiceMock:
    """Embedded WiFi hotspot service mock"""
    def __init__(self):
        self.is_active = False
        self.ssid = "SynergyHotspot"
    
    def test_wifi(self):
        return "WiFi hotspot service mock working from embedded code!"
    
    def start_hotspot(self, ssid="SynergyHotspot", password="12345678"):
        self.is_active = True
        self.ssid = ssid
        return {"status": "started", "ssid": ssid, "method": "embedded_mock"}
    
    def stop_hotspot(self):
        self.is_active = False
        return {"status": "stopped", "method": "embedded_mock"}

class FileTransferServiceMock:
    """Embedded file transfer service mock"""
    def __init__(self):
        self.active_transfers = []
    
    def test_transfer(self):
        return "File transfer service mock working from embedded code!"
    
    def send_file(self, file_path, destination):
        transfer_id = len(self.active_transfers) + 1
        transfer = {
            "id": transfer_id,
            "file": file_path,
            "destination": destination,
            "status": "completed",
            "method": "embedded_mock"
        }
        self.active_transfers.append(transfer)
        return transfer

# Global service instances
bluetooth_service = BluetoothServiceMock()
wifi_service = WiFiHotspotServiceMock()
file_service = FileTransferServiceMock()

# =============================================================================
# MAIN APPLICATION
# =============================================================================

class SynergyClientApp(App):
    def build(self):
        # Create main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # VERSION HEADER - Large and prominent
        version_label = Label(
            text=f"SYNERGY CLIENT {APP_VERSION}\nBuild: {BUILD_DATE}",
            font_size=dp(18),
            size_hint_y=None,
            height=dp(80),
            color=(1, 0, 1, 1),  # Magenta color for v3.0
            bold=True,
            halign='center'
        )
        version_label.bind(size=version_label.setter('text_size'))
        
        # App title
        title_label = Label(
            text='Single-File Solution - All Code Embedded',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            bold=True
        )
        
        # Status display
        self.status_label = Label(
            text='Initializing embedded services...',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(40),
            color=(0.7, 0.7, 0.7, 1)
        )
        
        # Service status display
        self.service_status = Label(
            text='Service Status: Loading...',
            font_size=dp(12),
            size_hint_y=None,
            height=dp(120),
            color=(0.8, 0.8, 0.8, 1),
            halign='left'
        )
        self.service_status.bind(size=self.service_status.setter('text_size'))
        
        # Debug button for file listing
        debug_button = Button(
            text='Show Available Files (v3.0 Single-File)',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        debug_button.bind(on_press=self.show_available_files)
        
        # Service test buttons
        bluetooth_btn = Button(
            text='Test Embedded Bluetooth',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        bluetooth_btn.bind(on_press=self.test_bluetooth)
        
        wifi_btn = Button(
            text='Test Embedded WiFi',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        wifi_btn.bind(on_press=self.test_wifi)
        
        transfer_btn = Button(
            text='Test Embedded File Transfer',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        transfer_btn.bind(on_press=self.test_transfer)
        
        # Add all widgets to layout
        main_layout.add_widget(version_label)
        main_layout.add_widget(title_label)
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(self.service_status)
        main_layout.add_widget(debug_button)
        main_layout.add_widget(bluetooth_btn)
        main_layout.add_widget(wifi_btn)
        main_layout.add_widget(transfer_btn)
        
        # Initialize services on startup
        self.initialize_services()
        
        return main_layout
    
    def initialize_services(self):
        """Initialize embedded services"""
        status_lines = []
        status_lines.append(f"Version: {APP_VERSION}")
        status_lines.append(f"Build Date: {BUILD_DATE}")
        status_lines.append("")
        status_lines.append("🔧 EMBEDDED SERVICES APPROACH:")
        status_lines.append("All service code is embedded in main.py")
        status_lines.append("No separate .py files needed!")
        status_lines.append("")
        
        # Test embedded services
        services_working = 0
        
        try:
            result = bluetooth_service.test_bluetooth()
            status_lines.append(f"✅ Bluetooth: {result}")
            services_working += 1
        except Exception as e:
            status_lines.append(f"❌ Bluetooth failed: {e}")
        
        try:
            result = wifi_service.test_wifi()
            status_lines.append(f"✅ WiFi: {result}")
            services_working += 1
        except Exception as e:
            status_lines.append(f"❌ WiFi failed: {e}")
        
        try:
            result = file_service.test_transfer()
            status_lines.append(f"✅ File Transfer: {result}")
            services_working += 1
        except Exception as e:
            status_lines.append(f"❌ File Transfer failed: {e}")
        
        status_lines.append("")
        status_lines.append(f"Embedded services working: {services_working}/3")
        
        self.service_status.text = "\n".join(status_lines)
        
        if services_working == 3:
            self.status_label.text = "✅ All embedded services working!"
            self.status_label.color = (0, 1, 0, 1)  # Green
        else:
            self.status_label.text = f"⚠️ Only {services_working}/3 embedded services working"
            self.status_label.color = (1, 1, 0, 1)  # Yellow
    
    def show_available_files(self, instance):
        """Show what Python files are available in the APK"""
        try:
            # Get all .py files in current directory and subdirectories
            py_files = []
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.endswith('.py'):
                        py_files.append(os.path.join(root, file))
            
            py_files.sort()
            
            files_text = f"=== v3.0 SINGLE-FILE APPROACH ===\n"
            
            if py_files:
                files_text += f"Found {len(py_files)} .py files:\n" + "\n".join(py_files[:15])
                if len(py_files) > 15:
                    files_text += f"\n... and {len(py_files) - 15} more"
            else:
                files_text += "No .py files found in APK"
            
            files_text += f"\n\n🔧 EMBEDDED SERVICES STATUS:"
            files_text += f"\n✅ BluetoothServiceMock: embedded in main.py"
            files_text += f"\n✅ WiFiHotspotServiceMock: embedded in main.py"
            files_text += f"\n✅ FileTransferServiceMock: embedded in main.py"
            files_text += f"\n\nNo separate service files needed!"
            
            print(f"=== v3.0 SINGLE-FILE LISTING ===")
            print(files_text)
            print("=" * 35)
            
            self.service_status.text = files_text
            
        except Exception as e:
            error_text = f"Error listing files: {e}"
            print(f"=== v3.0 ERROR ===")
            print(error_text)
            print("=" * 20)
            self.service_status.text = error_text
    
    def test_bluetooth(self, instance):
        """Test embedded Bluetooth service"""
        try:
            result = bluetooth_service.test_bluetooth()
            enable_result = bluetooth_service.enable_bluetooth()
            self.status_label.text = f"✅ Bluetooth: {result} | Status: {enable_result['status']}"
            self.status_label.color = (0, 1, 0, 1)
        except Exception as e:
            self.status_label.text = f"❌ Bluetooth test failed: {e}"
            self.status_label.color = (1, 0, 0, 1)
    
    def test_wifi(self, instance):
        """Test embedded WiFi service"""
        try:
            result = wifi_service.test_wifi()
            hotspot_result = wifi_service.start_hotspot()
            self.status_label.text = f"✅ WiFi: {result} | Hotspot: {hotspot_result['status']}"
            self.status_label.color = (0, 1, 0, 1)
        except Exception as e:
            self.status_label.text = f"❌ WiFi test failed: {e}"
            self.status_label.color = (1, 0, 0, 1)
    
    def test_transfer(self, instance):
        """Test embedded file transfer service"""
        try:
            result = file_service.test_transfer()
            transfer_result = file_service.send_file("test.txt", "device1")
            self.status_label.text = f"✅ Transfer: {result} | ID: {transfer_result['id']}"
            self.status_label.color = (0, 1, 0, 1)
        except Exception as e:
            self.status_label.text = f"❌ Transfer test failed: {e}"
            self.status_label.color = (1, 0, 0, 1)

if __name__ == '__main__':
    SynergyClientApp().run()