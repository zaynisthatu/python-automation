import os
inputerr=input("Enter path to rename files: ")
items = os.listdir(inputerr)
# num = int(input("Enter starting number for renaming: "))
old_extension = ".txt"
new_extension = ".md"
for name in items:
    if name.endswith(old_extension):
        old_path = os.path.join(inputerr, name)
        new_name = name.replace(old_extension, new_extension)
        new_path = os.path.join(inputerr, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {name} to {new_name}")
        

