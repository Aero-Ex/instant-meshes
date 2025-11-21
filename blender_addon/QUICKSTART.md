# Quick Start Guide

Get up and running with Instant Meshes in Blender in 60 seconds!

## Your First Retopology

### 1. Select a Mesh
- Click on a mesh object in your scene
- Make sure you're in **Object Mode** (Tab to switch)

### 2. Open Instant Meshes Panel
- Press `N` to show the sidebar
- Click the **"Instant Meshes"** tab

### 3. Run!
- Click the big **"Run Instant Meshes"** button
- Wait a few seconds
- A new retopologized mesh will appear!

That's it! The default settings work great for most meshes.

## Basic Controls

### Target Mesh Size
The most important setting - controls how detailed your output will be:

- **Small values** (500-2000): Low-poly for games
- **Medium values** (2000-10000): General purpose
- **Large values** (10000+): High detail preservation

**Quick tip**: Start with 1/16th of your original vertex count.

### Mesh Type
- **4-Way / Quad**: Creates quad meshes (best for subdivision)
- **6-Way / Triangle**: Creates triangle meshes (best for games)

## Common Use Cases

### Game Asset (Low Poly)
```
Size Mode: Vertex Count
Target Vertices: 1000
Orientation: 4-Way
Position: Quad
```

### Subdivision Surface Base
```
Size Mode: Vertex Count
Target Vertices: 5000
Orientation: 4-Way
Position: Quad
Smooth Iterations: 5
```

### Hard Surface Model
```
Size Mode: Face Count
Target Faces: 3000
Orientation: 4-Way
Position: Quad
Enable Crease Detection: ✓
Crease Angle: 30°
```

### Organic Character
```
Size Mode: Vertex Count
Target Vertices: 8000
Orientation: 4-Way
Position: Quad
Smooth Iterations: 3
Align to Boundaries: ✓ (if needed)
```

## Tips

✅ **DO:**
- Start with default settings
- Use quad output for subdivision
- Enable crease detection for hard surfaces
- Increase smooth iterations for better quality

❌ **DON'T:**
- Set vertex count too high (start small!)
- Expect UVs to transfer (they won't)
- Process very large meshes without patience
- Forget to save before processing

## Next Steps

Once comfortable with basics:
1. Explore **Advanced Options** panel
2. Try different symmetry settings
3. Experiment with edge length mode
4. Read the full README.md for details

## Keyboard Shortcuts

While there are no built-in shortcuts, you can create your own:
1. Right-click "Run Instant Meshes" button
2. Choose "Assign Shortcut"
3. Press your desired key combination

## Need More Help?

- Full documentation: [README.md](README.md)
- Installation help: [INSTALLATION.md](INSTALLATION.md)
- Instant Meshes website: http://igl.ethz.ch/projects/instant-meshes/
