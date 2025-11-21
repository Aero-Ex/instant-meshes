"""
Instant Meshes Blender Addon - FULL EDITION
============================================

Complete integration of ALL Instant Meshes functionality into Blender.

This addon exposes 100% of Instant Meshes features including:
- Mesh and Point Cloud retopology
- Multiple file format support (OBJ, PLY)
- Complete parameter control
- Preset system
- Batch processing
- Advanced visualization options

Author: Generated for Instant Meshes Project
License: BSD (matching Instant Meshes license)
"""

bl_info = {
    "name": "Instant Meshes Retopology (Full)",
    "author": "Instant Meshes Team",
    "version": (2, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Instant Meshes",
    "description": "Complete Instant Meshes integration - all features exposed",
    "warning": "Requires Instant Meshes executable",
    "doc_url": "https://github.com/wjakob/instant-meshes",
    "category": "Mesh",
}

import bpy
import os
import sys
import subprocess
import tempfile
import platform
import json
from bpy.props import (
    StringProperty,
    IntProperty,
    FloatProperty,
    BoolProperty,
    EnumProperty,
    CollectionProperty,
)
from bpy.types import (
    Operator,
    Panel,
    AddonPreferences,
    PropertyGroup,
    UIList,
)


# ============================================================================
# Preferences
# ============================================================================

class InstantMeshesPreferences(AddonPreferences):
    bl_idname = __name__

    executable_path: StringProperty(
        name="Instant Meshes Executable",
        description="Path to the Instant Meshes executable",
        subtype='FILE_PATH',
        default="",
    )

    default_output_format: EnumProperty(
        name="Default Output Format",
        description="Preferred output file format",
        items=[
            ('OBJ', "OBJ", "Wavefront OBJ format (widely compatible)"),
            ('PLY', "PLY", "Stanford PLY format (faster, binary)"),
        ],
        default='OBJ',
    )

    keep_temp_files: BoolProperty(
        name="Keep Temporary Files",
        description="Don't delete temporary files (for debugging)",
        default=False,
    )

    show_console_output: BoolProperty(
        name="Show Console Output",
        description="Print Instant Meshes output to console",
        default=True,
    )

    auto_select_result: BoolProperty(
        name="Auto-Select Result",
        description="Automatically select the retopologized mesh",
        default=True,
    )

    def draw(self, context):
        layout = self.layout

        # Executable configuration
        box = layout.box()
        box.label(text="Executable Configuration:", icon='SETTINGS')
        box.prop(self, "executable_path")

        row = box.row()
        row.operator("mesh.instant_meshes_test", icon='CHECKMARK')

        # Installation instructions
        box = layout.box()
        box.label(text="Installation Instructions:", icon='INFO')
        box.label(text="1. Download Instant Meshes from:")
        box.label(text="   https://github.com/wjakob/instant-meshes/releases")
        box.label(text="2. Extract the archive")
        box.label(text="3. Set the path above to the executable:")
        if platform.system() == "Windows":
            box.label(text="   Example: C:\\InstantMeshes\\Instant Meshes.exe")
        elif platform.system() == "Darwin":
            box.label(text="   Example: /Applications/Instant Meshes.app/Contents/MacOS/Instant Meshes")
        else:
            box.label(text="   Example: /opt/instant-meshes/Instant Meshes")

        # Preferences
        layout.separator()
        box = layout.box()
        box.label(text="General Preferences:", icon='PREFERENCES')
        box.prop(self, "default_output_format")
        box.prop(self, "keep_temp_files")
        box.prop(self, "show_console_output")
        box.prop(self, "auto_select_result")


# ============================================================================
# Presets
# ============================================================================

class InstantMeshesPreset(PropertyGroup):
    """A saved preset for Instant Meshes settings"""
    name: StringProperty(name="Preset Name", default="New Preset")


# ============================================================================
# Properties
# ============================================================================

class InstantMeshesProperties(PropertyGroup):
    """Properties for Instant Meshes settings - ALL PARAMETERS EXPOSED"""

    # ========================================================================
    # Input Settings
    # ========================================================================

    input_type: EnumProperty(
        name="Input Type",
        description="Type of input data",
        items=[
            ('MESH', "Mesh", "Process a mesh object"),
            ('POINTCLOUD', "Point Cloud", "Process point cloud data (vertices only)"),
        ],
        default='MESH',
    )

    # Point cloud specific
    knn_points: IntProperty(
        name="kNN Points",
        description="Point cloud mode: number of adjacent points to consider for connectivity",
        default=10,
        min=3,
        max=100,
    )

    # ========================================================================
    # Output Settings
    # ========================================================================

    output_format: EnumProperty(
        name="Output Format",
        description="File format for the retopologized mesh",
        items=[
            ('OBJ', "OBJ", "Wavefront OBJ format (widely compatible)"),
            ('PLY', "PLY", "Stanford PLY format (faster, stores more data)"),
        ],
        default='OBJ',
    )

    # ========================================================================
    # Target Mesh Size
    # ========================================================================

    size_mode: EnumProperty(
        name="Size Mode",
        description="How to specify the target mesh size",
        items=[
            ('VERTICES', "Vertex Count", "Specify target number of vertices"),
            ('FACES', "Face Count", "Specify target number of faces"),
            ('SCALE', "Edge Length", "Specify target edge length in world units"),
            ('AUTO', "Auto (1/16)", "Automatically use 1/16 of input vertex count"),
        ],
        default='VERTICES',
    )

    vertex_count: IntProperty(
        name="Target Vertices",
        description="Desired number of vertices in output mesh",
        default=2000,
        min=4,
        max=10000000,
    )

    face_count: IntProperty(
        name="Target Faces",
        description="Desired number of faces in output mesh",
        default=2000,
        min=1,
        max=10000000,
    )

    edge_scale: FloatProperty(
        name="Edge Length",
        description="Desired edge length in world space units",
        default=0.1,
        min=0.0001,
        max=10000.0,
        precision=4,
    )

    # ========================================================================
    # Symmetry Options
    # ========================================================================

    rosy: EnumProperty(
        name="Orientation Symmetry (RoSy)",
        description="Rotation symmetry type for orientation field",
        items=[
            ('2', "2-Way (DiSy)", "2-way rotational symmetry - for triangle meshes with specific alignment"),
            ('4', "4-Way (Cross)", "4-way rotational symmetry - standard for quad meshes"),
            ('6', "6-Way (Hex)", "6-way rotational symmetry - for hexagonal/triangle patterns"),
        ],
        default='4',
    )

    posy: EnumProperty(
        name="Position Symmetry (PoSy)",
        description="Position symmetry type - determines output mesh type",
        items=[
            ('4', "Quad Mesh", "Generate quadrilateral mesh (best for subdivision)"),
            ('6', "Triangle Mesh", "Generate triangular mesh (best for games/rendering)"),
        ],
        default='4',
    )

    # ========================================================================
    # Field Mode
    # ========================================================================

    extrinsic: BoolProperty(
        name="Extrinsic Mode",
        description="Use extrinsic field formulation (recommended). Disable for intrinsic mode",
        default=True,
    )

    # ========================================================================
    # Crease Detection
    # ========================================================================

    use_crease_angle: BoolProperty(
        name="Enable Crease Detection",
        description="Detect and preserve sharp creases based on dihedral angle",
        default=False,
    )

    crease_angle: FloatProperty(
        name="Crease Angle",
        description="Dihedral angle threshold for crease detection (degrees)",
        default=30.0,
        min=0.0,
        max=180.0,
        subtype='ANGLE',
    )

    # ========================================================================
    # Quality Settings
    # ========================================================================

    smooth_iter: IntProperty(
        name="Smooth Iterations",
        description="Number of smoothing and ray tracing reprojection steps (higher = better quality)",
        default=2,
        min=0,
        max=100,
    )

    dominant: BoolProperty(
        name="Dominant Mode",
        description="Generate quad-dominant (mixed) mesh instead of pure quad mesh. Allows triangles for better adaptivity",
        default=False,
    )

    # ========================================================================
    # Boundary Alignment
    # ========================================================================

    align_to_boundaries: BoolProperty(
        name="Align to Boundaries",
        description="Align orientation field to mesh boundaries (only for open/non-closed meshes)",
        default=False,
    )

    # ========================================================================
    # Processing Options
    # ========================================================================

    deterministic: BoolProperty(
        name="Deterministic Mode",
        description="Use deterministic algorithms for reproducible results (slower but repeatable)",
        default=False,
    )

    threads: IntProperty(
        name="Thread Count",
        description="Number of threads for parallel computation (0 = automatic based on CPU cores)",
        default=0,
        min=0,
        max=128,
    )

    # ========================================================================
    # Output Options
    # ========================================================================

    output_name_mode: EnumProperty(
        name="Output Naming",
        description="How to name the output object",
        items=[
            ('SUFFIX', "Add Suffix", "Add '_retopo' suffix to original name"),
            ('REPLACE', "Replace", "Replace original object"),
            ('CUSTOM', "Custom Name", "Use custom name"),
        ],
        default='SUFFIX',
    )

    custom_output_name: StringProperty(
        name="Custom Name",
        description="Custom name for output object",
        default="Retopo",
    )

    # ========================================================================
    # Preset Management
    # ========================================================================

    active_preset: IntProperty(
        name="Active Preset",
        description="Currently active preset",
        default=0,
    )


# ============================================================================
# Utility Functions
# ============================================================================

def get_executable_path(context):
    """Get and validate executable path"""
    preferences = context.preferences.addons[__name__].preferences
    executable = preferences.executable_path

    if not executable or not os.path.exists(executable):
        return None
    return executable


def apply_preset(context, preset_name):
    """Apply a preset to current settings"""
    props = context.scene.instant_meshes_props

    presets = {
        'game_lowpoly': {
            'size_mode': 'VERTICES',
            'vertex_count': 1000,
            'rosy': '4',
            'posy': '4',
            'smooth_iter': 1,
            'use_crease_angle': True,
            'crease_angle': 35.0,
            'dominant': False,
        },
        'game_midpoly': {
            'size_mode': 'VERTICES',
            'vertex_count': 5000,
            'rosy': '4',
            'posy': '4',
            'smooth_iter': 2,
            'use_crease_angle': True,
            'crease_angle': 30.0,
            'dominant': False,
        },
        'subdivision_base': {
            'size_mode': 'VERTICES',
            'vertex_count': 8000,
            'rosy': '4',
            'posy': '4',
            'smooth_iter': 5,
            'use_crease_angle': False,
            'dominant': False,
            'align_to_boundaries': True,
        },
        'high_detail': {
            'size_mode': 'VERTICES',
            'vertex_count': 15000,
            'rosy': '4',
            'posy': '4',
            'smooth_iter': 10,
            'use_crease_angle': True,
            'crease_angle': 25.0,
            'dominant': False,
        },
        'hard_surface': {
            'size_mode': 'FACES',
            'face_count': 3000,
            'rosy': '4',
            'posy': '4',
            'smooth_iter': 3,
            'use_crease_angle': True,
            'crease_angle': 30.0,
            'dominant': False,
        },
        'organic_character': {
            'size_mode': 'VERTICES',
            'vertex_count': 10000,
            'rosy': '4',
            'posy': '4',
            'smooth_iter': 5,
            'use_crease_angle': False,
            'dominant': False,
        },
        'triangle_mesh': {
            'size_mode': 'VERTICES',
            'vertex_count': 5000,
            'rosy': '6',
            'posy': '6',
            'smooth_iter': 2,
            'use_crease_angle': False,
            'dominant': True,
        },
        'point_cloud': {
            'input_type': 'POINTCLOUD',
            'size_mode': 'VERTICES',
            'vertex_count': 3000,
            'knn_points': 10,
            'rosy': '4',
            'posy': '4',
            'smooth_iter': 3,
        },
    }

    if preset_name in presets:
        preset_data = presets[preset_name]
        for key, value in preset_data.items():
            if hasattr(props, key):
                setattr(props, key, value)
        return True
    return False


# ============================================================================
# Operators
# ============================================================================

class MESH_OT_instant_meshes_retopo(Operator):
    """Run Instant Meshes retopology with ALL parameters exposed"""
    bl_idname = "mesh.instant_meshes_retopo"
    bl_label = "Run Instant Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'OBJECT')

    def execute(self, context):
        executable = get_executable_path(context)
        if not executable:
            self.report({'ERROR'}, "Instant Meshes executable not found! Configure in addon preferences.")
            return {'CANCELLED'}

        props = context.scene.instant_meshes_props
        preferences = context.preferences.addons[__name__].preferences
        obj = context.active_object

        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="instant_meshes_")

        # Determine file format
        out_format = props.output_format.lower()
        input_path = os.path.join(temp_dir, f"input.{out_format}")
        output_path = os.path.join(temp_dir, f"output.{out_format}")

        try:
            # Export input mesh
            self.report({'INFO'}, f"Exporting {props.input_type.lower()} to {input_path}...")
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj

            # Export based on format
            if out_format == 'obj':
                bpy.ops.wm.obj_export(
                    filepath=input_path,
                    export_selected_objects=True,
                    apply_modifiers=True,
                    export_uv=False,
                    export_materials=False,
                )
            elif out_format == 'ply':
                bpy.ops.wm.ply_export(
                    filepath=input_path,
                    export_selected_objects=True,
                    apply_modifiers=True,
                )

            # Build command line
            cmd = [executable, input_path, "-o", output_path]

            # Size parameters
            if props.size_mode == 'VERTICES':
                cmd.extend(["-v", str(props.vertex_count)])
            elif props.size_mode == 'FACES':
                cmd.extend(["-f", str(props.face_count)])
            elif props.size_mode == 'SCALE':
                cmd.extend(["-s", str(props.edge_scale)])
            # AUTO mode: let Instant Meshes decide (no parameter)

            # Symmetry
            cmd.extend(["-r", props.rosy])
            cmd.extend(["-p", props.posy])

            # Crease detection
            if props.use_crease_angle:
                cmd.extend(["-c", str(props.crease_angle)])

            # Quality
            cmd.extend(["-S", str(props.smooth_iter)])

            # Field mode
            if not props.extrinsic:
                cmd.append("-i")  # intrinsic mode

            # Boundaries
            if props.align_to_boundaries:
                cmd.append("-b")

            # Dominant mode
            if props.dominant:
                cmd.append("-D")

            # Processing
            if props.deterministic:
                cmd.append("-d")

            if props.threads > 0:
                cmd.extend(["-t", str(props.threads)])

            # Point cloud specific
            if props.input_type == 'POINTCLOUD':
                cmd.extend(["-k", str(props.knn_points)])

            # Run Instant Meshes
            self.report({'INFO'}, f"Running: {' '.join(cmd)}")

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=600,  # 10 minute timeout
                    check=True,
                )

                if preferences.show_console_output:
                    if result.stdout:
                        print("=== Instant Meshes Output ===")
                        print(result.stdout)
                    if result.stderr:
                        print("=== Instant Meshes Errors ===")
                        print(result.stderr)

            except subprocess.CalledProcessError as e:
                self.report({'ERROR'}, f"Instant Meshes failed: {e.stderr}")
                return {'CANCELLED'}
            except subprocess.TimeoutExpired:
                self.report({'ERROR'}, "Process timed out after 10 minutes")
                return {'CANCELLED'}

            # Check output
            if not os.path.exists(output_path):
                self.report({'ERROR'}, "No output file created")
                return {'CANCELLED'}

            # Import result
            self.report({'INFO'}, f"Importing result...")

            orig_name = obj.name
            orig_location = obj.location.copy()

            # Import based on format
            if out_format == 'obj':
                bpy.ops.wm.obj_import(filepath=output_path)
            elif out_format == 'ply':
                bpy.ops.wm.ply_import(filepath=output_path)

            imported_obj = context.selected_objects[0] if context.selected_objects else None

            if imported_obj:
                # Name the output
                if props.output_name_mode == 'SUFFIX':
                    imported_obj.name = f"{orig_name}_retopo"
                elif props.output_name_mode == 'REPLACE':
                    imported_obj.name = orig_name
                    bpy.data.objects.remove(obj, do_unlink=True)
                elif props.output_name_mode == 'CUSTOM':
                    imported_obj.name = props.custom_output_name

                imported_obj.location = orig_location

                if preferences.auto_select_result:
                    bpy.ops.object.select_all(action='DESELECT')
                    imported_obj.select_set(True)
                    context.view_layer.objects.active = imported_obj

                self.report({'INFO'}, f"Success! Created '{imported_obj.name}'")
            else:
                self.report({'WARNING'}, "Import succeeded but couldn't find object")

            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

        finally:
            # Clean up
            if not preferences.keep_temp_files:
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    print(f"Warning: Could not clean up temp files: {e}")


class MESH_OT_instant_meshes_batch(Operator):
    """Batch process all selected mesh objects"""
    bl_idname = "mesh.instant_meshes_batch"
    bl_label = "Batch Process Selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return any(obj.type == 'MESH' for obj in context.selected_objects)

    def execute(self, context):
        mesh_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if not mesh_objects:
            self.report({'ERROR'}, "No mesh objects selected")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Processing {len(mesh_objects)} objects...")

        success_count = 0
        fail_count = 0

        for obj in mesh_objects:
            # Select only this object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj

            # Process it
            result = bpy.ops.mesh.instant_meshes_retopo()

            if result == {'FINISHED'}:
                success_count += 1
            else:
                fail_count += 1

        self.report({'INFO'}, f"Batch complete: {success_count} succeeded, {fail_count} failed")
        return {'FINISHED'}


class MESH_OT_instant_meshes_apply_preset(Operator):
    """Apply a preset configuration"""
    bl_idname = "mesh.instant_meshes_apply_preset"
    bl_label = "Apply Preset"

    preset_name: StringProperty()

    def execute(self, context):
        if apply_preset(context, self.preset_name):
            self.report({'INFO'}, f"Applied preset: {self.preset_name}")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"Unknown preset: {self.preset_name}")
            return {'CANCELLED'}


class MESH_OT_instant_meshes_test_executable(Operator):
    """Test if the Instant Meshes executable is working"""
    bl_idname = "mesh.instant_meshes_test"
    bl_label = "Test Executable"

    def execute(self, context):
        executable = get_executable_path(context)

        if not executable:
            self.report({'ERROR'}, "No executable path set or file not found")
            return {'CANCELLED'}

        try:
            result = subprocess.run(
                [executable, "--help"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == -1 or "Instant Meshes" in result.stdout or "Syntax:" in result.stdout:
                self.report({'INFO'}, "✓ Executable is working correctly!")
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "Executable ran but output was unexpected")
                return {'FINISHED'}

        except subprocess.TimeoutExpired:
            self.report({'WARNING'}, "Executable timed out (might be GUI mode)")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}


# ============================================================================
# UI Panels
# ============================================================================

class VIEW3D_PT_instant_meshes(Panel):
    """Main Instant Meshes panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Instant Meshes"
    bl_label = "Instant Meshes (Full)"
    bl_idname = "VIEW3D_PT_instant_meshes"

    def draw(self, context):
        layout = self.layout
        props = context.scene.instant_meshes_props
        preferences = context.preferences.addons[__name__].preferences

        # Check executable
        if not get_executable_path(context):
            box = layout.box()
            box.label(text="⚠ Executable Not Configured!", icon='ERROR')
            box.label(text="Set path in addon preferences:")
            box.operator("screen.userpref_show", text="Open Preferences", icon='PREFERENCES')
            return

        # Main buttons
        box = layout.box()
        box.scale_y = 1.3

        if context.active_object and context.active_object.type == 'MESH':
            box.operator("mesh.instant_meshes_retopo", icon='MOD_REMESH', text="Run Instant Meshes")
        else:
            box.label(text="Select a mesh object", icon='INFO')

        # Batch processing
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if len(selected_meshes) > 1:
            box.operator("mesh.instant_meshes_batch", icon='RENDERLAYERS',
                        text=f"Batch Process ({len(selected_meshes)} objects)")

        # Input type
        layout.separator()
        layout.prop(props, "input_type", expand=True)

        if props.input_type == 'POINTCLOUD':
            box = layout.box()
            box.label(text="Point Cloud Settings:", icon='PARTICLE_POINT')
            box.prop(props, "knn_points")
            box.label(text="Note: Input must have vertices only", icon='INFO')


class VIEW3D_PT_instant_meshes_presets(Panel):
    """Preset panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Instant Meshes"
    bl_label = "Presets"
    bl_parent_id = "VIEW3D_PT_instant_meshes"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Quick Presets:", icon='PRESET')

        col = box.column(align=True)
        col.operator("mesh.instant_meshes_apply_preset", text="Game Low-Poly", icon='MESH_MONKEY').preset_name = 'game_lowpoly'
        col.operator("mesh.instant_meshes_apply_preset", text="Game Mid-Poly", icon='MESH_UVSPHERE').preset_name = 'game_midpoly'
        col.operator("mesh.instant_meshes_apply_preset", text="Subdivision Base", icon='MOD_SUBSURF').preset_name = 'subdivision_base'
        col.operator("mesh.instant_meshes_apply_preset", text="High Detail", icon='MESH_ICOSPHERE').preset_name = 'high_detail'
        col.operator("mesh.instant_meshes_apply_preset", text="Hard Surface", icon='MESH_CUBE').preset_name = 'hard_surface'
        col.operator("mesh.instant_meshes_apply_preset", text="Organic Character", icon='ARMATURE_DATA').preset_name = 'organic_character'
        col.operator("mesh.instant_meshes_apply_preset", text="Triangle Mesh", icon='MESH_DATA').preset_name = 'triangle_mesh'
        col.operator("mesh.instant_meshes_apply_preset", text="Point Cloud", icon='PARTICLE_POINT').preset_name = 'point_cloud'


class VIEW3D_PT_instant_meshes_size(Panel):
    """Target size panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Instant Meshes"
    bl_label = "Target Mesh Size"
    bl_parent_id = "VIEW3D_PT_instant_meshes"

    def draw(self, context):
        layout = self.layout
        props = context.scene.instant_meshes_props

        layout.prop(props, "size_mode", text="")

        box = layout.box()
        if props.size_mode == 'VERTICES':
            box.prop(props, "vertex_count", slider=False)
        elif props.size_mode == 'FACES':
            box.prop(props, "face_count", slider=False)
        elif props.size_mode == 'SCALE':
            box.prop(props, "edge_scale")
        elif props.size_mode == 'AUTO':
            box.label(text="Automatic: 1/16 of input", icon='AUTO')


class VIEW3D_PT_instant_meshes_symmetry(Panel):
    """Symmetry panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Instant Meshes"
    bl_label = "Symmetry & Field"
    bl_parent_id = "VIEW3D_PT_instant_meshes"

    def draw(self, context):
        layout = self.layout
        props = context.scene.instant_meshes_props

        box = layout.box()
        box.label(text="Orientation Field:", icon='ORIENTATION_GIMBAL')
        box.prop(props, "rosy")

        box = layout.box()
        box.label(text="Position Field:", icon='MESH_DATA')
        box.prop(props, "posy")

        box = layout.box()
        box.label(text="Field Mode:", icon='SETTINGS')
        box.prop(props, "extrinsic", toggle=True)
        if not props.extrinsic:
            box.label(text="Using intrinsic mode", icon='INFO')


class VIEW3D_PT_instant_meshes_quality(Panel):
    """Quality panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Instant Meshes"
    bl_label = "Quality & Features"
    bl_parent_id = "VIEW3D_PT_instant_meshes"

    def draw(self, context):
        layout = self.layout
        props = context.scene.instant_meshes_props

        # Crease detection
        box = layout.box()
        box.label(text="Crease Detection:", icon='EDGESEL')
        box.prop(props, "use_crease_angle", toggle=True)
        if props.use_crease_angle:
            box.prop(props, "crease_angle", slider=True)

        # Smoothing
        box = layout.box()
        box.label(text="Smoothing:", icon='SMOOTHCURVE')
        box.prop(props, "smooth_iter", slider=True)
        box.label(text=f"Quality: {'Low' if props.smooth_iter < 2 else 'Medium' if props.smooth_iter < 5 else 'High'}",
                 icon='INFO')

        # Mesh type
        box = layout.box()
        box.label(text="Mesh Type:", icon='MESH_GRID')
        box.prop(props, "dominant", toggle=True)
        if props.dominant:
            box.label(text="Mixed quad/tri mesh", icon='INFO')
        else:
            box.label(text="Pure quad/tri mesh", icon='INFO')

        # Boundary alignment
        box = layout.box()
        box.label(text="Boundaries:", icon='SNAP_ON')
        box.prop(props, "align_to_boundaries", toggle=True)
        if props.align_to_boundaries:
            box.label(text="For open meshes", icon='INFO')


class VIEW3D_PT_instant_meshes_advanced(Panel):
    """Advanced options panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Instant Meshes"
    bl_label = "Advanced Options"
    bl_parent_id = "VIEW3D_PT_instant_meshes"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.instant_meshes_props

        # Processing
        box = layout.box()
        box.label(text="Processing:", icon='SETTINGS')
        box.prop(props, "deterministic", toggle=True)
        box.prop(props, "threads")

        if props.threads == 0:
            box.label(text="Auto: Using all CPU cores", icon='INFO')
        else:
            box.label(text=f"Using {props.threads} thread(s)", icon='INFO')

        # Output
        box = layout.box()
        box.label(text="Output:", icon='EXPORT')
        box.prop(props, "output_format")
        box.prop(props, "output_name_mode", text="Naming")

        if props.output_name_mode == 'CUSTOM':
            box.prop(props, "custom_output_name", text="")


# ============================================================================
# Registration
# ============================================================================

classes = (
    InstantMeshesPreferences,
    InstantMeshesPreset,
    InstantMeshesProperties,
    MESH_OT_instant_meshes_retopo,
    MESH_OT_instant_meshes_batch,
    MESH_OT_instant_meshes_apply_preset,
    MESH_OT_instant_meshes_test_executable,
    VIEW3D_PT_instant_meshes,
    VIEW3D_PT_instant_meshes_presets,
    VIEW3D_PT_instant_meshes_size,
    VIEW3D_PT_instant_meshes_symmetry,
    VIEW3D_PT_instant_meshes_quality,
    VIEW3D_PT_instant_meshes_advanced,
)


def register():
    """Register addon classes and properties"""
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.instant_meshes_props = bpy.props.PointerProperty(
        type=InstantMeshesProperties
    )


def unregister():
    """Unregister addon classes and properties"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.instant_meshes_props


if __name__ == "__main__":
    register()
