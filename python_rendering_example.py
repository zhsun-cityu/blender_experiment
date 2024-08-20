import bpy
import subprocess
import os

# Function to create a cube
def create_cube():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("CubeMesh")
    obj = bpy.data.objects.new("Cube", mesh)

    # Link the object to the current scene
    scene = bpy.context.scene
    scene.collection.objects.link(obj)

    # Set the object as active and select it
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Define the vertices and faces of the cube
    vertices = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1),
                (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1)]
    faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 3, 7, 4),
             (1, 2, 6, 5), (0, 1, 5, 4), (2, 3, 7, 6)]

    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

def create_simplified_cube():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("SimplifiedCubeMesh")
    obj = bpy.data.objects.new("SimplifiedCube", mesh)

    # Link the object to the current scene
    scene = bpy.context.scene
    scene.collection.objects.link(obj)

    # Set the object as active and select it
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Define the vertices of the cube
    vertices = [(1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1),
                (1, 1, -1), (-1, -1, -1), (1, -1, -1)]

    # Define the faces using triangles (two triangles per quad face)
    faces = [(0, 1, 2), (0, 2, 3),  # Front face
             (4, 7, 6), (4, 6, 5),  # Back face
             (0, 3, 7), (0, 7, 4),  # Right face
             (1, 5, 6), (1, 6, 2),  # Left face
             (0, 4, 5), (0, 5, 1),  # Top face
             (2, 6, 7), (2, 7, 3)]  # Bottom face

    # Create the mesh from the vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()


# Function to animate the cube
def animate_cube():
    obj = bpy.context.scene.objects.get("Cube")
    if obj:
        # Set the keyframe data for the object's location
        obj.location = (0, 0, 0)
        obj.keyframe_insert(data_path="location", frame=1)

        obj.location = (5, 5, 5)
        obj.keyframe_insert(data_path="location", frame=50)

# Function to render a single image
def render_single_image(output_image_path, frame=1):
    # Set the frame to render
    bpy.context.scene.frame_set(frame)

    # Set the output file format and path
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.filepath = output_image_path

    # Render the image
    bpy.ops.render.render(write_still=True)
    print(f"Rendered image saved at {output_image_path}")

def render_animation(output_directory, start_frame=1, end_frame=50, file_format='PNG', fps=24):

    # Set the output file format and directory
    bpy.context.scene.render.image_settings.file_format = file_format  # Options: 'PNG', 'JPEG', 'TIFF', etc.
    bpy.context.scene.render.filepath = output_directory

    # Set the frame range
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Set frames per second
    bpy.context.scene.render.fps = fps

    # Render the animation
    bpy.ops.render.render(animation=True, write_still=True)
    print(f"Animation rendered and saved in {output_directory}")

# Custom operator example
class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, "Simple Operator Executed")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname)

def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


def main():
    # Create a cube
    create_cube()

    # Animate the cube
    animate_cube()

    # create_simplified_cube()
    # Render a single image
    output_image_path = "output_image.png"
    render_single_image(output_image_path, frame=1)

    output_dir = "cube_output/"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    fps = 24
    render_animation(output_dir, start_frame=1, end_frame=50,file_format="PNG", fps=fps)


    # ## create video
    # # Additional lines to combine the output images into a video
    output_video_path = os.path.join(output_dir, "animation.mp4")
    image_sequence_pattern = os.path.join(output_dir, "%4d.png")  # Adjust the pattern to match your rendered filenames

    ffmpeg_command = [
        "ffmpeg",
        "-framerate", str(fps),
        "-i", image_sequence_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video_path
    ]
    subprocess.run(ffmpeg_command)
    print(f"Video rendered and saved at {output_video_path}")


    # Register the custom operator
    register()

if __name__ == "__main__":
    main()
