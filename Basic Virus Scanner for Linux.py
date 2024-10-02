import os

# Mock virus signatures (replace with actual byte sequences in practice)
VIRUS_SIGNATURES = [
    b'BAD_VIRUS_SIGNATURE_1',  # Example signature 1
    b'ANOTHER_BAD_SIGNATURE',   # Example signature 2
    b'\x7fELF',                 # ELF binaries could indicate potential threats
    # Add more signatures as needed...
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

Explanation:

    Virus Signatures: The VIRUS_SIGNATURES list contains byte patterns that are associated with known malicious files. You’ll want to replace these examples with actual signatures specific to threats you want to detect.

    is_infected Function: This function reads each file's content in binary mode and checks against the virus signatures. If a signature is found, it indicates the file may be infected.

    scan_directory Function: This function traverses through the directory tree starting from a specified root directory. It checks each file using the is_infected function.

    Error Handling: Basic error handling is implemented to manage cases where a file might not be readable or accessible.

    Running the Scanner: When executed, the script prompts the user for a directory to scan.
