import os
import re
import json
import requests

def get_issue_data():
    token = os.environ['GITHUB_TOKEN']
    issue_number = os.environ['ISSUE_NUMBER']
    repo = os.environ['GITHUB_REPOSITORY']
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{repo}/issues/{issue_number}'
    response = requests.get(url, headers=headers)
    issue = response.json()
    
    # Parse issue body to extract blog information
    body = issue['body']
    match = re.search(r'博客名称:\s*(.+)', body)
    if match:
        blog_name = match.group(1)
    else:
        raise ValueError("Blog name not found in issue body")
    blog_url = re.search(r'博客链接:\s*(.+)', body).group(1)
    blog_author = re.search(r'作者:\s*(.+)', body).group(1)
    blog_focus = re.search(r'主要领域:\s*(.+)', body).group(1)
    
    return {
        'name': blog_name,
        'url': blog_url,
        'author': blog_author,
        'focus': blog_focus
    }

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    blog_data = get_issue_data()
    new_row = f"| {blog_data['name']} | [{blog_data['url']}]({blog_data['url']}) | {blog_data['author']} | {blog_data['focus']} |"
    
    # Find the table and add the new row
    table_pattern = r'(\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[\r\n]+)((?:\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[\r\n]+)*)'
    replacement = f'\\1\\2{new_row}\n'
    
    updated_content = re.sub(table_pattern, replacement, content)
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == '__main__':
    update_readme() 