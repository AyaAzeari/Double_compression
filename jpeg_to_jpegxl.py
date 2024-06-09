import subprocess
import os

def convert_jpeg_to_jpegxl(input_folder, output_folder, target_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Folder '{output_folder}' created.")

    files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]
    for file_name in files:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_name = os.path.splitext(file_name)[0] + '.jxl'
        output_file_path = os.path.join(output_folder, output_file_name)

        # Start with high quality and decrease until the file size is below the target size
        quality = 100
        while quality >= 0:
            # Conditionally set lossless flag based on quality
            lossless_flag = '--lossless_jpeg=0' if quality < 100 else ''
            command = ['cjxl', input_file_path, output_file_path, '--quality', str(quality)] + ([lossless_flag] if lossless_flag else [])
            
            try:
                subprocess.run(command, check=True)
                if os.path.getsize(output_file_path) <= target_size:
                    print(f"Converted {input_file_path} to {output_file_path} with quality={quality}")
                    break
            except subprocess.CalledProcessError as e:
                print(f"Error processing {input_file_path} at quality {quality}: {e}")

            quality -= 10  # Decrease quality to reduce file size

            if quality < 0:  # Final fallback to ensure output if no size requirement met
                print(f"Warning: Could not compress {output_file_path} to the target size even at lowest quality.")

# Example usage
input_folder = 'compressed_images_from_png_to_jpeg'  # Adjust as necessary
output_folder = 'compressed_images_from_jpeg_to_jpegxl'
target_compressed_size = 41943  # Target size in bytes, adjust as needed
convert_jpeg_to_jpegxl(input_folder, output_folder, target_compressed_size)
