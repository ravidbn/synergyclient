"""
Mock File Transfer Service for initial testing.
Provides basic interface without complex networking functionality.
"""

import logging
from typing import Callable, Optional, Dict, Any

logger = logging.getLogger(__name__)


class FileTransferService:
    """Mock file transfer service for testing purposes."""
    
    def __init__(self, hotspot_ip: str = "192.168.43.1"):
        self.hotspot_ip = hotspot_ip
        self.is_server_running = False
        self.progress_callback = None
        self.completion_callback = None
        
        logger.info("Mock file transfer service initialized")
    
    def set_callbacks(self, progress_callback: Callable = None,
                     completion_callback: Callable = None):
        """Set callback functions for progress and completion events."""
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
    
    def start_file_server(self, port: int = 8888) -> bool:
        """Mock start file server."""
        logger.info(f"Mock: Starting file server on port {port}")
        self.is_server_running = True
        return True
    
    def stop_file_server(self):
        """Mock stop file server."""
        logger.info("Mock: Stopping file server")
        self.is_server_running = False
    
    def generate_and_send_file(self, target_host: str, target_port: int,
                              size_mb: int, file_name: str = None) -> dict:
        """Mock file generation and send."""
        logger.info(f"Mock: Generating and sending {size_mb}MB file to {target_host}:{target_port}")
        
        return {
            "success": True,
            "transfer_complete": True,
            "total_bytes": size_mb * 1024 * 1024,
            "transfer_time_ms": 1000,
            "average_speed_mbps": 10.0,
            "file_checksum": "mock_checksum",
            "checksum_verified": True,
            "target_host": target_host,
            "target_port": target_port,
            "message": "Mock file transfer completed"
        }
    
    def create_file_transfer_request_message(self, file_size_mb: int,
                                           direction: str = "android_to_windows") -> dict:
        """Mock file transfer request message."""
        return {
            "action": "file_transfer_request",
            "file_size": file_size_mb * 1024 * 1024,
            "file_name": f"test_file_{file_size_mb}MB.bin",
            "direction": direction
        }
    
    def create_file_transfer_response_message(self, accepted: bool,
                                            tcp_port: int = 8888,
                                            error_message: str = None) -> dict:
        """Mock file transfer response message."""
        return {
            "action": "file_transfer_response",
            "accepted": accepted,
            "tcp_port": tcp_port,
            "error_message": error_message
        }
    
    def get_server_status(self) -> dict:
        """Mock server status."""
        return {
            "running": self.is_server_running,
            "host": self.hotspot_ip,
            "port": 8888
        }
    
    def cleanup(self):
        """Mock cleanup."""
        logger.info("Mock: File transfer cleanup")
        self.stop_file_server()