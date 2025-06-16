import os

def rename_files(root_dir):
    # Loop through each folder in the root directory
    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if there is an underscore in the filename
            if '_' in filename:
                # Split the filename at the first underscore
                new_filename = filename.split('_', 1)[1]
                old_filepath = os.path.join(foldername, filename)
                new_filepath = os.path.join(foldername, new_filename)

                # Rename the file
                os.rename(old_filepath, new_filepath)
                print(f"Renamed: {old_filepath} to {new_filepath}")

# Specify the root directory where your folders are located
root_directory = input("Enter path here ")
rename_files(root_directory)
