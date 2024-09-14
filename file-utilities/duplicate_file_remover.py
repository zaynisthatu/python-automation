import os
import hashlib

def calculate_hash(file_path):
    """
    Calculate the hash of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Hash of the file.
    """
    with open(file_path, 'rb') as file:
        file_hash = hashlib.md5()
        while chunk := file.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def find_and_remove_duplicates(directory):
    """
    Find and remove duplicate files and folders in a directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        None
    """
    file_hashes = {}
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_hash(file_path)
            if file_hash in file_hashes:
                os.remove(file_path)
                print(f"Removed duplicate file: {file_path}")
            else:
                file_hashes[file_hash] = file_path

    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty folder: {dir_path}")

if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    if os.path.isdir(directory):
        find_and_remove_duplicates(directory)
    else:
        print("Invalid directory path.")
