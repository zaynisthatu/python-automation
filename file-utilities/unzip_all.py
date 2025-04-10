import os
import zipfile
from pathlib import Path

def unzip_all_in_directory():
    # Ask user for directory path
    dir_path = input("Enter the directory path containing ZIP files (or press Enter for current directory): ").strip()
    
    # Use current directory if empty input
    if not dir_path:
        dir_path = os.getcwd()
    
    # Validate directory exists
    if not os.path.isdir(dir_path):
        print(f"Error: Directory not found - {dir_path}")
        return
    
    # Find all .zip files in the directory
    zip_files = [f for f in os.listdir(dir_path) if f.lower().endswith('.zip')]
    
    if not zip_files:
        print(f"No ZIP files found in directory: {dir_path}")
        return
    
    print(f"\nFound {len(zip_files)} ZIP file(s) in {dir_path}:")
    for i, zip_file in enumerate(zip_files, 1):
        print(f"{i}. {zip_file}")
    
    print("\nStarting extraction...\n")
    
    for zip_file in zip_files:
        try:
            # Create paths
            zip_path = os.path.join(dir_path, zip_file)
            folder_name = os.path.splitext(zip_file)[0]
            output_path = os.path.join(dir_path, folder_name)
            
            # Create output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
            
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_path)
            
            print(f"✓ Extracted: {zip_file} → {folder_name}/")
            
        except Exception as e:
            print(f"✗ Failed to extract {zip_file}: {str(e)}")
    
    print("\nExtraction complete!")

if __name__ == "__main__":
    unzip_all_in_directory()