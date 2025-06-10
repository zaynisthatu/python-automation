import os 
import shutil
source_folder = '.'
orgnize_files=os.listdir(source_folder)
for f in orgnize_files:
    file_path = os.path.join(source_folder,f)

    if os.path.isfile(file_path):
        filename , file_extension   = os.path.splitext(file_path)
        file_extension=file_extension.lower()

        if file_extension :
            temp_folder_name = file_extension[1:] + '_Files'
            
            destination_folder = os.path.join(source_folder,temp_folder_name)

            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            shutil.move(file_path,destination_folder)
            print(f"Moved {f} to folder {temp_folder_name}")