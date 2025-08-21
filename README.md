# Synergy Demo System

A comprehensive cross-platform demo system consisting of an Android application and Windows 10 application that communicate through Bluetooth and transfer files via Wi-Fi.

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Android Application Setup](#android-application-setup)
- [Windows Application Setup](#windows-application-setup)
- [Usage Instructions](#usage-instructions)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Contributing](#contributing)

## Overview

The Synergy Demo System demonstrates advanced cross-platform communication capabilities:

- **Android Application**: Creates Wi-Fi hotspot, handles Bluetooth communication, generates and transfers files
- **Windows Application**: Connects to Android via Bluetooth, displays color commands, transfers files over Wi-Fi
- **Communication**: JSON-based protocol over Bluetooth Classic (RFCOMM)
- **File Transfer**: TCP-based transfer with progress tracking and integrity verification

### Key Features

- ✅ Bluetooth device discovery and pairing
- ✅ Wi-Fi hotspot creation and connection
- ✅ Real-time color command display (red/yellow/green squares)
- ✅ Bidirectional file transfer with progress tracking
- ✅ File generation with random content (10MB-100MB)
- ✅ Comprehensive error handling and recovery
- ✅ Material Design UI (Android) and modern WPF UI (Windows)

## System Requirements

### Android Application

**Minimum Requirements:**
- Android 6.0 (API level 23) or higher
- 2GB RAM
- 500MB available storage
- Bluetooth 4.0+ support
- Wi-Fi capability with hotspot support

**Recommended:**
- Android 8.0 (API level 26) or higher
- 4GB RAM
- 1GB available storage

**Required Permissions:**
- `BLUETOOTH` and `BLUETOOTH_ADMIN`
- `ACCESS_WIFI_STATE` and `CHANGE_WIFI_STATE`
- `ACCESS_FINE_LOCATION` and `ACCESS_COARSE_LOCATION`
- `CHANGE_NETWORK_STATE`
- `WRITE_EXTERNAL_STORAGE`
- `INTERNET`

### Windows Application

**Minimum Requirements:**
- Windows 10 version 1903 or later
- .NET 6.0 Runtime
- 4GB RAM
- 200MB available storage
- Bluetooth 4.0+ support
- Wi-Fi capability

**Recommended:**
- Windows 10 version 21H2 or later
- 8GB RAM
- 500MB available storage

## Android Application Setup

### Prerequisites

1. **Install Python 3.8+**
   ```bash
   # On Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   
   # On Windows (use Python installer from python.org)
   # On macOS
   brew install python3
   ```

2. **Install Android SDK and NDK**
   ```bash
   # Install Android Studio or standalone SDK
   # Set environment variables:
   export ANDROID_HOME=$HOME/Android/Sdk
   export ANDROID_NDK_HOME=$HOME/Android/Sdk/ndk/25.1.8937393
   export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
   ```

3. **Install Java Development Kit (JDK) 11**
   ```bash
   # On Ubuntu/Debian
   sudo apt install openjdk-11-jdk
   
   # Set JAVA_HOME
   export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
   ```

### Installation Steps

1. **Clone and Navigate to Project**
   ```bash
   git clone <repository-url>
   cd SynergyClient
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Buildozer**
   ```bash
   pip install buildozer
   ```

5. **Initialize Buildozer (First Time Only)**
   ```bash
   buildozer init
   ```

6. **Configure Buildozer**
   Edit [`buildozer.spec`](buildozer.spec) if needed:
   ```ini
   [app]
   title = Synergy Demo
   package.name = synergydemo
   package.domain = com.example.synergy
   
   [buildozer]
   log_level = 2
   ```

### Building the APK

1. **Debug Build**
   ```bash
   buildozer android debug
   ```

2. **Release Build**
   ```bash
   buildozer android release
   ```

3. **Install on Device**
   ```bash
   # Enable USB debugging on your Android device
   adb install bin/synergydemo-*-debug.apk
   ```

### Running in Development Mode

```bash
# For desktop testing (limited functionality)
python main.py

# For full Android testing, use buildozer
buildozer android debug deploy run
```

## Windows Application Setup

### Prerequisites

1. **Install .NET 6.0 SDK**
   - Download from [Microsoft .NET Downloads](https://dotnet.microsoft.com/download/dotnet/6.0)
   - Or use package manager:
   ```bash
   # Windows (using winget)
   winget install Microsoft.DotNet.SDK.6
   
   # Or using chocolatey
   choco install dotnet-6.0-sdk
   ```

2. **Install Visual Studio 2022 or Visual Studio Code**
   - Visual Studio 2022 Community (recommended)
   - Or Visual Studio Code with C# extension

### Installation Steps

1. **Navigate to Windows Project**
   ```bash
   cd SynergyWindows
   ```

2. **Restore NuGet Packages**
   ```bash
   dotnet restore
   ```

3. **Build the Application**
   ```bash
   # Debug build
   dotnet build
   
   # Release build
   dotnet build --configuration Release
   ```

4. **Run the Application**
   ```bash
   # From command line
   dotnet run
   
   # Or open in Visual Studio and press F5
   ```

### Creating Deployment Package

1. **Publish Self-Contained Application**
   ```bash
   dotnet publish -c Release -r win10-x64 --self-contained true
   ```

2. **Create Installer (Optional)**
   ```bash
   # Install WiX Toolset for MSI creation
   # Or use Inno Setup for executable installer
   ```

## Usage Instructions

### Initial Setup

1. **Start Windows Application**
   - Launch SynergyWindows.exe
   - Ensure Bluetooth is enabled
   - The application will start scanning for devices

2. **Start Android Application**
   - Install and launch the Synergy Demo app
   - Grant all required permissions when prompted
   - Tap "Start Services" to initialize Bluetooth and Wi-Fi

### Pairing Devices

1. **On Windows:**
   - Click "Scan for Devices"
   - Select your Android device from the list
   - Click "Pair Device"

2. **On Android:**
   - Accept pairing request when prompted
   - Enter PIN if required (usually 0000 or 1234)

### Color Control Demo

1. **On Android:**
   - Use color buttons (Red, Yellow, Green) in the interface
   - Commands are sent via Bluetooth to Windows

2. **On Windows:**
   - Colored square display updates in real-time
   - Connection status shows active Bluetooth link

### File Transfer Demo

1. **Setup Wi-Fi Connection:**
   - Android automatically creates hotspot
   - Windows connects to Android's hotspot network

2. **Generate Test Files:**
   - On Android: Use "Generate File" with size selection (10MB-100MB)
   - On Windows: Use "Generate Test File" feature

3. **Transfer Files:**
   - Select file and choose transfer direction
   - Monitor progress with real-time updates
   - Verify integrity with automatic checksum validation

### Advanced Features

- **Error Recovery**: Automatic reconnection on connection loss
- **Performance Monitoring**: View transfer speeds and throughput
- **Logging**: Detailed logs for troubleshooting

## Testing

### Running Android Tests

1. **Unit Tests**
   ```bash
   python run_tests.py
   ```

2. **Specific Test Modules**
   ```bash
   python run_tests.py -m test_protocol
   python run_tests.py -m test_file_generator
   python run_tests.py -m test_integration
   ```

3. **Performance Tests**
   ```bash
   python run_tests.py --performance
   ```

4. **Smoke Tests**
   ```bash
   python run_tests.py --smoke
   ```

### Running Windows Tests

1. **Using Visual Studio**
   - Open Test Explorer
   - Run All Tests

2. **Using Command Line**
   ```bash
   cd SynergyWindows/Testing
   dotnet test
   ```

3. **Specific Test Categories**
   ```bash
   dotnet test --filter Category=Unit
   dotnet test --filter Category=Integration
   ```

### Cross-Platform Integration Testing

1. **Setup Test Environment**
   - Ensure both applications are built
   - Have Android device and Windows PC ready
   - Enable developer options on Android

2. **Run Integration Tests**
   - Start both applications
   - Follow pairing procedure
   - Execute test scenarios from [`Testing/TestingStrategy.md`](Testing/TestingStrategy.md)

## Troubleshooting

### Common Android Issues

**Build Errors:**
```bash
# NDK version mismatch
buildozer android clean
# Update buildozer.spec with correct NDK version

# Permission issues
chmod +x ~/.buildozer/android/platform/apache-ant-*/bin/ant
```

**Runtime Issues:**
- **Bluetooth not working**: Check permissions in Android settings
- **Hotspot creation fails**: Verify location services are enabled
- **App crashes**: Check logs with `adb logcat`

### Common Windows Issues

**Build Errors:**
```bash
# Missing .NET SDK
dotnet --version
# Install .NET 6.0 SDK if not present

# NuGet package issues
dotnet nuget locals all --clear
dotnet restore
```

**Runtime Issues:**
- **Bluetooth not working**: Enable Bluetooth in Windows settings
- **Permission denied**: Run as administrator for initial setup
- **Wi-Fi connection issues**: Check Windows Wi-Fi service is running

### Network Issues

**Bluetooth Pairing:**
1. Clear Bluetooth cache on Android
2. Remove device from Windows Bluetooth settings
3. Restart Bluetooth service on both devices
4. Try pairing again

**Wi-Fi Hotspot:**
1. Check Android hotspot settings
2. Verify password and SSID
3. Reset network settings if needed
4. Try different frequency band (2.4GHz vs 5GHz)

**File Transfer:**
1. Verify IP connectivity with ping
2. Check firewall settings on Windows
3. Ensure ports 8888-8890 are available
4. Try different port ranges

### Performance Issues

**Slow File Transfer:**
```bash
# Check Wi-Fi signal strength
# Use 5GHz band if available
# Close other network-intensive applications
```

**High Memory Usage:**
```bash
# Monitor with task manager/memory profiler
# Check for memory leaks in logs
# Restart applications periodically
```

### Getting Help

1. **Check Logs:**
   - Android: `adb logcat | grep Synergy`
   - Windows: Check Application Events in Event Viewer

2. **Enable Debug Mode:**
   - Set log level to DEBUG in configuration
   - Enable verbose logging in both applications

3. **Common Log Locations:**
   - Android: `/storage/emulated/0/Android/data/com.example.synergy/files/logs/`
   - Windows: `%LOCALAPPDATA%/SynergyWindows/logs/`

## Architecture

### System Architecture
- **Client-Server Model**: Android acts as server, Windows as client
- **Protocol**: JSON-based messaging over Bluetooth RFCOMM
- **File Transfer**: TCP over Wi-Fi with chunked transfer protocol
- **UI Patterns**: MVP (Android with Kivy), MVVM (Windows WPF)

### Key Components
- **[`bluetooth_service.py`](bluetooth_service.py)**: Android Bluetooth service
- **[`wifi_hotspot_service.py`](wifi_hotspot_service.py)**: Android Wi-Fi hotspot management
- **[`file_transfer_service.py`](file_transfer_service.py)**: File transfer implementation
- **[`BluetoothService.cs`](../SynergyWindows/SynergyWindows/Services/BluetoothService.cs)**: Windows Bluetooth service
- **[`FileTransferService.cs`](../SynergyWindows/SynergyWindows/Services/FileTransferService.cs)**: Windows file transfer

### Protocol Specification
See [`protocol_specification.md`](protocol_specification.md) for detailed message formats and communication flows.

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Follow coding standards:
   - Python: PEP 8
   - C#: Microsoft coding conventions
4. Add tests for new features
5. Update documentation

### Code Quality
- **Python**: Use `pylint`, `black`, `mypy`
- **C#**: Use Visual Studio Code Analysis
- **Tests**: Maintain >90% code coverage
- **Documentation**: Update README for API changes

### Submitting Changes
1. Ensure all tests pass
2. Update CHANGELOG.md
3. Submit pull request with detailed description
4. Address review feedback

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Kivy Framework**: Cross-platform Python UI framework
- **Material Design**: Android UI components via KivyMD
- **Windows Presentation Foundation**: Modern Windows UI framework
- **Bluetooth Classic**: Reliable device-to-device communication
- **TCP/IP Protocol**: High-performance file transfer implementation