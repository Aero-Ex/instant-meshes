"""
Batch Retopology Example Script
================================

This script demonstrates how to use the Instant Meshes addon
programmatically to process multiple objects.

Usage:
1. Open Blender
2. Make sure Instant Meshes addon is installed and configured
3. Open this script in Blender's Text Editor
4. Run the script

The script will retopologize all mesh objects in the scene.
"""

import bpy


def retopologize_object(obj, vertex_count=2000, use_crease=False):
    """
    Retopologize a single object using Instant Meshes

    Args:
        obj: Blender object to retopologize
        vertex_count: Target number of vertices
        use_crease: Whether to enable crease detection

    Returns:
        The new retopologized object, or None if failed
    """

    # Make sure it's a mesh
    if obj.type != 'MESH':
        print(f"Skipping {obj.name} - not a mesh")
        return None

    # Select the object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Configure settings
    props = bpy.context.scene.instant_meshes_props
    props.size_mode = 'VERTICES'
    props.vertex_count = vertex_count
    props.use_crease_angle = use_crease
    if use_crease:
        props.crease_angle = 30.0

    # Run retopology
    print(f"Retopologizing {obj.name}...")
    result = bpy.ops.mesh.instant_meshes_retopo()

    if result == {'FINISHED'}:
        # Get the new object (should be selected)
        new_obj = bpy.context.active_object
        print(f"  ✓ Created {new_obj.name}")
        return new_obj
    else:
        print(f"  ✗ Failed to retopologize {obj.name}")
        return None


def batch_retopologize_all(vertex_count=2000, use_crease=False):
    """
    Retopologize all mesh objects in the scene

    Args:
        vertex_count: Target number of vertices for all meshes
        use_crease: Whether to enable crease detection
    """

    # Store original objects
    original_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

    print(f"Found {len(original_objects)} mesh objects to process")
    print("=" * 60)

    # Process each object
    results = []
    for obj in original_objects:
        new_obj = retopologize_object(obj, vertex_count, use_crease)
        if new_obj:
            results.append((obj, new_obj))

    # Summary
    print("=" * 60)
    print(f"Processed {len(results)} out of {len(original_objects)} objects")

    return results


def retopologize_with_custom_settings():
    """
    Example of retopologizing with custom settings for different objects
    """

    # Get all mesh objects
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

    for obj in meshes:
        # Select the object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        # Configure settings based on object name or properties
        props = bpy.context.scene.instant_meshes_props

        # Example: Different settings for different object types
        if "character" in obj.name.lower():
            # High detail for characters
            props.size_mode = 'VERTICES'
            props.vertex_count = 8000
            props.smooth_iter = 3
            props.use_crease_angle = False

        elif "prop" in obj.name.lower():
            # Medium detail for props
            props.size_mode = 'VERTICES'
            props.vertex_count = 2000
            props.smooth_iter = 2
            props.use_crease_angle = True
            props.crease_angle = 30.0

        elif "background" in obj.name.lower():
            # Low detail for background
            props.size_mode = 'VERTICES'
            props.vertex_count = 500
            props.smooth_iter = 1
            props.use_crease_angle = False

        else:
            # Default settings
            props.size_mode = 'VERTICES'
            props.vertex_count = 2000
            props.smooth_iter = 2
            props.use_crease_angle = False

        # Run retopology
        print(f"Processing {obj.name}...")
        result = bpy.ops.mesh.instant_meshes_retopo()

        if result == {'FINISHED'}:
            print(f"  ✓ Success")
        else:
            print(f"  ✗ Failed")


def retopologize_by_size():
    """
    Example of using different size modes
    """

    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']

    for obj in meshes:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        props = bpy.context.scene.instant_meshes_props

        # Calculate 1/16th of original vertex count
        original_verts = len(obj.data.vertices)
        target_verts = max(100, original_verts // 16)

        props.size_mode = 'VERTICES'
        props.vertex_count = target_verts

        print(f"Processing {obj.name}: {original_verts} → {target_verts} vertices")
        bpy.ops.mesh.instant_meshes_retopo()


def retopologize_selected():
    """
    Retopologize only selected objects with preset configurations
    """

    selected = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']

    if not selected:
        print("No mesh objects selected!")
        return

    print(f"Processing {len(selected)} selected objects...")

    # Ask for preset (in a real addon, this would be a UI element)
    # For this example, we'll use different presets

    presets = {
        'game_low': {
            'vertex_count': 1000,
            'smooth_iter': 1,
            'use_crease_angle': True,
        },
        'game_medium': {
            'vertex_count': 5000,
            'smooth_iter': 2,
            'use_crease_angle': True,
        },
        'subdivision': {
            'vertex_count': 8000,
            'smooth_iter': 5,
            'use_crease_angle': False,
        },
    }

    # Use 'game_medium' preset for this example
    preset = presets['game_medium']

    props = bpy.context.scene.instant_meshes_props
    props.size_mode = 'VERTICES'
    props.vertex_count = preset['vertex_count']
    props.smooth_iter = preset['smooth_iter']
    props.use_crease_angle = preset['use_crease_angle']
    if preset['use_crease_angle']:
        props.crease_angle = 30.0

    for obj in selected:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        print(f"Processing {obj.name}...")
        bpy.ops.mesh.instant_meshes_retopo()


# =============================================================================
# Main execution
# =============================================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("INSTANT MESHES BATCH RETOPOLOGY")
    print("=" * 60 + "\n")

    # Check if addon is available
    if not hasattr(bpy.context.scene, 'instant_meshes_props'):
        print("ERROR: Instant Meshes addon not found!")
        print("Please install and enable the addon first.")
    else:
        # Choose one of the following examples:

        # Example 1: Simple batch processing
        print("Running Example 1: Batch retopologize all meshes")
        batch_retopologize_all(vertex_count=2000, use_crease=False)

        # Example 2: Custom settings per object
        # print("Running Example 2: Custom settings per object")
        # retopologize_with_custom_settings()

        # Example 3: Adaptive sizing based on original mesh
        # print("Running Example 3: Adaptive sizing")
        # retopologize_by_size()

        # Example 4: Process only selected objects
        # print("Running Example 4: Process selected objects")
        # retopologize_selected()

        print("\n" + "=" * 60)
        print("BATCH PROCESSING COMPLETE")
        print("=" * 60)


# =============================================================================
# Additional utility functions
# =============================================================================

def save_preset(name, settings):
    """
    Save a custom preset (would need to be saved to file in production)

    Args:
        name: Preset name
        settings: Dictionary of settings
    """
    # In a real implementation, this would save to a JSON file
    pass


def load_preset(name):
    """
    Load a custom preset

    Args:
        name: Preset name

    Returns:
        Dictionary of settings
    """
    # In a real implementation, this would load from a JSON file
    pass


def apply_settings_dict(settings_dict):
    """
    Apply a dictionary of settings to the addon properties

    Args:
        settings_dict: Dictionary with property names and values
    """
    props = bpy.context.scene.instant_meshes_props

    for key, value in settings_dict.items():
        if hasattr(props, key):
            setattr(props, key, value)
        else:
            print(f"Warning: Unknown property '{key}'")
