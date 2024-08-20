import bpy
import os

def export_all_objects_as_ply(blend_file_path, export_folder):
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Ensure the export folder exists
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # Loop through all mesh objects and export them separately
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            # Define the export path
            export_path = os.path.join(export_folder, f"{obj.name}.ply")

            # Export the selected object
            bpy.ops.export_mesh.ply(filepath=export_path, use_selection=True)
            print(f"PLY file exported to: {export_path}")

# Example usage
blend_file_path = "../blender_dataset/blender-3.3-splash.blend"
export_folder = "../blender_dataset-ply/blender-3.3-splash"

export_all_objects_as_ply(blend_file_path, export_folder)
