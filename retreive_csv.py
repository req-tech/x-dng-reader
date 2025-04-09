import os
import re
import csv
import sys
import glob
from html.parser import HTMLParser

class PropertiesTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_properties_table = False
        self.in_row = False
        self.in_heading = False
        self.found_properties_heading = False
        self.current_cell = ""
        self.properties = []
        self.current_property = []
        self.column_index = 0
        self.headers = ["Project", "Shape", "Property Name", "Property label", "URI"]
        
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'h2' and not self.found_properties_heading:
            self.in_heading = True
        elif tag.lower() == 'table' and self.found_properties_heading:
            self.in_properties_table = True
        elif tag.lower() == 'tr' and self.in_properties_table:
            self.in_row = True
            self.current_property = []
            self.column_index = 0
        elif tag.lower() == 'th' and self.in_properties_table:
            pass  # We already know the headers
        elif tag.lower() == 'td' and self.in_row:
            self.current_cell = ""
            
    def handle_endtag(self, tag):
        if tag.lower() == 'h2':
            self.in_heading = False
        elif tag.lower() == 'table' and self.in_properties_table:
            self.in_properties_table = False
        elif tag.lower() == 'tr' and self.in_row:
            self.in_row = False
            if self.current_property:  # Skip empty rows
                self.properties.append(self.current_property)
        elif tag.lower() == 'td' and self.in_row:
            self.current_property.append(self.current_cell.strip())
            self.column_index += 1
            
    def handle_data(self, data):
        if self.in_heading and data.strip() == "Properties with no shape":
            self.found_properties_heading = True
        elif self.in_row:
            self.current_cell += data

def extract_properties_from_html(html_file):
    # Extract project name from HTML filename
    project_name = os.path.basename(html_file)
    project_name = os.path.splitext(project_name)[0]  # Remove .html extension
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252']
    
    html_content = None
    for encoding in encodings:
        try:
            with open(html_file, 'r', encoding=encoding) as f:
                html_content = f.read()
                print(f"Successfully read file {html_file} using {encoding} encoding")
                break
        except UnicodeDecodeError:
            print(f"Failed to decode {html_file} with {encoding}, trying next encoding...")
    
    if html_content is None:
        # Try binary read as fallback
        try:
            with open(html_file, 'rb') as f:
                html_content = f.read().decode('utf-8', errors='replace')
                print(f"Using binary read with replacement for decoding {html_file}")
        except Exception as e:
            print(f"Failed to read the file {html_file}: {e}")
            return []
    
    # Parse the HTML to extract the properties table
    parser = PropertiesTableParser()
    parser.feed(html_content)
    
    # Add project name to each property
    result = []
    for prop in parser.properties:
        result.append([project_name] + prop)
    
    print(f"Extracted {len(result)} properties from {html_file}")
    return result, parser.headers

def process_all_html_files(reports_dir, output_csv):
    # Check if directory exists
    if not os.path.exists(reports_dir):
        print(f"Error: Directory {reports_dir} does not exist.")
        return
    
    # Get all HTML files in the directory
    html_files = glob.glob(os.path.join(reports_dir, "*.html"))
    if not html_files:
        print(f"No HTML files found in {reports_dir}")
        return
    
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file and collect all properties
    all_properties = []
    headers = None
    
    for html_file in html_files:
        properties, file_headers = extract_properties_from_html(html_file)
        all_properties.extend(properties)
        if headers is None:
            headers = file_headers
    
    # Create directory for the output file if needed
    os.makedirs(os.path.dirname(os.path.abspath(output_csv)), exist_ok=True)
    
    # Write all properties to a single CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers first
        writer.writerow(headers)
        # Write all data rows
        writer.writerows(all_properties)
    
    print(f"Processed {len(html_files)} files. Total of {len(all_properties)} properties written to {output_csv}")
    return headers

if __name__ == "__main__":
    # Get input directory and output file from command-line arguments
    if len(sys.argv) >= 3:
        reports_dir = sys.argv[1]
        csv_file = sys.argv[2]
    else:
        # Default paths
        reports_dir = "htmlreports"
        csv_file = "all_properties.csv"
    
    # Process all HTML files and create a single CSV
    headers = process_all_html_files(reports_dir, csv_file)
    
    # If this is being run directly (not imported), print the headers for the batch file
    if len(sys.argv) >= 4 and sys.argv[3] == "--print-headers":
        print(",".join(headers))