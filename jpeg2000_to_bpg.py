import subprocess
import os

def convert_png_to_bpg(input_folder, output_folder_bpg, target_size):
    """
    Convert PNG files to BPG format using the bpgenc tool, attempting to meet a specified file size.

    Args:
    input_folder (str): Directory containing PNG files.
    output_folder_bpg (str): Directory where BPG files will be saved.
    target_size (int): Desired maximum file size for BPG images in bytes.

    Returns:
    None
    """
    if not os.path.exists(output_folder_bpg):
        os.makedirs(output_folder_bpg)
    print(f"BPG folder '{output_folder_bpg}' created.")

    png_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]
    for png in png_files:
        source_path = os.path.join(input_folder, png)
        bpg_filename = os.path.splitext(png)[0] + '.bpg'
        destination_path = os.path.join(output_folder_bpg, bpg_filename)

        # Initial quality for BPG is set to 51 (the highest quality in bpgenc), and decrement by steps
        quality = 20
        smallest_quality_met_size = None
        final_quality = None

        while quality >= 0:
            command = ['bpgenc', '-o', destination_path, '-q', str(quality), source_path]
            subprocess.run(command, check=True)
            file_size = os.path.getsize(destination_path)
            if file_size <= target_size:
                smallest_quality_met_size = file_size
                final_quality = quality
                print(f"Converted {source_path} to BPG: {destination_path} with quality={quality}, size={file_size} bytes")
                break
            quality += 2  # Decrease quality to try and meet file size requirement

            if quality == 0 and smallest_quality_met_size is None:  # Ensures we've attempted at least one conversion at lowest quality
                print(f"Warning: Could not compress {destination_path} to target size {target_size} bytes at any quality.")
                break

def main():
    input_folder = 'compressed_images_from_jpeg2000_to_png_intermediate'  # Path to your intermediate PNG files
    output_folder_bpg = 'compressed_images_from_jpeg2000_to_bpg'  # Path where you want to save the BPG files
    target_size = 41943  # Target size in bytes, adjust as needed

    # Convert PNG to BPG
    convert_png_to_bpg(input_folder, output_folder_bpg, target_size)

if __name__ == "__main__":
    main()
