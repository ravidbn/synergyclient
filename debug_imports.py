"""
Debug script to test service imports and see what's available in the APK.
This will help us understand exactly why the imports are failing.
"""

import sys
import os

print("=== DEBUG IMPORT TESTING ===")
print(f"Python path: {sys.path}")
print(f"Current working directory: {os.getcwd()}")
print("")

# List all Python files in current directory
print("=== FILES IN CURRENT DIRECTORY ===")
try:
    files = [f for f in os.listdir('.') if f.endswith('.py')]
    for f in sorted(files):
        print(f"Found: {f}")
    print("")
except Exception as e:
    print(f"Error listing files: {e}")

# Test individual imports with detailed error info
print("=== TESTING SERVICE IMPORTS ===")

# Test bluetooth_service_mock import
print("1. Testing bluetooth_service_mock import...")
try:
    import bluetooth_service_mock
    print("✅ bluetooth_service_mock imported successfully")
    print(f"   Location: {bluetooth_service_mock.__file__}")
except ImportError as e:
    print(f"❌ bluetooth_service_mock import failed: {e}")
except Exception as e:
    print(f"❌ bluetooth_service_mock other error: {e}")

# Test bluetooth_service import
print("2. Testing bluetooth_service import...")
try:
    import bluetooth_service
    print("✅ bluetooth_service imported successfully")
    print(f"   Location: {bluetooth_service.__file__}")
except ImportError as e:
    print(f"❌ bluetooth_service import failed: {e}")
except Exception as e:
    print(f"❌ bluetooth_service other error: {e}")

# Test wifi services
print("3. Testing wifi_hotspot_service_mock import...")
try:
    import wifi_hotspot_service_mock
    print("✅ wifi_hotspot_service_mock imported successfully")
except ImportError as e:
    print(f"❌ wifi_hotspot_service_mock import failed: {e}")

print("4. Testing wifi_hotspot_service import...")
try:
    import wifi_hotspot_service
    print("✅ wifi_hotspot_service imported successfully")
except ImportError as e:
    print(f"❌ wifi_hotspot_service import failed: {e}")

# Test file services
print("5. Testing file_transfer_service_mock import...")
try:
    import file_transfer_service_mock
    print("✅ file_transfer_service_mock imported successfully")
except ImportError as e:
    print(f"❌ file_transfer_service_mock import failed: {e}")

print("6. Testing file_transfer_service import...")
try:
    import file_transfer_service
    print("✅ file_transfer_service imported successfully")
except ImportError as e:
    print(f"❌ file_transfer_service import failed: {e}")

# Test utils module
print("7. Testing utils.protocol import...")
try:
    from utils.protocol import ColorType
    print("✅ utils.protocol imported successfully")
except ImportError as e:
    print(f"❌ utils.protocol import failed: {e}")

# Test jnius (Android API)
print("8. Testing jnius import...")
try:
    from jnius import autoclass
    print("✅ jnius imported successfully")
except ImportError as e:
    print(f"❌ jnius import failed: {e}")

print("")
print("=== DEBUG COMPLETE ===")
print("This output will help identify exactly which files are missing from the APK.")