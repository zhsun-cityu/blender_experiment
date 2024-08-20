import os,glob
import csv
import pandas as pd
import matplotlib.pyplot as plt


# Example usage
original_folder = "../blender_dataset-ply2/ocean-scene"
compressed_base = "../blender_dataset-ply2/ocean-scene-vmesh/encode"
# compressed_folders = [
#     "/path/to/compressed/folder1",
#     "/path/to/compressed/folder2",
#     "/path/to/compressed/folder3"
# ]

# compressed_folders = glob.glob(os.path.join(compressed_folder, '*'))

compressed_folders = os.listdir(compressed_base)
compressed_folders.sort()
output_csv = "compression_ratios.csv"


def get_file_size(file_path):
    """Get the size of the file in bytes."""
    return os.path.getsize(file_path)

def calculate_compression_ratio(original_size, compressed_size):
    """Calculate the compression ratio."""
    if original_size == 0:
        return 0
    return compressed_size / original_size

def measure_compression_ratios(original_folder, compressed_folders, output_csv):
    """Measure the compression ratios for files."""
    data = []

    # Get a list of original files
    original_files = [f for f in os.listdir(original_folder) if os.path.isfile(os.path.join(original_folder, f))]
    print(original_files)
    for original_file in original_files:
        original_file_path = os.path.join(original_folder, original_file)
        original_size = get_file_size(original_file_path)

        row = {"filename": original_file, "original_size": original_size}

        original_file_base = os.path.splitext(original_file)[0]

        for compressed_folder in compressed_folders:
            compressed_file = original_file_base + ".*"
            print(os.path.join(compressed_base, compressed_folder, compressed_file))
            if len(glob.glob(os.path.join(compressed_base, compressed_folder, compressed_file))) != 0:
                compressed_file_path = glob.glob(os.path.join(compressed_base, compressed_folder, compressed_file))[0]
            else:
                continue
            if os.path.isfile(compressed_file_path):
                compressed_size = get_file_size(compressed_file_path)
                ratio = calculate_compression_ratio(original_size, compressed_size)
                row[os.path.basename(compressed_folder)] = f"{ratio*100:.4f}%"
            else:
                row[os.path.basename(compressed_folder)] = None

        data.append(row)

    # Write the results to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ["filename", "original_size"] + compressed_folders
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return data

def plot_compression_ratios(data, output_csv):
    """Plot the compression ratios."""
    df = pd.read_csv(output_csv)
    df.set_index('filename', inplace=True)

    # Plot the data
    ax = df.plot(kind='bar', figsize=(15, 7))
    ax.set_ylabel('Compression Ratio')
    plt.title('Compression Ratios for Files')
    plt.show()


data = measure_compression_ratios(original_folder, compressed_folders, output_csv)
plot_compression_ratios(data, output_csv)
