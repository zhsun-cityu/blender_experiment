import bpy
import os
import pandas as pd

def collect_statistics(blend_file_path):
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    statistics = {
        "file_path": blend_file_path,
        "num_vertices": 0,
        "num_textures": 0,
        "total_texture_size": 0,
        "num_objects": len(bpy.data.objects),
        "num_meshes": len(bpy.data.meshes),
        "num_cameras": len([obj for obj in bpy.data.objects if obj.type == 'CAMERA']),
        "num_lights": len([obj for obj in bpy.data.objects if obj.type == 'LIGHT']),
        "num_materials": len(bpy.data.materials),
    }

    for mesh in bpy.data.meshes:
        statistics["num_vertices"] += len(mesh.vertices)

    for image in bpy.data.images:
        statistics["num_textures"] += 1
        if image.filepath:
            try:
                statistics["total_texture_size"] += os.path.getsize(bpy.path.abspath(image.filepath))
            except Exception as e:
                print(f"Could not get size for texture {image.filepath}: {e}")

    return statistics

def collect_statistics_from_files(blend_file_paths):
    all_statistics = []
    for blend_file_path in blend_file_paths:
        stats = collect_statistics(blend_file_path)
        all_statistics.append(stats)
    return all_statistics

# def print_statistics(statistics):
#     for stats in statistics:
#         print(f"File: {stats['file_path']}")
#         print(f"  Number of vertices: {stats['num_vertices']}")
#         print(f"  Number of textures: {stats['num_textures']}")
#         print(f"  Total texture size: {stats['total_texture_size']} bytes")
#         print(f"  Number of objects: {stats['num_objects']}")
#         print(f"  Number of meshes: {stats['num_meshes']}")
#         print(f"  Number of cameras: {stats['num_cameras']}")
#         print(f"  Number of lights: {stats['num_lights']}")
#         print(f"  Number of materials: {stats['num_materials']}")
#         print("\n")

def print_statistics(statistics):
    # Create a DataFrame to store the statistics
    df = pd.DataFrame(statistics)

    # Print the DataFrame as a table
    print(df.to_string(index=False))


def main():
    blend_file_paths = [
        "../blender_dataset/ocean-scene.blend",
        "../blender_dataset/blender-3.3-splash.blend",
        "../blender_dataset/Blender_partytug.blend",
        "../blender_dataset/castle-landscape.blend",
        "../blender_dataset/lone-monk_cycles_and_exposure-node_demo.blend",
        "../blender_dataset/barbershop_interior.blend",
        "../blender_dataset/blender-278-splash/Blenderman.blend",
        "../blender_dataset/splash279/splash279.blend",
        "../blender_dataset/restaurant_anim_test/rain_restaurant.blend",
        "../blender_dataset/classroom/classroom.blend",
        # Add more file paths as needed
    ]

    statistics = collect_statistics_from_files(blend_file_paths)
    print_statistics(statistics)

if __name__ == "__main__":
    main()
