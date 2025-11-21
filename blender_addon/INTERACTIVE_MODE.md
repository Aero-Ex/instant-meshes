# Interactive Field Editing Guide

## 🎨 NEW! Interactive Field Editing

Version 3.0.0 introduces **Interactive Field Editing** - the ability to manually edit orientation and position fields using the Instant Meshes GUI!

---

## ✨ What is Interactive Field Editing?

Interactive mode launches the full Instant Meshes GUI application, allowing you to:

- **Visualize** the orientation field (directional lines showing quad/triangle alignment)
- **Edit** the orientation field with brush tools
- **Place constraints** manually at specific locations
- **Visualize** the position field (isolines showing mesh density)
- **Edit** the position field with brushes
- **See singularities** in real-time
- **Comb** the field to fix problem areas
- **Extract** the mesh when satisfied
- **Import back** to Blender with one click

---

## 🚀 Quick Start

### Basic Workflow

```
1. Select your mesh in Blender
2. Click "Edit Fields Interactively"
3. → Instant Meshes GUI opens automatically
4. Solve orientation field
5. Edit with brushes if needed
6. Solve position field
7. Edit with brushes if needed
8. Extract mesh
9. Save output (File → Export)
10. Return to Blender
11. Click "Reimport Result"
12. Done!
```

---

## 📖 Detailed Instructions

### Step 1: Launch Interactive Session

1. **Select a mesh object** in Blender (Object Mode)
2. Open the **Instant Meshes** panel (press N, click "Instant Meshes" tab)
3. Find the **"Interactive Field Editing"** section
4. Click **"Edit Fields Interactively"**

**What happens:**
- Blender exports your mesh to a temporary file
- Instant Meshes GUI launches automatically
- Your mesh is loaded and ready for editing
- The session is tracked in Blender

### Step 2: Work in Instant Meshes GUI

The Instant Meshes GUI will open with your mesh. Now you can:

#### 2a. Solve Orientation Field
- Click the first blue button **"Solve Orientation Field"**
- Watch the field arrows appear on your mesh
- This shows how quads/triangles will be aligned

#### 2b. Edit Orientation Field (Optional)
- Enable the **Orientation Brush** (first tool row)
- Click and drag on the mesh to adjust field direction
- Options:
  - **Stroke**: Paint field directions
  - **Smooth**: Smooth out the field
  - **Size**: Adjust brush size
- Place **hard constraints** by clicking specific points

#### 2c. Solve Position Field
- Click the second blue button **"Solve Position Field"**
- Isolines appear showing where edges will be
- This determines mesh density

#### 2d. Edit Position Field (Optional)
- Enable the **Position Brush** (second tool row)
- Click and drag to adjust mesh density
- Options:
  - **Stroke**: Paint isoline positions
  - **Smooth**: Smooth the position field
  - **Size**: Adjust brush size

#### 2e. Extract Mesh
- Click **"Export Mesh"** button
- The retopologized mesh is generated

#### 2f. Save Output
- Go to **File → Export Mesh**
- Save to the default location (already set correctly)
- **Important**: Don't change the filename or location!
- The default path is set to communicate with Blender

### Step 3: Reimport to Blender

1. Return to Blender (don't close Instant Meshes yet)
2. The **Interactive Field Editing** section now shows:
   - ✓ Session Active
   - Reimport Result button
   - Close Session button
3. Click **"Reimport Result"**
4. Your retopologized mesh appears in Blender!

**Options:**
- You can repeat steps 2-3 to iterate
- Edit more in Instant Meshes, save, reimport again
- The session stays active until you close it

### Step 4: Close Session

When you're done:
1. Close the Instant Meshes GUI
2. In Blender, click **"Close Session"**
3. Temporary files are cleaned up

---

## 🎯 Interactive Mode Features

### What You Can Do

| Feature | Description |
|---------|-------------|
| **Visualize Orientation Field** | See directional arrows showing quad alignment |
| **Visualize Position Field** | See isolines showing edge placement |
| **Brush Editing** | Paint and smooth both fields with brushes |
| **Hard Constraints** | Click to place exact orientation/position constraints |
| **Singularity Visualization** | See field singularities highlighted |
| **Real-time Preview** | See changes as you edit |
| **Crease Detection** | Sharp edges automatically detected and aligned |
| **Boundary Alignment** | Mesh boundaries automatically aligned |
| **Parameter Control** | Adjust all parameters in the GUI |
| **Multiple Iterations** | Edit → Save → Reimport → Repeat |

---

## 💡 When to Use Interactive Mode

### Use Interactive Mode When:
- ✅ You need **precise control** over field directions
- ✅ The automatic result has **problem areas** you want to fix
- ✅ You want to **align specific features** manually
- ✅ You need to **see the fields visually**
- ✅ You're working on a **hero asset** that needs perfection
- ✅ You want to **learn** how the fields work

### Use Batch Mode When:
- ✅ You have **many objects** to process
- ✅ The automatic results are **good enough**
- ✅ You want **fast, scripted** workflows
- ✅ You're doing **iterative testing**
- ✅ You need **reproducible** results (deterministic mode)

---

## 🛠️ Tips & Tricks

### Getting the Best Results

**1. Start with Good Parameters**
- Configure RoSy, PoSy, crease angle, etc. BEFORE launching interactive mode
- These settings are passed to Instant Meshes

**2. Use Crease Detection**
- Enable crease detection for hard-surface models
- Instant Meshes will pre-align the field to sharp edges
- Saves you manual editing work

**3. Work in Stages**
- First, solve and perfect the **orientation field**
- Only then move to the **position field**
- Don't try to do everything at once

**4. Use Brush Smoothing**
- If you make a mistake, use the **Smooth** brush mode
- It's easier than trying to repaint the correct direction

**5. Strategic Constraints**
- Place hard constraints at key features
- The field solver will respect these and interpolate smoothly

**6. Save Often**
- Save your work in Instant Meshes frequently
- You can reimport multiple times

**7. Compare Results**
- Try both automatic (batch mode) and interactive mode
- Often automatic is good enough!

### Keyboard Shortcuts in Instant Meshes

- **Left Mouse**: Rotate view
- **Right Mouse** / **Shift + Left Mouse**: Pan view
- **Mouse Wheel**: Zoom
- **Space**: Reset camera
- **Ctrl + Z**: Undo
- **Ctrl + Y**: Redo

### Common Issues

**Problem**: "Output file not found"
- **Solution**: Make sure you exported the mesh from Instant Meshes (File → Export)

**Problem**: "Output file hasn't changed"
- **Solution**: You need to save in Instant Meshes after making changes

**Problem**: Can't see the fields
- **Solution**: Click "Solve Orientation Field" or "Solve Position Field" first

**Problem**: Instant Meshes crashes
- **Solution**: Check that your mesh is manifold and has no errors

**Problem**: Session button missing
- **Solution**: Make sure you have a mesh selected in Object Mode

---

## 🎓 Understanding the Fields

### Orientation Field (RoSy)

The **orientation field** determines:
- Direction of edges (for quads: two perpendicular directions)
- How features align to mesh boundaries
- Where singularities occur

**Visualization**: Directional arrows or crosses on the mesh

**Control**:
- Brush editing: Paint field directions
- Constraints: Force specific alignments

### Position Field (PoSy)

The **position field** determines:
- Where edges will be placed
- Mesh density (spacing between edges)
- How well the output conforms to the input

**Visualization**: Isolines showing edge placement

**Control**:
- Brush editing: Adjust isoline spacing
- Constraints: Force edges through specific points

### Singularities

**Singularities** are special points where the field is undefined:
- **Orientation singularities**: Where quad layout has irregular vertices
- **Position singularities**: Where isolines merge

**In the GUI**: Highlighted with special markers

**Normal behavior**: Some singularities are necessary and good
**Problem**: Too many or poorly placed singularities

---

## 📊 Comparison: Batch vs. Interactive

| Aspect | Batch Mode | Interactive Mode |
|--------|-----------|------------------|
| **Speed** | ⚡ Fast (seconds) | 🐌 Slow (minutes to hours) |
| **Control** | 🔄 Automatic | ✋ Manual |
| **Visualization** | ❌ None | ✅ Full visualization |
| **Field Editing** | ❌ No | ✅ Yes, with brushes |
| **Best For** | Production, batching | Hero assets, learning |
| **Skill Required** | Low | Medium-High |
| **Reproducibility** | ✅ Perfect | ❌ Manual process |
| **Iteration** | ⚡ Instant | 🐌 Slow |

---

## 🔄 Example Workflows

### Workflow 1: Quick Fix

```
Problem: Automatic result is good except one area

1. Run batch mode first
2. Check the result
3. If one area needs fixing:
   - Launch interactive mode
   - Solve fields (don't edit)
   - Focus on problem area with brushes
   - Extract and save
   - Reimport
```

### Workflow 2: Full Manual Control

```
Goal: Perfect retopology for hero character

1. Launch interactive mode
2. Solve orientation field
3. Carefully edit orientation:
   - Align to facial features
   - Fix any singularities
   - Ensure smooth flow
4. Solve position field
5. Carefully edit position:
   - More density where needed
   - Less density elsewhere
6. Extract and refine
7. Iterate if needed
8. Reimport final result
```

### Workflow 3: Learning

```
Goal: Understand how fields work

1. Launch interactive mode
2. Solve orientation field
3. Observe the field directions
4. Try editing with brushes
5. See how it affects the result
6. Experiment with constraints
7. Solve position field
8. See how density is distributed
9. Extract and examine
10. Iterate and learn!
```

---

## 🆚 When NOT to Use Interactive Mode

**Skip interactive mode if:**
- ❌ You're processing hundreds of objects
- ❌ You need scripted, automated workflows
- ❌ You're just testing parameters
- ❌ The automatic result is already good
- ❌ You're on a tight deadline

**Use batch mode instead!** It's much faster and often produces excellent results automatically.

---

## 🐛 Troubleshooting

### Instant Meshes Won't Launch

**Check:**
1. Executable path is correct in addon preferences
2. You have permission to execute the file
3. You're in Object Mode
4. You have a mesh selected

### Can't Reimport

**Check:**
1. You saved the output from Instant Meshes (File → Export)
2. You saved to the default location (don't change path)
3. The session is still active in Blender
4. The output file exists

### Session is Stuck

**Solution:**
1. Click "Close Session" in Blender
2. Manually close Instant Meshes GUI
3. Try again

### Temporary Files Building Up

**Solution:**
- Enable "Keep Temporary Files" in addon preferences to debug
- Disable it to auto-clean up temp files
- Manual cleanup: Check `/tmp/instant_meshes_sessions/` (Linux/Mac) or `%TEMP%\instant_meshes_sessions\` (Windows)

---

## 📚 Learn More

- **Official Instant Meshes Video**: https://www.youtube.com/watch?v=U6wtw6W4x3I
- **Paper**: "Instant Field-Aligned Meshes" (SIGGRAPH Asia 2015)
- **Project Page**: http://igl.ethz.ch/projects/instant-meshes/

---

## 🎉 Summary

Interactive field editing gives you **complete control** over the retopology process:

✅ **Visualize** orientation and position fields
✅ **Edit** with intuitive brush tools
✅ **Place** hard constraints where needed
✅ **Iterate** between Blender and Instant Meshes
✅ **Perfect** your hero assets

Use it when you need precision, use batch mode when you need speed!

**The best of both worlds: Automatic processing for most cases, manual control when you need it.**
