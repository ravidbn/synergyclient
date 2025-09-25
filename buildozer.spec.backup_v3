[app]
title = Synergy Client v2.0
package.name = synergyclient
package.domain = org.synergy
source.dir = .
version = 2.0

# AGGRESSIVE SOURCE INCLUSION - Multiple methods
source.include_exts = py,kv,txt,json
source.include_patterns = *.py,*_mock.py,*_service*.py,main*.py,utils/*.py,gui/*.kv

# Minimal exclusions to avoid conflicts
source.exclude_dirs = tests,bin,venv,buildenv,.buildozer,.git,.github,__pycache__
source.exclude_patterns = *.spec,*.md,*.sh,*.bat,*.log,build_log.txt

# Use EXPLICIT file inclusion via android.add_src
android.add_src = bluetooth_service_mock.py,wifi_hotspot_service_mock.py,file_transfer_service_mock.py,bluetooth_service.py,wifi_hotspot_service.py,file_transfer_service.py

requirements = python3,kivy==2.3.0,requests,pyjnius
orientation = portrait
fullscreen = 0

# Essential Android settings for toolchain success
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

# Essential permissions
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_FINE_LOCATION,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,INTERNET

[buildozer]
log_level = 2