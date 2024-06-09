import subprocess
import os

def convert_png_to_heic(input_folder, output_folder_heic, target_size):
    """
    Convert PNG files to HEIC format using ImageMagick, attempting to meet a specified file size.

    Args:
    input_folder (str): Directory containing PNG files.
    output_folder_heic (str): Directory where HEIC files will be saved.
    target_size (int): Desired maximum file size for HEIC images in bytes.

    Returns:
    None
    """
    if not os.path.exists(output_folder_heic):
        os.makedirs(output_folder_heic)
    print(f"HEIC folder '{output_folder_heic}' created.")

    png_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]
    for png in png_files:
        source_path = os.path.join(input_folder, png)
        heic_filename = os.path.splitext(png)[0] + '.heic'
        destination_path = os.path.join(output_folder_heic, heic_filename)

        # Start with a high quality value and decrease it to adjust file size
        quality = 70
        while quality > 0:
            command = ['magick', source_path, '-quality', str(quality), destination_path]
            subprocess.run(command, check=True)
            file_size = os.path.getsize(destination_path)
            if file_size <= target_size:
                print(f"Converted {source_path} to HEIC: {destination_path} with quality={quality}, size={file_size} bytes")
                break
            quality -= 5  # Decrease quality by 5 units in each iteration

            if quality == 0:  # If quality reaches zero, report if target size is not achieved
                print(f"Warning: Could not compress {destination_path} to target size {target_size} bytes at any quality.")

def main():
    input_folder = 'compressed_images_from_jpeg2000_to_png_intermediate'  # Path to your intermediate PNG files
    output_folder_heic = 'compressed_images_from_jpeg2000_to_heic'  # Path where you want to save the HEIC files
    target_size = 41943  # Target size in bytes, adjust as needed

    # Convert PNG to HEIC
    convert_png_to_heic(input_folder, output_folder_heic, target_size)

if __name__ == "__main__":
    main()
