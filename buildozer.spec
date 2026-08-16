[app]
title = Medicine Manager
package.name = medicineapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0.0
requirements = python3,kivy

orientation = portrait
osx.kivy_version = 2.2.1

fullscreen = 0
android.presplash_color = #141a21

# Permissions
android.permissions = INTERNET

# Android specific configurations
android.api = 33
android.minapi = 21
android.ndk = 25.2.9519653
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
