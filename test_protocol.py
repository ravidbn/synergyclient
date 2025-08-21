"""
Unit tests for protocol message handling in Android application
"""
import unittest
import json
from datetime import datetime
from utils.protocol import ProtocolMessage, MessageType, ActionType, ColorType


class TestProtocolMessage(unittest.TestCase):
    """Test cases for ProtocolMessage class"""

    def test_create_color_change_command(self):
        """Test creating a color change command message"""
        # Arrange
        color = ColorType.RED
        
        # Act
        message = ProtocolMessage.create_color_change_command(color)
        
        # Assert
        self.assertEqual(message.type, MessageType.COMMAND.value.lower())
        self.assertEqual(message.action, ActionType.COLOR_CHANGE.value.lower())
        self.assertEqual(message.data['color'], color.value)
        self.assertEqual(message.source, 'android')
        self.assertIsNotNone(message.message_id)
        self.assertIsNotNone(message.timestamp)

    def test_create_wifi_hotspot_info(self):
        """Test creating WiFi hotspot info message"""
        # Arrange
        ssid = "TestHotspot"
        password = "TestPassword123"
        ip_address = "192.168.43.1"
        port = 8888
        
        # Act
        message = ProtocolMessage.create_wifi_hotspot_info(ssid, password, ip_address, port)
        
        # Assert
        self.assertEqual(message.type, MessageType.NOTIFICATION.value.lower())
        self.assertEqual(message.action, ActionType.WIFI_HOTSPOT_INFO.value.lower())
        self.assertEqual(message.data['ssid'], ssid)
        self.assertEqual(message.data['password'], password)
        self.assertEqual(message.data['ip_address'], ip_address)
        self.assertEqual(message.data['port'], port)

    def test_json_serialization_deserialization(self):
        """Test JSON serialization and deserialization"""
        # Arrange
        original_message = ProtocolMessage.create_color_change_command(ColorType.YELLOW)
        
        # Act
        json_str = original_message.to_json()
        parsed_message = ProtocolMessage.from_json(json_str)
        
        # Assert
        self.assertIsNotNone(parsed_message)
        self.assertEqual(parsed_message.message_id, original_message.message_id)
        self.assertEqual(parsed_message.type, original_message.type)
        self.assertEqual(parsed_message.action, original_message.action)
        self.assertEqual(parsed_message.data, original_message.data)
        self.assertEqual(parsed_message.source, original_message.source)

    def test_invalid_json_handling(self):
        """Test handling of invalid JSON"""
        # Arrange
        invalid_json = '{"invalid": json}'
        
        # Act
        result = ProtocolMessage.from_json(invalid_json)
        
        # Assert
        self.assertIsNone(result)

    def test_message_validation(self):
        """Test message validation"""
        # Arrange
        valid_message = ProtocolMessage.create_color_change_command(ColorType.GREEN)
        
        # Act
        is_valid = valid_message.validate()
        
        # Assert
        self.assertTrue(is_valid)

    def test_message_id_uniqueness(self):
        """Test that message IDs are unique"""
        # Arrange & Act
        message1 = ProtocolMessage.create_color_change_command(ColorType.RED)
        message2 = ProtocolMessage.create_color_change_command(ColorType.RED)
        
        # Assert
        self.assertNotEqual(message1.message_id, message2.message_id)

    def test_timestamp_format(self):
        """Test timestamp format is ISO 8601"""
        # Arrange & Act
        message = ProtocolMessage.create_color_change_command(ColorType.RED)
        
        # Assert
        # Should be able to parse the timestamp
        try:
            datetime.fromisoformat(message.timestamp.replace('Z', '+00:00'))
            timestamp_valid = True
        except ValueError:
            timestamp_valid = False
        
        self.assertTrue(timestamp_valid)

    def test_error_message_creation(self):
        """Test creating error messages"""
        # Arrange
        error_code = "BT_001"
        error_type = "ConnectionError"
        error_message = "Bluetooth connection failed"
        suggestions = ["Check Bluetooth is enabled", "Try repairing devices"]
        
        # Act
        message = ProtocolMessage.create_error_message(error_code, error_type, error_message, suggestions)
        
        # Assert
        self.assertEqual(message.type, MessageType.RESPONSE.value.lower())
        self.assertEqual(message.action, ActionType.ERROR.value.lower())
        self.assertEqual(message.data['error_code'], error_code)
        self.assertEqual(message.data['error_type'], error_type)
        self.assertEqual(message.data['error_message'], error_message)
        self.assertEqual(message.data['recovery_suggestions'], suggestions)

    def test_file_transfer_request_creation(self):
        """Test creating file transfer request"""
        # Arrange
        file_size = 1024 * 1024  # 1MB
        file_name = "test_file.bin"
        direction = "upload"
        
        # Act
        message = ProtocolMessage.create_file_transfer_request(file_size, file_name, direction)
        
        # Assert
        self.assertEqual(message.type, MessageType.REQUEST.value.lower())
        self.assertEqual(message.action, ActionType.FILE_TRANSFER_REQUEST.value.lower())
        self.assertEqual(message.data['file_size'], file_size)
        self.assertEqual(message.data['file_name'], file_name)
        self.assertEqual(message.data['transfer_direction'], direction)

    def test_acknowledgment_creation(self):
        """Test creating acknowledgment messages"""
        # Arrange
        original_message = ProtocolMessage.create_color_change_command(ColorType.GREEN)
        
        # Act
        ack_message = ProtocolMessage.create_acknowledgment(original_message)
        
        # Assert
        self.assertEqual(ack_message.type, MessageType.RESPONSE.value.lower())
        self.assertEqual(ack_message.action, f"{original_message.action}ack")
        self.assertEqual(ack_message.data['original_message_id'], original_message.message_id)
        self.assertEqual(ack_message.data['status'], 'acknowledged')


class TestColorType(unittest.TestCase):
    """Test cases for ColorType enum"""

    def test_color_values(self):
        """Test color enum values"""
        self.assertEqual(ColorType.RED.value, "RED")
        self.assertEqual(ColorType.YELLOW.value, "YELLOW")
        self.assertEqual(ColorType.GREEN.value, "GREEN")

    def test_color_from_string(self):
        """Test creating ColorType from string"""
        self.assertEqual(ColorType.from_string("RED"), ColorType.RED)
        self.assertEqual(ColorType.from_string("red"), ColorType.RED)
        self.assertEqual(ColorType.from_string("YELLOW"), ColorType.YELLOW)
        self.assertEqual(ColorType.from_string("GREEN"), ColorType.GREEN)
        self.assertEqual(ColorType.from_string("invalid"), ColorType.RED)  # Default


class TestMessageType(unittest.TestCase):
    """Test cases for MessageType enum"""

    def test_message_type_values(self):
        """Test message type enum values"""
        self.assertEqual(MessageType.COMMAND.value, "COMMAND")
        self.assertEqual(MessageType.RESPONSE.value, "RESPONSE")
        self.assertEqual(MessageType.REQUEST.value, "REQUEST")
        self.assertEqual(MessageType.NOTIFICATION.value, "NOTIFICATION")


class TestActionType(unittest.TestCase):
    """Test cases for ActionType enum"""

    def test_action_type_values(self):
        """Test action type enum values"""
        self.assertEqual(ActionType.COLOR_CHANGE.value, "COLOR_CHANGE")
        self.assertEqual(ActionType.WIFI_HOTSPOT_INFO.value, "WIFI_HOTSPOT_INFO")
        self.assertEqual(ActionType.FILE_TRANSFER_REQUEST.value, "FILE_TRANSFER_REQUEST")
        self.assertEqual(ActionType.ERROR.value, "ERROR")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)