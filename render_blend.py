import bpy
from pathlib import Path

def render_image(blend_file_path, output_image_path):
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Set the output file format and path
    bpy.context.scene.render.image_settings.file_format = 'PNG'  # Options: 'PNG', 'JPEG', 'TIFF', etc.
    bpy.context.scene.render.filepath = output_image_path

    # Render the image
    bpy.ops.render.render(write_still=True)
    print(f"Rendered image saved at {output_image_path}")


def get_frame_range():
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    return start_frame, end_frame

def render_animation(blend_file_path, output_directory, file_format='PNG', fps=24):
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Get the frame range
    start_frame, end_frame = get_frame_range()
    print(f"Rendering animation from frame {start_frame} to {end_frame}")

    # Set the output file format and directory
    bpy.context.scene.render.image_settings.file_format = file_format  # Options: 'PNG', 'JPEG', 'TIFF', etc.
    bpy.context.scene.render.filepath = output_directory

    # Set frames per second
    bpy.context.scene.render.fps = fps

    # Render the animation
    bpy.ops.render.render(animation=True, write_still=True)
    print(f"Animation rendered and saved in {output_directory}")

def render_animation_start_end(blend_file_path, output_directory, start_frame, end_frame, file_format='PNG', fps=24):
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Get the valid frame range
    valid_start_frame, valid_end_frame = get_frame_range()

    # Ensure the specified frames are within the valid range
    if start_frame < valid_start_frame:
        print(f"Start frame {start_frame} is out of bounds. Using {valid_start_frame} instead.")
        start_frame = valid_start_frame
    if end_frame > valid_end_frame:
        print(f"End frame {end_frame} is out of bounds. Using {valid_end_frame} instead.")
        end_frame = valid_end_frame
    if start_frame > end_frame:
        print(f"Start frame {start_frame} cannot be greater than end frame {end_frame}. Adjusting the frame range.")
        start_frame, end_frame = valid_start_frame, valid_end_frame

    print(f"Rendering animation from frame {start_frame} to {end_frame}")

    # Set the custom frame range
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Set the output file format and directory
    bpy.context.scene.render.image_settings.file_format = file_format  # Options: 'PNG', 'JPEG', 'TIFF', etc.
    bpy.context.scene.render.filepath = output_directory

    # Set frames per second
    bpy.context.scene.render.fps = fps

    # Render the animation
    bpy.ops.render.render(animation=True, write_still=True)
    print(f"Animation rendered and saved in {output_directory}")

def render_viewport(blend_file_path, output_image_path, frame=1):
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Set the frame to render
    bpy.context.scene.frame_set(frame)

    # Set the output file path
    bpy.context.scene.render.filepath = output_image_path

    # Render the viewport
    bpy.ops.render.opengl(write_still=True)
    print(f"Viewport rendered image saved at {output_image_path}")

def render_opengl(blend_file_path, output_image_path, frame=1):
    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Set the frame to render
    bpy.context.scene.frame_set(frame)

    # Set the output file path
    bpy.context.scene.render.filepath = output_image_path

    # Render the scene using OpenGL
    bpy.ops.render.opengl(animation=False, write_still=True)
    print(f"OpenGL rendered image saved at {output_image_path}")


def main():
    blend_list = [
    # "../blender_dataset/Blender_partytug.blend",
    # "../blender_dataset/barbershop_interior.blend",
    # "../blender_dataset/blender-3.3-splash.blend",
    # "../blender_dataset/castle-landscape.blend",
    # "../blender_dataset/lone-monk_cycles_and_exposure-node_demo.blend",
    # "../blender_dataset/ocean-scene.blend",
    "../blender_dataset/classroom/classroom.blend",
    # "../blender_dataset/restaurant_anim_test/rain_restaurant.blend",
    # "../blender_dataset/splash279/splash279.blend",
    # "../blender_dataset/blender-278-splash/Blenderman.blend"
    ]

    # blend_list = ["../blender_dataset/restaurant_anim_test/rain_restaurant.blend"]

    for blend_file_path in blend_list:
        output_image_path = Path(blend_file_path).stem + '.png'
        render_image(blend_file_path, output_image_path)


    # blend_file_path = "../blender_dataset/restaurant_anim_test/rain_restaurant.blend"
    # output_image_path = "rain_restaurant.png"
    #
    # render_image(blend_file_path, output_image_path)
    # render_viewport(blend_file_path, output_image_path)
    # render_animation(blend_file_path, "rain_restaurant_animation")
if __name__ == "__main__":
    main()
