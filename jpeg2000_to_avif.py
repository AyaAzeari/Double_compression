import subprocess
import os

def convert_png_to_avif(input_folder, output_folder_avif, target_size):
    """
    Convert PNG files to AVIF format using the avifenc tool, aiming to meet a specified file size.

    Args:
    input_folder (str): Directory containing PNG files.
    output_folder_avif (str): Directory where AVIF files will be saved.
    target_size (int): Desired maximum file size for AVIF images in bytes.

    Returns:
    None
    """
    if not os.path.exists(output_folder_avif):
        os.makedirs(output_folder_avif)
    print(f"AVIF folder '{output_folder_avif}' created.")

    png_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]
    for png in png_files:
        source_path = os.path.join(input_folder, png)
        avif_filename = os.path.splitext(png)[0] + '.avif'
        destination_path = os.path.join(output_folder_avif, avif_filename)

        
        quality = 20  # Initial quality setting
        step = 5  # Step to adjust quality to meet size constraints

        # Initial conversion with starting quality
        command = ['avifenc', source_path, destination_path, '--min', str(quality), '--max', str(quality), '--speed', '5']
        subprocess.run(command, check=True)
        file_size = os.path.getsize(destination_path)

        # Adjust the quality until the file size is under the target or the quality reaches a limit
        while file_size > target_size and quality > 10:
            quality += step
            command = ['avifenc', source_path, destination_path, '--min', str(quality), '--max', str(quality), '--speed', '5']
            subprocess.run(command, check=True)
            file_size = os.path.getsize(destination_path)

        if file_size <= target_size:
            print(f"Converted {source_path} to AVIF: {destination_path} with fixed quality {quality}, size {file_size} bytes")
        else:
            print(f"Warning: Could not compress {destination_path} to target size {target_size} bytes even at the lowest quality setting.")

def main():
    input_folder = 'compressed_images_from_jpeg2000_to_png_intermediate'  # Update this path
    output_folder_avif = 'compressed_images_from_jpeg2000_to_avif'  # Update this path
    target_size = 41943  # Target size in bytes, adjust as needed

    # Convert PNG to AVIF
    convert_png_to_avif(input_folder, output_folder_avif, target_size)

if __name__ == "__main__":
    main()
