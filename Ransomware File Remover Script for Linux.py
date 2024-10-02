import os

# Commonly associated ransomware file extensions
RANSOMWARE_EXTENSIONS = [
    '.locked', '.crypto', '.encrypted', '.ransom', 
    '.rgss', '.lockedfile', '.encryptedfile', 
    '.cerber', '.zzz', '.pay', '.file', 
    '.map', '.redu', '.data', '.decrypt'
]

def is_ransomware_file(file_path):
    """Check if the file has a ransomware-like extension."""
    _, ext = os.path.splitext(file_path)
    return ext.lower() in RANSOMWARE_EXTENSIONS

def scan_directory(directory):
    """Scan the specified directory for potential ransomware-encrypted files."""
    ransomware_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_ransomware_file(file_path):
                ransomware_files.append(file_path)

    return ransomware_files

def remove_ransomware_files(files):
    """Attempt to remove ransomware-encrypted files."""
    for file_path in files:
        try:
            os.remove(file_path)
            print(f"Removed: {file_path}")
        except Exception as e:
            print(f"Could not remove {file_path}: {e}")

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory to scan for ransomware files: ")
    
    # Ensure the directory exists
    if not os.path.exists(directory_to_scan):
        print("The specified directory does not exist.")
    elif not os.path.isdir(directory_to_scan):
        print("The specified path is not a directory.")
    else:
        found_ransomware = scan_directory(directory_to_scan)

        if found_ransomware:
            print("Potential ransomware files found:")
            for ransomware in found_ransomware:
                print(ransomware)

            delete_option = input("\nDo you want to remove these files? (yes/no): ").strip().lower()
            if delete_option == 'yes':
                remove_ransomware_files(found_ransomware)
            else:
                print("Operation cancelled.")
        else:
            print("No potential ransomware files found.")
