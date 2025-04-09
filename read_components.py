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

# Dictionary to store projects and their components
project_components = {}
current_project = None

# Parse the projs_components.txt file
with open("projs_components.txt", "r") as f:
    for line in f:
        # Check if this line contains a project name
        if "Component 'X' not found in project" in line:
            match = re.search(r"project (.*?) - Available components are:", line)
            if match:
                current_project = match.group(1)
                project_components[current_project] = []
        
        # Check if this line contains a component (lines that start with spaces followed by a quote)
        elif line.strip().startswith("'") and current_project is not None:
            match = re.search(r"  '(.*?)'", line)
            if match:
                component = match.group(1)
                project_components[current_project].append(component)

# Execute commands for each project-component pair
for project, components in project_components.items():
    for component in components:
        # Create a safe filename
        safe_project = re.sub(r'[^\w]', '_', project)
        safe_component = re.sub(r'[^\w]', '_', component)
        output_file = os.path.join(reports_dir, f"{safe_project}_{safe_component}_attributes.html")
        
        command = (
            f'oslcquery '
            f'-J {server} '
            f'-U {user} '
            f'-P {password} '
            f'-p "{project}" '
            f'-C "{component}" '
            f'-F "X" '
            f'-r "oslc_rm:Requirement" '
            f'--typesystemreport {output_file}'
        )
        print(f"Project={project}", flush=True)
        print(f"Component={component}", flush=True)
        subprocess.run(command, shell=True)

print(f"Processing complete. Reports saved in {reports_dir} directory.")