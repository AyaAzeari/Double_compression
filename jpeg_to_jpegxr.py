import subprocess
import os

def jpeg_to_bmp(jpeg_folder, bmp_folder):
    """Converts JPEG images to BMP format."""
    if not os.path.exists(bmp_folder):
        os.makedirs(bmp_folder)
    print(f"Folder '{bmp_folder}' created.")

    jpeg_files = [f for f in os.listdir(jpeg_folder) if f.lower().endswith('.jpg')]
    for jpeg in jpeg_files:
        input_path = os.path.join(jpeg_folder, jpeg)
        output_path = os.path.join(bmp_folder, os.path.splitext(jpeg)[0] + '.bmp')
        subprocess.run(['magick', 'convert', input_path, output_path], check=True)
        original_size = os.path.getsize(input_path)
        converted_size = os.path.getsize(output_path)
        print(f"Converted {input_path} to {output_path}")
        print(f"Original size: {original_size} bytes, BMP size: {converted_size} bytes")

def bmp_to_jpegxr(bmp_folder, jpegxr_folder, target_size):
    """Converts BMP images to JPEG XR format, adjusting quality to meet a target size."""
    if not os.path.exists(jpegxr_folder):
        os.makedirs(jpegxr_folder)
    print(f"Folder '{jpegxr_folder}' created.")

    bmp_files = [f for f in os.listdir(bmp_folder) if f.lower().endswith('.bmp')]
    for bmp in bmp_files:
        input_path = os.path.join(bmp_folder, bmp)
        base_name = os.path.splitext(bmp)[0]
        output_path = os.path.join(jpegxr_folder, base_name + '.jxr')
        quality = 1  # Start with the highest quality
        while quality <= 255:
            command = ['JxrEncApp', '-i', input_path, '-o', output_path, '-q', str(quality), '-c', '9']
            subprocess.run(command, check=True)
            current_size = os.path.getsize(output_path)
            if current_size <= target_size:
                print(f"Converted {input_path} to {output_path} with quality {quality}, size {current_size} bytes meets target size")
                break
            if quality == 255:
                print(f"Warning: Maximum compression reached without meeting target size for {output_path}.")
                break
            quality += 5  # Increment quality level for more compression

def main():
    jpeg_folder = 'compressed_images_from_png_to_jpeg'
    bmp_folder = 'bmp_images_from_jpeg'
    jpegxr_folder = 'compressed_images_from_jpeg_to_jpegxr'
    target_size = 41943  # Target file size in bytes

    #jpeg_to_bmp(jpeg_folder, bmp_folder)
    bmp_to_jpegxr(bmp_folder, jpegxr_folder, target_size)

if __name__ == "__main__":
    main()
