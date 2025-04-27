#!/usr/bin/env python3
"""
Script to add PlantUML rendering links to markdown files that contain PlantUML code blocks.
"""

import os
import re
import sys
import argparse

def add_plantuml_rendering_links(file_path, username, repo_name):
    """
    Add PlantUML rendering links to a markdown file after each PlantUML code block.
    
    Args:
        file_path: Path to the markdown file
        username: GitHub username
        repo_name: GitHub repository name
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find PlantUML code blocks
    pattern = r'```puml\n@startmindmap.*?@endmindmap\n```'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    # Keep track of positions to avoid messing up the indices
    offset = 0
    
    for match in matches:
        # Calculate current position considering the offset
        start_pos = match.end() + offset
        
        # Create the rendering link with proper paths
        rel_path = os.path.relpath(file_path)
        diagram_id = os.path.splitext(os.path.basename(file_path))[0].lower().replace(' ', '_')
        
        # Extract puml content to create a temporary file
        puml_content = match.group(0)[7:-3]  # Remove ```puml and ``` delimiters
        
        # Create puml file from the content if it doesn't exist
        puml_file_name = f"{diagram_id}_{start_pos}.puml"
        puml_file_path = os.path.join(os.path.dirname(file_path), puml_file_name)
        
        with open(puml_file_path, 'w', encoding='utf-8') as puml_file:
            puml_file.write(puml_content)
        
        # Get relative path for the puml file
        rel_puml_path = os.path.relpath(puml_file_path)
        
        # Create the link to add
        rendering_link = f"""

**Rendered Diagram:**

![{diagram_id.replace('_', ' ').title()}](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/{username}/{repo_name}/main/{rel_puml_path.replace('\\', '/')})

"""
        
        # Insert the rendering link after the code block
        content = content[:start_pos] + rendering_link + content[start_pos:]
        
        # Update offset
        offset += len(rendering_link)
        
        print(f"Added rendering link for PlantUML block in {file_path}")
        print(f"Created PlantUML file: {puml_file_path}")
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Add PlantUML rendering links to markdown files.")
    parser.add_argument("--username", required=True, help="GitHub username")
    parser.add_argument("--repo", required=True, help="GitHub repository name")
    parser.add_argument("--file", help="Specific markdown file to process")
    parser.add_argument("--dir", help="Directory containing markdown files (default: current directory)")
    
    args = parser.parse_args()
    
    if args.file:
        # Process a specific file
        if os.path.exists(args.file) and args.file.endswith(('.md', '.markdown')):
            add_plantuml_rendering_links(args.file, args.username, args.repo)
        else:
            print(f"Error: {args.file} is not a valid markdown file.")
            return 1
    elif args.dir:
        # Process all markdown files in a directory
        if not os.path.isdir(args.dir):
            print(f"Error: {args.dir} is not a valid directory.")
            return 1
        
        for root, _, files in os.walk(args.dir):
            for file in files:
                if file.endswith(('.md', '.markdown')):
                    file_path = os.path.join(root, file)
                    add_plantuml_rendering_links(file_path, args.username, args.repo)
    else:
        # Default: process current directory
        for file in os.listdir('.'):
            if file.endswith(('.md', '.markdown')):
                add_plantuml_rendering_links(file, args.username, args.repo)
    
    print("Done!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 