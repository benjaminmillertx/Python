import os
from datetime import datetime

# Define paths
BASE_DIR = os.path.expanduser("~/Pentest_Reports")
TEMPLATE_PATH = os.path.join(BASE_DIR, "report_template.md")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Create directories if they don't exist
os.makedirs(REPORTS_DIR, exist_ok=True)

# Report Template
REPORT_TEMPLATE = """# Penetration Test Report

## Client Information
- **Client Name**: 
- **Date**: 
- **Assessment Type**: 
- **Scope**: 

---

## Executive Summary
Provide a high-level summary of the findings.

---

## Vulnerabilities
### 1. Vulnerability Title
- **Severity**: 
- **Description**: 
- **Impact**: 
- **Recommendation**: 

### 2. Vulnerability Title
- **Severity**: 
- **Description**: 
- **Impact**: 
- **Recommendation**: 

---

## Tools and Techniques
List of tools and techniques used during the assessment.

---

## Appendices
- **Logs**:
- **Screenshots**:
"""

# Function to create the report template if it doesn't exist
def create_template():
    if not os.path.isfile(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "w") as template_file:
            template_file.write(REPORT_TEMPLATE)
        print(f"Template created at {TEMPLATE_PATH}")
    else:
        print(f"Template already exists at {TEMPLATE_PATH}")

# Function to create a new report
def create_report():
    client_name = input("Enter the client name: ")
    today = datetime.now().strftime("%Y%m%d")
    report_name = f"report_{client_name}_{today}.md"
    report_path = os.path.join(REPORTS_DIR, report_name)

    # Copy template content to the new report
    with open(TEMPLATE_PATH, "r") as template_file:
        template_content = template_file.read()

    # Create the new report file
    with open(report_path, "w") as report_file:
        report_file.write(template_content)

    print(f"New report created at {report_path}")
    return report_path

# Function to add a note to an existing report
def add_note():
    keyword = input("Enter the client name or report date (YYYYMMDD) to find the report: ")
    matching_files = [f for f in os.listdir(REPORTS_DIR) if keyword in f]

    if matching_files:
        print(f"Found the following reports: {matching_files}")
        report_name = matching_files[0]  # Assuming the first match
        report_path = os.path.join(REPORTS_DIR, report_name)

        with open(report_path, "a") as report_file:
            note = input("Enter the note you want to add: ")
            report_file.write(f"\n## Additional Note ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n{note}\n")
        print(f"Note added to {report_name}")
    else:
        print(f"No report found with the keyword '{keyword}'.")

# Menu system
def main_menu():
    while True:
        print("\nPenetration Test Reporting Tool")
        print("1. Create New Report")
        print("2. Add Notes to Existing Report")
        print("3. Exit")

        choice = input("Select an option [1-3]: ")
        if choice == "1":
            create_report()
        elif choice == "2":
            add_note()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    create_template()  # Ensure the template is created
    main_menu()
