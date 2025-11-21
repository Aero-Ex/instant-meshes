# Instant Meshes Blender Addon

A fully-featured Blender addon that integrates the powerful Instant Meshes retopology algorithm directly into Blender's workflow.

![Instant Meshes Logo](../resources/icon.png)

## Overview

This addon provides seamless integration of Instant Meshes into Blender, allowing you to:

- **Automatic Retopology**: Generate clean, quad-based topology from high-resolution meshes
- **Customizable Output**: Control vertex count, face count, or edge length
- **Advanced Features**: Crease detection, boundary alignment, and more
- **Native Blender UI**: All features accessible through a clean, intuitive interface
- **Non-Destructive**: Original mesh is preserved, retopo is created as a new object

## Features

### Core Functionality
- ✅ One-click retopology from Blender's 3D viewport
- ✅ Full parameter control matching Instant Meshes capabilities
- ✅ Automatic OBJ export/import workflow
- ✅ Progress reporting and error handling

### Mesh Size Control
Choose how to define your target mesh:
- **Vertex Count**: Specify exact number of vertices
- **Face Count**: Specify exact number of faces
- **Edge Length**: Define edge length in world units

### Symmetry Options
- **Orientation Symmetry (RoSy)**: 2-way, 4-way, or 6-way rotational symmetry
- **Position Symmetry (PoSy)**: Quad mesh or Triangle mesh output

### Advanced Options
- **Crease Detection**: Preserve sharp edges with adjustable angle threshold
- **Smooth Iterations**: Control quality with smoothing and ray-tracing steps
- **Boundary Alignment**: Align field to mesh boundaries (for open meshes)
- **Dominant Mode**: Generate quad-dominant instead of pure quad meshes
- **Deterministic Mode**: Reproducible results (slower)
- **Thread Control**: Adjust parallel processing threads

## Installation

### Step 1: Install Instant Meshes

First, you need the Instant Meshes executable:

#### Option A: Download Pre-compiled Binary

1. Visit the [Instant Meshes releases page](https://github.com/wjakob/instant-meshes/releases)
2. Download the appropriate version for your OS:
   - **Windows**: `instant-meshes-windows.zip`
   - **macOS**: `instant-meshes-macos.zip`
   - **Linux**: `instant-meshes-linux.zip`
3. Extract the archive to a location on your computer

#### Option B: Build from Source

If you prefer to build from source (especially on Linux):

```bash
git clone --recursive https://github.com/wjakob/instant-meshes
cd instant-meshes
cmake .
make -j 4
```

**Note for Linux users**: Install required dependencies first:
```bash
sudo apt-get install libxrandr-dev libxinerama-dev libxcursor-dev libxi-dev
```

### Step 2: Install the Blender Addon

1. **Download the Addon**:
   - Copy the entire `blender_addon` folder from this repository

2. **Install in Blender**:
   - Open Blender
   - Go to `Edit` → `Preferences` → `Add-ons`
   - Click `Install...`
   - Navigate to the `blender_addon` folder and select `__init__.py`
   - Click `Install Add-on`

3. **Enable the Addon**:
   - Search for "Instant Meshes" in the addon list
   - Check the checkbox to enable it

### Step 3: Configure Executable Path

1. In the Addon preferences (visible when addon is enabled), set the path to your Instant Meshes executable:

   - **Windows**: `C:\path\to\Instant Meshes.exe`
   - **macOS**: `/Applications/Instant Meshes.app/Contents/MacOS/Instant Meshes`
   - **Linux**: `/opt/instant-meshes/Instant Meshes` (or wherever you built it)

2. **Optional**: Click "Test Executable" to verify it's working

## Usage

### Basic Workflow

1. **Select Your Mesh**:
   - Select the high-resolution mesh you want to retopologize
   - Ensure you're in **Object Mode**

2. **Open the Panel**:
   - Press `N` to open the sidebar in the 3D Viewport
   - Click the **"Instant Meshes"** tab

3. **Configure Settings**:
   - Choose your target mesh size (vertex count, face count, or edge length)
   - Adjust symmetry settings if needed
   - Expand "Advanced Options" for fine control

4. **Run Retopology**:
   - Click **"Run Instant Meshes"**
   - Wait for processing (check the console for progress)
   - A new object with "_retopo" suffix will be created

### Quick Start Examples

#### Example 1: Simple Retopology
```
1. Select your mesh
2. Set Target Vertices to 2000
3. Click "Run Instant Meshes"
```

#### Example 2: High-Quality Quad Mesh
```
1. Select your mesh
2. Size Mode: Face Count = 5000
3. Orientation Symmetry: 4-Way
4. Position Symmetry: Quad
5. Smooth Iterations: 5
6. Click "Run Instant Meshes"
```

#### Example 3: Preserve Sharp Edges
```
1. Select your mesh
2. Size Mode: Vertex Count = 3000
3. Enable Crease Detection
4. Crease Angle: 30°
5. Align to Boundaries: ON (if mesh is open)
6. Click "Run Instant Meshes"
```

## Parameter Reference

### Target Mesh Size

| Parameter | Description | Recommended Range |
|-----------|-------------|-------------------|
| **Vertex Count** | Number of vertices in output | 500 - 50,000 |
| **Face Count** | Number of faces in output | 500 - 50,000 |
| **Edge Length** | World-space edge length | 0.01 - 1.0 |

**Note**: Only one size parameter can be active at a time.

### Symmetry Settings

| Parameter | Options | Description |
|-----------|---------|-------------|
| **Orientation Symmetry** | 2, 4, 6 | Rotational symmetry for orientation field. Use 4 for quads, 6 for triangles |
| **Position Symmetry** | Quad, Triangle | Output mesh type |

### Advanced Options

| Parameter | Type | Description |
|-----------|------|-------------|
| **Crease Detection** | Boolean | Enable/disable sharp edge preservation |
| **Crease Angle** | 0-180° | Threshold angle for detecting creases |
| **Smooth Iterations** | 0-20 | Number of smoothing passes (higher = better quality, slower) |
| **Dominant Mode** | Boolean | Allow non-quad faces for better adaptivity |
| **Align to Boundaries** | Boolean | Align field to mesh boundaries (for open meshes) |
| **Deterministic** | Boolean | Use deterministic algorithms (reproducible but slower) |
| **Intrinsic Mode** | Boolean | Advanced: use intrinsic formulation |
| **Threads** | 0-64 | Thread count (0 = automatic) |

## Tips and Best Practices

### Getting the Best Results

1. **Clean Input Mesh**:
   - Remove duplicate vertices
   - Fix non-manifold geometry
   - Ensure normals are correct

2. **Appropriate Density**:
   - Start with 1/16th of original vertex count
   - Adjust based on detail requirements
   - Use edge length mode for consistent sizing

3. **Crease Detection**:
   - Enable for hard-surface models
   - Try angles between 20-45° depending on model
   - Disable for organic/smooth surfaces

4. **Boundary Alignment**:
   - Enable for open meshes (clothing, surfaces)
   - Disable for closed objects

5. **Performance**:
   - Adjust thread count for faster processing
   - Disable deterministic mode for speed
   - Reduce smooth iterations if processing is slow

### Troubleshooting

**Problem**: "Executable not found" error
- **Solution**: Check the executable path in addon preferences
- Ensure the file actually exists at that location
- On macOS, navigate inside the .app bundle to find the executable

**Problem**: Processing takes too long
- **Solution**: Reduce target vertex/face count
- Decrease smooth iterations
- Increase thread count
- Disable deterministic mode

**Problem**: Output mesh has poor quality
- **Solution**: Increase smooth iterations
- Try different symmetry settings
- Enable crease detection for hard surfaces
- Increase target mesh density

**Problem**: Sharp edges not preserved
- **Solution**: Enable crease detection
- Lower the crease angle threshold
- Increase smooth iterations

**Problem**: Mesh boundaries look wrong
- **Solution**: Enable "Align to Boundaries"
- Check if input mesh has boundary issues
- Ensure normals are correct

## Technical Details

### File Format Support
- **Input**: OBJ format (exported automatically)
- **Output**: OBJ format (imported automatically)
- All export/import happens in temporary directory (auto-cleaned)

### Blender Compatibility
- **Minimum**: Blender 2.80
- **Recommended**: Blender 3.0+
- **Tested**: Blender 2.80 - 4.0

### Processing Pipeline
1. Export selected mesh to temporary OBJ file
2. Call Instant Meshes executable with parameters
3. Import resulting mesh
4. Position new mesh at original location
5. Clean up temporary files

### Performance Considerations
- Large meshes (>1M vertices) may take several minutes
- SSD recommended for faster temp file I/O
- Multi-threading scales well with CPU cores

## Known Limitations

1. **Executable Required**: Must have Instant Meshes executable (not pure Python)
2. **Object Mode Only**: Must be in Object Mode to run
3. **OBJ Format**: Limited to OBJ capabilities (no vertex colors, limited UVs)
4. **Single Object**: Processes one object at a time
5. **Temporary Files**: Requires disk space for temp files

## FAQ

**Q: Can I use this for game asset creation?**
A: Yes! It's perfect for creating low-poly game meshes from high-poly sculpts.

**Q: Does it preserve UVs?**
A: No, you'll need to re-UV the retopologized mesh. Consider using Blender's "Transfer Data" or baking workflows.

**Q: Can I batch process multiple objects?**
A: Not currently. Select and process each object individually.

**Q: Is this faster than manual retopology?**
A: For most meshes, yes! It can complete in seconds what would take hours manually.

**Q: Can I adjust the result afterwards?**
A: Yes! The output is a standard mesh object you can edit normally in Blender.

**Q: Does it work with modifiers?**
A: Yes, modifiers are automatically applied during export.

## Contributing

This addon is part of the Instant Meshes project. Contributions are welcome!

### Reporting Issues
- Check if the issue is with the addon or Instant Meshes itself
- Provide Blender version and OS
- Include error messages from Blender's console
- Describe steps to reproduce

### Improving the Addon
- Fork the repository
- Make your changes
- Test with multiple Blender versions
- Submit a pull request

## License

This addon is provided under the same BSD-style license as Instant Meshes.

See [LICENSE.txt](../LICENSE.txt) for details.

## Credits

- **Instant Meshes Algorithm**: Wenzel Jakob, Marco Tarini, Daniele Panozzo, Olga Sorkine-Hornung
- **Original Paper**: "Instant Field-Aligned Meshes" (SIGGRAPH Asia 2015)
- **Blender Addon**: Created to integrate Instant Meshes into Blender workflow

## References

- [Instant Meshes Project](https://github.com/wjakob/instant-meshes)
- [Research Paper](http://igl.ethz.ch/projects/instant-meshes/instant-meshes-SA-2015-jakob-et-al.pdf)
- [Project Website](http://igl.ethz.ch/projects/instant-meshes/)
- [Demo Video](https://www.youtube.com/watch?v=U6wtw6W4x3I)

## Changelog

### Version 1.0.0
- Initial release
- Full integration with Instant Meshes batch mode
- Complete parameter support
- Advanced options panel
- Comprehensive documentation
- Error handling and validation
