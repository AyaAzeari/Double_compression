from PIL import Image
import os

def convert_folder_to_jpeg2000(input_folder, output_folder, target_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Folder '{output_folder}' created.")

    files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.jpg')]
    if not files:
        print("No JPEG files found in the input folder.")
        return

    for file_path in files:
        img = Image.open(file_path)
        output_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + '.jp2')
        quality = 100  # Start with high quality (in Pillow, the 'quality' for JPEG 2000 ranges from 1 to 100)
        print(f"Processing {file_path}")

        # Adjusting quality to fit the target size
        step = 10  # Initial quality step
        while step > 0:
            img.save(output_file_path, 'JPEG2000', quality_mode='rates', quality_layers=[quality])
            file_size = os.path.getsize(output_file_path)
            if file_size <= target_size:
                print(f"Saved {output_file_path} with quality={quality}, size={file_size} bytes")
                break
            quality -= step  # Decrease quality in steps
            if quality < step:
                step = 1  # Smaller step for fine tuning

        if os.path.getsize(output_file_path) > target_size:
            print(f"Warning: Could not compress {output_file_path} to the target size even at lowest quality.")
        else:
            print(f"Successfully compressed to {target_size} bytes.")

# Example usage:
input_folder = "compressed_images_from_png_to_jpeg"
output_folder = "compressed_images_from_jpeg_to_jpeg2000"
target_size = 41943  # approximately 41 KB
convert_folder_to_jpeg2000(input_folder, output_folder, target_size)
