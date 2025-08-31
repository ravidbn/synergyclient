"""
Mock WiFi Hotspot Service for initial testing.
Provides basic interface without Android-specific functionality.
"""

import logging
from utils.protocol import ConnectionState

logger = logging.getLogger(__name__)


class WiFiHotspotService:
    """Mock WiFi hotspot service for testing purposes."""
    
    def __init__(self):
        self.hotspot_active = False
        self.hotspot_ssid = "SynergyHotspot"
        self.hotspot_password = "synergy123"
        self.hotspot_ip = "192.168.43.1"
        self.connection_state = ConnectionState()
        
        logger.info("Mock WiFi hotspot service initialized")
        self.connection_state.update_wifi_state("disabled")
    
    def create_hotspot(self, ssid: str = None, password: str = None) -> dict:
        """Mock hotspot creation."""
        logger.info("Mock: Creating WiFi hotspot")
        
        if ssid:
            self.hotspot_ssid = ssid
        if password:
            self.hotspot_password = password
        
        self.hotspot_active = True
        self.connection_state.update_wifi_state("hotspot_active")
        
        return {
            'success': True,
            'ssid': self.hotspot_ssid,
            'password': self.hotspot_password,
            'ip_address': self.hotspot_ip,
            'security_type': 'WPA2',
            'message': 'Mock hotspot created successfully'
        }
    
    def stop_hotspot(self) -> dict:
        """Mock hotspot stop."""
        logger.info("Mock: Stopping WiFi hotspot")
        
        self.hotspot_active = False
        self.connection_state.update_wifi_state("disabled")
        
        return {
            'success': True,
            'message': 'Mock hotspot stopped successfully'
        }
    
    def get_hotspot_status(self) -> dict:
        """Mock hotspot status."""
        return {
            'active': self.hotspot_active,
            'ssid': self.hotspot_ssid if self.hotspot_active else None,
            'ip_address': self.hotspot_ip if self.hotspot_active else None,
            'connected_devices': 0,
            'connection_state': self.connection_state.to_dict()
        }
    
    def is_hotspot_active(self) -> bool:
        """Check if hotspot is active."""
        return self.hotspot_active
    
    def get_connection_state(self) -> dict:
        """Get connection state."""
        return self.connection_state.to_dict()
    
    def cleanup(self):
        """Mock cleanup."""
        logger.info("Mock: WiFi hotspot cleanup")
        if self.hotspot_active:
            self.stop_hotspot()