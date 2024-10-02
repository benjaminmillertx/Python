Basic Backdoor Finder Script for Linux

This script searches for suspicious network connections, strange or unusual files, and other indicators commonly associated with backdoors.
Python Script
python

import os
import subprocess

# Define suspicious executable patterns
SUSPICIOUS_FILES = [
    "nc",           # Netcat
    "bash",         # Shells
    "sh",
    "php",          # PHP scripts
    "perl",         # Perl scripts
    "python",       # Python scripts
    "powershell",   # Windows PowerShell
    "wget",         # File download utilities
]

def find_suspicious_files(path):
    """Search for suspicious files in the specified path."""
    suspicious_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower() in SUSPICIOUS_FILES:
                suspicious_files.append(os.path.join(root, file))
    return suspicious_files

def check_open_connections():
    """Check for suspicious open network connections."""
    try:
        # Using `ss` to check for open sockets
        connections = subprocess.check_output(["ss", "-tuna"]).decode('utf-8')
        return connections
    except Exception as e:
        print(f"Error checking open connections: {e}")
        return ""

def main():
    print("Searching for suspicious files...")
    home_dir = os.path.expanduser("~")
    suspicious_files = find_suspicious_files(home_dir)

    if suspicious_files:
        print("\nSuspicious files found:")
        for file in suspicious_files:
            print(file)
    else:
        print("\nNo suspicious files found.")

    print("\nChecking for open network connections...")
    connections = check_open_connections()
    print(connections)

if __name__ == "__main__":
    main()
