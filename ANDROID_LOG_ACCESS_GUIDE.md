# How to Access Synergy Client Logs on Android

## 🔍 You're Right - Let's Check the Logs!

If the app is loading with mock services instead of real services on your Android phone, the logs will tell us exactly why the real services failed to load.

## 📱 Method 1: View Logs via ADB (Recommended)

### From Your Computer (WSL/Linux):
```bash
# Connect phone via USB with debugging enabled
adb devices

# View live app logs
adb logcat | grep -i synergy

# Or filter for Python/Kivy logs
adb logcat | grep -E "(python|kivy|synergy)"

# Save logs to file for analysis
adb logcat | grep -i synergy > synergy_logs.txt
```

### What to Look For:
```
# These indicate why real services failed:
"FALLBACK: Using mock Bluetooth service"
"ERROR: No Bluetooth service available" 
"ImportError: No module named 'jnius'"
"PermissionError:"
"Android APIs not available"
```

## 📱 Method 2: On-Device Log Viewing

### Using Terminal Emulator App:
1. **Install Termux** (from F-Droid or GitHub)
2. **Run these commands:**
   ```bash
   # View system logs
   logcat | grep synergy
   
   # Or install busybox and use
   logcat | busybox grep -i python
   ```

### Using LogCat Apps:
1. **Install "aLogcat"** or "MatLog" from Play Store
2. **Filter by "synergy"** or "python"
3. **Look for import errors and service failures**

## 📱 Method 3: Check App's Internal Logs

### Built-in Debug Button:
1. **Open Synergy Client**
2. **Tap "Show Debug Info"** button
3. **Look at console output** (limited but helpful)

### Expected Debug Output:
```
✅ Android APIs available / ⚠️ Android APIs not available
✅ REAL Bluetooth service imported / ⚠️ Fallback to MOCK
✅ REAL WiFi service imported / ⚠️ Fallback to MOCK  
✅ REAL File Transfer service imported / ⚠️ Fallback to MOCK
```

## 🔧 Common Reasons for Mock Service Fallback

### 1. Missing Android Dependencies:
```python
# These imports might be failing:
from jnius import autoclass
from android.permissions import request_permissions
```

### 2. Python-for-Android Issues:
```
# P4A might not include required modules:
- pyjnius
- android permissions
- bluetooth modules
```

### 3. Android API Level Issues:
```
# App built for wrong API level
# Check buildozer.spec:
android.api = 33
android.minapi = 23
```

## 🔍 Debugging Commands

### Check What's Actually Installed:
```bash
# From ADB
adb shell pm dump org.synergy.synergyclient | grep -i version

# Check app architecture
adb shell dumpsys package org.synergy.synergyclient | grep -A5 -B5 "versionCode"
```

### Test Python Modules:
```bash
# Connect to your running app (if possible)
adb shell "run-as org.synergy.synergyclient python3 -c 'import jnius; print(\"jnius OK\")'"
```

## 🚀 Quick Log Analysis

### Run This Command (from computer):
```bash
# Get comprehensive logs
adb logcat -c  # Clear logs
# Open app on phone
adb logcat | grep -E "(synergy|python|kivy|Import|Error)" | head -50
```

### Share the Results:
Look for lines containing:
- `"ImportError"` - Missing Python modules
- `"Android APIs not available"` - System access issues  
- `"FALLBACK: Using mock"` - Specific service failures
- `"Permission denied"` - Access restrictions

## 📋 Log Collection Script

### Save this as `collect_logs.sh`:
```bash
#!/bin/bash
echo "=== Collecting Synergy Client Logs ==="

# Clear old logs
adb logcat -c

echo "1. Start the app on your phone now..."
echo "2. Press Enter when app is fully loaded"
read

echo "Collecting logs for 10 seconds..."
timeout 10s adb logcat | grep -E "(synergy|python|kivy|Import|Error|jnius|android)" > app_debug.log

echo "Logs saved to app_debug.log"
echo "Look for 'ImportError', 'FALLBACK', or 'Android APIs not available'"
```

## 🎯 Expected Real Service Loading

### Successful Real Service Loading Looks Like:
```
✅ Android APIs available
✅ REAL Bluetooth service imported successfully  
✅ REAL WiFi service imported successfully
✅ REAL File Transfer service imported successfully
Real services: 3/3
```

### Failed Loading (Using Mocks):
```
⚠️ Android APIs not available - running in desktop mode
⚠️ Fallback to MOCK Bluetooth service (ImportError: No module named 'jnius')
⚠️ Fallback to MOCK WiFi service (ImportError: No module named 'android.permissions')
Real services: 0/3
```

## 🔧 Quick Fixes Based on Log Results

### If logs show "jnius not found":
- Need to rebuild APK with proper buildozer requirements
- Check `requirements.txt` includes `pyjnius`

### If logs show "Android APIs not available":
- App thinks it's running on desktop
- May need to fix Android detection logic

### If logs show "Permission denied":
- Back to permission issues we discussed earlier

## 📞 Next Steps

1. **Run the ADB log command**: `adb logcat | grep -i synergy`
2. **Start the app** and watch for errors
3. **Share the error messages** you see - that will tell us exactly why it's using mock services instead of real Android services

The logs will reveal the exact import errors or system issues preventing real service loading!