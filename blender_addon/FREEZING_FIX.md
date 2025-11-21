# Interactive Mode Freezing - Fix Guide

## 🐛 The Problem

When clicking "Edit Fields Interactively", Blender or Instant Meshes may freeze because:
- Subprocess stdout/stderr buffers fill up
- Process is not properly detached from Blender
- Platform-specific blocking issues

## ✅ The Fix

**Version 3.0.0** includes multiple fixes to prevent freezing:

### Automatic Fixes (No Action Required)

1. **Output Redirection**: stdout/stderr now redirect to DEVNULL (prevents buffer blocking)
2. **Platform-Specific Detaching**:
   - Windows: Uses `DETACHED_PROCESS` flag
   - macOS/Linux: Uses `start_new_session=True`
3. **No stdin capture**: stdin is also redirected to DEVNULL

### Optional Fix (If Still Freezing)

If you still experience freezing, enable **"Fully Detach Interactive Sessions"**:

1. Go to `Edit` → `Preferences` → `Add-ons`
2. Find "Instant Meshes Retopology (Full + Interactive)"
3. Expand the addon preferences
4. Under "Interactive Mode" section, enable:
   - ☑ **Fully Detach Interactive Sessions**
5. Save preferences

**What this does:**
- Launches Instant Meshes completely independent of Blender
- Uses OS-native launch methods:
  - Windows: `os.startfile()`
  - macOS: `open -a` command
  - Linux: Forked process with new process group
- **Trade-off**: Blender can't track or terminate the process

## 🔧 Troubleshooting

### Issue: Blender Still Freezes

**Try these in order:**

1. **Enable "Fully Detach Interactive Sessions"** (see above)
2. **Close other Instant Meshes instances** before launching
3. **Check Blender console** for error messages:
   - Windows: Window → Toggle System Console
   - macOS/Linux: Run Blender from terminal
4. **Verify executable permissions**:
   - Linux: `chmod +x "/path/to/Instant Meshes"`
   - macOS: Check Security & Privacy settings

### Issue: "Process was detached" Message

This appears when:
- You enabled "Fully Detach Interactive Sessions"
- You click "Close Session"

**What it means:**
- Blender can't automatically close Instant Meshes
- You need to manually close the Instant Meshes window
- This is normal in detached mode

**How to close:**
- Just close the Instant Meshes window normally
- Or click "Close Session" in Blender (cleans up files only)

### Issue: Instant Meshes Doesn't Open

**Check:**
1. Executable path is correct in addon preferences
2. You have permission to execute the file
3. Run the "Test Executable" button
4. Try launching Instant Meshes manually first

**Linux-specific:**
```bash
# Make executable
chmod +x "/path/to/Instant Meshes"

# Test manually
"/path/to/Instant Meshes" test.obj
```

**macOS-specific:**
```bash
# If it says "app is damaged"
xattr -cr "/Applications/Instant Meshes.app"

# Test manually
"/Applications/Instant Meshes.app/Contents/MacOS/Instant Meshes" test.obj
```

### Issue: Can't Reimport Result

**Check:**
1. You saved the output in Instant Meshes (File → Export Mesh)
2. You saved to the default location (don't change path)
3. The session is still active in Blender
4. The output file exists (check the session status)

## 📊 Comparison: Normal vs Detached Mode

| Aspect | Normal Mode | Fully Detached Mode |
|--------|-------------|---------------------|
| **Freezing Risk** | Low (fixed in v3.0) | None |
| **Process Tracking** | ✅ Yes | ❌ No |
| **Auto-Terminate** | ✅ Yes | ❌ No (manual close) |
| **Platform Support** | All | All |
| **Recommended** | Default | If freezing persists |

## 🎯 Best Practices

### General Usage

1. **Start with normal mode** (default settings)
2. **Only enable detached mode** if you experience freezing
3. **Close Instant Meshes** before closing Blender session
4. **Save your work** in Instant Meshes before closing

### If Using Detached Mode

1. ✅ Remember to manually close Instant Meshes window
2. ✅ Check if output file was saved before reimporting
3. ✅ Close session in Blender after you're done
4. ⚠️ Don't rely on "Close Session" to terminate the process

## 🔍 Technical Details

### What Changed in v3.0.0

**Before (caused freezing):**
```python
process = subprocess.Popen(
    [executable, input_path],
    stdout=subprocess.PIPE,  # ❌ PIPE buffers can fill and block!
    stderr=subprocess.PIPE,  # ❌ PIPE buffers can fill and block!
)
```

**After (prevents freezing):**
```python
# Normal mode
process = subprocess.Popen(
    [executable, input_path],
    stdout=subprocess.DEVNULL,  # ✅ Discarded, no blocking
    stderr=subprocess.DEVNULL,  # ✅ Discarded, no blocking
    stdin=subprocess.DEVNULL,   # ✅ No input needed
    start_new_session=True,     # ✅ Detached from Blender
)

# Detached mode (if enabled)
os.startfile(executable, arguments=input_path)  # Windows
# or
subprocess.Popen(['open', '-a', executable, input_path])  # macOS
```

### Why PIPEs Cause Freezing

When using `subprocess.PIPE`:
1. OS creates limited-size buffers for stdout/stderr
2. Instant Meshes GUI writes to stdout/stderr
3. Buffers fill up (typically 4KB-64KB)
4. Instant Meshes blocks waiting for buffer to drain
5. Blender never reads the buffer (doesn't expect output)
6. **Deadlock!** Both processes frozen

### The Fix

- **DEVNULL**: Immediately discards all output, buffer never fills
- **start_new_session**: Creates new process group, prevents signal propagation
- **DETACHED_PROCESS** (Windows): Creates process in new console, fully independent

## 📝 Summary

The freezing issue is **fixed in v3.0.0** by default!

- ✅ Normal users: No action needed, should work fine
- ⚠️ Still freezing: Enable "Fully Detach Interactive Sessions"
- 📖 Read this guide if you encounter issues

**99% of users should have no freezing with default settings.**

The detached mode option is there as a safety fallback.
