import os

# Define system directories to exclude
system_dirs = [
    "/System",
    "/Library",
    "/Applications",
    "/Network",
    "/Volumes",
    "/private/var/vm",  # Exclude the directory containing the sleepimage file
    "/usr",
]

# Also exclude the Library directory in user home directories
home_dir = os.path.expanduser("~")
user_system_dirs = [
    os.path.join(home_dir, "Library")
]

# Function to check if a path is in a system directory
def is_in_system_dir(path):
    for sys_dir in system_dirs + user_system_dirs:
        if path.startswith(sys_dir):
            return True
    return False

# Step 1: Walk the filesystem
file_metadata = {}

# Traverse the filesystem from the root directory
for root, directories, files in os.walk('/'):
    # Skip system directories
    if is_in_system_dir(root):
        continue
    for _file in files:
        try:
            full_path = os.path.join(root, _file)
            size_bytes = os.path.getsize(full_path)
            # Convert size to GB
            size_gb = size_bytes / (1024 * 1024 * 1024)
            file_metadata[full_path] = size_gb
        except (OSError, PermissionError):
            # Skip files that can't be accessed
            continue

# Step 2: Define a function to sort and prompt for deletion
def by_value(item):
    return item[1]

# Step 3: Prompt the user and delete files based on their response
for path, size_gb in sorted(file_metadata.items(), key=by_value, reverse=True):
    print(f"Size: {size_gb:.2f} GB - Path: {path}")
    response = input(f"Do you want to delete this file? (y/n): ").strip().lower()
    if response == 'y':
        try:
            os.remove(path)
            print(f"Deleted: {path}")
        except Exception as e:
            print(f"Error deleting {path}: {e}")
