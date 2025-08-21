"""
Unit tests for file generator utility in Android application
"""
import unittest
import os
import tempfile
import hashlib
from unittest.mock import Mock, patch
from utils.file_generator import FileGenerator


class TestFileGenerator(unittest.TestCase):
    """Test cases for FileGenerator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.progress_callback = Mock()

    def tearDown(self):
        """Clean up test fixtures"""
        # Clean up any generated files
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.temp_dir)

    def test_generate_small_file(self):
        """Test generating a small file"""
        # Arrange
        file_size = 1024  # 1KB
        file_path = os.path.join(self.temp_dir, "test_small.bin")
        
        # Act
        result = FileGenerator.generate_file(file_size, file_path, self.progress_callback)
        
        # Assert
        self.assertTrue(result)
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(os.path.getsize(file_path), file_size)
        self.progress_callback.assert_called()

    def test_generate_medium_file(self):
        """Test generating a medium file (10MB)"""
        # Arrange
        file_size = 10 * 1024 * 1024  # 10MB
        file_path = os.path.join(self.temp_dir, "test_medium.bin")
        
        # Act
        result = FileGenerator.generate_file(file_size, file_path, self.progress_callback)
        
        # Assert
        self.assertTrue(result)
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(os.path.getsize(file_path), file_size)

    def test_generate_large_file(self):
        """Test generating a large file (50MB)"""
        # Arrange
        file_size = 50 * 1024 * 1024  # 50MB
        file_path = os.path.join(self.temp_dir, "test_large.bin")
        
        # Act
        result = FileGenerator.generate_file(file_size, file_path, self.progress_callback)
        
        # Assert
        self.assertTrue(result)
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(os.path.getsize(file_path), file_size)

    def test_progress_callback_called(self):
        """Test that progress callback is called during generation"""
        # Arrange
        file_size = 5 * 1024 * 1024  # 5MB
        file_path = os.path.join(self.temp_dir, "test_progress.bin")
        
        # Act
        FileGenerator.generate_file(file_size, file_path, self.progress_callback)
        
        # Assert
        # Progress callback should be called multiple times
        self.assertGreater(self.progress_callback.call_count, 1)
        
        # Check that progress values are reasonable
        calls = self.progress_callback.call_args_list
        progress_values = [call[0][0] for call in calls]
        
        # First call should be 0 or small value
        self.assertLessEqual(progress_values[0], 10)
        # Last call should be 100
        self.assertEqual(progress_values[-1], 100)

    def test_file_checksum_calculation(self):
        """Test file checksum calculation"""
        # Arrange
        file_size = 1024
        file_path = os.path.join(self.temp_dir, "test_checksum.bin")
        
        # Act
        FileGenerator.generate_file(file_size, file_path)
        calculated_checksum = FileGenerator.calculate_file_checksum(file_path)
        
        # Assert
        self.assertIsNotNone(calculated_checksum)
        self.assertEqual(len(calculated_checksum), 64)  # SHA256 hex length
        
        # Verify checksum by calculating manually
        with open(file_path, 'rb') as f:
            content = f.read()
        expected_checksum = hashlib.sha256(content).hexdigest()
        self.assertEqual(calculated_checksum, expected_checksum)

    def test_verify_file_integrity(self):
        """Test file integrity verification"""
        # Arrange
        file_size = 2048
        file_path = os.path.join(self.temp_dir, "test_integrity.bin")
        
        # Act
        FileGenerator.generate_file(file_size, file_path)
        original_checksum = FileGenerator.calculate_file_checksum(file_path)
        is_valid = FileGenerator.verify_file_integrity(file_path, original_checksum)
        
        # Assert
        self.assertTrue(is_valid)

    def test_verify_corrupted_file(self):
        """Test verification of corrupted file"""
        # Arrange
        file_size = 1024
        file_path = os.path.join(self.temp_dir, "test_corrupted.bin")
        
        # Act
        FileGenerator.generate_file(file_size, file_path)
        
        # Corrupt the file
        with open(file_path, 'r+b') as f:
            f.seek(500)
            f.write(b'\x00\x00\x00\x00')
        
        # Use original checksum (which won't match)
        wrong_checksum = "a" * 64
        is_valid = FileGenerator.verify_file_integrity(file_path, wrong_checksum)
        
        # Assert
        self.assertFalse(is_valid)

    def test_invalid_file_path(self):
        """Test handling of invalid file path"""
        # Arrange
        invalid_path = "/invalid/path/test.bin"
        file_size = 1024
        
        # Act
        result = FileGenerator.generate_file(file_size, invalid_path)
        
        # Assert
        self.assertFalse(result)

    def test_zero_file_size(self):
        """Test handling of zero file size"""
        # Arrange
        file_size = 0
        file_path = os.path.join(self.temp_dir, "test_zero.bin")
        
        # Act
        result = FileGenerator.generate_file(file_size, file_path)
        
        # Assert
        self.assertTrue(result)
        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(os.path.getsize(file_path), 0)

    def test_negative_file_size(self):
        """Test handling of negative file size"""
        # Arrange
        file_size = -1024
        file_path = os.path.join(self.temp_dir, "test_negative.bin")
        
        # Act
        result = FileGenerator.generate_file(file_size, file_path)
        
        # Assert
        self.assertFalse(result)

    def test_get_random_content_patterns(self):
        """Test that generated content has random patterns"""
        # Arrange
        chunk_size = 1024
        
        # Act
        chunk1 = FileGenerator._generate_random_chunk(chunk_size)
        chunk2 = FileGenerator._generate_random_chunk(chunk_size)
        
        # Assert
        self.assertEqual(len(chunk1), chunk_size)
        self.assertEqual(len(chunk2), chunk_size)
        self.assertNotEqual(chunk1, chunk2)  # Should be different

    def test_performance_tracking(self):
        """Test performance tracking during file generation"""
        # Arrange
        file_size = 5 * 1024 * 1024  # 5MB
        file_path = os.path.join(self.temp_dir, "test_performance.bin")
        
        # Act
        start_time = FileGenerator._get_current_time()
        result = FileGenerator.generate_file(file_size, file_path, self.progress_callback)
        end_time = FileGenerator._get_current_time()
        
        # Assert
        self.assertTrue(result)
        duration = end_time - start_time
        
        # Should complete within reasonable time (less than 30 seconds for 5MB)
        self.assertLess(duration, 30.0)
        
        # Calculate rough speed (should be at least 100KB/s)
        speed_kb_per_sec = (file_size / 1024) / duration
        self.assertGreater(speed_kb_per_sec, 100)

    @patch('utils.file_generator.os.makedirs')
    def test_directory_creation(self, mock_makedirs):
        """Test that directories are created if they don't exist"""
        # Arrange
        nested_path = os.path.join(self.temp_dir, "nested", "path", "test.bin")
        file_size = 1024
        
        # Act
        FileGenerator.generate_file(file_size, nested_path)
        
        # Assert
        mock_makedirs.assert_called()

    def test_concurrent_file_generation(self):
        """Test generating multiple files concurrently (simulation)"""
        # Arrange
        file_paths = [
            os.path.join(self.temp_dir, f"concurrent_{i}.bin")
            for i in range(3)
        ]
        file_size = 1024 * 1024  # 1MB each
        
        # Act
        results = []
        for file_path in file_paths:
            result = FileGenerator.generate_file(file_size, file_path)
            results.append(result)
        
        # Assert
        self.assertTrue(all(results))
        for file_path in file_paths:
            self.assertTrue(os.path.exists(file_path))
            self.assertEqual(os.path.getsize(file_path), file_size)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)