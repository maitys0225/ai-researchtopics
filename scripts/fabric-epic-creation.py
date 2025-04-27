# 
# Here's a Python script that uses the GitLab API to:
# Create an Epic in a GitLab group.
# Create Issues under that Epic based on acceptance criteria.
# Assign milestones for tracking.
# Add a placeholder for the evaluation report and other deliverables.
# Note: You’ll need:
# A GitLab personal access token with appropriate permissions.
# The group ID where the Epic will be created.
# The project ID where issues will be created (you can use one project or split them across several).
#

# How to Use
# Replace YOUR_GITLAB_PERSONAL_ACCESS_TOKEN, YOUR_GROUP_ID, and YOUR_PROJECT_ID with your real values.

# Install requests if you haven’t:

# ```bash
# pip install requests
# ````
# Run the script from your terminal or Python IDE.

import requests

# ==== CONFIGURATION ====
GITLAB_URL = "https://gitlab.com"  # Change this if using self-hosted GitLab
PRIVATE_TOKEN = "YOUR_GITLAB_PERSONAL_ACCESS_TOKEN"
GROUP_ID = "YOUR_GROUP_ID"  # Replace with your GitLab group ID
PROJECT_ID = "YOUR_PROJECT_ID"  # Replace with your GitLab project ID

HEADERS = {"PRIVATE-TOKEN": PRIVATE_TOKEN}

# ==== EPIC DATA ====
epic_title = "Evaluate and Integrate Microsoft Fabric for Unified Analytics Platform"
epic_description = "This Epic focuses on evaluating Microsoft Fabric and assessing its suitability for integration."

# ==== MILESTONES ====
milestones = [
    "Week 1: Setup Fabric workspace and permissions",
    "Week 2-3: Execute integration tests with Databricks and ADF",
    "Week 4: Test Data Gateway and legacy source integration",
    "Week 5: Validate Blob Storage access and Spark process compatibility",
    "Week 6: Prepare findings and strategic roadmap"
]

# ==== ISSUES ====
issues = [
    {
        "title": "Create working pipeline using Azure Databricks activity in Fabric",
        "description": "- Use ADLS passthrough or service principal\n- Confirm integration with Power BI",
    },
    {
        "title": "Mount ADF pipelines in Fabric",
        "description": "- Use Azure Data Factory item type\n- Invoke and validate pipeline runs",
    },
    {
        "title": "Implement Entra ID-based RBAC model in Fabric",
        "description": "- Configure workspace roles, RLS, CLS\n- Test group-based permissions",
    },
    {
        "title": "Install and test On-Premises Data Gateway",
        "description": "- Connect to Oracle or DB2\n- Transfer data into Fabric pipeline",
    },
    {
        "title": "Create and test OneLake shortcuts to Azure Blob Storage",
        "description": "- Validate access and query performance\n- Assess cost implications",
    },
    {
        "title": "Evaluate Spark & ADF pipeline migration feasibility",
        "description": "- Rebuild one ADF pipeline manually\n- Test Spark code compatibility",
    },
    {
        "title": "Draft final Fabric evaluation report",
        "description": "- Include performance benchmarks, migration plan, security assessment",
    }
]

# ==== CREATE EPIC ====
epic_url = f"{GITLAB_URL}/api/v4/groups/{GROUP_ID}/epics"
epic_payload = {"title": epic_title, "description": epic_description}
epic_response = requests.post(epic_url, headers=HEADERS, json=epic_payload)
epic_response.raise_for_status()
epic_iid = epic_response.json()["iid"]
print(f"✅ Epic created: {epic_title} (IID: {epic_iid})")

# ==== CREATE MILESTONES ====
milestone_ids = {}
for title in milestones:
    payload = {"title": title}
    response = requests.post(f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/milestones", headers=HEADERS, json=payload)
    response.raise_for_status()
    milestone_ids[title] = response.json()["id"]
    print(f"📅 Milestone created: {title}")

# ==== CREATE ISSUES AND LINK TO EPIC ====
for issue in issues:
    issue_payload = {
        "title": issue["title"],
        "description": issue["description"],
        "milestone_id": list(milestone_ids.values())[0],  # Assign to first milestone as placeholder
    }
    issue_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/issues"
    issue_response = requests.post(issue_url, headers=HEADERS, json=issue_payload)
    issue_response.raise_for_status()
    issue_iid = issue_response.json()["iid"]

    # Link issue to Epic
    epic_issue_url = f"{GITLAB_URL}/api/v4/groups/{GROUP_ID}/epics/{epic_iid}/issues"
    link_payload = {"issue_id": issue_response.json()["id"]}
    link_response = requests.post(epic_issue_url, headers=HEADERS, json=link_payload)
    link_response.raise_for_status()

    print(f"🔗 Issue '{issue['title']}' created and linked to epic.")

print("🎉 All issues and milestones created successfully.")
