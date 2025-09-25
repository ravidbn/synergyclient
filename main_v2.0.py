import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp

# VERSION DISPLAY
APP_VERSION = "v2.0 - SOURCE FIX ATTEMPT"
BUILD_DATE = "2025-09-25"

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
            color=(1, 1, 0, 1),  # Yellow color for visibility
            bold=True,
            halign='center'
        )
        version_label.bind(size=version_label.setter('text_size'))
        
        # App title
        title_label = Label(
            text='Synergy Client - File Transfer System',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(50),
            bold=True
        )
        
        # Status display
        self.status_label = Label(
            text='Initializing services...',
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
            height=dp(100),
            color=(0.8, 0.8, 0.8, 1),
            halign='left'
        )
        self.service_status.bind(size=self.service_status.setter('text_size'))
        
        # Debug button for file listing
        debug_button = Button(
            text='Show Available Files (v2.0 Debug)',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        debug_button.bind(on_press=self.show_available_files)
        
        # Service test buttons
        bluetooth_btn = Button(
            text='Test Bluetooth Service',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        bluetooth_btn.bind(on_press=self.test_bluetooth)
        
        wifi_btn = Button(
            text='Test WiFi Service',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(14)
        )
        wifi_btn.bind(on_press=self.test_wifi)
        
        # Add all widgets to layout
        main_layout.add_widget(version_label)
        main_layout.add_widget(title_label)
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(self.service_status)
        main_layout.add_widget(debug_button)
        main_layout.add_widget(bluetooth_btn)
        main_layout.add_widget(wifi_btn)
        
        # Initialize services on startup
        self.initialize_services()
        
        return main_layout
    
    def initialize_services(self):
        """Initialize services and update status"""
        status_lines = []
        status_lines.append(f"Version: {APP_VERSION}")
        status_lines.append(f"Build Date: {BUILD_DATE}")
        status_lines.append("")
        
        # Try to import services
        services_imported = 0
        
        try:
            import bluetooth_service_mock
            status_lines.append("✅ bluetooth_service_mock imported successfully")
            services_imported += 1
        except ImportError as e:
            status_lines.append(f"❌ bluetooth_service_mock import failed: {e}")
        
        try:
            import wifi_hotspot_service_mock
            status_lines.append("✅ wifi_hotspot_service_mock imported successfully")
            services_imported += 1
        except ImportError as e:
            status_lines.append(f"❌ wifi_hotspot_service_mock import failed: {e}")
        
        try:
            import file_transfer_service_mock
            status_lines.append("✅ file_transfer_service_mock imported successfully")
            services_imported += 1
        except ImportError as e:
            status_lines.append(f"❌ file_transfer_service_mock import failed: {e}")
        
        status_lines.append("")
        status_lines.append(f"Services imported: {services_imported}/3")
        
        self.service_status.text = "\n".join(status_lines)
        
        if services_imported == 3:
            self.status_label.text = "✅ All services loaded successfully!"
            self.status_label.color = (0, 1, 0, 1)  # Green
        else:
            self.status_label.text = f"⚠️ Only {services_imported}/3 services loaded"
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
            
            if py_files:
                files_text = f"Found {len(py_files)} .py files:\n" + "\n".join(py_files[:20])
                if len(py_files) > 20:
                    files_text += f"\n... and {len(py_files) - 20} more"
            else:
                files_text = "No .py files found in APK"
            
            print(f"=== v2.0 FILE LISTING ===")
            print(files_text)
            print("=" * 30)
            
            self.service_status.text = files_text
            
        except Exception as e:
            error_text = f"Error listing files: {e}"
            print(f"=== v2.0 ERROR ===")
            print(error_text)
            print("=" * 20)
            self.service_status.text = error_text
    
    def test_bluetooth(self, instance):
        """Test Bluetooth service"""
        try:
            import bluetooth_service_mock
            result = bluetooth_service_mock.test_bluetooth()
            self.status_label.text = f"✅ Bluetooth test: {result}"
            self.status_label.color = (0, 1, 0, 1)
        except Exception as e:
            self.status_label.text = f"❌ Bluetooth test failed: {e}"
            self.status_label.color = (1, 0, 0, 1)
    
    def test_wifi(self, instance):
        """Test WiFi service"""
        try:
            import wifi_hotspot_service_mock
            result = wifi_hotspot_service_mock.test_wifi()
            self.status_label.text = f"✅ WiFi test: {result}"
            self.status_label.color = (0, 1, 0, 1)
        except Exception as e:
            self.status_label.text = f"❌ WiFi test failed: {e}"
            self.status_label.color = (1, 0, 0, 1)

if __name__ == '__main__':
    SynergyClientApp().run()