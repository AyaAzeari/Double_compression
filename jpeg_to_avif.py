import subprocess
import os

def convert_jpeg_to_avif(input_folder, output_folder, target_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]
    results = []  # To store results for reporting

    for file_name in files:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_name = os.path.splitext(file_name)[0] + '.avif'
        output_file_path = os.path.join(output_folder, output_file_name)

        # Start from a medium quality and adjust based on file size
        quality = 50
        min_quality, max_quality = 1, 100
        best_size = float('inf')
        best_quality = quality

        while min_quality <= max_quality:
            command = ['avifenc', input_file_path, output_file_path, '--qcolor', str(quality), '--speed', '6']
            subprocess.run(command, check=True)
            current_size = os.path.getsize(output_file_path)

            if current_size > target_size:
                max_quality = quality - 1
            elif current_size < target_size:
                min_quality = quality + 1
                if current_size < best_size:  # Keep track of the closest size under target
                    best_size = current_size
                    best_quality = quality
            else:  # Exact match
                best_size = current_size
                best_quality = quality
                break

            quality = (min_quality + max_quality) // 2  # Adjust quality based on binary search

        results.append((output_file_name, best_quality, best_size))

        print(f"Encoded {file_name} to {output_file_path} with quality {best_quality} and size {best_size} bytes")

    return results

# Example usage
input_folder = 'compressed_images_from_png_to_jpeg'
output_folder = 'compressed_images_from_jpeg_to_avif'
target_compressed_size = 41943  # Target size in bytes, adjust as needed
results = convert_jpeg_to_avif(input_folder, output_folder, target_compressed_size)

# Printing all results for review
for result in results:
    print(f"File {result[0]} encoded with quality {result[1]} to size {result[2]} bytes")
