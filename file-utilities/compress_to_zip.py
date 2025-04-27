import zipfile
import os

def zip_item(item_path, zip_path):
    try:
        # Ensure zip_path ends with .zip
        if not zip_path.lower().endswith('.zip'):
            zip_path += '.zip'
            
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isfile(item_path):
                # If it's a file, just add it
                zipf.write(item_path, os.path.basename(item_path))
            elif os.path.isdir(item_path):
                # If it's a folder, add all contents
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(item_path))
                        zipf.write(file_path, arcname)
            print(f"Successfully created {zip_path}")
            print(f"Location: {os.path.abspath(zip_path)}")
            return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    print("Zip Creator - Simple file/folder compression")
    print("-------------------------------------------")
    
    item_path = input("Enter the path of the file or folder to zip: ").strip('"').strip()
    zip_path = input("Enter the path where to save the zip file (include filename): ").strip('"').strip()
    
    # Normalize paths (convert to absolute paths)
    item_path = os.path.abspath(item_path)
    zip_path = os.path.abspath(zip_path)
    
    print("\nVerifying paths...")
    print(f"Source: {item_path}")
    print(f"Destination: {zip_path}")
    
    if not os.path.exists(item_path):
        print("\nERROR: The path you want to zip doesn't exist")
        print("Please check the path and try again")
        return
    
    if not os.path.exists(os.path.dirname(zip_path)):
        print("\nERROR: The destination folder doesn't exist")
        print("Please create the folder first or choose a different location")
        return
    
    print("\nStarting compression...")
    if zip_item(item_path, zip_path):
        print("Done!")
    else:
        print("Failed to create zip file")

if __name__ == "__main__":
    main()