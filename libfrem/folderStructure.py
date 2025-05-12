import os

def generate_directory_structure(folder_path, output_file):
    with open(output_file, 'w') as file:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            file.write(f"{item}\n")  # Write the name of the item (file/folder)

            # If the item is a directory, inspect its contents
            if os.path.isdir(item_path):
                for subitem in os.listdir(item_path):
                    subitem_path = os.path.join(item_path, subitem)

                    # Check if the subitem is a directory
                    if os.path.isdir(subitem_path):
                        # Count files in the subdirectory
                        n_files = len([f for f in os.listdir(subitem_path) if os.path.isfile(os.path.join(subitem_path, f))])
                        file.write(f"-  {subitem}  {n_files}\n")


import os

def generate_file_structure(folder_path, indent_level=0):
    # Generate an indentation for subdirectories
    indent = '    ' * indent_level
    try:
        # List all items in the current directory
        with os.scandir(folder_path) as entries:
            for entry in entries:
                # Print the current entry with indentation
                print(f"{indent}|-- {entry.name}")
                # If the entry is a directory, recurse into it
                if entry.is_dir():
                    generate_file_structure(entry.path, indent_level + 1)
    except PermissionError:
        # Handle directories that cannot be accessed
        print(f"{indent}|-- [Permission Denied]")

# Usage
generate_directory_structure(".", "output.txt")
