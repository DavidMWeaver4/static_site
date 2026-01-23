import os
import shutil

def copy_files_recursive(src, dest):
    """
    Recursively copies all contents from src to dest.
    Assumes dest is clean or already deleted at the start.
    """
    # If src is a file, copy it
    if os.path.isfile(src):
        # Ensure parent directory exists
        os.makedirs(dest, exist_ok=True)
        shutil.copy(src, dest)
        print(f"Copied file: {src} -> {dest}")
        return

    # src is a directory
    if not os.path.exists(dest):
        os.mkdir(dest)
        print(f"Created directory: {dest}")

    # Recursively copy everything inside
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        copy_files_recursive(src_path, dest_path)
