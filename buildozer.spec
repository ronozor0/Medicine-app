[app]
title = Medicine Manager
package.name = medicineapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0.0
requirements = python3==3.11.0,kivy==2.3.0


orientation = portrait
fullscreen = 0
android.presplash_color = #141a21

# Permissions
android.permissions = INTERNET

# Let Buildozer manage SDK/NDK automatically
android.accept_sdk_license = True
android.archs = arm64-v8a 
p4a.branch = develop



[buildozer]
log_level = 2
warn_on_root = 1
