import subprocess
import os

def convert_folder_to_heic(input_folder, output_folder, target_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Folder '{output_folder}' created.")

    files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.jpg')]
    if not files:
        print("No JPEG files found in the input folder.")
        return

    for file_path in files:
        output_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + '.heic')
        quality = 100  # Start with high quality and decrease if necessary
        min_quality = 10  # Minimum acceptable quality
        step = 10  # Quality adjustment step

        print(f"Processing {file_path}")
        while quality >= min_quality:
            command = f'magick convert "{file_path}" -quality {quality} "{output_file_path}"'
            subprocess.run(command, shell=True)
            current_size = os.path.getsize(output_file_path)

            if current_size <= target_size:
                print(f"Saved {output_file_path} with quality={quality}, size={current_size} bytes")
                break
            else:
                print(f"At quality {quality}, size is {current_size}, which is above target.")
                quality -= step

        if os.path.getsize(output_file_path) > target_size:
            print(f"Warning: Could not compress {output_file_path} to the target size. Closest size: {current_size} bytes at quality {quality}.")

# Example usage:
input_folder = "compressed_images_from_png_to_jpeg"
output_folder = "compressed_images_from_jpeg_to_heic"
target_size = 41943  # approximately 41 KB
convert_folder_to_heic(input_folder, output_folder, target_size)
