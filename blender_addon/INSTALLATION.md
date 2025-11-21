# Quick Installation Guide

Follow these simple steps to get the Instant Meshes Blender addon running.

## 1. Get Instant Meshes Executable

### Windows
1. Download: https://instant-meshes.s3.eu-central-1.amazonaws.com/Release/instant-meshes-windows.zip
2. Extract to `C:\InstantMeshes\`
3. Note the path: `C:\InstantMeshes\Instant Meshes.exe`

### macOS
1. Download: https://instant-meshes.s3.eu-central-1.amazonaws.com/instant-meshes-macos.zip
2. Extract and move to Applications
3. Note the path: `/Applications/Instant Meshes.app/Contents/MacOS/Instant Meshes`

### Linux
1. Download: https://instant-meshes.s3.eu-central-1.amazonaws.com/instant-meshes-linux.zip
2. Extract to `/opt/instant-meshes/`
3. Make executable: `chmod +x "/opt/instant-meshes/Instant Meshes"`
4. Install zenity: `sudo apt-get install zenity`
5. Note the path: `/opt/instant-meshes/Instant Meshes`

## 2. Install Addon in Blender

### Method 1: Direct Installation
1. Open Blender
2. Go to `Edit` → `Preferences` → `Add-ons`
3. Click `Install...`
4. Navigate to this folder and select `__init__.py`
5. Click `Install Add-on`
6. Enable the addon by checking its checkbox

### Method 2: Manual Installation
1. Find your Blender addons folder:
   - Windows: `%APPDATA%\Blender Foundation\Blender\{version}\scripts\addons\`
   - macOS: `~/Library/Application Support/Blender/{version}/scripts/addons/`
   - Linux: `~/.config/blender/{version}/scripts/addons/`
2. Copy the entire `blender_addon` folder there
3. Rename it to `instant_meshes_addon`
4. Restart Blender
5. Enable in `Edit` → `Preferences` → `Add-ons`

## 3. Configure Executable Path

1. In addon preferences, set the "Instant Meshes Executable" path
2. Use the full path noted in step 1
3. Save preferences (bottom left: ☰ → Save Preferences)

## 4. Verify Installation

1. Press `N` in 3D Viewport to open sidebar
2. Look for "Instant Meshes" tab
3. Select a mesh object
4. The "Run Instant Meshes" button should be enabled

## Done!

You're ready to start retopologizing! See [README.md](README.md) for usage instructions.

## Need Help?

If you encounter issues:
1. Check Blender's console for error messages (Window → Toggle System Console)
2. Verify the executable path is correct
3. Test the executable manually from command line
4. See the Troubleshooting section in README.md
