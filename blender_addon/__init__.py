"""
Instant Meshes Blender Addon
=============================

A Blender addon for automatic retopology using Instant Meshes.

This addon provides a seamless integration of the Instant Meshes algorithm
into Blender, allowing users to generate clean, quad-based topology from
high-resolution meshes directly within Blender.

Author: Generated for Instant Meshes Project
License: BSD (matching Instant Meshes license)
"""

bl_info = {
    "name": "Instant Meshes Retopology",
    "author": "Instant Meshes Team",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Instant Meshes",
    "description": "Automatic retopology using Instant Meshes algorithm",
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
from bpy.props import (
    StringProperty,
    IntProperty,
    FloatProperty,
    BoolProperty,
    EnumProperty,
)
from bpy.types import (
    Operator,
    Panel,
    AddonPreferences,
    PropertyGroup,
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

    def draw(self, context):
        layout = self.layout
        layout.label(text="Configure the path to Instant Meshes executable:")
        layout.prop(self, "executable_path")

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


# ============================================================================
# Properties
# ============================================================================

class InstantMeshesProperties(PropertyGroup):
    """Properties for Instant Meshes settings"""

    # Target mesh size
    size_mode: EnumProperty(
        name="Size Mode",
        description="How to specify the target mesh size",
        items=[
            ('VERTICES', "Vertex Count", "Specify target number of vertices"),
            ('FACES', "Face Count", "Specify target number of faces"),
            ('SCALE', "Edge Length", "Specify target edge length in world units"),
        ],
        default='VERTICES',
    )

    vertex_count: IntProperty(
        name="Target Vertices",
        description="Desired number of vertices in output mesh",
        default=2000,
        min=4,
        max=1000000,
    )

    face_count: IntProperty(
        name="Target Faces",
        description="Desired number of faces in output mesh",
        default=2000,
        min=1,
        max=1000000,
    )

    edge_scale: FloatProperty(
        name="Edge Length",
        description="Desired edge length in world space units",
        default=0.1,
        min=0.0001,
        max=1000.0,
    )

    # Symmetry options
    rosy: EnumProperty(
        name="Orientation Symmetry",
        description="Rotation symmetry type for orientation field",
        items=[
            ('2', "2-Way", "2-way rotational symmetry (for triangle meshes)"),
            ('4', "4-Way", "4-way rotational symmetry (for quad meshes)"),
            ('6', "6-Way", "6-way rotational symmetry (for hex meshes)"),
        ],
        default='4',
    )

    posy: EnumProperty(
        name="Position Symmetry",
        description="Position symmetry type for position field",
        items=[
            ('4', "Quad", "Generate quad mesh"),
            ('6', "Triangle", "Generate triangle mesh"),
        ],
        default='4',
    )

    # Advanced options
    use_crease_angle: BoolProperty(
        name="Enable Crease Detection",
        description="Detect and preserve sharp creases",
        default=False,
    )

    crease_angle: FloatProperty(
        name="Crease Angle",
        description="Dihedral angle threshold for crease detection (in degrees)",
        default=30.0,
        min=0.0,
        max=180.0,
        subtype='ANGLE',
    )

    smooth_iter: IntProperty(
        name="Smooth Iterations",
        description="Number of smoothing and ray tracing reprojection steps",
        default=2,
        min=0,
        max=20,
    )

    deterministic: BoolProperty(
        name="Deterministic",
        description="Use deterministic algorithms (slower but reproducible)",
        default=False,
    )

    intrinsic: BoolProperty(
        name="Intrinsic Mode",
        description="Use intrinsic mode instead of extrinsic (advanced)",
        default=False,
    )

    align_to_boundaries: BoolProperty(
        name="Align to Boundaries",
        description="Align field to mesh boundaries (for open meshes)",
        default=False,
    )

    dominant: BoolProperty(
        name="Dominant Mode",
        description="Generate quad-dominant mesh instead of pure quad mesh",
        default=False,
    )

    # Threading
    threads: IntProperty(
        name="Threads",
        description="Number of threads for parallel computation (0 = auto)",
        default=0,
        min=0,
        max=64,
    )


# ============================================================================
# Operators
# ============================================================================

class MESH_OT_instant_meshes_retopo(Operator):
    """Run Instant Meshes retopology on the selected mesh"""
    bl_idname = "mesh.instant_meshes_retopo"
    bl_label = "Run Instant Meshes"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'OBJECT')

    def execute(self, context):
        # Get preferences
        preferences = context.preferences.addons[__name__].preferences
        executable = preferences.executable_path

        # Validate executable path
        if not executable or not os.path.exists(executable):
            self.report({'ERROR'},
                       "Instant Meshes executable not found! Please set it in addon preferences.")
            return {'CANCELLED'}

        # Get properties
        props = context.scene.instant_meshes_props
        obj = context.active_object

        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix="instant_meshes_")
        input_path = os.path.join(temp_dir, "input.obj")
        output_path = os.path.join(temp_dir, "output.obj")

        try:
            # Export input mesh
            self.report({'INFO'}, f"Exporting mesh to {input_path}...")
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj

            # Export as OBJ
            bpy.ops.wm.obj_export(
                filepath=input_path,
                export_selected_objects=True,
                apply_modifiers=True,
                export_uv=False,
                export_materials=False,
            )

            # Build command line arguments
            cmd = [executable, input_path, "-o", output_path]

            # Add size parameters
            if props.size_mode == 'VERTICES':
                cmd.extend(["-v", str(props.vertex_count)])
            elif props.size_mode == 'FACES':
                cmd.extend(["-f", str(props.face_count)])
            elif props.size_mode == 'SCALE':
                cmd.extend(["-s", str(props.edge_scale)])

            # Add symmetry parameters
            cmd.extend(["-r", props.rosy])
            cmd.extend(["-p", props.posy])

            # Add crease angle if enabled
            if props.use_crease_angle:
                cmd.extend(["-c", str(props.crease_angle)])

            # Add smoothing iterations
            cmd.extend(["-S", str(props.smooth_iter)])

            # Add boolean flags
            if props.deterministic:
                cmd.append("-d")
            if props.intrinsic:
                cmd.append("-i")
            if props.align_to_boundaries:
                cmd.append("-b")
            if props.dominant:
                cmd.append("-D")

            # Add thread count if specified
            if props.threads > 0:
                cmd.extend(["-t", str(props.threads)])

            # Run Instant Meshes
            self.report({'INFO'}, f"Running Instant Meshes: {' '.join(cmd)}")

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minute timeout
                    check=True,
                )

                # Print output for debugging
                if result.stdout:
                    print("Instant Meshes output:")
                    print(result.stdout)
                if result.stderr:
                    print("Instant Meshes errors:")
                    print(result.stderr)

            except subprocess.CalledProcessError as e:
                self.report({'ERROR'}, f"Instant Meshes failed: {e.stderr}")
                return {'CANCELLED'}
            except subprocess.TimeoutExpired:
                self.report({'ERROR'}, "Instant Meshes timed out after 5 minutes")
                return {'CANCELLED'}

            # Check if output was created
            if not os.path.exists(output_path):
                self.report({'ERROR'}, "Instant Meshes did not create output file")
                return {'CANCELLED'}

            # Import result
            self.report({'INFO'}, f"Importing result from {output_path}...")

            # Store original object name and location
            orig_name = obj.name
            orig_location = obj.location.copy()

            # Import OBJ
            bpy.ops.wm.obj_import(filepath=output_path)

            # Get the imported object (should be the most recently added)
            imported_obj = context.selected_objects[0] if context.selected_objects else None

            if imported_obj:
                # Rename and position
                imported_obj.name = f"{orig_name}_retopo"
                imported_obj.location = orig_location

                # Select the new object
                bpy.ops.object.select_all(action='DESELECT')
                imported_obj.select_set(True)
                context.view_layer.objects.active = imported_obj

                self.report({'INFO'}, f"Retopology complete! Created '{imported_obj.name}'")
            else:
                self.report({'WARNING'}, "Import succeeded but couldn't find imported object")

            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Error during retopology: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

        finally:
            # Clean up temporary files
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Warning: Could not clean up temp directory: {e}")


class MESH_OT_instant_meshes_test_executable(Operator):
    """Test if the Instant Meshes executable is working"""
    bl_idname = "mesh.instant_meshes_test"
    bl_label = "Test Executable"

    def execute(self, context):
        preferences = context.preferences.addons[__name__].preferences
        executable = preferences.executable_path

        if not executable:
            self.report({'ERROR'}, "No executable path set")
            return {'CANCELLED'}

        if not os.path.exists(executable):
            self.report({'ERROR'}, f"File not found: {executable}")
            return {'CANCELLED'}

        try:
            # Try to run with --help
            result = subprocess.run(
                [executable, "--help"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == -1 or "Instant Meshes" in result.stdout or "Syntax:" in result.stdout:
                self.report({'INFO'}, "Executable is working correctly!")
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "Executable ran but output was unexpected")
                return {'FINISHED'}

        except subprocess.TimeoutExpired:
            self.report({'WARNING'}, "Executable timed out (this might be normal)")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error testing executable: {str(e)}")
            return {'CANCELLED'}


# ============================================================================
# UI Panels
# ============================================================================

class VIEW3D_PT_instant_meshes(Panel):
    """Main Instant Meshes panel"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Instant Meshes"
    bl_label = "Instant Meshes"
    bl_idname = "VIEW3D_PT_instant_meshes"

    def draw(self, context):
        layout = self.layout
        props = context.scene.instant_meshes_props

        # Check if executable is set
        preferences = context.preferences.addons[__name__].preferences
        if not preferences.executable_path or not os.path.exists(preferences.executable_path):
            box = layout.box()
            box.label(text="Executable not configured!", icon='ERROR')
            box.label(text="Please set the path in addon preferences")
            box.operator("screen.userpref_show", text="Open Preferences", icon='PREFERENCES')
            return

        # Main retopology button
        box = layout.box()
        box.scale_y = 1.5

        if context.active_object and context.active_object.type == 'MESH':
            box.operator("mesh.instant_meshes_retopo", icon='MOD_REMESH')
        else:
            box.label(text="Select a mesh object", icon='INFO')

        # Target mesh size
        layout.separator()
        box = layout.box()
        box.label(text="Target Mesh Size:", icon='MESH_DATA')
        box.prop(props, "size_mode", text="")

        if props.size_mode == 'VERTICES':
            box.prop(props, "vertex_count")
        elif props.size_mode == 'FACES':
            box.prop(props, "face_count")
        elif props.size_mode == 'SCALE':
            box.prop(props, "edge_scale")

        # Symmetry settings
        layout.separator()
        box = layout.box()
        box.label(text="Symmetry:", icon='ORIENTATION_GIMBAL')
        box.prop(props, "rosy")
        box.prop(props, "posy")


class VIEW3D_PT_instant_meshes_advanced(Panel):
    """Advanced Instant Meshes settings"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Instant Meshes"
    bl_label = "Advanced Options"
    bl_parent_id = "VIEW3D_PT_instant_meshes"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.instant_meshes_props

        # Crease detection
        box = layout.box()
        box.label(text="Crease Detection:", icon='EDGESEL')
        box.prop(props, "use_crease_angle")
        if props.use_crease_angle:
            box.prop(props, "crease_angle")

        # Quality settings
        layout.separator()
        box = layout.box()
        box.label(text="Quality:", icon='SMOOTHCURVE')
        box.prop(props, "smooth_iter")
        box.prop(props, "dominant")

        # Alignment options
        layout.separator()
        box = layout.box()
        box.label(text="Alignment:", icon='SNAP_ON')
        box.prop(props, "align_to_boundaries")

        # Processing options
        layout.separator()
        box = layout.box()
        box.label(text="Processing:", icon='SETTINGS')
        box.prop(props, "deterministic")
        box.prop(props, "intrinsic")
        box.prop(props, "threads")


# ============================================================================
# Registration
# ============================================================================

classes = (
    InstantMeshesPreferences,
    InstantMeshesProperties,
    MESH_OT_instant_meshes_retopo,
    MESH_OT_instant_meshes_test_executable,
    VIEW3D_PT_instant_meshes,
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
