[app]

# (str) Title of your application
title = Mini Sudokemistry

# (str) Package name
package.name = minisudokemistry

# (str) Package domain (needed for android packaging)
package.domain = org.mol23

version = 1.0

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) Application requirements
# Ensure python3 and pygame are here
requirements = python3==3.10.12,pygame

# (str) Supported orientations (valid options are: landscape, portrait, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific configurations
# =============================================================================

# (list) Permissions. Keeping only internet for future Ads.
# No audio or hardware permissions requested.
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as higher as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (bool) If True, then skip try to dock the app into the widget list
android.skip_update = False

# (bool) Register application as game
android.meta_data = android.app_id=game

# (list) Architecture to build for (ARM64 is standard for modern phones)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow code to be run as root (just in case)
android.allow_backup = True

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
