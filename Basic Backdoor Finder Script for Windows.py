This script scans for suspicious files, running processes, and active network connections that are commonly associated with backdoors.
Python Script
python

import os
import psutil
import socket

# Define suspicious executable patterns (names of common tools)
SUSPICIOUS_FILES = [
    "nc.exe",       # Netcat
    "powershell.exe",  # PowerShell
    "cmd.exe",      # Command prompt
    "bash.exe",     # Bash
    "python.exe",   # Python interpreter
    "perl.exe",     # Perl interpreter
    "php.exe",      # PHP interpreter
]

def find_suspicious_files(path):
    """Search for suspicious files in the specified path."""
    suspicious_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower() in SUSPICIOUS_FILES:
                suspicious_files.append(os.path.join(root, file))
    return suspicious_files

def find_suspicious_processes():
    """Identify suspicious processes running on the system."""
    suspicious_processes = []
    for proc in psutil.process_iter(['name', 'cmdline']):
        if proc.info['name'].lower() in [file.lower() for file in SUSPICIOUS_FILES]:
            suspicious_processes.append(proc.info)
    return suspicious_processes

def check_open_connections():
    """Check for open network connections."""
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        connections.append((conn.laddr, conn.raddr, conn.status))
    return connections

def main():
    print("Searching for suspicious files...")
    suspicious_files = find_suspicious_files("C:\\")  # Scan from the root directory

    if suspicious_files:
        print("\nSuspicious files found:")
        for file in suspicious_files:
            print(file)
    else:
        print("\nNo suspicious files found.")

    print("\nChecking for suspicious processes...")
    suspicious_processes = find_suspicious_processes()
    
    if suspicious_processes:
        print("\nSuspicious processes found:")
        for proc in suspicious_processes:
            print(f"Name: {proc['name']}, Command Line: {' '.join(proc['cmdline'])}")
    else:
        print("No suspicious processes found.")

    print("\nChecking for open network connections...")
    connections = check_open_connections()
    
    if connections:
        print("\nActive network connections:")
        for conn in connections:
            print(f"Local Address: {conn[0]}, Remote Address: {conn[1]}, Status: {conn[2]}")
    else:
        print("No active network connections found.")

if __name__ == "__main__":
    main()
