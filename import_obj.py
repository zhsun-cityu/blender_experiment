import bpy
import os

def clear_objects():
    """Clear all mesh objects from the current scene."""
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

def import_obj(obj_file_path):
    """Import an .obj file."""
    bpy.ops.import_scene.obj(filepath=obj_file_path)

def render_and_save_image(output_path):
    """Render the scene and save the image."""
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered image saved at: {output_path}")

def process_obj_files(input_folder, output_folder):
    """Process all .obj files in the input folder and save rendered images to the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.obj'):
            obj_file_path = os.path.join(input_folder, filename)
            image_output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")

            clear_objects()
            import_obj(obj_file_path)
            render_and_save_image(image_output_path)

def process_folders(root_folder, output_root_folder):
    """Traverse folders and process .obj files in each."""
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            output_folder = os.path.join(output_root_folder, folder_name)
            process_obj_files(folder_path, output_folder)

# Load the initial .blend file
blend_file_path = "../blender_dataset/ocean-scene.blend"
bpy.ops.wm.open_mainfile(filepath=blend_file_path)

# Example usage
root_folder = "../blender_dataset-ply2/ocean-scene-vmesh/decode/"
output_root_folder = "../blender_dataset-ply2/ocean-scene-vmesh"

process_folders(root_folder, output_root_folder)
