"""
Enhanced Bluetooth Service for Android using PyJNIus.
Handles Bluetooth Classic (RFCOMM) connections, protocol messages, and device management.
"""

import threading
import time
import json
import queue
from typing import Callable, Optional, Dict, Any, List
from jnius import autoclass, PythonJavaClass, java_method, cast
from android.permissions import request_permissions, Permission
from utils.protocol import (
    ProtocolMessage, MessageFactory, MessageType, ActionType, 
    ColorType, ConnectionState, validate_message
)
import logging

# Android Java classes
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
BluetoothServerSocket = autoclass('android.bluetooth.BluetoothServerSocket')
UUID = autoclass('java.util.UUID')
InputStream = autoclass('java.io.InputStream')
OutputStream = autoclass('java.io.OutputStream')

logger = logging.getLogger(__name__)


class BluetoothService:
    """Enhanced Bluetooth service supporting RFCOMM connections and protocol messaging."""
    
    # Standard UUID for SPP (Serial Port Profile)
    SPP_UUID = "00001101-0000-1000-8000-00805F9B34FB"
    
    def __init__(self):
        self.adapter = BluetoothAdapter.getDefaultAdapter()
        self.server_socket = None
        self.client_socket = None
        self.connected_device = None
        self.connection_state = ConnectionState()
        
        # Threading
        self.server_thread = None
        self.client_thread = None
        self.message_listener_thread = None
        
        # Message handling
        self.message_queue = queue.Queue()
        self.outgoing_queue = queue.Queue()
        self.message_callbacks = {}
        self.is_server = False
        self.is_running = False
        
        # Request Bluetooth permissions
        self._request_permissions()
        
        # Initialize connection state
        self.connection_state.update_bluetooth_state("disconnected")
    
    def _request_permissions(self):
        """Request necessary Bluetooth permissions."""
        request_permissions([
            Permission.BLUETOOTH,
            Permission.BLUETOOTH_ADMIN,
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION
        ])
    
    def set_message_callback(self, action: ActionType, callback: Callable):
        """Set callback function for specific message actions."""
        self.message_callbacks[action.value] = callback
    
    def start_server(self, service_name: str = "SynergyServer") -> bool:
        """Start Bluetooth server to accept incoming connections."""
        try:
            if not self.adapter or not self.adapter.isEnabled():
                logger.error("Bluetooth adapter not available or not enabled")
                return False
            
            self.is_server = True
            self.connection_state.update_bluetooth_state("connecting")
            
            # Create server socket
            uuid_obj = UUID.fromString(self.SPP_UUID)
            self.server_socket = self.adapter.listenUsingRfcommWithServiceRecord(
                service_name, uuid_obj
            )
            
            logger.info(f"Bluetooth server started: {service_name}")
            
            # Start server thread
            self.server_thread = threading.Thread(target=self._server_listen_loop)
            self.server_thread.daemon = True
            self.is_running = True
            self.server_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start Bluetooth server: {str(e)}")
            self.connection_state.update_bluetooth_state("error")
            return False
    
    def _server_listen_loop(self):
        """Server loop to accept incoming connections."""
        while self.is_running and self.server_socket:
            try:
                logger.info("Waiting for Bluetooth client connection...")
                client_socket = self.server_socket.accept()
                
                if client_socket:
                    logger.info("Client connected to Bluetooth server")
                    self.client_socket = client_socket
                    self.connected_device = client_socket.getRemoteDevice()
                    self.connection_state.update_bluetooth_state("connected")
                    
                    # Start message handling
                    self._start_message_handling()
                    
                    # Wait for disconnection
                    self._handle_connection()
                
            except Exception as e:
                if self.is_running:
                    logger.error(f"Error in server listen loop: {str(e)}")
                break
    
    def connect_to_device(self, device_address: str) -> bool:
        """Connect to a specific Bluetooth device as client."""
        try:
            if not self.adapter or not self.adapter.isEnabled():
                logger.error("Bluetooth adapter not available or not enabled")
                return False
            
            self.is_server = False
            self.connection_state.update_bluetooth_state("connecting")
            
            # Get device by address
            device = self.adapter.getRemoteDevice(device_address)
            if not device:
                logger.error(f"Device not found: {device_address}")
                return False
            
            # Create client socket
            uuid_obj = UUID.fromString(self.SPP_UUID)
            self.client_socket = device.createRfcommSocketToServiceRecord(uuid_obj)
            
            # Connect
            self.client_socket.connect()
            self.connected_device = device
            self.connection_state.update_bluetooth_state("connected")
            
            logger.info(f"Connected to device: {device.getName()} ({device_address})")
            
            # Start message handling
            self._start_message_handling()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to device: {str(e)}")
            self.connection_state.update_bluetooth_state("error")
            return False
    
    def _start_message_handling(self):
        """Start threads for message sending and receiving."""
        self.is_running = True
        
        # Start message listener thread
        self.message_listener_thread = threading.Thread(target=self._message_listener_loop)
        self.message_listener_thread.daemon = True
        self.message_listener_thread.start()
        
        # Start message sender thread
        self.client_thread = threading.Thread(target=self._message_sender_loop)
        self.client_thread.daemon = True
        self.client_thread.start()
    
    def _message_listener_loop(self):
        """Listen for incoming messages."""
        if not self.client_socket:
            return
        
        try:
            input_stream = self.client_socket.getInputStream()
            
            while self.is_running and self.client_socket:
                try:
                    # Read message length first (4 bytes)
                    length_bytes = bytearray(4)
                    bytes_read = 0
                    while bytes_read < 4:
                        b = input_stream.read()
                        if b == -1:
                            raise Exception("Connection closed")
                        length_bytes[bytes_read] = b
                        bytes_read += 1
                    
                    message_length = int.from_bytes(length_bytes, byteorder='big')
                    
                    # Read the actual message
                    message_bytes = bytearray(message_length)
                    bytes_read = 0
                    while bytes_read < message_length:
                        b = input_stream.read()
                        if b == -1:
                            raise Exception("Connection closed")
                        message_bytes[bytes_read] = b
                        bytes_read += 1
                    
                    # Decode and process message
                    message_str = message_bytes.decode('utf-8')
                    self._process_received_message(message_str)
                    
                except Exception as e:
                    if self.is_running:
                        logger.error(f"Error reading message: {str(e)}")
                    break
                    
        except Exception as e:
            logger.error(f"Error in message listener: {str(e)}")
        finally:
            self._handle_disconnection()
    
    def _message_sender_loop(self):
        """Send queued outgoing messages."""
        if not self.client_socket:
            return
        
        try:
            output_stream = self.client_socket.getOutputStream()
            
            while self.is_running and self.client_socket:
                try:
                    # Get message from queue (blocking with timeout)
                    message = self.outgoing_queue.get(timeout=1.0)
                    
                    # Convert message to bytes
                    if isinstance(message, ProtocolMessage):
                        message_str = message.to_json()
                    else:
                        message_str = json.dumps(message)
                    
                    message_bytes = message_str.encode('utf-8')
                    
                    # Send message length first (4 bytes)
                    length_bytes = len(message_bytes).to_bytes(4, byteorder='big')
                    for byte_val in length_bytes:
                        output_stream.write(byte_val)
                    
                    # Send the actual message
                    for byte_val in message_bytes:
                        output_stream.write(byte_val)
                    
                    output_stream.flush()
                    
                    logger.debug(f"Sent message: {message_str[:100]}...")
                    
                except queue.Empty:
                    continue
                except Exception as e:
                    if self.is_running:
                        logger.error(f"Error sending message: {str(e)}")
                    break
                    
        except Exception as e:
            logger.error(f"Error in message sender: {str(e)}")
    
    def _process_received_message(self, message_str: str):
        """Process received message and trigger callbacks."""
        try:
            message_dict = json.loads(message_str)
            
            # Validate message format
            if not validate_message(message_dict):
                logger.error("Invalid message format received")
                return
            
            logger.info(f"Received message: {message_dict['action']}")
            
            # Create protocol message object
            message = ProtocolMessage.from_json(message_str)
            
            # Add to message queue for processing
            self.message_queue.put(message)
            
            # Trigger callback if registered
            action = message_dict.get('action')
            if action in self.message_callbacks:
                callback = self.message_callbacks[action]
                callback(message)
            
        except Exception as e:
            logger.error(f"Error processing received message: {str(e)}")
    
    def send_message(self, message: ProtocolMessage) -> bool:
        """Send a protocol message."""
        if not self.is_connected():
            logger.error("Cannot send message: not connected")
            return False
        
        try:
            self.outgoing_queue.put(message)
            return True
        except Exception as e:
            logger.error(f"Error queuing message: {str(e)}")
            return False
    
    def send_color_command(self, color: ColorType) -> bool:
        """Send a color change command."""
        message = MessageFactory.create_color_change_command(color)
        return self.send_message(message)
    
    def send_wifi_info(self, ssid: str, password: str, ip_address: str, port: int) -> bool:
        """Send WiFi hotspot information."""
        message = MessageFactory.create_wifi_hotspot_info(ssid, password, ip_address, port)
        return self.send_message(message)
    
    def send_file_transfer_request(self, file_size: int, file_name: str, 
                                  direction: str) -> bool:
        """Send file transfer request."""
        message = MessageFactory.create_file_transfer_request(file_size, file_name, direction)
        return self.send_message(message)
    
    def send_file_transfer_response(self, accepted: bool, tcp_port: int, 
                                   error_message: str = None) -> bool:
        """Send file transfer response."""
        message = MessageFactory.create_file_transfer_response(accepted, tcp_port, error_message)
        return self.send_message(message)
    
    def get_received_messages(self) -> List[ProtocolMessage]:
        """Get all received messages from queue."""
        messages = []
        while not self.message_queue.empty():
            try:
                messages.append(self.message_queue.get_nowait())
            except queue.Empty:
                break
        return messages
    
    def scan_for_devices(self, timeout: int = 10) -> List[Dict[str, Any]]:
        """Scan for available Bluetooth devices."""
        if not self.adapter or not self.adapter.isEnabled():
            return []
        
        devices = []
        
        # Get bonded (paired) devices
        bonded_devices = self.adapter.getBondedDevices().toArray()
        for device in bonded_devices:
            devices.append({
                'name': device.getName() or "Unknown Device",
                'address': device.getAddress(),
                'bonded': True,
                'device': device
            })
        
        # Note: Discovery of new devices requires more complex implementation
        # For now, we'll focus on bonded devices
        
        logger.info(f"Found {len(devices)} bonded devices")
        return devices
    
    def is_connected(self) -> bool:
        """Check if Bluetooth connection is active."""
        return (self.client_socket is not None and 
                self.connection_state.bluetooth_state == "connected")
    
    def get_connected_device_info(self) -> Optional[Dict[str, str]]:
        """Get information about connected device."""
        if self.connected_device:
            return {
                'name': self.connected_device.getName() or "Unknown Device",
                'address': self.connected_device.getAddress(),
                'bonded': self.connected_device.getBondState() == BluetoothDevice.BOND_BONDED
            }
        return None
    
    def _handle_connection(self):
        """Handle active connection."""
        while self.is_running and self.client_socket:
            try:
                time.sleep(1)
                # Connection is maintained by message threads
            except Exception:
                break
    
    def _handle_disconnection(self):
        """Handle connection loss."""
        logger.info("Bluetooth connection lost")
        self.connection_state.update_bluetooth_state("disconnected")
        self.connected_device = None
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
    
    def disconnect(self):
        """Disconnect from current device."""
        logger.info("Disconnecting Bluetooth")
        self.is_running = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None
        
        self.connection_state.update_bluetooth_state("disconnected")
        self.connected_device = None
    
    def get_connection_state(self) -> Dict[str, Any]:
        """Get current connection state."""
        return {
            **self.connection_state.to_dict(),
            'is_server': self.is_server,
            'connected_device': self.get_connected_device_info(),
            'message_queue_size': self.message_queue.qsize(),
            'outgoing_queue_size': self.outgoing_queue.qsize()
        }
    
    def is_bluetooth_enabled(self) -> bool:
        """Check if Bluetooth is enabled."""
        return self.adapter and self.adapter.isEnabled()
    
    def enable_bluetooth(self) -> bool:
        """Request to enable Bluetooth."""
        if self.adapter:
            return self.adapter.enable()
        return False
    
    def cleanup(self):
        """Cleanup resources and connections."""
        self.disconnect()
