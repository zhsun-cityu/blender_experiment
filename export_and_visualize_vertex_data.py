import bpy
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def export_vertex_data(blend_file_path, export_folder):
    # Load the .blend file
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

def read_vertex_data(vertex_data_folder):
    vertex_data = {}

    for filename in os.listdir(vertex_data_folder):
        if filename.endswith(".verts"):
            filepath = os.path.join(vertex_data_folder, filename)
            with open(filepath, 'r') as file:
                vertices = []
                for line in file:
                    if line.startswith("Vertex:"):
                        parts = line.split(":")[1].strip().split(",")
                        if len(parts) == 3:
                            x, y, z = map(float, parts)
                            vertices.append((x, y, z))
                        else:
                            print(f"Skipping malformed vertex line: {line.strip()}")

                if vertices:
                    obj_name = filename.replace(".verts", "")
                    vertex_data[obj_name] = vertices
                else:
                    print(f"No valid vertices found in file: {filepath}")

    return vertex_data

def visualize_vertex_data(vertex_data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    color_index = 0

    for obj_name, vertices in vertex_data.items():
        if vertices:
            xs, ys, zs = zip(*vertices)
            ax.scatter(xs, ys, zs, c=colors[color_index % len(colors)], label=obj_name, s=1)
            color_index += 1
        else:
            print(f"No vertices to plot for object: {obj_name}")

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.legend()
    plt.show()


def main():
    blend_file_path = "../blender_dataset/blender-3.3-splash.blend"
    export_folder = "../blender_dataset_vertex/blender-3.3-splash/"

    # Export vertex data
    export_vertex_data(blend_file_path, export_folder)

    # Read and visualize vertex data
    vertex_data = read_vertex_data(export_folder)
    visualize_vertex_data(vertex_data)

if __name__ == "__main__":
    main()
