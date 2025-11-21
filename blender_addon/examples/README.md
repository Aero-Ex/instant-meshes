# Example Scripts

This directory contains example scripts demonstrating how to use the Instant Meshes addon programmatically.

## Files

### batch_retopo.py

A comprehensive example showing how to:
- Retopologize multiple objects
- Use different settings for different objects
- Process objects based on naming conventions
- Create custom presets
- Automate retopology workflows

## Usage

### In Blender's Text Editor

1. Open Blender
2. Switch to the "Scripting" workspace
3. Click "Open" and select `batch_retopo.py`
4. Click "Run Script" (or press Alt+P)

### From Command Line

```bash
blender --background my_file.blend --python batch_retopo.py
```

### As a Startup Script

Copy the script to:
- Windows: `%APPDATA%\Blender Foundation\Blender\{version}\scripts\startup\`
- macOS: `~/Library/Application Support/Blender/{version}/scripts/startup/`
- Linux: `~/.config/blender/{version}/scripts/startup/`

## Example Functions

### batch_retopologize_all()
Processes all mesh objects in the scene with the same settings.

```python
batch_retopologize_all(vertex_count=2000, use_crease=False)
```

### retopologize_with_custom_settings()
Applies different settings based on object names.

```python
retopologize_with_custom_settings()
```

### retopologize_by_size()
Automatically calculates target size based on original mesh size.

```python
retopologize_by_size()
```

### retopologize_selected()
Processes only selected objects with preset configurations.

```python
retopologize_selected()
```

## Creating Your Own Scripts

### Basic Template

```python
import bpy

# Get the addon properties
props = bpy.context.scene.instant_meshes_props

# Configure settings
props.size_mode = 'VERTICES'
props.vertex_count = 2000
props.rosy = '4'
props.posy = '4'

# Select your object
obj = bpy.data.objects['MyObject']
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

# Run retopology
bpy.ops.mesh.instant_meshes_retopo()
```

### Available Properties

```python
# Size mode
props.size_mode = 'VERTICES' | 'FACES' | 'SCALE'
props.vertex_count = 2000
props.face_count = 2000
props.edge_scale = 0.1

# Symmetry
props.rosy = '2' | '4' | '6'
props.posy = '4' | '6'

# Crease detection
props.use_crease_angle = True | False
props.crease_angle = 30.0  # degrees

# Quality
props.smooth_iter = 2  # 0-20
props.dominant = True | False

# Alignment
props.align_to_boundaries = True | False

# Processing
props.deterministic = True | False
props.intrinsic = True | False
props.threads = 0  # 0 = auto
```

## Tips for Scripting

1. **Always check object type**:
   ```python
   if obj.type == 'MESH':
       # proceed
   ```

2. **Handle errors gracefully**:
   ```python
   result = bpy.ops.mesh.instant_meshes_retopo()
   if result != {'FINISHED'}:
       print(f"Failed to process {obj.name}")
   ```

3. **Store original selection**:
   ```python
   original_selection = bpy.context.selected_objects
   # ... do work ...
   # restore selection if needed
   ```

4. **Use context overrides for batch processing**:
   ```python
   for obj in objects:
       bpy.context.view_layer.objects.active = obj
       # process
   ```

5. **Monitor progress**:
   ```python
   total = len(objects)
   for i, obj in enumerate(objects):
       print(f"Processing {i+1}/{total}: {obj.name}")
   ```

## Common Use Cases

### Game Asset Pipeline

Process all meshes for game export:

```python
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and 'game_' in obj.name:
        props.vertex_count = 1000
        props.use_crease_angle = True
        # process obj
```

### LOD Generation

Create multiple Level of Detail versions:

```python
lod_levels = [5000, 2000, 500, 100]
for lod, vcount in enumerate(lod_levels):
    props.vertex_count = vcount
    # create LOD version
    # rename to include LOD level
```

### Batch Processing Directory

Process all .obj files in a directory:

```python
import os

directory = "/path/to/meshes"
for filename in os.listdir(directory):
    if filename.endswith(".obj"):
        # import, process, export
```

## Debugging

Enable Blender's system console to see output:
- **Windows**: Window → Toggle System Console
- **macOS/Linux**: Run Blender from terminal

Check the console for:
- Processing status
- Error messages
- Instant Meshes output

## Further Reading

- [Blender Python API](https://docs.blender.org/api/current/)
- [bpy.ops](https://docs.blender.org/api/current/bpy.ops.html)
- [Instant Meshes Documentation](../README.md)
