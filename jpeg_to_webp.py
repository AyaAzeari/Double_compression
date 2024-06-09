import subprocess
import os

def convert_folder_to_webp(input_folder, output_folder, target_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Folder '{output_folder}' created.")

    files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.jpg')]  # Ensure correct file extension
    if not files:
        print("No JPEG files found in the input folder.")
        return

    for file_path in files:
        output_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + '.webp')
        quality = 100  # Start with high quality
        print(f"Processing {file_path}")

        while quality >= 0:
            command = f'cwebp -q {quality} "{file_path}" -o "{output_file_path}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Command failed with error: {result.stderr}")
                break

            if os.path.exists(output_file_path) and os.path.getsize(output_file_path) <= target_size:
                print(f"Saved {output_file_path} with quality={quality}, size={os.path.getsize(output_file_path)} bytes")
                break

            quality -= 5  # Decrement quality

        if not os.path.exists(output_file_path) or os.path.getsize(output_file_path) > target_size:
            print(f"Warning: Could not achieve target size at any quality for {output_file_path}.")

# Example usage:
input_folder = "compressed_images_from_png_to_jpeg"
output_folder = "compressed_images_from_jpeg_to_webp"
target_size = 41943  # approximately 205 KB
convert_folder_to_webp(input_folder, output_folder, target_size)
