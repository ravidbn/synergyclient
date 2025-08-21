"""
File generator utility for creating random test files.
Supports configurable file sizes and progress tracking.
"""

import os
import random
import hashlib
import time
from typing import Callable, Optional


class FileGenerator:
    """Utility class for generating random test files."""
    
    def __init__(self):
        self.chunk_size = 1024 * 1024  # 1MB chunks
    
    def generate_file(self, file_path: str, size_mb: int, 
                     progress_callback: Optional[Callable[[int, int], None]] = None) -> dict:
        """
        Generate a random file with specified size.
        
        Args:
            file_path: Path where the file will be created
            size_mb: Size of the file in megabytes
            progress_callback: Optional callback function for progress updates
                             Called with (bytes_written, total_bytes)
        
        Returns:
            Dictionary with file information including checksum and generation time
        """
        start_time = time.time()
        total_bytes = size_mb * 1024 * 1024
        bytes_written = 0
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Initialize SHA256 hash calculator
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, 'wb') as f:
                while bytes_written < total_bytes:
                    # Calculate chunk size for this iteration
                    remaining_bytes = total_bytes - bytes_written
                    current_chunk_size = min(self.chunk_size, remaining_bytes)
                    
                    # Generate random chunk
                    chunk = self._generate_random_chunk(current_chunk_size)
                    
                    # Write chunk to file and update hash
                    f.write(chunk)
                    sha256_hash.update(chunk)
                    bytes_written += current_chunk_size
                    
                    # Call progress callback if provided
                    if progress_callback:
                        progress_callback(bytes_written, total_bytes)
        
        except Exception as e:
            # Clean up partial file on error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise e
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        return {
            'file_path': file_path,
            'size_bytes': total_bytes,
            'size_mb': size_mb,
            'checksum': sha256_hash.hexdigest(),
            'checksum_type': 'SHA256',
            'generation_time_seconds': generation_time,
            'generation_speed_mbps': (size_mb * 8) / generation_time if generation_time > 0 else 0
        }
    
    def _generate_random_chunk(self, size: int) -> bytes:
        """
        Generate a random chunk of specified size.
        Uses a mix of patterns to make the data somewhat realistic.
        """
        # Use different patterns for variety
        pattern_type = random.randint(0, 3)
        
        if pattern_type == 0:
            # Pure random bytes
            return bytes([random.randint(0, 255) for _ in range(size)])
        elif pattern_type == 1:
            # Text-like pattern
            text_chars = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 \n\t'
            return bytes([random.choice(text_chars) for _ in range(size)])
        elif pattern_type == 2:
            # Repetitive pattern with some randomness
            base_pattern = bytes([random.randint(0, 255) for _ in range(256)])
            result = bytearray()
            for i in range(size):
                result.append(base_pattern[i % 256])
                # Add some randomness
                if random.randint(0, 100) < 5:  # 5% chance
                    result[-1] = random.randint(0, 255)
            return bytes(result)
        else:
            # Mixed pattern
            chunk = bytearray(size)
            for i in range(size):
                if i % 4 == 0:
                    chunk[i] = random.randint(0, 255)
                elif i % 4 == 1:
                    chunk[i] = (i // 4) % 256
                elif i % 4 == 2:
                    chunk[i] = ord('A') + (i % 26)
                else:
                    chunk[i] = ord('0') + (i % 10)
            return bytes(chunk)
    
    def calculate_file_checksum(self, file_path: str) -> str:
        """Calculate SHA256 checksum of an existing file."""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(self.chunk_size):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def verify_file_checksum(self, file_path: str, expected_checksum: str) -> bool:
        """Verify file checksum matches expected value."""
        actual_checksum = self.calculate_file_checksum(file_path)
        return actual_checksum.lower() == expected_checksum.lower()
    
    def get_file_info(self, file_path: str) -> dict:
        """Get information about an existing file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        checksum = self.calculate_file_checksum(file_path)
        
        return {
            'file_path': file_path,
            'size_bytes': file_size,
            'size_mb': file_size / (1024 * 1024),
            'checksum': checksum,
            'checksum_type': 'SHA256'
        }
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    @staticmethod
    def format_speed(speed_mbps: float) -> str:
        """Format transfer speed in human-readable format."""
        if speed_mbps < 1.0:
            return f"{speed_mbps * 1000:.1f} Kbps"
        else:
            return f"{speed_mbps:.1f} Mbps"
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Format time duration in human-readable format."""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        else:
            hours = seconds / 3600
            return f"{hours:.1f} hours"


class ProgressTracker:
    """Helper class for tracking file operation progress."""
    
    def __init__(self, total_size: int, update_interval: float = 1.0):
        self.total_size = total_size
        self.update_interval = update_interval
        self.last_update = 0
        self.start_time = time.time()
    
    def update(self, current_size: int) -> dict:
        """
        Update progress and return progress information.
        
        Returns:
            Dictionary with progress information including percentage, speed, etc.
        """
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        progress_info = {
            'current_size': current_size,
            'total_size': self.total_size,
            'percentage': (current_size / self.total_size) * 100 if self.total_size > 0 else 0,
            'elapsed_time': elapsed_time,
            'speed_mbps': 0,
            'eta_seconds': 0
        }
        
        if elapsed_time > 0:
            speed_bps = current_size / elapsed_time
            progress_info['speed_mbps'] = (speed_bps * 8) / (1024 * 1024)  # Convert to Mbps
            
            if current_size > 0:
                remaining_bytes = self.total_size - current_size
                eta = remaining_bytes / speed_bps if speed_bps > 0 else 0
                progress_info['eta_seconds'] = eta
        
        self.last_update = current_time
        return progress_info
    
    def should_update(self) -> bool:
        """Check if enough time has passed for a progress update."""
        return time.time() - self.last_update >= self.update_interval


# Predefined file sizes for easy selection
PRESET_FILE_SIZES = {
    'small': 10,      # 10MB
    'medium': 25,     # 25MB
    'large': 50,      # 50MB
    'extra_large': 100  # 100MB
}


def create_test_file(size_preset: str, file_name: str = None, 
                    progress_callback: Callable = None) -> dict:
    """
    Convenience function to create test files with preset sizes.
    
    Args:
        size_preset: One of 'small', 'medium', 'large', 'extra_large'
        file_name: Optional custom filename
        progress_callback: Optional progress callback function
    
    Returns:
        Dictionary with file information
    """
    if size_preset not in PRESET_FILE_SIZES:
        raise ValueError(f"Invalid size preset. Must be one of: {list(PRESET_FILE_SIZES.keys())}")
    
    size_mb = PRESET_FILE_SIZES[size_preset]
    
    if file_name is None:
        file_name = f"test_file_{size_mb}MB.bin"
    
    # Create files in a temporary directory
    file_path = os.path.join("/tmp", "synergy_files", file_name)
    
    generator = FileGenerator()
    return generator.generate_file(file_path, size_mb, progress_callback)