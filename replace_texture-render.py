import bpy
import os
import numpy as np

def get_image_data(image):
    """Get the image data as a numpy array."""
    image_pixels = np.array(image.pixels[:])
    return image_pixels

def compare_image_data(image, new_texture_file_path):
    """Compare image data before and after reloading the image."""
    # Get the original image data
    original_data = get_image_data(image)

    # Reload the image with the new texture
    image.filepath = new_texture_file_path
    image.reload()

    # Get the new image data
    new_data = get_image_data(image)

    # Compare the data
    is_different = not np.array_equal(original_data, new_data)

    return is_different

def replace_textures_and_render(blend_file_path, textures_folder, output_image_path):
    """Replace textures in the Blender file with modified textures and render an image."""
    # Load the Blender file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Traverse all image textures in the Blender file
    for image in bpy.data.images:
        # # Construct the path to the modified texture file with .jpg extension
        texture_name = os.path.splitext(image.name.split('.')[0])[0]  # Remove any appended numbers and extensions
        texture_file_path = os.path.join(textures_folder, texture_name + '.jpg')

        if os.path.exists(texture_file_path):
            # # Load the modified texture
            image.filepath = texture_file_path
            image.reload()
            # image.node_tree.nodes["Image Texture"].image = bpy.data.images.load(texture_file_path)

            print(f"Replaced texture: {texture_name}.jpg")
            if compare_image_data(image, texture_file_path):
                print(f"Replaced texture: {texture_name}.jpg")
            else:
                print(f"Texture data did not change for: {texture_name}.jpg")
        else:
            print(f"Texture file not found: {texture_file_path}")

    # Set the output path for the rendered image
    bpy.context.scene.render.filepath = output_image_path

    # Render the image
    bpy.ops.render.render(write_still=True)
    print(f"Rendered image saved at: {output_image_path}")

# Example usage
blend_file_path = "../blender_dataset/ocean-scene.blend"
textures_folder = "../blender_dataset-texture/ocean-scene-compressed"
output_image_path = "ocean-scene-compressed-texture.png"

replace_textures_and_render(blend_file_path, textures_folder, output_image_path)
