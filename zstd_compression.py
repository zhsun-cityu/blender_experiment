import os
import subprocess

def compress_files(input_folder, output_folder, compression_level=3):
    """Compress all files in the input_folder and save them to the output_folder using zstd."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(input_file_path, input_folder)
            output_file_path = os.path.join(output_folder, relative_path + ".zst")

            output_file_dir = os.path.dirname(output_file_path)
            if not os.path.exists(output_file_dir):
                os.makedirs(output_file_dir)

            command = f"zstd -{compression_level} {input_file_path} -o {output_file_path}"
            print(f"Compressing {input_file_path} to {output_file_path}")
            subprocess.run(command, shell=True, check=True)

# Example usage
input_folder = "../blender_dataset-ply2/ocean-scene"
output_folder = "../blender_dataset-ply2/ocean-scene-vmesh/encode/encode-zstd"

compress_files(input_folder, output_folder)
