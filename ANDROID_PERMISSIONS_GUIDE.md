# Android Permissions Setup Guide

## Issue: Phone Not Permitting App Access

Your phone is blocking the app from accessing Bluetooth, WiFi, Location, and other system features needed for real services. Here's how to fix it:

## 🔧 Quick Fix - Grant All Permissions

### Method 1: Through App Settings (Recommended)

1. **Open Android Settings**
   - Go to `Settings` → `Apps` (or `Application Manager`)
   - Find and tap `Synergy Client`

2. **Grant Permissions**
   - Tap `Permissions` (or `App permissions`)
   - Enable ALL of these permissions:
     - ✅ **Location** (Required for Bluetooth scanning)
     - ✅ **Phone** (For device access)
     - ✅ **Storage** (For file operations)
     - ✅ **Camera** (May be requested)
     - ✅ **Nearby devices** (For Bluetooth on Android 12+)

3. **Additional Settings**
   - Tap `Special app access` or `Advanced`
   - Enable `Modify system settings` if available
   - Enable `Display over other apps` if available

### Method 2: When App Requests Permissions

1. **Launch the App**
   - Open Synergy Client
   - App will request permissions one by one

2. **Grant Each Permission**
   - When prompted, tap `Allow` or `While using the app`
   - **Never tap "Deny"** or "Don't allow"

3. **If You Accidentally Denied**
   - Follow Method 1 above to manually enable

## 📱 Step-by-Step Visual Guide

### Samsung Phones:
```
Settings → Apps → Synergy Client → Permissions
- Location: Allow all the time (or While using app)
- Phone: Allow
- Storage: Allow
- Nearby devices: Allow
```

### Google Pixel/Stock Android:
```
Settings → Apps & notifications → Synergy Client → Permissions
- Location: Allow all the time
- Phone: Allow  
- Storage: Allow
- Nearby devices: Allow
```

### Other Android Phones:
```
Settings → Application Manager → Synergy Client → Permissions
- Enable all requested permissions
```

## 🚨 Critical Permissions Explained

| Permission | Why Needed | Impact if Denied |
|------------|------------|------------------|
| **Location** | Required for Bluetooth device scanning (Android security) | ❌ Bluetooth scanning fails |
| **Phone** | Access to device hardware states | ❌ Can't detect Bluetooth/WiFi status |
| **Storage** | File transfer operations | ❌ File operations fail |
| **Nearby devices** | Bluetooth on Android 12+ | ❌ Modern Bluetooth features fail |

## 🔍 Troubleshooting Permission Issues

### Issue 1: "Location permission denied"
**Solution:**
1. Settings → Apps → Synergy Client → Permissions
2. Tap `Location` 
3. Select `Allow all the time` (not just "While using app")

### Issue 2: "Bluetooth scanning not working"
**Solution:**
1. Ensure Location is enabled (see above)
2. Enable Bluetooth in system settings
3. Check `Nearby devices` permission (Android 12+)

### Issue 3: "WiFi hotspot creation fails"
**Solution:**
1. Enable `Modify system settings` permission
2. Check WiFi is enabled in system settings
3. Some phones require manual hotspot activation first

### Issue 4: "File transfer not working"
**Solution:**
1. Enable `Storage` permission
2. For Android 11+, may need `Manage external storage`

## 🔧 Advanced Permission Setup

### For Android 11+ (API 30+):
```
Settings → Apps → Special app access → All files access
- Find Synergy Client → Enable
```

### For Android 12+ (API 31+):
```
Settings → Apps → Synergy Client → Permissions
- Enable "Nearby devices"
- Enable "Precise location" (not just approximate)
```

## ⚡ Quick Test After Enabling Permissions

1. **Open Synergy Client**
2. **Tap "Show Service Details"** button
3. **Look for status changes:**
   - Should show more "✅ Real" indicators
   - Fewer "⚠️ Mock" fallbacks

4. **Test Each Service:**
   - `Test Bluetooth Service` - should find real devices
   - `Test WiFi Hotspot` - should create actual hotspot
   - `Test File Transfer` - should work with real files

## 📋 Permission Checklist

Before using the app, ensure these are enabled:

```
☐ Location (Allow all the time)
☐ Phone/Device access
☐ Storage/Files
☐ Nearby devices (Android 12+)
☐ Modify system settings
☐ Display over other apps (optional)
☐ All files access (Android 11+)
```

## 🔄 If Permissions Still Don't Work

### Option 1: Reinstall App
1. Uninstall Synergy Client
2. Reinstall: `adb install bin/*.apk`
3. Grant all permissions immediately when prompted

### Option 2: Developer Options
1. Enable `Developer Options` in Android settings
2. Enable `USB Debugging` 
3. Enable `Install via USB`

### Option 3: Check Phone Security Settings
- Some phones have additional security layers
- Check `Security` → `Special access` → `Device admin apps`
- Look for any restrictions on the app

## 🎯 Expected Results After Permissions

Once all permissions are granted:

1. **Bluetooth Service**: Shows "✅ Real" and finds actual paired devices
2. **WiFi Service**: Shows "✅ Real" and can create actual hotspots  
3. **File Service**: Shows "✅ Real" and performs real file operations
4. **UI**: All features work without "Permission denied" errors

## 🆘 Still Having Issues?

If permissions are granted but services still show as "Mock":

1. **Check Android Version**: Some features need Android 6.0+ (API 23+)
2. **Check Hardware**: Ensure your phone has Bluetooth 4.0+ and WiFi capabilities
3. **Restart App**: Close and reopen Synergy Client after granting permissions
4. **Check Logs**: Look for specific error messages in the app's debug output

The app is designed to work with mock services if real services fail, so it will still be functional even if some permissions are denied, but you'll get the full experience with all permissions enabled.