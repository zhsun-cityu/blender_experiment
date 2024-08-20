import os
import subprocess

def compress_images(input_folder, output_folder, quality=50):
    """Compress all images in the input_folder using ImageMagick with JPEG compression."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".jpg")

                output_file_dir = os.path.dirname(output_file_path)
                if not os.path.exists(output_file_dir):
                    os.makedirs(output_file_dir)

                command = f"magick '{input_file_path}' -strip -quality {quality} -interlace JPEG '{output_file_path}'"
                print(f"Compressing {input_file_path} to {output_file_path}")
                subprocess.run(command, shell=True, check=True)

# Example usage
input_folder = "../blender_dataset-texture/ocean-scene"
output_folder = "../blender_dataset-texture/ocean-scene-compressed"
quality = 50  # JPEG quality

compress_images(input_folder, output_folder, quality)
