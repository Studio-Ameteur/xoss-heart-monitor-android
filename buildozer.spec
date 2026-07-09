[app]
title = XOSS Heart Monitor
package.name = xossheartmonitor
package.domain = org.studioamateur
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
icon.filename = %(source.dir)s/icon.png
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION
android.api = 34
android.minapi = 23
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
