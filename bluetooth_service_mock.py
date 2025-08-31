"""
Mock Bluetooth Service for initial testing.
Provides basic interface without Android-specific functionality.
"""

import logging
from typing import Callable, Optional, Dict, Any, List
from utils.protocol import ConnectionState, ColorType

logger = logging.getLogger(__name__)


class BluetoothService:
    """Mock Bluetooth service for testing purposes."""
    
    def __init__(self):
        self.connection_state = ConnectionState()
        self.connected_device = None
        self.message_callbacks = {}
        self.is_server = False
        
        logger.info("Mock Bluetooth service initialized")
        self.connection_state.update_bluetooth_state("disconnected")
    
    def set_message_callback(self, action, callback: Callable):
        """Set callback function for specific message actions."""
        self.message_callbacks[action] = callback
    
    def start_server(self, service_name: str = "SynergyServer") -> bool:
        """Mock server start."""
        logger.info(f"Mock: Starting Bluetooth server: {service_name}")
        self.is_server = True
        return True
    
    def connect_to_device(self, device_address: str) -> bool:
        """Mock device connection."""
        logger.info(f"Mock: Connecting to device: {device_address}")
        self.connection_state.update_bluetooth_state("connected")
        self.connected_device = {"name": "Mock Device", "address": device_address}
        return True
    
    def send_color_command(self, color: ColorType) -> bool:
        """Mock color command."""
        logger.info(f"Mock: Sending color command: {color}")
        return True
    
    def send_wifi_info(self, ssid: str, password: str, ip_address: str, port: int) -> bool:
        """Mock WiFi info send."""
        logger.info(f"Mock: Sending WiFi info: {ssid}")
        return True
    
    def send_file_transfer_request(self, file_size: int, file_name: str, direction: str) -> bool:
        """Mock file transfer request."""
        logger.info(f"Mock: File transfer request: {file_name}")
        return True
    
    def send_file_transfer_response(self, accepted: bool, tcp_port: int, error_message: str = None) -> bool:
        """Mock file transfer response."""
        logger.info(f"Mock: File transfer response: {accepted}")
        return True
    
    def scan_for_devices(self, timeout: int = 10) -> List[Dict[str, Any]]:
        """Mock device scan."""
        logger.info("Mock: Scanning for devices")
        return [
            {"name": "Mock Device 1", "address": "00:11:22:33:44:55", "bonded": True},
            {"name": "Mock Device 2", "address": "AA:BB:CC:DD:EE:FF", "bonded": True}
        ]
    
    def is_connected(self) -> bool:
        """Check if connected."""
        return self.connection_state.bluetooth_state == "connected"
    
    def get_connected_device_info(self) -> Optional[Dict[str, str]]:
        """Get connected device info."""
        return self.connected_device
    
    def disconnect(self):
        """Mock disconnect."""
        logger.info("Mock: Disconnecting Bluetooth")
        self.connection_state.update_bluetooth_state("disconnected")
        self.connected_device = None
    
    def get_connection_state(self) -> Dict[str, Any]:
        """Get connection state."""
        return {
            **self.connection_state.to_dict(),
            'is_server': self.is_server,
            'connected_device': self.get_connected_device_info(),
            'message_queue_size': 0,
            'outgoing_queue_size': 0
        }
    
    def is_bluetooth_enabled(self) -> bool:
        """Mock Bluetooth enabled check."""
        return True
    
    def enable_bluetooth(self) -> bool:
        """Mock Bluetooth enable."""
        return True
    
    def cleanup(self):
        """Mock cleanup."""
        logger.info("Mock: Bluetooth cleanup")
        self.disconnect()