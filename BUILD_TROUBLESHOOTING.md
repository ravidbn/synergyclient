# Buildozer Build Troubleshooting Guide

## Error: "Unknown command/target android"

### Quick Fix Steps

1. **Verify Buildozer Installation**
   ```bash
   # Check if buildozer is installed
   buildozer --version
   
   # If not installed or outdated, reinstall
   pip uninstall buildozer
   pip install buildozer
   ```

2. **Initialize Buildozer (First Time Setup)**
   ```bash
   # Run this in the project directory (where main.py is located)
   buildozer init
   
   # This will create a new buildozer.spec file
   # You can then replace it with our custom one or merge settings
   ```

3. **Verify Project Structure**
   ```
   SynergyClient/
   ├── main.py              # Must be present
   ├── buildozer.spec       # Must be present
   ├── requirements.txt
   ├── bluetooth_service.py
   ├── wifi_hotspot_service.py
   ├── file_transfer_service.py
   ├── utils/
   │   ├── protocol.py
   │   └── file_generator.py
   └── gui/
       └── main_screen.kv
   ```

4. **Check Dependencies**
   ```bash
   # Install required system dependencies (Ubuntu/Debian)
   sudo apt update
   sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   
   # Install Android dependencies
   sudo apt install -y android-tools-adb android-tools-fastboot
   ```

5. **Clean and Rebuild**
   ```bash
   # Clean previous build attempts
   buildozer android clean
   
   # Build debug APK
   buildozer android debug
   ```

### Alternative: Manual Buildozer Setup

If the above doesn't work, follow these detailed steps:

**Step 1: Complete Environment Setup**
```bash
# Install Python dependencies
python3 -m pip install --upgrade pip
python3 -m pip install buildozer cython==0.29.33

# Install Java 8 (required for older Android builds)
sudo apt install openjdk-8-jdk
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64' >> ~/.bashrc

# Install Android SDK dependencies
sudo apt install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386
```

**Step 2: Initialize Buildozer with Custom Spec**
```bash
# First, backup our custom buildozer.spec
cp buildozer.spec buildozer.spec.backup

# Initialize buildozer (creates default spec)
buildozer init

# Restore our custom configuration
cp buildozer.spec.backup buildozer.spec
```

**Step 3: First Build (This will take 20-60 minutes)**
```bash
# First build downloads SDK, NDK, and builds dependencies
buildozer android debug
```

### Common Issues and Solutions

**Issue 1: Java Version Conflicts**
```bash
# Force Java 8
sudo update-alternatives --config java
# Select Java 8 from the list

# Verify Java version
java -version
# Should show version 1.8.x
```

**Issue 2: Android SDK License Issues**
```bash
# Accept SDK licenses manually
buildozer android debug
# When prompted, type 'y' to accept all licenses

# Or set auto-accept in buildozer.spec (already configured):
# android.accept_sdk_license = True
```

**Issue 3: NDK Version Issues**
```bash
# Update buildozer.spec with compatible NDK version
# In buildozer.spec, line 110:
android.ndk = 25c

# Or try older version:
android.ndk = 23c
```

**Issue 4: Memory Issues During Build**
```bash
# Add swap space (Linux)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Or close other applications to free RAM
```

**Issue 5: Permission Issues**
```bash
# Fix permissions for buildozer directory
sudo chown -R $USER:$USER ~/.buildozer
chmod -R 755 ~/.buildozer
```

### Windows Users (WSL/Docker Alternative)

If you're on Windows, consider using WSL2 or Docker:

**WSL2 Setup:**
```bash
# Install WSL2 Ubuntu
wsl --install Ubuntu

# In WSL2 terminal:
sudo apt update
sudo apt upgrade
sudo apt install python3-pip git

# Clone project and follow Linux instructions above
```

**Docker Alternative:**
```dockerfile
# Create Dockerfile
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip git openjdk-8-jdk \
    zip unzip autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev libncursesw5-dev libtinfo5 cmake \
    libffi-dev libssl-dev

RUN pip3 install buildozer cython==0.29.33

WORKDIR /app
COPY . .

CMD ["buildozer", "android", "debug"]
```

### Verification Steps

After successful build:

```bash
# Check if APK was created
ls -la bin/
# Should see: synergyclient-0.1-arm64-v8a-debug.apk

# Install on connected Android device
adb devices
adb install bin/synergyclient-0.1-arm64-v8a-debug.apk

# Launch app
adb shell am start -n org.synergy.synergyclient/org.kivy.android.PythonActivity
```

### Alternative Build Methods

**Method 1: Using GitHub Actions (Automated)**
Create `.github/workflows/build-android.yml`:
```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer cython==0.29.33
        
    - name: Build APK
      run: buildozer android debug
      
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: android-apk
        path: bin/*.apk
```

**Method 2: Using Kivy Buildozer Docker Image**
```bash
# Pull official buildozer image
docker pull kivy/buildozer:latest

# Build using Docker
docker run --rm -v $PWD:/home/user/hostcwd kivy/buildozer android debug
```

### Getting Help

If you continue having issues:

1. **Check Buildozer Logs**
   ```bash
   # Enable verbose logging
   buildozer android debug -v
   
   # Check log files
   tail -f .buildozer/android/platform/build-arm64-v8a/dists/synergyclient/build.log
   ```

2. **Common Log Locations**
   - Build logs: `.buildozer/android/platform/build-*/dists/*/build.log`
   - Gradle logs: `.buildozer/android/platform/build-*/gradle.log`
   - Python logs: `.buildozer/android/platform/python-for-android/dist/*/build.log`

3. **Community Resources**
   - Kivy Discord: https://discord.gg/kivy
   - Buildozer GitHub Issues: https://github.com/kivy/buildozer/issues
   - Stack Overflow: Tag with `kivy`, `buildozer`, `android`

4. **Report Issues**
   Include this information when asking for help:
   ```bash
   # System information
   uname -a
   python3 --version
   buildozer --version
   
   # Build environment
   echo $JAVA_HOME
   java -version
   
   # Project structure
   find . -name "*.py" -o -name "*.kv" -o -name "buildozer.spec" | head -20
   ```

Remember: The first build always takes the longest (20-60 minutes) as it downloads and compiles all dependencies. Subsequent builds are much faster (2-5 minutes).