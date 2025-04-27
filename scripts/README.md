# Scripts for Repository Maintenance

This directory contains utility scripts for maintaining and working with this repository.

## PlantUML Rendering Script

The `add_plantuml_rendering.py` script automatically adds GitHub-compatible rendering links to PlantUML diagrams in markdown files.

### Usage

```bash
# Process a specific markdown file
./add_plantuml_rendering.py --username YOUR_GITHUB_USERNAME --repo YOUR_REPO_NAME --file path/to/file.md

# Process all markdown files in a directory
./add_plantuml_rendering.py --username YOUR_GITHUB_USERNAME --repo YOUR_REPO_NAME --dir path/to/directory

# Process all markdown files in the current directory
./add_plantuml_rendering.py --username YOUR_GITHUB_USERNAME --repo YOUR_REPO_NAME
```

### What it does

1. Scans markdown files for PlantUML code blocks
2. Extracts the PlantUML content to separate `.puml` files
3. Adds rendering links that reference these `.puml` files using the GitHub-compatible syntax:
   ```
   ![Diagram Title](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/USERNAME/REPOSITORY_NAME/main/path/to/diagram.puml)
   ```

### Example

Running:
```bash
./add_plantuml_rendering.py --username myuser --repo my-repo --file ../topics/Database\ Performance\ for\ Large\ Datasets_.md
```

Will:
1. Extract PlantUML code blocks from the markdown file
2. Create separate `.puml` files for each block
3. Add rendering links after each code block in the markdown

### Requirements

- Python 3.6+
- The script must have execution permissions:
  ```bash
  chmod +x add_plantuml_rendering.py
  ``` 