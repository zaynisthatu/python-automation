import os

def remove_empty_folders(directory):
    if not os.path.isdir(directory):
        print("The provided path is not a directory.")
        return

    # Walk through the directory
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            folder_path = os.path.join(root, name)
            try:
                # Remove the folder if it's empty
                os.rmdir(folder_path)
                print(f"Removed empty folder: {folder_path}")
            except OSError:
                pass  # folder is not empty or an error occurred

if __name__ == "__main__":
    dir_to_clean = input("Enter the path of the directory to clean: ")
    remove_empty_folders(dir_to_clean)
