import os

# Mock virus signatures (in real use, this would come from a database of known viruses)
VIRUS_SIGNATURES = [
    b'BAD_VIRUS_SIGNATURE_1',  # Example signature
    b'ANOTHER_BAD_SIGNATURE',   # Another example signature
    # Add more signatures as needed
]

def is_infected(file_path):
    """Check if the file contains any known virus signatures."""
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            for signature in VIRUS_SIGNATURES:
                if signature in content:
                    return True
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return False

def scan_directory(directory):
    """Scan the specified directory for infected files."""
    infected_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_infected(file_path):
                infected_files.append(file_path)
    return infected_files

if __name__ == "__main__":
    directory_to_scan = input("Enter the directory to scan for viruses: ")
    found_infected = scan_directory(directory_to_scan)

    if found_infected:
        print("Infected files found:")
        for infected in found_infected:
            print(infected)
    else:
        print("No infected files found.")
