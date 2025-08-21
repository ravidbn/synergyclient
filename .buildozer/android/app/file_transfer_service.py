"""
File Transfer Service for Android.
Handles TCP server/client functionality, file transfers with progress tracking,
and checksum verification.
"""

import socket
import threading
import json
import time
import os
import hashlib
from typing import Callable, Optional, Dict, Any
from utils.protocol import MessageFactory, ProtocolMessage, DEFAULT_TCP_PORT, FILE_CHUNK_SIZE
from utils.file_generator import FileGenerator, ProgressTracker
import logging

logger = logging.getLogger(__name__)


class FileTransferServer:
    """TCP server for receiving files from Windows client."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = DEFAULT_TCP_PORT):
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False
        self.client_socket = None
        self.transfer_thread = None
        self.progress_callback = None
        self.completion_callback = None
        
    def start_server(self, progress_callback: Callable = None, 
                    completion_callback: Callable = None) -> bool:
        """Start the TCP server for file reception."""
        try:
            self.progress_callback = progress_callback
            self.completion_callback = completion_callback
            
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            
            self.is_running = True
            logger.info(f"File transfer server started on {self.host}:{self.port}")
            
            # Start listening thread
            self.transfer_thread = threading.Thread(target=self._listen_for_connections)
            self.transfer_thread.daemon = True
            self.transfer_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start server: {str(e)}")
            return False
    
    def _listen_for_connections(self):
        """Listen for incoming connections and handle file transfers."""
        while self.is_running:
            try:
                logger.info("Waiting for file transfer connection...")
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"Client connected from {client_address}")
                
                self.client_socket = client_socket
                self._handle_file_transfer(client_socket)
                
            except socket.error as e:
                if self.is_running:
                    logger.error(f"Socket error in server: {str(e)}")
                break
            except Exception as e:
                logger.error(f"Error in server listen loop: {str(e)}")
    
    def _handle_file_transfer(self, client_socket: socket.socket):
        """Handle incoming file transfer from client."""
        try:
            # Receive handshake
            handshake_data = self._receive_json_message(client_socket)
            if not handshake_data:
                logger.error("Failed to receive handshake")
                return
            
            file_metadata = handshake_data.get('file_metadata', {})
            file_name = file_metadata.get('name', 'received_file.bin')
            file_size = file_metadata.get('size', 0)
            expected_checksum = file_metadata.get('checksum', '')
            chunk_size = file_metadata.get('chunk_size', FILE_CHUNK_SIZE)
            transfer_id = handshake_data.get('transfer_id', '')
            
            logger.info(f"Receiving file: {file_name} ({file_size} bytes)")
            
            # Send acknowledgment
            ack_message = {
                "status": "ready",
                "message": "Ready to receive file",
                "transfer_id": transfer_id
            }
            self._send_json_message(client_socket, ack_message)
            
            # Receive file
            file_path = os.path.join("/tmp", "synergy_files", "received", file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            result = self._receive_file_chunks(client_socket, file_path, file_size, 
                                             expected_checksum, chunk_size)
            
            # Send final status
            self._send_json_message(client_socket, result)
            
            # Notify completion
            if self.completion_callback:
                self.completion_callback(result)
            
        except Exception as e:
            logger.error(f"Error handling file transfer: {str(e)}")
            error_result = {
                "transfer_complete": False,
                "error": str(e),
                "message": "File transfer failed"
            }
            try:
                self._send_json_message(client_socket, error_result)
            except:
                pass
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def _receive_file_chunks(self, client_socket: socket.socket, file_path: str,
                           total_size: int, expected_checksum: str, chunk_size: int) -> dict:
        """Receive file in chunks with progress tracking."""
        start_time = time.time()
        bytes_received = 0
        sha256_hash = hashlib.sha256()
        
        progress_tracker = ProgressTracker(total_size, update_interval=1.0)
        
        try:
            with open(file_path, 'wb') as f:
                while bytes_received < total_size:
                    # Receive chunk header
                    chunk_header = self._receive_json_message(client_socket)
                    if not chunk_header:
                        raise Exception("Failed to receive chunk header")
                    
                    chunk_id = chunk_header['chunk_id']
                    expected_chunk_size = chunk_header['chunk_size']
                    chunk_checksum = chunk_header['chunk_checksum']
                    is_last_chunk = chunk_header['is_last_chunk']
                    
                    # Receive chunk data
                    chunk_data = self._receive_exact_bytes(client_socket, expected_chunk_size)
                    if not chunk_data or len(chunk_data) != expected_chunk_size:
                        raise Exception(f"Failed to receive chunk {chunk_id}")
                    
                    # Verify chunk checksum
                    actual_chunk_checksum = hashlib.sha256(chunk_data).hexdigest()
                    if actual_chunk_checksum != chunk_checksum:
                        raise Exception(f"Chunk {chunk_id} checksum mismatch")
                    
                    # Write chunk and update hash
                    f.write(chunk_data)
                    sha256_hash.update(chunk_data)
                    bytes_received += len(chunk_data)
                    
                    # Send chunk acknowledgment
                    chunk_ack = {
                        "chunk_id": chunk_id,
                        "status": "received",
                        "message": "Chunk received successfully"
                    }
                    self._send_json_message(client_socket, chunk_ack)
                    
                    # Update progress
                    if self.progress_callback and progress_tracker.should_update():
                        progress_info = progress_tracker.update(bytes_received)
                        self.progress_callback(progress_info)
        
        except Exception as e:
            # Clean up partial file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise e
        
        # Final verification
        end_time = time.time()
        transfer_time = end_time - start_time
        actual_checksum = sha256_hash.hexdigest()
        checksum_verified = actual_checksum.lower() == expected_checksum.lower()
        
        if not checksum_verified:
            os.remove(file_path)
            raise Exception("File checksum verification failed")
        
        # Calculate transfer statistics
        speed_mbps = (bytes_received * 8) / (transfer_time * 1024 * 1024) if transfer_time > 0 else 0
        
        return {
            "transfer_complete": True,
            "total_bytes": bytes_received,
            "transfer_time_ms": int(transfer_time * 1000),
            "average_speed_mbps": round(speed_mbps, 2),
            "file_checksum": actual_checksum,
            "checksum_verified": checksum_verified,
            "file_path": file_path
        }
    
    def _receive_json_message(self, sock: socket.socket) -> Optional[dict]:
        """Receive a JSON message from socket."""
        try:
            # Receive message length first (4 bytes)
            length_bytes = self._receive_exact_bytes(sock, 4)
            if not length_bytes:
                return None
            
            message_length = int.from_bytes(length_bytes, byteorder='big')
            
            # Receive the actual message
            message_bytes = self._receive_exact_bytes(sock, message_length)
            if not message_bytes:
                return None
            
            return json.loads(message_bytes.decode('utf-8'))
            
        except Exception as e:
            logger.error(f"Error receiving JSON message: {str(e)}")
            return None
    
    def _send_json_message(self, sock: socket.socket, message: dict):
        """Send a JSON message over socket."""
        try:
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')
            
            # Send message length first (4 bytes)
            length_bytes = len(message_bytes).to_bytes(4, byteorder='big')
            sock.send(length_bytes)
            
            # Send the actual message
            sock.send(message_bytes)
            
        except Exception as e:
            logger.error(f"Error sending JSON message: {str(e)}")
            raise
    
    def _receive_exact_bytes(self, sock: socket.socket, num_bytes: int) -> Optional[bytes]:
        """Receive exact number of bytes from socket."""
        data = bytearray()
        while len(data) < num_bytes:
            packet = sock.recv(num_bytes - len(data))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)
    
    def stop_server(self):
        """Stop the file transfer server."""
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass


class FileTransferClient:
    """TCP client for sending files to Windows application."""
    
    def __init__(self):
        self.socket = None
        self.file_generator = FileGenerator()
    
    def send_file(self, host: str, port: int, file_path: str,
                 progress_callback: Callable = None) -> dict:
        """Send a file to the specified host and port."""
        try:
            # Connect to server
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            
            logger.info(f"Connected to {host}:{port} for file transfer")
            
            # Get file info
            file_info = self.file_generator.get_file_info(file_path)
            file_name = os.path.basename(file_path)
            
            # Send handshake
            handshake = {
                "protocol_version": "1.0",
                "file_metadata": {
                    "name": file_name,
                    "size": file_info['size_bytes'],
                    "checksum": file_info['checksum'],
                    "chunk_size": FILE_CHUNK_SIZE
                },
                "transfer_id": f"transfer_{int(time.time())}"
            }
            
            self._send_json_message(self.socket, handshake)
            
            # Wait for acknowledgment
            ack = self._receive_json_message(self.socket)
            if not ack or ack.get('status') != 'ready':
                raise Exception("Server not ready for file transfer")
            
            # Send file in chunks
            result = self._send_file_chunks(file_path, file_info, progress_callback)
            
            # Receive final status
            final_status = self._receive_json_message(self.socket)
            
            result.update(final_status or {})
            return result
            
        except Exception as e:
            logger.error(f"Error in file transfer: {str(e)}")
            return {
                "transfer_complete": False,
                "error": str(e),
                "message": "File transfer failed"
            }
        finally:
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
    
    def _send_file_chunks(self, file_path: str, file_info: dict,
                         progress_callback: Callable = None) -> dict:
        """Send file in chunks with progress tracking."""
        start_time = time.time()
        total_size = file_info['size_bytes']
        bytes_sent = 0
        chunk_id = 0
        
        progress_tracker = ProgressTracker(total_size, update_interval=1.0)
        
        try:
            with open(file_path, 'rb') as f:
                while bytes_sent < total_size:
                    # Read chunk
                    remaining_bytes = total_size - bytes_sent
                    current_chunk_size = min(FILE_CHUNK_SIZE, remaining_bytes)
                    chunk_data = f.read(current_chunk_size)
                    
                    if not chunk_data:
                        break
                    
                    chunk_id += 1
                    chunk_checksum = hashlib.sha256(chunk_data).hexdigest()
                    is_last_chunk = bytes_sent + len(chunk_data) >= total_size
                    
                    # Send chunk header
                    chunk_header = {
                        "chunk_id": chunk_id,
                        "chunk_size": len(chunk_data),
                        "chunk_checksum": chunk_checksum,
                        "is_last_chunk": is_last_chunk
                    }
                    self._send_json_message(self.socket, chunk_header)
                    
                    # Send chunk data
                    self.socket.send(chunk_data)
                    bytes_sent += len(chunk_data)
                    
                    # Wait for chunk acknowledgment
                    chunk_ack = self._receive_json_message(self.socket)
                    if not chunk_ack or chunk_ack.get('status') != 'received':
                        raise Exception(f"Chunk {chunk_id} not acknowledged")
                    
                    # Update progress
                    if progress_callback and progress_tracker.should_update():
                        progress_info = progress_tracker.update(bytes_sent)
                        progress_callback(progress_info)
        
        except Exception as e:
            raise e
        
        # Calculate transfer statistics
        end_time = time.time()
        transfer_time = end_time - start_time
        speed_mbps = (bytes_sent * 8) / (transfer_time * 1024 * 1024) if transfer_time > 0 else 0
        
        return {
            "transfer_complete": True,
            "total_chunks": chunk_id,
            "total_bytes": bytes_sent,
            "transfer_time_ms": int(transfer_time * 1000),
            "average_speed_mbps": round(speed_mbps, 2),
            "file_checksum": file_info['checksum'],
            "checksum_verified": True
        }
    
    def _send_json_message(self, sock: socket.socket, message: dict):
        """Send a JSON message over socket."""
        try:
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')
            
            # Send message length first (4 bytes)
            length_bytes = len(message_bytes).to_bytes(4, byteorder='big')
            sock.send(length_bytes)
            
            # Send the actual message
            sock.send(message_bytes)
            
        except Exception as e:
            logger.error(f"Error sending JSON message: {str(e)}")
            raise
    
    def _receive_json_message(self, sock: socket.socket) -> Optional[dict]:
        """Receive a JSON message from socket."""
        try:
            # Receive message length first (4 bytes)
            length_bytes = self._receive_exact_bytes(sock, 4)
            if not length_bytes:
                return None
            
            message_length = int.from_bytes(length_bytes, byteorder='big')
            
            # Receive the actual message
            message_bytes = self._receive_exact_bytes(sock, message_length)
            if not message_bytes:
                return None
            
            return json.loads(message_bytes.decode('utf-8'))
            
        except Exception as e:
            logger.error(f"Error receiving JSON message: {str(e)}")
            return None
    
    def _receive_exact_bytes(self, sock: socket.socket, num_bytes: int) -> Optional[bytes]:
        """Receive exact number of bytes from socket."""
        data = bytearray()
        while len(data) < num_bytes:
            packet = sock.recv(num_bytes - len(data))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)


class FileTransferService:
    """Main file transfer service that manages both server and client functionality."""
    
    def __init__(self, hotspot_ip: str = "192.168.43.1"):
        self.hotspot_ip = hotspot_ip
        self.server = FileTransferServer(host=hotspot_ip)
        self.client = FileTransferClient()
        self.file_generator = FileGenerator()
        self.is_server_running = False
        
        # Callbacks
        self.progress_callback = None
        self.completion_callback = None
    
    def set_callbacks(self, progress_callback: Callable = None,
                     completion_callback: Callable = None):
        """Set callback functions for progress and completion events."""
        self.progress_callback = progress_callback
        self.completion_callback = completion_callback
    
    def start_file_server(self, port: int = DEFAULT_TCP_PORT) -> bool:
        """Start the file transfer server."""
        self.server.port = port
        success = self.server.start_server(
            progress_callback=self.progress_callback,
            completion_callback=self.completion_callback
        )
        self.is_server_running = success
        return success
    
    def stop_file_server(self):
        """Stop the file transfer server."""
        self.server.stop_server()
        self.is_server_running = False
    
    def generate_and_send_file(self, target_host: str, target_port: int,
                              size_mb: int, file_name: str = None) -> dict:
        """Generate a random file and send it to the target."""
        try:
            # Generate file
            if file_name is None:
                file_name = f"test_file_{size_mb}MB.bin"
            
            file_path = os.path.join("/tmp", "synergy_files", "generated", file_name)
            
            logger.info(f"Generating {size_mb}MB file for transfer")
            file_info = self.file_generator.generate_file(
                file_path, size_mb, self.progress_callback
            )
            
            logger.info(f"Sending file to {target_host}:{target_port}")
            # Send file
            transfer_result = self.client.send_file(
                target_host, target_port, file_path, self.progress_callback
            )
            
            # Combine generation and transfer info
            result = {
                **file_info,
                **transfer_result,
                'target_host': target_host,
                'target_port': target_port
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in generate and send: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate and send file"
            }
    
    def create_file_transfer_request_message(self, file_size_mb: int,
                                           direction: str = "android_to_windows") -> dict:
        """Create a file transfer request message."""
        file_size_bytes = file_size_mb * 1024 * 1024
        file_name = f"test_file_{file_size_mb}MB.bin"
        
        message = MessageFactory.create_file_transfer_request(
            file_size_bytes, file_name, direction
        )
        
        return message.to_dict()
    
    def create_file_transfer_response_message(self, accepted: bool,
                                            tcp_port: int = DEFAULT_TCP_PORT,
                                            error_message: str = None) -> dict:
        """Create a file transfer response message."""
        message = MessageFactory.create_file_transfer_response(
            accepted, tcp_port, error_message
        )
        
        return message.to_dict()
    
    def get_server_status(self) -> dict:
        """Get current server status."""
        return {
            "running": self.is_server_running,
            "host": self.hotspot_ip,
            "port": self.server.port if self.server else DEFAULT_TCP_PORT
        }
    
    def cleanup(self):
        """Cleanup resources."""
        self.stop_file_server()