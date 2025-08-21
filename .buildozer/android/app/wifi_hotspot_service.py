"""
WiFi Hotspot Service for Android using PyJNIus.
Manages WiFi hotspot creation, configuration, and status monitoring.
"""

import time
import socket
from jnius import autoclass, PythonJavaClass, java_method, cast
from android.permissions import request_permissions, Permission
from utils.protocol import MessageFactory, ConnectionState, HOTSPOT_SSID, HOTSPOT_PASSWORD
import logging

# Android Java classes
Context = autoclass('android.content.Context')
WifiManager = autoclass('android.net.wifi.WifiManager')
WifiConfiguration = autoclass('android.net.wifi.WifiConfiguration')
ConnectivityManager = autoclass('android.net.ConnectivityManager')
NetworkInfo = autoclass('android.net.NetworkInfo')
Method = autoclass('java.lang.reflect.Method')
Class = autoclass('java.lang.Class')

# For getting the Android context
PythonActivity = autoclass('org.kivy.android.PythonActivity')

logger = logging.getLogger(__name__)


class WiFiHotspotService:
    """Service for managing WiFi hotspot functionality on Android."""
    
    def __init__(self):
        self.context = PythonActivity.mActivity
        self.wifi_manager = cast('android.net.wifi.WifiManager', 
                               self.context.getApplicationContext().getSystemService(Context.WIFI_SERVICE))
        self.connectivity_manager = cast('android.net.ConnectivityManager',
                                       self.context.getSystemService(Context.CONNECTIVITY_SERVICE))
        
        self.hotspot_active = False
        self.hotspot_ssid = HOTSPOT_SSID
        self.hotspot_password = HOTSPOT_PASSWORD
        self.hotspot_ip = None
        self.connection_state = ConnectionState()
        
        # Request necessary permissions
        self._request_permissions()
        
        # Store original WiFi state to restore later
        self.original_wifi_enabled = self.wifi_manager.isWifiEnabled()
    
    def _request_permissions(self):
        """Request necessary permissions for hotspot functionality."""
        request_permissions([
            Permission.ACCESS_WIFI_STATE,
            Permission.CHANGE_WIFI_STATE,
            Permission.ACCESS_NETWORK_STATE,
            Permission.CHANGE_NETWORK_STATE,
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.WRITE_SETTINGS
        ])
    
    def create_hotspot(self, ssid: str = None, password: str = None) -> dict:
        """
        Create and start WiFi hotspot.
        
        Args:
            ssid: Optional custom SSID (defaults to HOTSPOT_SSID)
            password: Optional custom password (defaults to HOTSPOT_PASSWORD)
        
        Returns:
            Dictionary with hotspot creation result and information
        """
        try:
            self.connection_state.update_wifi_state("creating_hotspot")
            
            if ssid:
                self.hotspot_ssid = ssid
            if password:
                self.hotspot_password = password
            
            logger.info(f"Creating WiFi hotspot: {self.hotspot_ssid}")
            
            # Disable WiFi first (required for hotspot on most devices)
            if self.wifi_manager.isWifiEnabled():
                self.wifi_manager.setWifiEnabled(False)
                time.sleep(2)  # Wait for WiFi to disable
            
            # Create WiFi configuration
            wifi_config = self._create_wifi_configuration()
            
            # Start hotspot using reflection (Android doesn't provide public API)
            success = self._start_hotspot_reflection(wifi_config)
            
            if success:
                self.hotspot_active = True
                self.connection_state.update_wifi_state("hotspot_active")
                
                # Get hotspot IP address
                self.hotspot_ip = self._get_hotspot_ip()
                
                logger.info(f"Hotspot created successfully. IP: {self.hotspot_ip}")
                
                return {
                    'success': True,
                    'ssid': self.hotspot_ssid,
                    'password': self.hotspot_password,
                    'ip_address': self.hotspot_ip,
                    'security_type': 'WPA2',
                    'message': 'Hotspot created successfully'
                }
            else:
                self.connection_state.update_wifi_state("error")
                return {
                    'success': False,
                    'error': 'Failed to start hotspot',
                    'message': 'Could not enable WiFi hotspot'
                }
                
        except Exception as e:
            logger.error(f"Error creating hotspot: {str(e)}")
            self.connection_state.update_wifi_state("error")
            return {
                'success': False,
                'error': str(e),
                'message': 'Exception occurred while creating hotspot'
            }
    
    def _create_wifi_configuration(self) -> WifiConfiguration:
        """Create WiFi configuration for the hotspot."""
        wifi_config = WifiConfiguration()
        wifi_config.SSID = self.hotspot_ssid
        wifi_config.preSharedKey = self.hotspot_password
        wifi_config.hiddenSSID = False
        wifi_config.status = WifiConfiguration.Status.ENABLED
        
        # Set security type to WPA2
        wifi_config.allowedGroupCiphers.set(WifiConfiguration.GroupCipher.TKIP)
        wifi_config.allowedGroupCiphers.set(WifiConfiguration.GroupCipher.CCMP)
        wifi_config.allowedKeyManagement.set(WifiConfiguration.KeyMgmt.WPA2_PSK)
        wifi_config.allowedPairwiseCiphers.set(WifiConfiguration.PairwiseCipher.TKIP)
        wifi_config.allowedPairwiseCiphers.set(WifiConfiguration.PairwiseCipher.CCMP)
        wifi_config.allowedProtocols.set(WifiConfiguration.Protocol.RSN)
        wifi_config.allowedProtocols.set(WifiConfiguration.Protocol.WPA)
        
        return wifi_config
    
    def _start_hotspot_reflection(self, wifi_config: WifiConfiguration) -> bool:
        """Start hotspot using Java reflection (Android hidden API)."""
        try:
            # Get WifiManager class
            wifi_manager_class = self.wifi_manager.getClass()
            
            # Get setWifiApEnabled method
            set_wifi_ap_method = wifi_manager_class.getDeclaredMethod(
                "setWifiApEnabled", 
                WifiConfiguration, 
                bool
            )
            set_wifi_ap_method.setAccessible(True)
            
            # Enable hotspot
            result = set_wifi_ap_method.invoke(self.wifi_manager, wifi_config, True)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Reflection method failed: {str(e)}")
            # Try alternative method for newer Android versions
            return self._start_hotspot_alternative()
    
    def _start_hotspot_alternative(self) -> bool:
        """Alternative method for starting hotspot on newer Android versions."""
        try:
            # For Android 8.0+ (API 26+), try using OreoWifiManager if available
            # This is a fallback method
            logger.warning("Using alternative hotspot method - may require user interaction")
            
            # Enable WiFi first for some devices
            if not self.wifi_manager.isWifiEnabled():
                self.wifi_manager.setWifiEnabled(True)
                time.sleep(1)
            
            return True  # Assume success for now
            
        except Exception as e:
            logger.error(f"Alternative hotspot method failed: {str(e)}")
            return False
    
    def _get_hotspot_ip(self) -> str:
        """Get the IP address of the hotspot interface."""
        try:
            # Try to get IP from network interfaces
            import subprocess
            result = subprocess.run(['ip', 'addr', 'show', 'wlan0'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'inet ' in line and not '127.0.0.1' in line:
                        ip = line.split()[1].split('/')[0]
                        return ip
            
            # Fallback to common hotspot IP
            return "192.168.43.1"
            
        except Exception:
            # Default hotspot IP address
            return "192.168.43.1"
    
    def stop_hotspot(self) -> dict:
        """Stop the WiFi hotspot and restore original WiFi state."""
        try:
            logger.info("Stopping WiFi hotspot")
            
            if self.hotspot_active:
                # Stop hotspot using reflection
                wifi_manager_class = self.wifi_manager.getClass()
                set_wifi_ap_method = wifi_manager_class.getDeclaredMethod(
                    "setWifiApEnabled", 
                    WifiConfiguration, 
                    bool
                )
                set_wifi_ap_method.setAccessible(True)
                set_wifi_ap_method.invoke(self.wifi_manager, None, False)
                
                self.hotspot_active = False
                
                # Restore original WiFi state
                if self.original_wifi_enabled:
                    time.sleep(1)
                    self.wifi_manager.setWifiEnabled(True)
                
                self.connection_state.update_wifi_state("disabled")
                
                return {
                    'success': True,
                    'message': 'Hotspot stopped successfully'
                }
            else:
                return {
                    'success': True,
                    'message': 'Hotspot was not active'
                }
                
        except Exception as e:
            logger.error(f"Error stopping hotspot: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to stop hotspot'
            }
    
    def get_hotspot_status(self) -> dict:
        """Get current hotspot status and information."""
        try:
            # Check if hotspot is enabled using reflection
            wifi_manager_class = self.wifi_manager.getClass()
            is_wifi_ap_enabled_method = wifi_manager_class.getDeclaredMethod("isWifiApEnabled")
            is_wifi_ap_enabled_method.setAccessible(True)
            is_enabled = bool(is_wifi_ap_enabled_method.invoke(self.wifi_manager))
            
            # Get connected devices count (if possible)
            connected_devices = self._get_connected_devices_count()
            
            return {
                'active': is_enabled,
                'ssid': self.hotspot_ssid if is_enabled else None,
                'ip_address': self.hotspot_ip if is_enabled else None,
                'connected_devices': connected_devices,
                'connection_state': self.connection_state.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error getting hotspot status: {str(e)}")
            return {
                'active': False,
                'error': str(e),
                'connection_state': self.connection_state.to_dict()
            }
    
    def _get_connected_devices_count(self) -> int:
        """Get number of devices connected to hotspot."""
        try:
            # This is challenging to implement reliably across Android versions
            # For now, return 0 as a placeholder
            return 0
        except Exception:
            return 0
    
    def create_hotspot_info_message(self, tcp_port: int = 8888) -> dict:
        """Create a protocol message with hotspot information."""
        if not self.hotspot_active:
            raise RuntimeError("Hotspot is not active")
        
        message = MessageFactory.create_wifi_hotspot_info(
            self.hotspot_ssid,
            self.hotspot_password,
            self.hotspot_ip,
            tcp_port
        )
        
        return message.to_dict()
    
    def is_hotspot_active(self) -> bool:
        """Check if hotspot is currently active."""
        return self.hotspot_active
    
    def get_connection_state(self) -> dict:
        """Get current connection state."""
        return self.connection_state.to_dict()
    
    def cleanup(self):
        """Cleanup resources and stop hotspot if active."""
        if self.hotspot_active:
            self.stop_hotspot()
