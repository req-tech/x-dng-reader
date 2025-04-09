#!/usr/bin/env python3

import subprocess
import re
import os

# Create htmlreports directory if it doesn't exist
reports_dir = "htmlreports"
os.makedirs(reports_dir, exist_ok=True)

# Get server, user, and password from environment variables without defaults
server = os.environ.get('server')
user = os.environ.get('user')
password = os.environ.get('password')

# Parse the projs_components_configs.txt file
current_project = None
current_component = None
configs_to_process = []

with open("projs_components_configs.txt", "r") as f:
    skip_next_line = False
    for line in f:
        line = line.strip()
        
        # Check for project line
        if line.startswith("Project="):
            current_project = line[8:]  # Remove "Project=" prefix
            
        # Check for component line
        elif line.startswith("Component="):
            current_component = line[10:]  # Remove "Component=" prefix
            
        # Skip Version and Configuration 'X' not found lines
        elif line.startswith("Version") or "Configuration 'X' not found" in line:
            continue
            
        # Check for configuration lines (start with spaces and a quote)
        elif line.startswith("'") or (line.startswith("  '") and current_project and current_component):
            # Extract the configuration name within quotes
            match = re.search(r"'(.*?)'", line)
            if match:
                config = match.group(1)
                configs_to_process.append((current_project, current_component, config))

# Check if environment variables are set
if not server or not user or not password:
    print("Error: Environment variables 'server', 'user', and 'password' must be set.")
    exit(1)

# Execute commands for each project-component-config combination
for project, component, config in configs_to_process:
    # Create a safe filename
    safe_project = re.sub(r'[^\w]', '_', project)
    safe_component = re.sub(r'[^\w]', '_', component)
    safe_config = re.sub(r'[^\w]', '_', config)
    output_file = os.path.join(reports_dir, f"{safe_project}_{safe_component}_{safe_config}_attributes.html")
    
    command = (
        f'oslcquery '
        f'-J {server} '
        f'-U {user} '
        f'-P {password} '
        f'-p "{project}" '
        f'-C "{component}" '
        f'-F "{config}" '
        f'-r "oslc_rm:Requirement" '
        f'--typesystemreport {output_file}'
    )
    print(f"Project={project}", flush=True)
    print(f"Component={component}", flush=True)
    print(f"Configuration={config}", flush=True)
    subprocess.run(command, shell=True)

print(f"Processing complete. Reports saved in {reports_dir} directory.")