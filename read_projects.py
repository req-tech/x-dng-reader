#!/usr/bin/env python3

import subprocess
import re
import os

# Create htmlreports directory if it doesn't exist
reports_dir = "htmlreports"
os.makedirs(reports_dir, exist_ok=True)

# Get server, user, and password from environment variables
server = os.environ.get('server')
user = os.environ.get('user')  # Note: keeping quotes as in bat file
password = os.environ.get('password')

# Read projects from projects.txt file
projects = []
try:
    with open("projects.txt", "r") as file:
        for line in file:
            # Look for lines that start with spaces and contain project names in single quotes
            match = re.search(r"^\s+'([^']+)'", line)
            if match:
                project_name = match.group(1)
                projects.append(project_name)
    
    print(f"Loaded {len(projects)} projects from projects.txt")
except FileNotFoundError:
    print("Error: projects.txt file not found")
    exit(1)

# Check if any projects were loaded
if not projects:
    print("No projects found in projects.txt")
    exit(1)

# Loop through each project and run the oslcquery command
for project in projects:
    # Create a safe filename by replacing spaces and special characters with underscores
    safe_name = re.sub(r'[^\w]', '_', project)
    output_file = os.path.join(reports_dir, f"{safe_name}_attributes.html")
    
    command = (
        f'oslcquery '
        f'-J {server} '
        f'-U {user} '
        f'-P {password} '
        f'-p "{project}" '
        f'-C "X" '
        f'-r "oslc_rm:Requirement" '
        f'--typesystemreport {output_file}'
    )
    print(f"Executing: {command}")
    subprocess.run(command, shell=True)

print("Processing complete.")