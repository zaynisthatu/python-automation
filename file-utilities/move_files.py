import os
import shutil

# Ask for the source folder path
source_folder_path = input("Enter the path to the parent directory of all folders: ")

# Ask for the destination folder path
destination_folder_path = input("Enter the path to the folder where you want to move all the files: ")

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder_path):
    os.makedirs(destination_folder_path)

# Iterate through all subfolders in the source folder
for root, dirs, files in os.walk(source_folder_path):
    for file in files:
        # Get the file path
        file_path = os.path.join(root, file)
        # Move the file to the destination folder
        shutil.move(file_path, destination_folder_path)
        print(f"Moved {file} to {destination_folder_path}")
