import json
import os
import yaml

with open("_DATA_AND_OUTPUTS/data_and_configs.yaml","r") as f:
    data_and_configs = yaml.safe_load(f)
 
# Your Windows Graphviz DLL routing (Crucial for Windows!)
os.add_dll_directory(data_and_configs["graphviz_path"])
os.environ["PATH"] += os.pathsep + data_and_configs["graphviz_path"]

from eralchemy2 import render_er

def json_to_markdown(json_filepath, output_er_filepath):
    # 1. Load the new Claude-generated JSON data
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    markdown_lines = []

    # 2. Parse the Tables
    for table in data.get('tables', []):
        markdown_lines.append(f"[{table['name']}]")
        
        for col in table.get('columns', []):
            # Prefix with * if it's a primary key
            pk_marker = "*" if col.get('is_pk') else ""
            
            # Format data type and length (e.g., nvarchar(60))
            col_type = col.get('type', '')
            col_length = col.get('length')
            if col_length:
                col_type = f"{col_type}({col_length})"
                
            # Handle nullability
            null_status = "NULL" if col.get('is_nullable') else "NOT NULL"
            
            # Add the line to our markdown
            markdown_lines.append(f"{pk_marker}{col['name']} {col_type} {null_status}")
            
        markdown_lines.append("") # Empty line between tables for readability

    # 3. Parse the Relationships
    markdown_lines.append("# Relationships")
    for rel in data.get('relationships', []):
        # The new JSON nests the table names inside 'from_table' and 'to_table' dictionaries
        from_table = rel['from_table']['name']
        to_table = rel['to_table']['name']
        cardinality = rel['cardinality']
        
        rel_string = f"{from_table} {cardinality} {to_table}"
        markdown_lines.append(rel_string)

    # 4. Save the compiled markdown to an .er file
    final_markdown = "\n".join(markdown_lines)
    with open(output_er_filepath, 'w') as f:
        f.write(final_markdown)
        
    return final_markdown

# Execute the pipeline
try:
    # 1. Parse the JSON and write the markdown file
    print("Parsing modelling_data.json...")
    er_markdown = json_to_markdown('_DATA_AND_OUTPUTS/modelling_data.json', '_DATA_AND_OUTPUTS/m365_schema.er')
    
    # 2. Render the PNG directly from the generated markdown list
    print("Rendering PNG via ERAlchemy...")
    render_er(er_markdown.split('\n'), '_DATA_AND_OUTPUTS/m365_er_diagram.png')
    
    print("Success! m365_schema.er saved and m365_er_diagram.png generated.")
except Exception as e:
    print(f"An error occurred: {e}")