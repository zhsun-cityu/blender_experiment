import bpy
import os


def write_ply(filepath, obj):
    """Write the given object as a PLY file to the specified filepath."""
    vertices = obj.data.vertices
    faces = obj.data.polygons

    # Open the file for writing
    with open(filepath, 'w') as file:
        # Write the PLY header
        file.write("ply\n")
        file.write("format ascii 1.0\n")
        file.write(f"element vertex {len(vertices)}\n")
        file.write("property float x\n")
        file.write("property float y\n")
        file.write("property float z\n")
        file.write(f"element face {len(faces)}\n")
        file.write("property list uchar int vertex_indices\n")
        file.write("end_header\n")

        # Write the vertex data
        for vertex in vertices:
            file.write(f"{vertex.co.x} {vertex.co.y} {vertex.co.z}\n")

        # Write the face data
        for face in faces:
            file.write(f"{len(face.vertices)}")
            for vert_index in face.vertices:
                file.write(f" {vert_index}")
            file.write("\n")

def export_all_objects_as_ply(blend_file_path, export_folder):
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Ensure the export folder exists
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # Loop through all mesh objects and export them separately
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            # Define the export path
            export_path = os.path.join(export_folder, f"{obj.name}.ply")

            # Write the PLY file
            write_ply(export_path, obj)
            print(f"PLY file exported to: {export_path}")

# Example usage
blend_file_path = "../blender_dataset/blender-3.3-splash.blend"
export_folder = "../blender_dataset-ply/blender-3.3-splash"

export_all_objects_as_ply(blend_file_path, export_folder)
