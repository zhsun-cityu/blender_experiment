import bpy
import os
from pathlib import Path

def export_textures(blend_file_path, export_folder):
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    for image in bpy.data.images:
        if image.packed_file:
            image.unpack(method='WRITE_LOCAL')
        if not image.has_data:
            print(f"Error: Image '{image.name}' does not have any image data")
            continue
        if image.filepath.endswith(".png"):
            image.file_format = 'PNG'
        elif image.filepath.endswith(".jpg") or image.filepath.endswith(".jpeg"):
            image.file_format = 'JPEG'
        else:
            image.file_format = 'PNG'
        export_path = os.path.join(export_folder, os.path.basename(image.filepath_raw))
        image.filepath_raw = export_path
        image.save()
    print("Textures exported successfully.")

def export_materials(blend_file_path, export_folder):
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    for material in bpy.data.materials:
        material_name = material.name
        material_path = os.path.join(export_folder, f"{material_name}.mtl")
        with open(material_path, 'w') as f:
            f.write(f"newmtl {material_name}\n")
            if material.use_nodes:
                for node in material.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        base_color = node.inputs['Base Color'].default_value
                        roughness = node.inputs['Roughness'].default_value
                        metallic = node.inputs['Metallic'].default_value
                        f.write(f"Kd {base_color[0]} {base_color[1]} {base_color[2]}\n")
                        f.write(f"Ns {roughness}\n")
                        f.write(f"Ni {metallic}\n")
    print("Materials exported successfully.")


def ensure_ply_export_addon():
    """Ensure that the PLY export add-on is enabled."""
    if not bpy.ops.wm.addon_enable(module='io_mesh_ply'):
        bpy.ops.wm.addon_enable(module='io_mesh_ply')

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

def export_animations(blend_file_path, export_folder):
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    for obj in bpy.data.objects:
        if obj.animation_data:
            anim_name = obj.name
            anim_path = os.path.join(export_folder, f"{anim_name}.anim")
            with open(anim_path, 'w') as f:
                for fc in obj.animation_data.action.fcurves:
                    data_path = fc.data_path
                    index = fc.array_index
                    f.write(f"{data_path}[{index}]:\n")
                    for keyframe in fc.keyframe_points:
                        f.write(f"  frame: {keyframe.co[0]}, value: {keyframe.co[1]}\n")
    print("Animations exported successfully.")

def export_cameras(blend_file_path, export_folder):
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    for cam in [obj for obj in bpy.data.objects if obj.type == 'CAMERA']:
        cam_name = cam.name
        cam_path = os.path.join(export_folder, f"{cam_name}.camera")
        with open(cam_path, 'w') as f:
            f.write(f"Camera: {cam_name}\n")
            f.write(f"Location: {cam.location.x}, {cam.location.y}, {cam.location.z}\n")
            f.write(f"Rotation: {cam.rotation_euler.x}, {cam.rotation_euler.y}, {cam.rotation_euler.z}\n")
            f.write(f"Lens: {cam.data.lens}\n")
            f.write(f"Sensor Width: {cam.data.sensor_width}\n")
            f.write(f"Sensor Height: {cam.data.sensor_height}\n")
    print("Cameras exported successfully.")

def export_lights(blend_file_path, export_folder):
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    for light in [obj for obj in bpy.data.objects if obj.type == 'LIGHT']:
        light_name = light.name
        light_path = os.path.join(export_folder, f"{light_name}.light")
        with open(light_path, 'w') as f:
            f.write(f"Light: {light_name}\n")
            f.write(f"Location: {light.location.x}, {light.location.y}, {light.location.z}\n")
            f.write(f"Rotation: {light.rotation_euler.x}, {light.rotation_euler.y}, {light.rotation_euler.z}\n")
            f.write(f"Type: {light.data.type}\n")
            f.write(f"Energy: {light.data.energy}\n")
            f.write(f"Color: {light.data.color[0]}, {light.data.color[1]}, {light.data.color[2]}\n")
    print("Lights exported successfully.")

def export_transformations(blend_file_path, export_folder):
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    for obj in bpy.data.objects:
        obj_name = obj.name
        obj_path = os.path.join(export_folder, f"{obj_name}.transform")
        with open(obj_path, 'w') as f:
            f.write(f"Object: {obj_name}\n")
            f.write(f"Location: {obj.location.x}, {obj.location.y}, {obj.location.z}\n")
            f.write(f"Rotation: {obj.rotation_euler.x}, {obj.rotation_euler.y}, {obj.rotation_euler.z}\n")
            f.write(f"Scale: {obj.scale.x}, {obj.scale.y}, {obj.scale.z}\n")
    print("Transformations exported successfully.")

def export_vertex_data(blend_file_path, export_folder):
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            mesh = obj.data
            mesh_name = obj.name
            mesh_path = os.path.join(export_folder, f"{mesh_name}.verts")
            with open(mesh_path, 'w') as f:
                f.write(f"Mesh: {mesh_name}\n")
                for vert in mesh.vertices:
                    f.write(f"Vertex: {vert.co.x}, {vert.co.y}, {vert.co.z}\n")
                for loop in mesh.loops:
                    f.write(f"Normal: {loop.normal.x}, {loop.normal.y}, {loop.normal.z}\n")
                for uv_layer in mesh.uv_layers:
                    for uv in uv_layer.data:
                        f.write(f"UV: {uv.uv.x}, {uv.uv.y}\n")
    print("Vertex data exported successfully.")

def list_object_types(blend_file_path):
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)
    object_types = set()
    for obj in bpy.data.objects:
        object_types.add(obj.type)
    print("Object types in the Blender file:")
    for obj_type in object_types:
        print(obj_type)

def main():
    base_export_folder = "../blender_dataset-ply"

    blend_list = [
    # "../blender_dataset/Blender_partytug.blend",
    # "../blender_dataset/barbershop_interior.blend",
    # "../blender_dataset/blender-3.3-splash.blend",
    # "../blender_dataset/castle-landscape.blend",
    "../blender_dataset/lone-monk_cycles_and_exposure-node_demo.blend",
    "../blender_dataset/ocean-scene.blend",
    "../blender_dataset/classroom/classroom.blend",
    "../blender_dataset/restaurant_anim_test/rain_restaurant.blend",
    "../blender_dataset/splash279/splash279.blend",
    "../blender_dataset/blender-278-splash/Blenderman.blend"
    ]

    # blend_file_path = "/path/to/your/uploads_files_3481608_dog_fur4.blend"

    for blend_file_path in blend_list:
        filename = Path(blend_file_path).stem
        export_folder = os.path.join(base_export_folder, filename)

        # Create export folders
        # texture_folder = base_export_folder, "textures")
        # material_folder = os.path.join(base_export_folder, "materials")
        # animation_folder = os.path.join(base_export_folder, "animations")
        # camera_folder = os.path.join(base_export_folder, "cameras")
        # light_folder = os.path.join(base_export_folder, "lights")
        # transformation_folder = os.path.join(base_export_folder, "transformations")
        # vertex_folder = os.path.join(base_export_folder, "vertex_data")

        # Export data
        # export_textures(blend_file_path, export_folder)
        # export_materials(blend_file_path, material_folder)
        # export_animations(blend_file_path, animation_folder)
        # export_cameras(blend_file_path, camera_folder)
        # export_lights(blend_file_path, light_folder)
        # export_transformations(blend_file_path, transformation_folder)
        # export_vertex_data(blend_file_path, vertex_folder)
        # list_object_types(blend_file_path)

        export_all_objects_as_ply(blend_file_path, export_folder)

if __name__ == "__main__":
    main()
