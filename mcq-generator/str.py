import os

def create_project_structure(base_path='project_folder'):
    # Define folder names
    lectures_folder = os.path.join(base_path, 'lectures')
    mcq_outputs_folder = os.path.join(base_path, 'mcq_outputs')

    # Create base directory
    os.makedirs(base_path, exist_ok=True)

    # Create subdirectories
    os.makedirs(lectures_folder, exist_ok=True)
    os.makedirs(mcq_outputs_folder, exist_ok=True)

    # Create lec_1.txt to lec_45.txt inside lectures/
    for i in range(1, 46):
        file_path = os.path.join(lectures_folder, f'lec_{i}.txt')
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(f"")  # Write empty content or template text if needed

    print(f"Project structure created at '{base_path}'.")

if __name__ == '__main__':
    create_project_structure()
