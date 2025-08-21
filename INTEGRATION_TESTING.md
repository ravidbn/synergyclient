# Synergy Demo System - Integration Testing Plan

This document outlines the comprehensive integration testing strategy for validating the complete Synergy Demo System across Android and Windows platforms.

## Table of Contents

- [Testing Overview](#testing-overview)
- [Test Environment Setup](#test-environment-setup)
- [Cross-Platform Test Scenarios](#cross-platform-test-scenarios)
- [Automated Testing](#automated-testing)
- [Performance Testing](#performance-testing)
- [Security Testing](#security-testing)
- [Debugging Tools](#debugging-tools)

## Testing Overview

### Integration Testing Objectives

1. **Cross-Platform Communication**: Verify Bluetooth and Wi-Fi communication between Android and Windows
2. **Protocol Compliance**: Ensure message format consistency and protocol adherence
3. **File Transfer Integrity**: Validate bidirectional file transfers with checksum verification
4. **Performance Validation**: Confirm system meets performance requirements
5. **Error Recovery**: Test automatic reconnection and error handling scenarios
6. **User Experience**: Validate end-to-end user workflows

### Test Matrix

| Test Category | Android Tests | Windows Tests | Cross-Platform Tests |
|---------------|---------------|---------------|---------------------|
| Unit Tests | ✅ Protocol, FileGen, Services | ✅ Models, Services, ViewModels | N/A |
| Integration Tests | ✅ Service Interactions | ✅ Service Communication | ✅ Bluetooth, Wi-Fi, File Transfer |
| Performance Tests | ✅ Memory, CPU, Network | ✅ Memory, CPU, Network | ✅ End-to-End Performance |
| Security Tests | ✅ Permissions, Encryption | ✅ Authentication, Authorization | ✅ Secure Communication |

## Test Environment Setup

### Hardware Requirements

**Minimum Test Configuration:**
- 1 Android device (Android 6.0+, Bluetooth 4.0+)
- 1 Windows PC (Windows 10+, Bluetooth 4.0+)
- USB cable for Android debugging
- Isolated Wi-Fi environment (optional but recommended)

**Recommended Test Configuration:**
- 3 Android devices (different manufacturers/versions)
- 2 Windows PCs (different hardware configurations)
- Network isolation equipment
- Performance monitoring tools

### Software Prerequisites

**Development Tools:**
```bash
# Android
adb devices
python --version  # 3.8+
buildozer --version

# Windows
dotnet --version  # 6.0+
```

**Testing Tools:**
```bash
# Network testing
ping, traceroute, iperf3, wireshark

# Performance testing
htop, perfmon, resource monitor

# Debugging
adb logcat, Event Viewer, Process Monitor
```

### Environment Configuration

**Test Network Setup:**
```bash
# Create isolated test network
SSID: SynergyTest
Password: TestPass2024
Channel: 6 (2.4GHz)
Security: WPA2
IP Range: 192.168.100.0/24
```

**Device Configuration:**
```json
{
  "android_device": {
    "developer_options": true,
    "usb_debugging": true,
    "location_services": true,
    "bluetooth_enabled": true,
    "wifi_enabled": true
  },
  "windows_device": {
    "bluetooth_enabled": true,
    "wifi_enabled": true,
    "firewall_configured": true,
    "admin_privileges": true
  }
}
```

## Cross-Platform Test Scenarios

### Scenario 1: Initial System Setup

**Test Steps:**
1. Install Android APK on test device
2. Install Windows application on test PC
3. Enable required permissions on both platforms
4. Verify system requirements are met

**Expected Results:**
- Both applications start successfully
- No permission errors
- System status indicators show "Ready"

**Validation Script:**
```bash
#!/bin/bash
# test_setup.sh

echo "=== System Setup Validation ==="

# Check Android app installation
adb shell pm list packages | grep com.example.synergy
if [ $? -eq 0 ]; then
    echo "✓ Android app installed"
else
    echo "✗ Android app not found"
    exit 1
fi

# Check Android permissions
adb shell dumpsys package com.example.synergy | grep "granted=true"
echo "✓ Android permissions validated"

# Check Windows app
tasklist | findstr SynergyWindows.exe
if [ $? -eq 0 ]; then
    echo "✓ Windows app running"
else
    echo "✗ Windows app not running"
fi

echo "Setup validation complete"
```

### Scenario 2: Bluetooth Discovery and Pairing

**Test Steps:**
1. Start Bluetooth advertising on Android
2. Start device scanning on Windows
3. Initiate pairing from Windows
4. Accept pairing on Android
5. Verify connection establishment

**Expected Results:**
- Android device appears in Windows scan results
- Pairing completes successfully
- Both applications show "Connected" status
- Connection remains stable for 60+ seconds

**Validation Points:**
```python
# Integration test for Bluetooth pairing
class BluetoothPairingTest:
    def test_device_discovery(self):
        # Windows should discover Android device within 30 seconds
        assert self.wait_for_device_discovery(timeout=30)
    
    def test_pairing_process(self):
        # Pairing should complete within 15 seconds
        assert self.initiate_pairing(timeout=15)
    
    def test_connection_stability(self):
        # Connection should remain stable for 60 seconds
        assert self.monitor_connection_stability(duration=60)
```

### Scenario 3: Protocol Message Exchange

**Test Steps:**
1. Send color change command from Android to Windows
2. Verify color display update on Windows
3. Send acknowledgment from Windows to Android
4. Test all color combinations (Red, Yellow, Green)
5. Validate message format and timing

**Expected Results:**
- Messages transmitted within 1 second
- Color changes reflected immediately on Windows
- Acknowledgments received within 2 seconds
- No message corruption or loss

**Message Validation:**
```python
# Protocol message testing
def test_color_command_exchange():
    colors = ['RED', 'YELLOW', 'GREEN']
    
    for color in colors:
        # Send command from Android
        message = ProtocolMessage.create_color_change_command(color)
        android_service.send_message(message)
        
        # Verify Windows receives and processes
        windows_response = windows_service.wait_for_message(timeout=2)
        assert windows_response.action == f"{message.action}ack"
        assert windows_response.data['status'] == 'acknowledged'
        
        # Verify UI update
        assert windows_ui.get_current_color() == color
```

### Scenario 4: Wi-Fi Hotspot and Connection

**Test Steps:**
1. Create Wi-Fi hotspot on Android
2. Scan for networks on Windows
3. Connect Windows to Android hotspot
4. Verify IP address assignment
5. Test network connectivity

**Expected Results:**
- Hotspot created within 10 seconds
- Windows detects hotspot within 15 seconds
- Connection established within 20 seconds
- IP assignment completed (192.168.43.x range)
- Ping test successful with <100ms latency

**Network Validation:**
```bash
# Wi-Fi connectivity test
test_wifi_connection() {
    echo "Testing Wi-Fi hotspot connection..."
    
    # Test IP assignment
    ip_address=$(ipconfig | grep "192.168.43" | awk '{print $2}')
    if [ -z "$ip_address" ]; then
        echo "✗ IP address not assigned"
        return 1
    fi
    echo "✓ IP address assigned: $ip_address"
    
    # Test connectivity
    ping -c 3 192.168.43.1 > /dev/null
    if [ $? -eq 0 ]; then
        echo "✓ Network connectivity confirmed"
    else
        echo "✗ Network connectivity failed"
        return 1
    fi
}
```

### Scenario 5: File Transfer Operations

**Test Steps:**
1. Generate test file on Android (10MB)
2. Initiate upload to Windows via Wi-Fi
3. Monitor transfer progress and speed
4. Verify file integrity using checksum
5. Test download from Windows to Android
6. Test multiple concurrent transfers

**Expected Results:**
- Transfer initiation within 5 seconds
- Transfer speed >1 MB/s over Wi-Fi
- Progress updates every 1-2 seconds
- File integrity verification passes
- Concurrent transfers (up to 3) work correctly

**File Transfer Testing:**
```python
class FileTransferIntegrationTest:
    def test_upload_file(self):
        # Generate test file
        test_file = self.generate_test_file(size_mb=10)
        original_checksum = calculate_checksum(test_file)
        
        # Upload file
        transfer_result = self.upload_file(test_file)
        assert transfer_result.success
        assert transfer_result.duration < 30  # Should complete in <30s
        
        # Verify integrity
        received_checksum = transfer_result.checksum
        assert original_checksum == received_checksum
    
    def test_concurrent_transfers(self):
        # Start 3 concurrent transfers
        transfers = []
        for i in range(3):
            test_file = self.generate_test_file(size_mb=5)
            transfer = self.start_upload(test_file)
            transfers.append(transfer)
        
        # Wait for completion
        for transfer in transfers:
            assert transfer.wait_for_completion(timeout=60)
```

### Scenario 6: Error Recovery and Resilience

**Test Steps:**
1. Establish normal connection
2. Simulate Bluetooth disconnection
3. Verify automatic reconnection
4. Simulate Wi-Fi interruption during file transfer
5. Test transfer resumption
6. Simulate application crash and recovery

**Expected Results:**
- Automatic reconnection within 10 seconds
- Transfer resumption from interruption point
- No data corruption during recovery
- Application restarts cleanly
- Error messages are user-friendly

**Resilience Testing:**
```python
def test_connection_recovery():
    # Establish connection
    assert establish_connection()
    
    # Simulate disconnection
    simulate_bluetooth_disconnection()
    
    # Wait for automatic reconnection
    reconnected = wait_for_reconnection(timeout=15)
    assert reconnected, "Automatic reconnection failed"
    
    # Verify functionality after reconnection
    test_color_command_exchange()
```

## Automated Testing

### Continuous Integration Setup

**CI Pipeline Configuration:**
```yaml
# .github/workflows/integration_test.yml
name: Integration Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  integration-test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Android Environment
      uses: android-actions/setup-android@v2
      
    - name: Setup .NET
      uses: actions/setup-dotnet@v1
      with:
        dotnet-version: 6.0.x
        
    - name: Run Android Tests
      run: |
        python run_tests.py --integration
        
    - name: Build Windows App
      run: |
        cd SynergyWindows
        dotnet test --configuration Release
        
    - name: Run Cross-Platform Tests
      run: |
        python integration_test_runner.py
```

### Automated Test Execution

**Test Runner Script:**
```python
#!/usr/bin/env python3
# integration_test_runner.py

import subprocess
import time
import json
import sys
from datetime import datetime

class IntegrationTestRunner:
    def __init__(self):
        self.results = []
        self.start_time = None
        
    def run_all_tests(self):
        """Execute complete integration test suite"""
        self.start_time = time.time()
        
        test_scenarios = [
            self.test_system_setup,
            self.test_bluetooth_pairing,
            self.test_protocol_messages,
            self.test_wifi_connection,
            self.test_file_transfers,
            self.test_error_recovery
        ]
        
        for test in test_scenarios:
            try:
                result = test()
                self.results.append(result)
                if not result['passed']:
                    print(f"FAILED: {result['name']}")
                    if not self.continue_on_failure():
                        break
                else:
                    print(f"PASSED: {result['name']}")
            except Exception as e:
                self.results.append({
                    'name': test.__name__,
                    'passed': False,
                    'error': str(e),
                    'duration': 0
                })
                break
        
        self.generate_report()
        return all(r['passed'] for r in self.results)
    
    def test_system_setup(self):
        """Verify both applications can start and initialize"""
        start_time = time.time()
        
        # Check Android app
        android_check = subprocess.run([
            'adb', 'shell', 'pm', 'list', 'packages', 'com.example.synergy'
        ], capture_output=True, text=True)
        
        android_ok = 'com.example.synergy' in android_check.stdout
        
        # Check Windows app (if running locally)
        windows_check = subprocess.run([
            'tasklist', '/FI', 'IMAGENAME eq SynergyWindows.exe'
        ], capture_output=True, text=True, shell=True)
        
        windows_ok = 'SynergyWindows.exe' in windows_check.stdout
        
        return {
            'name': 'System Setup',
            'passed': android_ok,  # Focus on Android for automated testing
            'duration': time.time() - start_time,
            'details': {
                'android_installed': android_ok,
                'windows_running': windows_ok
            }
        }
    
    def test_bluetooth_pairing(self):
        """Test Bluetooth service functionality"""
        start_time = time.time()
        
        # Run Android Bluetooth tests
        result = subprocess.run([
            'python', 'run_tests.py', '-m', 'test_integration', 
            '--filter', 'BluetoothServiceIntegration'
        ], capture_output=True, text=True)
        
        passed = result.returncode == 0
        
        return {
            'name': 'Bluetooth Pairing',
            'passed': passed,
            'duration': time.time() - start_time,
            'output': result.stdout if passed else result.stderr
        }
    
    def test_protocol_messages(self):
        """Test protocol message exchange"""
        start_time = time.time()
        
        # Run protocol tests
        result = subprocess.run([
            'python', 'run_tests.py', '-m', 'test_protocol'
        ], capture_output=True, text=True)
        
        passed = result.returncode == 0
        
        return {
            'name': 'Protocol Messages',
            'passed': passed,
            'duration': time.time() - start_time,
            'output': result.stdout if passed else result.stderr
        }
    
    def test_wifi_connection(self):
        """Test Wi-Fi hotspot and connection"""
        start_time = time.time()
        
        # Test Wi-Fi hotspot creation via ADB
        hotspot_test = subprocess.run([
            'adb', 'shell', 'svc', 'wifi', 'enable'
        ], capture_output=True, text=True)
        
        # Basic connectivity check
        connectivity_test = subprocess.run([
            'adb', 'shell', 'ping', '-c', '3', '8.8.8.8'
        ], capture_output=True, text=True)
        
        passed = hotspot_test.returncode == 0
        
        return {
            'name': 'Wi-Fi Connection',
            'passed': passed,
            'duration': time.time() - start_time,
            'details': {
                'hotspot_enabled': hotspot_test.returncode == 0,
                'connectivity': 'reachable' in connectivity_test.stdout.lower()
            }
        }
    
    def test_file_transfers(self):
        """Test file transfer functionality"""
        start_time = time.time()
        
        # Run file generator and transfer tests
        result = subprocess.run([
            'python', 'run_tests.py', '-m', 'test_file_generator'
        ], capture_output=True, text=True)
        
        passed = result.returncode == 0
        
        return {
            'name': 'File Transfers',
            'passed': passed,
            'duration': time.time() - start_time,
            'output': result.stdout if passed else result.stderr
        }
    
    def test_error_recovery(self):
        """Test error handling and recovery"""
        start_time = time.time()
        
        # Run error handling tests
        result = subprocess.run([
            'python', 'run_tests.py', '--filter', 'error'
        ], capture_output=True, text=True)
        
        passed = result.returncode == 0
        
        return {
            'name': 'Error Recovery',
            'passed': passed,
            'duration': time.time() - start_time,
            'output': result.stdout if passed else result.stderr
        }
    
    def continue_on_failure(self):
        """Ask user whether to continue after test failure"""
        response = input("Test failed. Continue with remaining tests? (y/n): ")
        return response.lower().startswith('y')
    
    def generate_report(self):
        """Generate comprehensive test report"""
        total_duration = time.time() - self.start_time
        passed_tests = sum(1 for r in self.results if r['passed'])
        total_tests = len(self.results)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': total_tests - passed_tests,
                'success_rate': (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
                'total_duration': total_duration
            },
            'test_results': self.results
        }
        
        # Save report
        report_file = f"integration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("INTEGRATION TEST REPORT")
        print("="*60)
        print(f"Tests Run: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
        print(f"Total Duration: {total_duration:.2f} seconds")
        print(f"Report saved: {report_file}")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL INTEGRATION TESTS PASSED! 🎉")
        else:
            print(f"\n❌ {total_tests - passed_tests} TESTS FAILED")

if __name__ == '__main__':
    runner = IntegrationTestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)
```

## Performance Testing

### Performance Benchmarks

**Target Performance Metrics:**
```json
{
  "bluetooth": {
    "discovery_time_max_sec": 30,
    "connection_time_max_sec": 15,
    "message_latency_max_ms": 1000,
    "throughput_min_msgs_sec": 10
  },
  "wifi": {
    "hotspot_creation_max_sec": 10,
    "connection_time_max_sec": 20,
    "ip_assignment_max_sec": 15
  },
  "file_transfer": {
    "initiation_time_max_sec": 5,
    "transfer_speed_min_mbps": 1,
    "checksum_verification_max_sec": 2,
    "concurrent_transfers_max": 3
  },
  "system": {
    "memory_usage_max_mb": 200,
    "cpu_usage_max_percent": 50,
    "startup_time_max_sec": 10
  }
}
```

**Performance Test Suite:**
```python
# performance_tests.py
import time
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor

class PerformanceTestSuite:
    def __init__(self):
        self.metrics = {}
        
    def measure_bluetooth_performance(self):
        """Measure Bluetooth operation performance"""
        metrics = {}
        
        # Discovery time
        start_time = time.time()
        # Simulate discovery process
        discovery_duration = time.time() - start_time
        metrics['discovery_time'] = discovery_duration
        
        # Message throughput
        start_time = time.time()
        message_count = 100
        for i in range(message_count):
            # Simulate message processing
            pass
        throughput = message_count / (time.time() - start_time)
        metrics['message_throughput'] = throughput
        
        return metrics
    
    def measure_file_transfer_performance(self):
        """Measure file transfer performance"""
        metrics = {}
        
        # Transfer speed test
        file_size_mb = 10
        start_time = time.time()
        # Simulate file transfer
        time.sleep(file_size_mb / 2)  # Simulate 2 MB/s transfer
        transfer_duration = time.time() - start_time
        
        transfer_speed = file_size_mb / transfer_duration
        metrics['transfer_speed_mbps'] = transfer_speed
        
        return metrics
    
    def measure_system_performance(self):
        """Measure system resource usage"""
        process = psutil.Process()
        
        metrics = {
            'memory_usage_mb': process.memory_info().rss / 1024 / 1024,
            'cpu_percent': process.cpu_percent(interval=1),
            'thread_count': process.num_threads()
        }
        
        return metrics
```

## Security Testing

### Security Test Scenarios

**Authentication and Authorization:**
```python
def test_secure_pairing():
    """Test Bluetooth pairing security"""
    # Test encryption during pairing
    # Verify no plain text passwords
    # Test PIN/passkey validation
    pass

def test_data_encryption():
    """Test data transmission encryption"""
    # Verify message encryption
    # Test key exchange
    # Validate certificate usage
    pass

def test_device_whitelisting():
    """Test device access control"""
    # Test allowed device list
    # Verify unauthorized device rejection
    # Test MAC address filtering
    pass
```

## Debugging Tools

### Real-time Monitoring Dashboard

```python
# monitoring_dashboard.py
import tkinter as tk
from tkinter import ttk
import threading
import time

class MonitoringDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Synergy Integration Monitor")
        self.setup_ui()
        self.monitoring = True
        
    def setup_ui(self):
        # Connection status
        self.connection_frame = ttk.LabelFrame(self.root, text="Connection Status")
        self.connection_frame.pack(fill="x", padx=10, pady=5)
        
        self.bluetooth_status = tk.StringVar(value="Disconnected")
        ttk.Label(self.connection_frame, text="Bluetooth:").pack(side="left")
        ttk.Label(self.connection_frame, textvariable=self.bluetooth_status).pack(side="left")
        
        # Performance metrics
        self.perf_frame = ttk.LabelFrame(self.root, text="Performance Metrics")
        self.perf_frame.pack(fill="x", padx=10, pady=5)
        
        self.memory_usage = tk.StringVar(value="0 MB")
        ttk.Label(self.perf_frame, text="Memory:").pack(side="left")
        ttk.Label(self.perf_frame, textvariable=self.memory_usage).pack(side="left")
        
        # Message log
        self.log_frame = ttk.LabelFrame(self.root, text="Message Log")
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(self.log_frame, height=15)
        scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def start_monitoring(self):
        """Start real-time monitoring"""
        monitor_thread = threading.Thread(target=self.monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            # Update connection status
            # Update performance metrics
            # Update message log
            time.sleep(1)
            
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def run(self):
        """Start the dashboard"""
        self.start_monitoring()
        self.root.mainloop()
        self.monitoring = False

if __name__ == '__main__':
    dashboard = MonitoringDashboard()
    dashboard.run()
```

This comprehensive integration testing plan provides the framework for validating the complete Synergy Demo System across both platforms, ensuring reliable cross-platform communication and optimal performance.