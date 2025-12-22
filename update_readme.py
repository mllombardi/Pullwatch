#!/usr/bin/env python3
"""
GitHub PR Status Dashboard Generator
Fetches pull request data from multiple repositories and updates README.md
Uses GitHub's free REST API (no authentication required for public repos)
"""

import requests
import json
from datetime import datetime

# Configuration - List of repositories to monitor - needs parameterization
REPOS = [
    "mllombardi/lombardi-py-forge",
    "mllombardi/lombardi-node-forge",
    "mllombardi/lombardi-hcl-forge",
]

def get_pull_requests(repo):
    """Fetch open pull requests for a repository"""
    url = f"https://api.github.com/repos/{repo}/pulls"
    params = {"state": "open", "per_page": 10}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PRs for {repo}: {e}")
        return []

def format_pr_table(repo, prs):
    """Format PRs as a markdown table"""
    if not prs:
        return f"### {repo}\n\nNo open pull requests.\n\n"
    
    table = f"### {repo}\n\n"
    table += "| PR | Title | Author | Status | Created |\n"
    table += "|---|---|---|---|---|\n"
    
    for pr in prs:
        number = pr['number']
        title = pr['title'][:50] + ('...' if len(pr['title']) > 50 else '')
        author = pr['user']['login']
        
        # Check for review status - find better badging system later
        status_emoji = "🟡"  # Pending by default
        if pr.get('draft'):
            status_emoji = "⚪"  # Draft
        elif pr.get('mergeable_state') == 'clean':
            status_emoji = "🟢"  # Ready to merge
        
        created = datetime.strptime(pr['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        pr_link = f"[#{number}]({pr['html_url']})"
        
        table += f"| {pr_link} | {title} | @{author} | {status_emoji} | {created} |\n"
    
    table += "\n"
    return table

def generate_readme():
    """Generate the complete README content"""
    readme_content = "# Pull Request Dashboard\n\n"
    readme_content += f"*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*\n\n"
    readme_content += "## Status Legend\n\n"
    readme_content += "- 🟢 Ready to merge\n"
    readme_content += "- 🟡 Pending review\n"
    readme_content += "- ⚪ Draft\n\n"
    readme_content += "---\n\n"
    
    for repo in REPOS:
        print(f"Fetching PRs for {repo}...")
        prs = get_pull_requests(repo)
        readme_content += format_pr_table(repo, prs)
    
    return readme_content

def main():
    """Main execution function"""
    readme_content = generate_readme()
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ README.md updated successfully!")

if __name__ == "__main__":
    main()
