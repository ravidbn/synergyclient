# Build Strategy: Simplified Approach

## Current Issue
The build is failing at the autotools stage with persistent `autoreconf` errors, even after adding all required build dependencies. This suggests there may be deeper compatibility issues.

## Simplified Build Strategy

### Phase 1: Basic Kivy Build ✓
**Goal:** Get a minimal Kivy app building successfully

**Changes Made:**
1. **Updated Kivy version** from 2.1.0 to 2.3.0 (more recent, better compatibility)
2. **Removed KivyMD temporarily** from buildozer requirements
3. **Simplified main.py** to use basic Kivy widgets instead of KivyMD
4. **Minimal dependencies:** Only `python3,kivy==2.3.0,requests`

**Current buildozer.spec requirements:**
```
requirements = python3,kivy==2.3.0,requests
```

**Current requirements.txt:**
```
kivy==2.3.0
requests
```

### Phase 2: Add Back Complexity (Future)
Once basic build succeeds:
1. Add KivyMD back to requirements
2. Restore KivyMD imports in main.py
3. Test incremental additions

## Key Changes to main.py

### Replaced KivyMD Widgets:
- `MDApp` → `App`
- `MDScreen` → `Screen` 
- `MDScreenManager` → `ScreenManager`
- `MDDialog` → `Popup`
- `Snackbar` → `Popup`
- `OneLineListItem` → Basic `Label`

### Simplified UI:
- Removed Material Design components
- Using basic Kivy popups for notifications
- Simplified device selection dialog

## Expected Outcome

This simplified approach should:
1. ✅ **Bypass KivyMD compilation issues** (if any)
2. ✅ **Reduce native dependency complexity**
3. ✅ **Isolate the autotools problem**
4. ✅ **Establish a working baseline**

If this basic version builds successfully, we'll know the autotools issue was related to KivyMD or complex dependencies. If it still fails, we'll know the issue is more fundamental.

## Reverting Changes (When Ready)

To restore full KivyMD functionality later:

1. **Add KivyMD back to buildozer.spec:**
   ```
   requirements = python3,kivy==2.3.0,kivymd,requests
   ```

2. **Add KivyMD back to requirements.txt:**
   ```
   kivy==2.3.0
   kivymd
   requests
   ```

3. **Restore KivyMD imports in main.py** (uncommenting the KivyMD lines)

4. **Replace basic widgets with MD widgets** throughout the file

## Testing

The simplified app should:
- ✅ Launch successfully
- ✅ Show basic UI with popups
- ✅ Handle Bluetooth and WiFi service calls
- ✅ Build without autotools errors

Once this foundation works, we can incrementally add back the Material Design components.