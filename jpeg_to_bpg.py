import subprocess
import os

def convert_folder_to_bpg(input_folder, output_folder, target_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"Folder '{output_folder}' created.")

    jpeg_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.jpg')]
    for jpeg in jpeg_files:
        jpeg_path = os.path.join(input_folder, jpeg)
        bpg_path = os.path.join(output_folder, os.path.splitext(jpeg)[0] + '.bpg')
        quality = 25  # Start with the lowest reasonable quality
        previous_size = float('inf')  # Initialize with an infinitely large size
        quality_change = 2  # Initial change in quality for each step

        while quality <= 51:  # Maximum BPG quality level
            command = ['bpgenc', '-o', bpg_path, '-q', str(quality), jpeg_path]
            subprocess.run(command, check=True)
            current_size = os.path.getsize(bpg_path)

            print(f"Quality {quality}, File Size {current_size} bytes")
            if current_size <= target_size:
                print(f"Saved {bpg_path} with quality={quality}, size={current_size} bytes")
                break  # Stop if the file size is at or below the target

            if current_size > target_size and current_size < previous_size:
                # If the file is still too big but smaller than before, adjust quality
                previous_size = current_size  # Update last known size
                quality += quality_change  # Try a higher quality to reduce size
            else:
                # If size increases, make smaller adjustments in the opposite direction
                quality_change = max(1, quality_change - 1)  # Decrement change to fine-tune
                quality -= quality_change  # Decrease quality to decrease file size

        if current_size > target_size:
            print(f"Could not compress {bpg_path} to the target size of {target_size} bytes even at highest attempted quality.")

# Example usage:
input_folder = "compressed_images_from_png_to_jpeg"
output_folder = "compressed_images_from_jpeg_to_bpg"
target_size = 41943  # approximately 41 KB, adjust as needed
convert_folder_to_bpg(input_folder, output_folder, target_size)
