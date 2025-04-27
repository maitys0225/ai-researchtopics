# Viewing PlantUML Diagrams in GitHub

GitHub doesn't natively render PlantUML (.puml) diagrams. Here's how to make your PlantUML diagrams visible in GitHub:

## Method 1: Using Image Links in Markdown

Add the following markdown code after your PlantUML source code or in any markdown file where you want to display the diagram:

```markdown
![Diagram Title](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/USERNAME/REPOSITORY_NAME/main/path/to/diagram.puml)
```

Replace:
- `USERNAME` with your GitHub username
- `REPOSITORY_NAME` with your repository name
- `path/to/diagram.puml` with the actual path to the PlantUML file

## Method 2: Including in README.md

For this repository, use these links to view the diagrams:

### Database Performance MindMap (Full)
![Database Performance MindMap](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/USERNAME/REPOSITORY_NAME/main/topics/DB_Performance_MindMap.puml)

### Database Performance MindMap (Summary)
![Database Performance MindMap Summary](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/USERNAME/REPOSITORY_NAME/main/topics/db_performance_mindmap_summary.puml)

### Database Performance MindMap (Details)
![Database Performance MindMap Details](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/USERNAME/REPOSITORY_NAME/main/topics/db_performance_mindmap_details.puml)

## Method 3: In Existing Markdown Files

When embedding PlantUML code in markdown documents, you can add the rendered image right after the code block:

```markdown
```puml
@startmindmap
...your PlantUML code...
@endmindmap
```

**Rendered Diagram:**

![Diagram Title](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/USERNAME/REPOSITORY_NAME/main/path/to/diagram.puml)
```

## How It Works

This approach uses PlantUML's web service to render the diagram:
1. The service fetches the raw PlantUML file from your GitHub repository
2. It renders the diagram as an image
3. The image is then displayed in your markdown

The `cache=no` parameter ensures that the latest version is displayed whenever the page is refreshed. 