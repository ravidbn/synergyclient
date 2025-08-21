# Synergy Demo System - Deployment Guide

This guide provides step-by-step instructions for deploying the Synergy Demo System in various environments.

## Table of Contents

- [Quick Start](#quick-start)
- [Development Deployment](#development-deployment)
- [Production Deployment](#production-deployment)
- [Enterprise Deployment](#enterprise-deployment)
- [Configuration Management](#configuration-management)
- [Security Considerations](#security-considerations)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Quick Start

### For Developers (5-Minute Setup)

**Prerequisites:**
- Android device with developer options enabled
- Windows 10/11 PC
- USB cable for Android device

**Steps:**

1. **Download Pre-built Applications**
   ```bash
   # Download from releases page or build locally
   curl -L -o synergy-android.apk [release-url]
   curl -L -o synergy-windows.zip [release-url]
   ```

2. **Install Android App**
   ```bash
   adb install synergy-android.apk
   ```

3. **Run Windows App**
   ```bash
   unzip synergy-windows.zip
   cd synergy-windows
   ./SynergyWindows.exe
   ```

4. **Quick Pairing**
   - Enable Bluetooth on both devices
   - Launch both applications
   - Follow on-screen pairing instructions

### For End Users (Demo Setup)

1. **Android Setup**
   - Install APK from provided source
   - Grant all requested permissions
   - Enable location services for Wi-Fi hotspot

2. **Windows Setup**
   - Extract Windows application to desired folder
   - Run as administrator for first-time setup
   - Allow through Windows Firewall if prompted

3. **Demo Workflow**
   - Start Android app → Start Windows app
   - Pair devices via Bluetooth
   - Test color commands
   - Demonstrate file transfer

## Development Deployment

### Android Development Environment

**Environment Setup:**
```bash
# Clone repository
git clone https://github.com/your-org/synergy-demo.git
cd synergy-demo

# Setup Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install development tools
pip install buildozer
```

**Development Workflow:**
```bash
# Run tests
python run_tests.py

# Build debug APK
buildozer android debug

# Deploy to connected device
buildozer android debug deploy

# View logs
adb logcat | grep -i synergy
```

**Hot Reload Development:**
```bash
# For UI development (limited Android APIs)
python main.py

# For full development with device
buildozer android debug deploy run logcat
```

### Windows Development Environment

**Visual Studio Setup:**
1. Install Visual Studio 2022 with .NET desktop development workload
2. Install .NET 6.0 SDK
3. Clone repository and open `SynergyWindows.sln`

**Command Line Development:**
```bash
cd SynergyWindows

# Restore packages
dotnet restore

# Build and run
dotnet run

# Run tests
dotnet test

# Publish for distribution
dotnet publish -c Release -r win10-x64 --self-contained
```

**Development Configuration:**
```xml
<!-- appsettings.Development.json -->
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "SynergyWindows": "Trace"
    }
  },
  "Bluetooth": {
    "ScanTimeoutMs": 30000,
    "ConnectionTimeoutMs": 10000
  },
  "FileTransfer": {
    "DefaultPort": 8888,
    "ChunkSize": 8192
  }
}
```

## Production Deployment

### Android Production Build

**Signing Configuration:**
```ini
# buildozer.spec
[app]
version = 1.0.0
version.regex = __version__ = ['"](.+)['"]
version.filename = %(source.dir)s/main.py

[buildozer]
log_level = 1

# Release keystore
android.release_artifact = aab
android.release_artifact = apk
android.debug_keystore = ~/.android/debug.keystore
android.release_keystore = /path/to/release.keystore
android.release_keystore_passwd = your_password
android.release_key_alias = your_alias
android.release_key_passwd = your_key_password
```

**Build Process:**
```bash
# Clean previous builds
buildozer android clean

# Build signed release
buildozer android release

# Verify APK
aapt dump badging bin/synergydemo-*-release.apk
```

**Distribution:**
- Upload to Google Play Store
- Distribute via MDM (Mobile Device Management)
- Side-load for enterprise deployment

### Windows Production Build

**Release Configuration:**
```xml
<!-- SynergyWindows.csproj -->
<PropertyGroup Condition="'$(Configuration)' == 'Release'">
  <DebugType>none</DebugType>
  <DebugSymbols>false</DebugSymbols>
  <Optimize>true</Optimize>
  <DefineConstants>RELEASE</DefineConstants>
</PropertyGroup>
```

**Build and Package:**
```bash
# Clean and build
dotnet clean
dotnet build -c Release

# Create self-contained package
dotnet publish -c Release -r win10-x64 --self-contained true -p:PublishSingleFile=true

# Create installer (using WiX or Inno Setup)
# See installer-scripts/ directory for examples
```

**Distribution Options:**
1. **Standalone Executable**: Single .exe file with all dependencies
2. **MSI Installer**: Windows Installer package for enterprise deployment
3. **MSIX Package**: Modern Windows packaging format
4. **ClickOnce**: Web-based deployment for automatic updates

## Enterprise Deployment

### System Requirements

**Network Infrastructure:**
- Bluetooth 4.0+ support on all devices
- Wi-Fi infrastructure (if not using mobile hotspot)
- Firewall configuration for TCP ports 8888-8890
- Network segmentation for demo environment

**Device Requirements:**
- **Android**: Minimum 50 devices for large demos
- **Windows**: Minimum 10 PCs for demonstration stations
- **IT Support**: Device management and troubleshooting

### Mass Deployment

**Android Device Management:**
```bash
# MDM deployment script
#!/bin/bash
ADB_DEVICES=$(adb devices | grep -v "List" | awk '{print $1}')

for device in $ADB_DEVICES; do
    echo "Installing on device: $device"
    adb -s $device install -r synergy-demo.apk
    adb -s $device shell am start -n com.example.synergy/.MainActivity
done
```

**Windows Group Policy Deployment:**
```powershell
# PowerShell deployment script
$computers = Get-ADComputer -Filter * -SearchBase "OU=DemoStations,DC=company,DC=com"

foreach ($computer in $computers) {
    $session = New-PSSession -ComputerName $computer.Name
    
    Invoke-Command -Session $session -ScriptBlock {
        # Copy installation files
        Copy-Item "\\server\share\synergy-windows.msi" -Destination "C:\Temp\"
        
        # Install application
        Start-Process msiexec.exe -ArgumentList "/i C:\Temp\synergy-windows.msi /quiet" -Wait
        
        # Configure firewall
        New-NetFirewallRule -DisplayName "Synergy Demo" -Direction Inbound -Port 8888-8890 -Protocol TCP -Action Allow
    }
    
    Remove-PSSession $session
}
```

### Configuration Management

**Centralized Configuration:**
```json
{
  "deployment": {
    "environment": "enterprise",
    "auto_pairing": true,
    "demo_mode": true,
    "file_transfer_enabled": true,
    "max_file_size_mb": 100,
    "allowed_devices": ["*"],
    "logging_level": "info"
  },
  "bluetooth": {
    "scan_timeout_seconds": 30,
    "connection_timeout_seconds": 15,
    "auto_reconnect": true
  },
  "wifi": {
    "hotspot_ssid_prefix": "SynergyDemo",
    "hotspot_password": "Demo2024!",
    "preferred_channel": 6
  },
  "security": {
    "encryption_enabled": true,
    "certificate_validation": true,
    "allowed_ip_ranges": ["192.168.0.0/16", "10.0.0.0/8"]
  }
}
```

**Device Provisioning:**
```bash
# Android provisioning
adb shell settings put global development_settings_enabled 1
adb shell settings put secure install_non_market_apps 1
adb shell settings put global bluetooth_on 1
adb shell settings put global wifi_on 1

# Push configuration
adb push enterprise-config.json /sdcard/Android/data/com.example.synergy/files/
```

## Configuration Management

### Environment-Specific Configuration

**Development Environment:**
```json
{
  "bluetooth": {
    "scan_timeout": 60000,
    "debug_logging": true,
    "mock_devices": true
  },
  "file_transfer": {
    "chunk_size": 4096,
    "enable_compression": false
  },
  "ui": {
    "show_debug_info": true,
    "enable_developer_menu": true
  }
}
```

**Production Environment:**
```json
{
  "bluetooth": {
    "scan_timeout": 30000,
    "debug_logging": false,
    "mock_devices": false
  },
  "file_transfer": {
    "chunk_size": 65536,
    "enable_compression": true
  },
  "ui": {
    "show_debug_info": false,
    "enable_developer_menu": false
  }
}
```

### Runtime Configuration

**Android Configuration Override:**
```python
# config_manager.py
import json
import os

class ConfigManager:
    def __init__(self):
        self.config_path = "/sdcard/Android/data/com.example.synergy/files/config.json"
        self.default_config = {
            "bluetooth_timeout": 30000,
            "file_chunk_size": 32768,
            "ui_theme": "material"
        }
    
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self.default_config
    
    def save_config(self, config):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
```

**Windows Configuration Management:**
```csharp
// ConfigurationService.cs
public class ConfigurationService
{
    private readonly string _configPath;
    private DemoConfiguration _config;
    
    public ConfigurationService()
    {
        _configPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "SynergyWindows", "config.json");
    }
    
    public DemoConfiguration LoadConfiguration()
    {
        if (File.Exists(_configPath))
        {
            var json = File.ReadAllText(_configPath);
            return JsonSerializer.Deserialize<DemoConfiguration>(json);
        }
        
        return DemoConfiguration.Default;
    }
    
    public void SaveConfiguration(DemoConfiguration config)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(_configPath));
        var json = JsonSerializer.Serialize(config, new JsonSerializerOptions 
        { 
            WriteIndented = true 
        });
        File.WriteAllText(_configPath, json);
    }
}
```

## Security Considerations

### Network Security

**Bluetooth Security:**
- Use Bluetooth Classic with encryption
- Implement device whitelisting
- Regular security key rotation
- Monitor for unauthorized pairing attempts

**Wi-Fi Security:**
- WPA3 encryption for hotspot
- MAC address filtering
- Hidden SSID for production
- Regular password changes

**Data Protection:**
```csharp
// EncryptionService.cs
public class EncryptionService
{
    public byte[] EncryptData(byte[] data, string key)
    {
        using var aes = Aes.Create();
        aes.Key = SHA256.HashData(Encoding.UTF8.GetBytes(key));
        aes.GenerateIV();
        
        using var encryptor = aes.CreateEncryptor();
        using var msEncrypt = new MemoryStream();
        msEncrypt.Write(aes.IV, 0, aes.IV.Length);
        
        using var csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write);
        csEncrypt.Write(data, 0, data.Length);
        
        return msEncrypt.ToArray();
    }
}
```

### Application Security

**Code Obfuscation:**
```bash
# Android ProGuard configuration
-keep class com.example.synergy.** { *; }
-dontwarn javax.annotation.**
-dontwarn org.checkerframework.**
```

**Certificate Pinning:**
```python
# Android SSL pinning
import ssl
import hashlib

class CertificatePinner:
    def __init__(self, pin_hashes):
        self.pin_hashes = pin_hashes
    
    def verify_certificate(self, cert):
        cert_hash = hashlib.sha256(cert.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )).hexdigest()
        
        return cert_hash in self.pin_hashes
```

## Monitoring and Maintenance

### Health Monitoring

**Application Metrics:**
```csharp
// MetricsCollector.cs
public class MetricsCollector
{
    private readonly ILogger<MetricsCollector> _logger;
    private readonly Counter _connectionAttempts;
    private readonly Histogram _fileTransferDuration;
    
    public void RecordConnectionAttempt(bool successful)
    {
        _connectionAttempts.WithTags("status", successful ? "success" : "failure").Increment();
    }
    
    public void RecordFileTransfer(TimeSpan duration, long fileSize)
    {
        _fileTransferDuration.Record(duration.TotalSeconds, 
            KeyValuePair.Create<string, object>("file_size", fileSize));
    }
}
```

**System Health Checks:**
```python
# health_check.py
class HealthChecker:
    def __init__(self):
        self.checks = []
    
    def add_check(self, name, check_func):
        self.checks.append((name, check_func))
    
    def run_health_checks(self):
        results = {}
        for name, check_func in self.checks:
            try:
                results[name] = check_func()
            except Exception as e:
                results[name] = {"status": "error", "message": str(e)}
        return results
    
    def bluetooth_health_check(self):
        # Check Bluetooth adapter status
        return {"status": "healthy", "devices_found": 5}
    
    def wifi_health_check(self):
        # Check Wi-Fi connectivity
        return {"status": "healthy", "signal_strength": -45}
```

### Automated Maintenance

**Log Rotation:**
```bash
#!/bin/bash
# log-rotation.sh
LOG_DIR="/var/log/synergy"
MAX_SIZE="100M"
MAX_AGE="30"

find $LOG_DIR -name "*.log" -size +$MAX_SIZE -exec logrotate {} \;
find $LOG_DIR -name "*.log.*" -mtime +$MAX_AGE -delete
```

**Performance Optimization:**
```powershell
# Windows maintenance script
# performance-maintenance.ps1

# Clear temporary files
Get-ChildItem -Path "$env:LOCALAPPDATA\SynergyWindows\temp" -Recurse | Remove-Item -Force

# Optimize Bluetooth stack
Restart-Service bthserv

# Clear DNS cache
Clear-DnsClientCache

# Defragment if needed
Optimize-Volume -DriveLetter C -Defrag
```

### Troubleshooting Tools

**Diagnostic Collection:**
```bash
#!/bin/bash
# collect-diagnostics.sh
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DIAG_DIR="diagnostics_$TIMESTAMP"

mkdir -p $DIAG_DIR

# Collect Android logs
adb logcat -d > $DIAG_DIR/android_logcat.txt
adb shell dumpsys bluetooth > $DIAG_DIR/android_bluetooth.txt
adb shell dumpsys wifi > $DIAG_DIR/android_wifi.txt

# Collect Windows logs
Get-WinEvent -LogName Application | Where-Object {$_.ProviderName -eq "SynergyWindows"} | Export-Csv $DIAG_DIR/windows_app_logs.csv

# Collect network information
ipconfig /all > $DIAG_DIR/windows_network.txt
netstat -an > $DIAG_DIR/windows_connections.txt

# Create archive
tar -czf diagnostics_$TIMESTAMP.tar.gz $DIAG_DIR/
rm -rf $DIAG_DIR
```

**Remote Support Tools:**
```csharp
// RemoteDiagnostics.cs
public class RemoteDiagnostics
{
    public async Task<DiagnosticReport> GenerateReportAsync()
    {
        return new DiagnosticReport
        {
            Timestamp = DateTime.UtcNow,
            SystemInfo = await GetSystemInfoAsync(),
            BluetoothStatus = await GetBluetoothStatusAsync(),
            WiFiStatus = await GetWiFiStatusAsync(),
            ApplicationLogs = GetRecentLogs(TimeSpan.FromHours(24))
        };
    }
    
    public async Task SendDiagnosticsAsync(DiagnosticReport report, string supportEndpoint)
    {
        var json = JsonSerializer.Serialize(report);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        
        using var client = new HttpClient();
        await client.PostAsync(supportEndpoint, content);
    }
}
```

This deployment guide provides comprehensive instructions for deploying the Synergy Demo System in various environments, from development to enterprise production deployments.