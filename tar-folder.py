import sys
import subprocess
import tarfile
import os
import threading
from datetime import datetime

def create_tar_from_file_list(file_paths, output_tar_name):
    try:
        # Create the tar file
        with tarfile.open(output_tar_name, 'w:gz') as tar:
            # Add each file to the tar archive
            for file_path in file_paths:
                path=file_path.rstrip('\n')
                if os.path.exists(path):
                    tar.add(path)
        print(f"Tar file '{output_tar_name}' created successfully.")
    except Exception as e:
        print(f"Error creating tar file: {e}")

if __name__ == "__main__":
    # Check if the file name is provided as a command-line argument
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    # List files in the specified folder
    lines = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            lines.append(file_path)

    split_number = int(sys.argv[2])
    current_time=datetime.now().strftime("%Y-%m-%d-%H%M%S")
    folder_path=f"./backup_{current_time}"
    # Create the folder
    os.makedirs(folder_path)
    output_prefix = f"{folder_path}/part_"

    chunk_size = len(lines)
    chunk_part_lines =  round(chunk_size / split_number)
    
    print(f"chunk_size {chunk_size}")
    print(f"chunk_part_lines {chunk_part_lines}")

    part_files=[]
    for i in range(split_number):
        start_index = 0
        if i > 0:
            start_index = round(i * chunk_part_lines)

        end_index = round((i + 1) * chunk_part_lines)

        output_file_path = f"{output_prefix}_{i}.tar.gz"
        part_files.append(output_file_path)
        threads = []
        with open(output_file_path, 'w') as output_file:
            thread = threading.Thread(target=create_tar_from_file_list, args=(lines[start_index:end_index], output_file_path))
            threads.append(thread)
            thread.start()
        print(f"File {i + 1}: {output_file_path}")

    for thread in threads:
        thread.join()
