[app]
title = Synergy Client v3.0
package.name = synergyclient
package.domain = org.synergy
source.dir = .
version = 3.0

# SINGLE FILE APPROACH - Only main.py needed
source.include_exts = py
# NO exclusions that could cause conflicts
source.exclude_dirs = tests,bin,venv,buildenv,.buildozer,.git,.github,__pycache__

requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

# Essential Android settings
android.api = 33
android.minapi = 23
android.sdk = 33
android.ndk = 25c
android.ndk_api = 23
android.private_storage = True
android.accept_sdk_license = True
android.enable_androidx = True
android.add_compile_options = "sourceCompatibility = JavaVersion.VERSION_17", "targetCompatibility = JavaVersion.VERSION_17"
android.archs = arm64-v8a
android.allow_backup = True

# Minimal permissions
android.permissions = BLUETOOTH,ACCESS_FINE_LOCATION,ACCESS_WIFI_STATE,INTERNET

[buildozer]
log_level = 2