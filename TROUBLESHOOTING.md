# Synergy Demo System - Troubleshooting Guide

This comprehensive troubleshooting guide helps resolve common issues encountered during setup, deployment, and operation of the Synergy Demo System.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Android Issues](#android-issues)
- [Windows Issues](#windows-issues)
- [Communication Issues](#communication-issues)
- [Performance Issues](#performance-issues)
- [Advanced Diagnostics](#advanced-diagnostics)
- [Error Codes Reference](#error-codes-reference)

## Quick Diagnostics

### System Health Check

**Before starting troubleshooting, run these quick checks:**

1. **Android Device Check**
   ```bash
   adb devices  # Verify device is connected
   adb shell dumpsys bluetooth | grep -i "state"
   adb shell dumpsys wifi | grep -i "state"
   ```

2. **Windows System Check**
   ```powershell
   Get-Service bthserv | Select Status
   Get-NetAdapter | Where-Object {$_.MediaType -eq "802.11"}
   netstat -an | findstr ":8888"
   ```

3. **Network Connectivity**
   ```bash
   ping 192.168.43.1  # Default Android hotspot IP
   telnet 192.168.43.1 8888  # Test file transfer port
   ```

### Common Issues Quick Fix

| Issue | Quick Fix |
|-------|-----------|
| Bluetooth not working | Restart Bluetooth service on both devices |
| Wi-Fi hotspot not visible | Check location services on Android |
| File transfer fails | Verify firewall settings |
| App crashes on startup | Clear app data and restart |
| Connection timeout | Check device compatibility and distance |

## Android Issues

### Installation Problems

**Issue: APK Installation Fails**
```bash
# Check if device is properly connected
adb devices

# Install with additional flags
adb install -r -d synergy-demo.apk

# If still failing, try:
adb uninstall com.example.synergy
adb install synergy-demo.apk
```

**Issue: Build Errors with Buildozer**
```bash
# Clean build environment
buildozer android clean

# Update buildozer
pip install --upgrade buildozer

# Check Android SDK/NDK versions in buildozer.spec
[app]
android.api = 30
android.minapi = 21
android.ndk = 25b

# Rebuild
buildozer android debug
```

**Error: "Command failed: ant clean debug"**
```bash
# Fix permissions
chmod +x ~/.buildozer/android/platform/apache-ant-*/bin/ant

# Or reinstall ant
sudo apt-get remove ant
sudo apt-get install ant
```

### Runtime Issues

**Issue: Bluetooth Permission Denied**
- **Cause**: Missing Bluetooth permissions
- **Solution**: 
  1. Go to Android Settings → Apps → Synergy Demo → Permissions
  2. Enable "Location" and "Nearby devices" permissions
  3. For Android 12+, also enable "Bluetooth" permission specifically

**Issue: Wi-Fi Hotspot Creation Fails**
- **Symptoms**: "Failed to create hotspot" error message
- **Causes & Solutions**:

  1. **Location Services Disabled**
     ```bash
     # Enable via ADB
     adb shell settings put secure location_providers_allowed +gps
     adb shell settings put secure location_providers_allowed +network
     ```

  2. **Insufficient Permissions**
     ```xml
     <!-- Ensure these permissions in AndroidManifest.xml -->
     <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
     <uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
     <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
     ```

  3. **Device Restrictions**
     - Some devices don't support programmatic hotspot control
     - Enable hotspot manually in Android settings as workaround

**Issue: App Crashes with PyJNIus Errors**
```python
# Add error handling in wifi_hotspot_service.py
try:
    from jnius import autoclass
    Context = autoclass('android.content.Context')
    WifiManager = autoclass('android.net.wifi.WifiManager')
except ImportError as e:
    print(f"PyJNIus import failed: {e}")
    # Fallback to manual hotspot instructions
```

**Issue: File Generation Extremely Slow**
```python
# Optimize file_generator.py
class FileGenerator:
    @staticmethod
    def _generate_random_chunk(size):
        # Use os.urandom for better performance
        return os.urandom(size)
    
    @staticmethod 
    def generate_file(file_size, file_path, progress_callback=None):
        # Increase chunk size for better performance
        chunk_size = min(1024 * 1024, file_size)  # 1MB chunks
        # ... rest of implementation
```

### Performance Issues

**Issue: High Memory Usage**
```python
# Add memory monitoring in main.py
import psutil
import gc

class MemoryMonitor:
    def check_memory(self):
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        if memory_mb > 500:  # 500MB threshold
            gc.collect()  # Force garbage collection
            print(f"Memory usage: {memory_mb:.1f}MB - GC triggered")
```

## Windows Issues

### Installation Problems

**Issue: .NET Runtime Not Found**
```bash
# Check installed .NET versions
dotnet --list-runtimes

# Install .NET 6.0 if missing
winget install Microsoft.DotNet.Runtime.6
```

**Issue: Build Fails with Package Restore Errors**
```bash
# Clear NuGet cache
dotnet nuget locals all --clear

# Restore packages
dotnet restore --force

# If specific package fails
dotnet add package Microsoft.Toolkit.Mvvm --version 7.1.2
```

**Issue: Access Denied During Installation**
- Run installer/application as Administrator
- Check Windows SmartScreen settings
- Disable Windows Defender temporarily during installation

### Runtime Issues

**Issue: Bluetooth Service Unavailable**
```powershell
# Check Bluetooth service status
Get-Service bthserv

# Restart Bluetooth service
Restart-Service bthserv

# If service is disabled
Set-Service bthserv -StartupType Automatic
Start-Service bthserv
```

**Issue: Cannot Discover Android Device**
- **Solution 1**: Clear Bluetooth cache
  ```powershell
  # Remove paired devices
  Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.Name -like "*Bluetooth*"} | ForEach-Object {$_.Disable()}
  Start-Sleep 5
  Get-WmiObject -Class Win32_PnPEntity | Where-Object {$_.Name -like "*Bluetooth*"} | ForEach-Object {$_.Enable()}
  ```

- **Solution 2**: Reset Bluetooth stack
  ```cmd
  # Run as Administrator
  net stop bthserv
  net start bthserv
  ```

**Issue: Wi-Fi Connection Fails**
```powershell
# Check Wi-Fi adapter status
Get-NetAdapter | Where-Object {$_.MediaType -eq "802.11"}

# Reset Wi-Fi adapter
Disable-NetAdapter -Name "Wi-Fi"
Enable-NetAdapter -Name "Wi-Fi"

# Forget and reconnect to network
netsh wlan delete profile name="SynergyDemo"
netsh wlan connect name="SynergyDemo"
```

**Issue: File Transfer Port Blocked**
```powershell
# Check if port is in use
netstat -an | findstr ":8888"

# Add firewall exception
New-NetFirewallRule -DisplayName "Synergy Demo" -Direction Inbound -Port 8888 -Protocol TCP -Action Allow

# Test port connectivity
Test-NetConnection -ComputerName 192.168.43.1 -Port 8888
```

### Application Errors

**Issue: WPF XAML Binding Errors**
```xml
<!-- Add error handling in MainWindow.xaml -->
<Window.Resources>
    <Style TargetType="{x:Type TextBlock}">
        <Style.Triggers>
            <DataTrigger Binding="{Binding Path=., Converter={x:Static converters:IsNullConverter.Instance}}" Value="True">
                <Setter Property="Text" Value="Loading..." />
            </DataTrigger>
        </Style.Triggers>
    </Style>
</Window.Resources>
```

**Issue: Service Injection Fails**
```csharp
// Add error handling in App.xaml.cs
protected override void OnStartup(StartupEventArgs e)
{
    try
    {
        ConfigureServices();
        base.OnStartup(e);
    }
    catch (Exception ex)
    {
        MessageBox.Show($"Application startup failed: {ex.Message}", 
                       "Startup Error", MessageBoxButton.OK, MessageBoxImage.Error);
        Environment.Exit(1);
    }
}
```

## Communication Issues

### Bluetooth Connection Problems

**Issue: Pairing Fails**
1. **Check Compatibility**
   - Ensure both devices support Bluetooth Classic (not just BLE)
   - Verify Android device supports RFCOMM protocol

2. **Clear Bluetooth Cache**
   ```bash
   # Android
   adb shell pm clear com.android.bluetooth
   
   # Windows
   # Go to Device Manager → Bluetooth → Uninstall device → Scan for changes
   ```

3. **Manual Pairing Process**
   - Pair devices through system Bluetooth settings first
   - Then use application for communication

**Issue: Connection Drops Frequently**
```python
# Implement connection monitoring in bluetooth_service.py
class BluetoothService:
    def __init__(self):
        self.connection_monitor = threading.Thread(target=self._monitor_connection)
        self.connection_monitor.daemon = True
        self.connection_monitor.start()
    
    def _monitor_connection(self):
        while self.is_running:
            if not self._is_connection_alive():
                self._attempt_reconnection()
            time.sleep(5)
```

**Issue: Message Transmission Errors**
```python
# Add retry logic in protocol handling
class ProtocolMessage:
    @staticmethod
    def send_with_retry(socket, message, max_retries=3):
        for attempt in range(max_retries):
            try:
                socket.send(message.encode('utf-8'))
                return True
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(0.5)
        return False
```

### Wi-Fi Network Issues

**Issue: Windows Cannot Connect to Android Hotspot**
1. **Check Hotspot Settings**
   ```python
   # Verify hotspot configuration in wifi_hotspot_service.py
   HOTSPOT_CONFIG = {
       'ssid': 'SynergyDemo',
       'password': 'SynergyDemo2024',  # At least 8 characters
       'security': 'WPA2',
       'band': '2.4GHz'  # Use 2.4GHz for better compatibility
   }
   ```

2. **Network Profile Issues**
   ```powershell
   # Remove old network profiles
   netsh wlan show profiles
   netsh wlan delete profile name="SynergyDemo"
   
   # Manually connect
   netsh wlan connect name="SynergyDemo"
   ```

**Issue: IP Address Assignment Problems**
```bash
# Check DHCP on Android
adb shell dumpsys connectivity | grep -i dhcp

# Windows IP configuration
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

### File Transfer Issues

**Issue: Transfer Starts but Fails Midway**
```csharp
// Add robust error handling in FileTransferService.cs
public async Task<bool> TransferFileAsync(string filePath)
{
    const int maxRetries = 3;
    for (int retry = 0; retry < maxRetries; retry++)
    {
        try
        {
            await TransferFileInternal(filePath);
            return true;
        }
        catch (SocketException ex) when (retry < maxRetries - 1)
        {
            await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, retry))); // Exponential backoff
        }
    }
    return false;
}
```

**Issue: Checksum Verification Fails**
```python
# Ensure consistent checksum calculation
import hashlib

def calculate_file_checksum(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read in chunks to handle large files
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()
```

## Performance Issues

### Memory Leaks

**Android Memory Monitoring**
```python
# Add to main.py
import tracemalloc

class MemoryProfiler:
    def __init__(self):
        tracemalloc.start()
    
    def take_snapshot(self):
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        
        for stat in top_stats[:10]:
            print(f"{stat.traceback.format()}: {stat.size_diff / 1024:.1f} KB")
```

**Windows Memory Monitoring**
```csharp
// Add to MainViewModel.cs
public class PerformanceMonitor
{
    private readonly Timer _memoryTimer;
    
    public PerformanceMonitor()
    {
        _memoryTimer = new Timer(CheckMemoryUsage, null, TimeSpan.Zero, TimeSpan.FromMinutes(1));
    }
    
    private void CheckMemoryUsage(object state)
    {
        var process = Process.GetCurrentProcess();
        var memoryMB = process.WorkingSet64 / 1024 / 1024;
        
        if (memoryMB > 200) // 200MB threshold
        {
            GC.Collect();
            GC.WaitForPendingFinalizers();
            GC.Collect();
        }
    }
}
```

### Slow File Transfers

**Network Optimization**
```python
# Optimize TCP settings in file_transfer_service.py
import socket

def optimize_socket(sock):
    # Disable Nagle's algorithm for low latency
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    # Increase buffer sizes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)  # 1MB
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)  # 1MB
```

**Concurrent Transfer Optimization**
```csharp
// Limit concurrent operations in FileTransferService.cs
private readonly SemaphoreSlim _transferSemaphore = new SemaphoreSlim(3); // Max 3 concurrent

public async Task TransferFileAsync(string filePath)
{
    await _transferSemaphore.WaitAsync();
    try
    {
        await DoTransferAsync(filePath);
    }
    finally
    {
        _transferSemaphore.Release();
    }
}
```

## Advanced Diagnostics

### Logging Configuration

**Android Enhanced Logging**
```python
# Create enhanced_logger.py
import logging
import os
from datetime import datetime

class EnhancedLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.setup_handlers()
    
    def setup_handlers(self):
        # File handler with rotation
        log_dir = "/sdcard/Android/data/com.example.synergy/files/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(
            os.path.join(log_dir, f"synergy_{datetime.now().strftime('%Y%m%d')}.log")
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.DEBUG)
```

**Windows Advanced Logging**
```csharp
// Enhanced logging in LoggingService.cs
public class LoggingService
{
    private readonly ILogger<LoggingService> _logger;
    private readonly string _logPath;
    
    public LoggingService(ILogger<LoggingService> logger)
    {
        _logger = logger;
        _logPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "SynergyWindows", "logs");
        
        Directory.CreateDirectory(_logPath);
    }
    
    public void LogDetailed(LogLevel level, string category, string message, object data = null)
    {
        var logEntry = new
        {
            Timestamp = DateTime.UtcNow,
            Level = level.ToString(),
            Category = category,
            Message = message,
            Data = data,
            ThreadId = Thread.CurrentThread.ManagedThreadId,
            MemoryUsage = GC.GetTotalMemory(false)
        };
        
        var json = JsonSerializer.Serialize(logEntry, new JsonSerializerOptions { WriteIndented = true });
        File.AppendAllText(Path.Combine(_logPath, $"detailed_{DateTime.Now:yyyyMMdd}.json"), json + "\n");
    }
}
```

### Network Traffic Analysis

**Packet Capture Analysis**
```bash
# Capture Bluetooth traffic (Linux/Android)
sudo btmon > bluetooth_capture.log

# Analyze Wi-Fi traffic
sudo tcpdump -i wlan0 -w wifi_capture.pcap host 192.168.43.1

# Windows: Use Wireshark or netsh
netsh trace start capture=yes provider=Microsoft-Windows-WLAN-AutoConfig
```

### System Resource Monitoring

**Comprehensive System Monitor**
```python
# system_monitor.py
import psutil
import time
import json

class SystemMonitor:
    def __init__(self):
        self.metrics = []
    
    def collect_metrics(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        metrics = {
            'timestamp': time.time(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_mb': memory.available / 1024 / 1024,
            'disk_percent': disk.percent,
            'network_bytes_sent': network.bytes_sent,
            'network_bytes_recv': network.bytes_recv
        }
        
        self.metrics.append(metrics)
        return metrics
    
    def export_metrics(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.metrics, f, indent=2)
```

## Error Codes Reference

### Android Error Codes

| Code | Category | Description | Solution |
|------|----------|-------------|----------|
| BT_001 | Bluetooth | Adapter not available | Enable Bluetooth in system settings |
| BT_002 | Bluetooth | Permission denied | Grant Bluetooth permissions |
| BT_003 | Bluetooth | Connection timeout | Check device compatibility and range |
| BT_004 | Bluetooth | Pairing failed | Clear Bluetooth cache and retry |
| WIFI_001 | Wi-Fi | Hotspot creation failed | Enable location services |
| WIFI_002 | Wi-Fi | Permission denied | Grant location and Wi-Fi permissions |
| WIFI_003 | Wi-Fi | Device not supported | Use manual hotspot setup |
| FILE_001 | File Transfer | Server start failed | Check port availability |
| FILE_002 | File Transfer | Transfer interrupted | Verify network stability |
| FILE_003 | File Transfer | Checksum mismatch | Retry transfer with error correction |

### Windows Error Codes

| Code | Category | Description | Solution |
|------|----------|-------------|----------|
| WIN_BT_001 | Bluetooth | Service unavailable | Restart Bluetooth service |
| WIN_BT_002 | Bluetooth | Device not found | Check device is discoverable |
| WIN_BT_003 | Bluetooth | Connection refused | Verify device pairing |
| WIN_WIFI_001 | Wi-Fi | Adapter disabled | Enable Wi-Fi adapter |
| WIN_WIFI_002 | Wi-Fi | Network not found | Check hotspot is active |
| WIN_WIFI_003 | Wi-Fi | Authentication failed | Verify password |
| WIN_FILE_001 | File Transfer | Port blocked | Configure firewall |
| WIN_FILE_002 | File Transfer | Access denied | Run as administrator |

### System Error Codes

| Code | Category | Description | Solution |
|------|----------|-------------|----------|
| SYS_001 | System | Out of memory | Close other applications |
| SYS_002 | System | Disk space low | Free up storage space |
| SYS_003 | System | Permission denied | Check user permissions |
| SYS_004 | System | Service timeout | Restart affected service |

## Getting Additional Help

### Log Collection Script

```bash
#!/bin/bash
# collect_support_logs.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SUPPORT_DIR="support_logs_$TIMESTAMP"

mkdir -p $SUPPORT_DIR

# Android logs
adb logcat -d > $SUPPORT_DIR/android_logcat.txt
adb shell dumpsys > $SUPPORT_DIR/android_dumpsys.txt
adb shell getprop > $SUPPORT_DIR/android_properties.txt

# Windows logs (run in PowerShell as Administrator)
Get-WinEvent -LogName Application -MaxEvents 1000 | Export-Csv $SUPPORT_DIR/windows_app_events.csv
Get-WinEvent -LogName System -MaxEvents 1000 | Export-Csv $SUPPORT_DIR/windows_system_events.csv

# Network information
ipconfig /all > $SUPPORT_DIR/network_config.txt
netstat -an > $SUPPORT_DIR/network_connections.txt

# Create archive
tar -czf support_logs_$TIMESTAMP.tar.gz $SUPPORT_DIR/
echo "Support logs collected: support_logs_$TIMESTAMP.tar.gz"
```

### Remote Support Access

For advanced troubleshooting, the applications include remote diagnostic capabilities:

1. **Enable Remote Diagnostics** in application settings
2. **Generate Support Code** from help menu
3. **Share Support Code** with technical support team
4. **Follow Remote Instructions** provided by support

### Community Support

- **GitHub Issues**: Report bugs and feature requests
- **Documentation Wiki**: Community-maintained troubleshooting tips
- **Developer Forum**: Technical discussions and solutions
- **Video Tutorials**: Step-by-step troubleshooting guides

Remember to always include relevant log files and system information when seeking support.