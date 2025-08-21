"""
Main Android application for Synergy Client.
Kivy/KivyMD application with Material Design interface.
"""

import os
import sys
import logging
from threading import Thread
from typing import Optional

# Kivy imports
from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import StringProperty, BooleanProperty, NumericProperty

# KivyMD imports
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import OneLineListItem

# Service imports
from bluetooth_service import BluetoothService
from wifi_hotspot_service import WiFiHotspotService
from file_transfer_service import FileTransferService
from utils.protocol import ColorType, ActionType, MessageType
from utils.file_generator import PRESET_FILE_SIZES, FileGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MainScreen(MDScreen):
    """Main screen of the application."""
    
    # Properties for data binding
    bluetooth_status = StringProperty("Disconnected")
    wifi_status = StringProperty("Disabled")
    connection_info = StringProperty("")
    transfer_progress = NumericProperty(0)
    transfer_speed = StringProperty("0 Mbps")
    is_connected = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = None
    
    def set_app(self, app):
        """Set reference to main app."""
        self.app = app
    
    def on_bluetooth_connect(self):
        """Handle Bluetooth connection button press."""
        if self.app:
            self.app.show_device_selection_dialog()
    
    def on_bluetooth_disconnect(self):
        """Handle Bluetooth disconnection."""
        if self.app:
            self.app.disconnect_bluetooth()
    
    def on_wifi_toggle(self):
        """Handle WiFi hotspot toggle."""
        if self.app:
            self.app.toggle_wifi_hotspot()
    
    def on_color_button(self, color_name):
        """Handle color button press."""
        if self.app:
            self.app.send_color_command(color_name)
    
    def on_file_transfer_request(self, size_preset):
        """Handle file transfer request."""
        if self.app:
            self.app.request_file_transfer(size_preset)
    
    def update_status(self, bluetooth_status=None, wifi_status=None, 
                     connection_info=None, is_connected=None):
        """Update status displays."""
        if bluetooth_status is not None:
            self.bluetooth_status = bluetooth_status
        if wifi_status is not None:
            self.wifi_status = wifi_status
        if connection_info is not None:
            self.connection_info = connection_info
        if is_connected is not None:
            self.is_connected = is_connected
    
    def update_transfer_progress(self, progress, speed):
        """Update file transfer progress."""
        self.transfer_progress = progress
        self.transfer_speed = speed


class SynergyClientApp(MDApp):
    """Main application class."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Synergy Client"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Services
        self.bluetooth_service = BluetoothService()
        self.wifi_service = WiFiHotspotService()
        self.file_service = FileTransferService()
        
        # UI references
        self.main_screen = None
        self.device_dialog = None
        self.progress_dialog = None
        
        # State
        self.available_devices = []
        self.current_transfer = None
        
        # Setup service callbacks
        self._setup_service_callbacks()
    
    def build(self):
        """Build the application UI."""
        # Create screen manager
        sm = MDScreenManager()
        
        # Create main screen
        self.main_screen = MainScreen(name='main')
        self.main_screen.set_app(self)
        sm.add_widget(self.main_screen)
        
        # Schedule status updates
        Clock.schedule_interval(self._update_status, 1.0)
        
        return sm
    
    def on_start(self):
        """Called when the app starts."""
        logger.info("Synergy Client started")
        
        # Initialize services
        self._initialize_services()
        
        # Show welcome message
        Snackbar(text="Synergy Client started. Tap 'Connect' to begin.").open()
    
    def _initialize_services(self):
        """Initialize all services."""
        try:
            # Start Bluetooth server
            success = self.bluetooth_service.start_server("SynergyClient")
            if success:
                logger.info("Bluetooth server started successfully")
            else:
                logger.error("Failed to start Bluetooth server")
            
            # Set file service callbacks
            self.file_service.set_callbacks(
                progress_callback=self._on_transfer_progress,
                completion_callback=self._on_transfer_complete
            )
            
        except Exception as e:
            logger.error(f"Error initializing services: {str(e)}")
            self._show_error_dialog("Initialization Error", str(e))
    
    def _setup_service_callbacks(self):
        """Setup callbacks for service events."""
        # Bluetooth message callbacks
        self.bluetooth_service.set_message_callback(
            ActionType.WIFI_CONNECTION_STATUS, self._on_wifi_connection_status
        )
        self.bluetooth_service.set_message_callback(
            ActionType.FILE_TRANSFER_REQUEST, self._on_file_transfer_request
        )
        self.bluetooth_service.set_message_callback(
            ActionType.COLOR_CHANGE_ACK, self._on_color_change_ack
        )
    
    def show_device_selection_dialog(self):
        """Show dialog for Bluetooth device selection."""
        if not self.bluetooth_service.is_bluetooth_enabled():
            self._show_error_dialog("Bluetooth Error", "Bluetooth is not enabled")
            return
        
        # Scan for devices
        self.available_devices = self.bluetooth_service.scan_for_devices()
        
        if not self.available_devices:
            self._show_error_dialog("No Devices", "No paired Bluetooth devices found")
            return
        
        # Create device list items
        device_items = []
        for device in self.available_devices:
            item = OneLineListItem(
                text=f"{device['name']} ({device['address']})",
                on_release=lambda x, dev=device: self._connect_to_device(dev)
            )
            device_items.append(item)
        
        # Show dialog
        self.device_dialog = MDDialog(
            title="Select Bluetooth Device",
            type="simple",
            items=device_items,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.device_dialog.dismiss()
                )
            ]
        )
        self.device_dialog.open()
    
    def _connect_to_device(self, device):
        """Connect to selected Bluetooth device."""
        self.device_dialog.dismiss()
        
        # Show progress
        self._show_progress_dialog("Connecting", "Connecting to Bluetooth device...")
        
        # Connect in background thread
        def connect_thread():
            success = self.bluetooth_service.connect_to_device(device['address'])
            Clock.schedule_once(lambda dt: self._on_bluetooth_connection_result(success, device))
        
        Thread(target=connect_thread, daemon=True).start()
    
    def _on_bluetooth_connection_result(self, success, device):
        """Handle Bluetooth connection result."""
        self._dismiss_progress_dialog()
        
        if success:
            logger.info(f"Connected to {device['name']}")
            Snackbar(text=f"Connected to {device['name']}").open()
            
            # Start WiFi hotspot
            self._start_wifi_hotspot()
        else:
            logger.error(f"Failed to connect to {device['name']}")
            self._show_error_dialog("Connection Failed", f"Could not connect to {device['name']}")
    
    def _start_wifi_hotspot(self):
        """Start WiFi hotspot and send info to connected device."""
        def hotspot_thread():
            # Create hotspot
            result = self.wifi_service.create_hotspot()
            
            if result['success']:
                # Start file transfer server
                self.file_service.start_file_server()
                
                # Send hotspot info via Bluetooth
                self.bluetooth_service.send_wifi_info(
                    result['ssid'],
                    result['password'],
                    result['ip_address'],
                    8888  # Default file transfer port
                )
                
                Clock.schedule_once(lambda dt: self._on_hotspot_created(result))
            else:
                Clock.schedule_once(lambda dt: self._on_hotspot_error(result))
        
        Thread(target=hotspot_thread, daemon=True).start()
    
    def _on_hotspot_created(self, result):
        """Handle successful hotspot creation."""
        logger.info("WiFi hotspot created successfully")
        Snackbar(text=f"WiFi hotspot '{result['ssid']}' created").open()
    
    def _on_hotspot_error(self, result):
        """Handle hotspot creation error."""
        logger.error(f"Failed to create hotspot: {result.get('error', 'Unknown error')}")
        self._show_error_dialog("WiFi Error", result.get('message', 'Failed to create hotspot'))
    
    def disconnect_bluetooth(self):
        """Disconnect Bluetooth and stop services."""
        self.bluetooth_service.disconnect()
        self.wifi_service.stop_hotspot()
        self.file_service.stop_file_server()
        
        Snackbar(text="Disconnected").open()
    
    def toggle_wifi_hotspot(self):
        """Toggle WiFi hotspot on/off."""
        if self.wifi_service.is_hotspot_active():
            self.wifi_service.stop_hotspot()
            Snackbar(text="WiFi hotspot stopped").open()
        else:
            self._start_wifi_hotspot()
    
    def send_color_command(self, color_name):
        """Send color change command via Bluetooth."""
        if not self.bluetooth_service.is_connected():
            Snackbar(text="Not connected to any device").open()
            return
        
        # Convert color name to ColorType
        color_map = {
            'red': ColorType.RED,
            'yellow': ColorType.YELLOW,
            'green': ColorType.GREEN
        }
        
        color = color_map.get(color_name.lower())
        if color:
            success = self.bluetooth_service.send_color_command(color)
            if success:
                Snackbar(text=f"Sent {color_name.title()} command").open()
            else:
                Snackbar(text="Failed to send command").open()
    
    def request_file_transfer(self, size_preset):
        """Request file transfer with specified size."""
        if not self.bluetooth_service.is_connected():
            Snackbar(text="Not connected to any device").open()
            return
        
        size_mb = PRESET_FILE_SIZES.get(size_preset, 25)
        
        # Send file transfer request
        success = self.bluetooth_service.send_file_transfer_request(
            size_mb * 1024 * 1024,  # Convert to bytes
            f"test_file_{size_mb}MB.bin",
            "android_to_windows"
        )
        
        if success:
            Snackbar(text=f"Requesting {size_mb}MB file transfer...").open()
        else:
            Snackbar(text="Failed to send transfer request").open()
    
    def _on_wifi_connection_status(self, message):
        """Handle WiFi connection status message."""
        data = message.data
        if data.get('connected'):
            logger.info("Windows device connected to WiFi hotspot")
            Clock.schedule_once(
                lambda dt: Snackbar(text="Windows device connected to WiFi").open()
            )
    
    def _on_file_transfer_request(self, message):
        """Handle incoming file transfer request."""
        data = message.data
        file_size_mb = data.get('file_size', 0) / (1024 * 1024)
        
        # Auto-accept transfer requests
        self.bluetooth_service.send_file_transfer_response(True, 8888)
        
        Clock.schedule_once(
            lambda dt: Snackbar(text=f"Receiving {file_size_mb:.1f}MB file...").open()
        )
    
    def _on_color_change_ack(self, message):
        """Handle color change acknowledgment."""
        data = message.data
        if data.get('success'):
            color = data.get('current_color', 'Unknown')
            Clock.schedule_once(
                lambda dt: Snackbar(text=f"Color changed to {color}").open()
            )
    
    def _on_transfer_progress(self, progress_info):
        """Handle file transfer progress updates."""
        percentage = progress_info.get('percentage', 0)
        speed = progress_info.get('speed_mbps', 0)
        
        Clock.schedule_once(
            lambda dt: self.main_screen.update_transfer_progress(
                percentage, f"{speed:.1f} Mbps"
            )
        )
    
    def _on_transfer_complete(self, result):
        """Handle file transfer completion."""
        if result.get('transfer_complete'):
            speed = result.get('average_speed_mbps', 0)
            time_ms = result.get('transfer_time_ms', 0)
            
            Clock.schedule_once(
                lambda dt: Snackbar(
                    text=f"Transfer complete! {speed:.1f} Mbps in {time_ms/1000:.1f}s"
                ).open()
            )
        else:
            error = result.get('error', 'Unknown error')
            Clock.schedule_once(
                lambda dt: self._show_error_dialog("Transfer Failed", error)
            )
    
    def _update_status(self, dt):
        """Update UI status information."""
        if not self.main_screen:
            return
        
        # Get connection states
        bt_state = self.bluetooth_service.get_connection_state()
        wifi_state = self.wifi_service.get_connection_state()
        
        # Update Bluetooth status
        bt_status = bt_state.get('bluetooth_state', 'disconnected').title()
        device_info = bt_state.get('connected_device')
        
        if device_info:
            connection_info = f"Connected to {device_info['name']}"
        else:
            connection_info = "No device connected"
        
        # Update WiFi status
        wifi_status = wifi_state.get('wifi_state', 'disabled').title()
        if self.wifi_service.is_hotspot_active():
            wifi_status = f"Hotspot Active"
        
        # Update UI
        self.main_screen.update_status(
            bluetooth_status=bt_status,
            wifi_status=wifi_status,
            connection_info=connection_info,
            is_connected=self.bluetooth_service.is_connected()
        )
    
    def _show_progress_dialog(self, title, text):
        """Show progress dialog."""
        self.progress_dialog = MDDialog(
            title=title,
            text=text,
            type="custom"
        )
        self.progress_dialog.open()
    
    def _dismiss_progress_dialog(self):
        """Dismiss progress dialog."""
        if self.progress_dialog:
            self.progress_dialog.dismiss()
            self.progress_dialog = None
    
    def _show_error_dialog(self, title, message):
        """Show error dialog."""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def on_stop(self):
        """Called when the app stops."""
        logger.info("Synergy Client stopping")
        
        # Cleanup services
        self.bluetooth_service.cleanup()
        self.wifi_service.cleanup()
        self.file_service.cleanup()


# Main entry point
if __name__ == '__main__':
    try:
        app = SynergyClientApp()
        app.run()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)
