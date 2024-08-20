from PIL import Image
import os

def arrange_images_grid(image_folder, output_image_path):
    # List all PNG images in the folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

    # Ensure there are exactly 10 images
    if len(image_files) != 10:
        print("Error: There must be exactly 10 PNG images in the folder.")
        return

    # Load the images
    images = [Image.open(os.path.join(image_folder, img)) for img in image_files]

    # Determine the size of the individual images (assuming all images have the same size)
    image_width, image_height = images[0].size

    # Create a blank image for the grid
    grid_width = 5 * image_width
    grid_height = 2 * image_height
    grid_image = Image.new('RGB', (grid_width, grid_height))

    # Paste the images into the grid
    for i, img in enumerate(images):
        x = (i % 5) * image_width
        y = (i // 5) * image_height
        grid_image.paste(img, (x, y))

    # Save the grid image
    grid_image.save(output_image_path)
    print(f"Grid image saved at {output_image_path}")

def main():
    image_folder = "blend_result"  # Update with the path to your image folder
    output_image_path = "render_examples.png"  # Update with the desired output path
    arrange_images_grid(image_folder, output_image_path)

if __name__ == "__main__":
    main()
