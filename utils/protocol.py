"""
Protocol utilities for Synergy Android application.
Handles message serialization, deserialization, and protocol definitions.
"""

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, Optional


class MessageType(Enum):
    """Enumeration of message types for Bluetooth communication."""
    COMMAND = "command"
    RESPONSE = "response"
    REQUEST = "request"
    NOTIFICATION = "notification"


class ActionType(Enum):
    """Enumeration of action types for different operations."""
    COLOR_CHANGE = "color_change"
    COLOR_CHANGE_ACK = "color_change_ack"
    WIFI_HOTSPOT_INFO = "wifi_hotspot_info"
    WIFI_CONNECTION_STATUS = "wifi_connection_status"
    FILE_TRANSFER_REQUEST = "file_transfer_request"
    FILE_TRANSFER_RESPONSE = "file_transfer_response"
    ERROR = "error"


class ColorType(Enum):
    """Enumeration of supported colors."""
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class ErrorCode(Enum):
    """Error codes for system operations."""
    E001 = "E001"  # Bluetooth connection failed
    E002 = "E002"  # Wi-Fi hotspot creation failed
    E003 = "E003"  # Wi-Fi connection failed
    E004 = "E004"  # File transfer initialization failed
    E005 = "E005"  # File transfer interrupted
    E006 = "E006"  # Checksum verification failed
    E007 = "E007"  # Invalid message format
    E008 = "E008"  # Unsupported operation


class ProtocolMessage:
    """Class representing a protocol message."""
    
    def __init__(self, message_type: MessageType, action: ActionType, 
                 data: Dict[str, Any], source: str = "android"):
        self.message_id = str(uuid.uuid4())
        self.type = message_type.value
        self.action = action.value
        self.data = data
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.source = source
    
    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps({
            "message_id": self.message_id,
            "type": self.type,
            "action": self.action,
            "data": self.data,
            "timestamp": self.timestamp,
            "source": self.source
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "message_id": self.message_id,
            "type": self.type,
            "action": self.action,
            "data": self.data,
            "timestamp": self.timestamp,
            "source": self.source
        }
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ProtocolMessage':
        """Create message from JSON string."""
        data = json.loads(json_str)
        message = cls.__new__(cls)
        message.message_id = data.get("message_id", str(uuid.uuid4()))
        message.type = data["type"]
        message.action = data["action"]
        message.data = data["data"]
        message.timestamp = data.get("timestamp", datetime.now(timezone.utc).isoformat())
        message.source = data.get("source", "unknown")
        return message


class MessageFactory:
    """Factory class for creating common message types."""
    
    @staticmethod
    def create_color_change_command(color: ColorType) -> ProtocolMessage:
        """Create a color change command message."""
        return ProtocolMessage(
            MessageType.COMMAND,
            ActionType.COLOR_CHANGE,
            {"color": color.value}
        )
    
    @staticmethod
    def create_wifi_hotspot_info(ssid: str, password: str, ip_address: str, port: int) -> ProtocolMessage:
        """Create a Wi-Fi hotspot information notification."""
        return ProtocolMessage(
            MessageType.NOTIFICATION,
            ActionType.WIFI_HOTSPOT_INFO,
            {
                "ssid": ssid,
                "password": password,
                "ip_address": ip_address,
                "port": port,
                "security_type": "WPA2"
            }
        )
    
    @staticmethod
    def create_file_transfer_request(file_size: int, file_name: str, 
                                   transfer_direction: str) -> ProtocolMessage:
        """Create a file transfer request message."""
        return ProtocolMessage(
            MessageType.REQUEST,
            ActionType.FILE_TRANSFER_REQUEST,
            {
                "file_size": file_size,
                "file_name": file_name,
                "transfer_direction": transfer_direction,
                "checksum_type": "SHA256",
                "compression": False
            }
        )
    
    @staticmethod
    def create_file_transfer_response(accepted: bool, tcp_port: int, 
                                    error_message: Optional[str] = None) -> ProtocolMessage:
        """Create a file transfer response message."""
        return ProtocolMessage(
            MessageType.RESPONSE,
            ActionType.FILE_TRANSFER_RESPONSE,
            {
                "accepted": accepted,
                "tcp_port": tcp_port,
                "ready_for_transfer": accepted,
                "error_message": error_message
            }
        )
    
    @staticmethod
    def create_error_message(error_code: ErrorCode, error_type: str, 
                           error_message: str, recovery_suggestions: list) -> ProtocolMessage:
        """Create an error message."""
        return ProtocolMessage(
            MessageType.RESPONSE,
            ActionType.ERROR,
            {
                "error_code": error_code.value,
                "error_type": error_type,
                "error_message": error_message,
                "recovery_suggestions": recovery_suggestions,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )


class ConnectionState:
    """Class to track connection states."""
    
    def __init__(self):
        self.bluetooth_state = "disconnected"
        self.wifi_state = "disabled"
        self.file_transfer_state = "idle"
        self.last_activity = datetime.now(timezone.utc).isoformat()
    
    def update_bluetooth_state(self, state: str):
        """Update Bluetooth connection state."""
        self.bluetooth_state = state
        self.last_activity = datetime.now(timezone.utc).isoformat()
    
    def update_wifi_state(self, state: str):
        """Update Wi-Fi connection state."""
        self.wifi_state = state
        self.last_activity = datetime.now(timezone.utc).isoformat()
    
    def update_file_transfer_state(self, state: str):
        """Update file transfer state."""
        self.file_transfer_state = state
        self.last_activity = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, str]:
        """Convert connection state to dictionary."""
        return {
            "bluetooth_state": self.bluetooth_state,
            "wifi_state": self.wifi_state,
            "file_transfer_state": self.file_transfer_state,
            "last_activity": self.last_activity
        }


def validate_message(message_dict: Dict[str, Any]) -> bool:
    """Validate message format and required fields."""
    required_fields = ["message_id", "type", "action", "data", "timestamp", "source"]
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in message_dict:
            return False
    
    # Validate message type
    valid_types = [t.value for t in MessageType]
    if message_dict["type"] not in valid_types:
        return False
    
    # Validate action type
    valid_actions = [a.value for a in ActionType]
    if message_dict["action"] not in valid_actions:
        return False
    
    return True


def generate_message_id() -> str:
    """Generate a unique message ID."""
    return str(uuid.uuid4())


def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


# Constants for the protocol
PROTOCOL_VERSION = "1.0"
DEFAULT_TCP_PORT = 8888
HOTSPOT_SSID = "SynergyDemo"
HOTSPOT_PASSWORD = "synergy123"
MAX_MESSAGE_SIZE = 512  # bytes
FILE_CHUNK_SIZE = 1048576  # 1MB
TRANSFER_TIMEOUT = 10  # seconds
CONNECTION_TIMEOUT = 30  # seconds