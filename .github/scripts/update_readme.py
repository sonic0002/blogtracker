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
    
    # Debug print to see the actual issue body format
    print("Issue body:", issue['body'])
    
    # Parse issue body to extract blog information
    body = issue['body']
    
    # Updated regex patterns to match the form field format
    blog_name_match = re.search(r'### 博客名称\n\n(.*?)(?=\n\n|$)', body, re.DOTALL)
    blog_url_match = re.search(r'### 博客链接\n\n(.*?)(?=\n\n|$)', body, re.DOTALL)
    blog_author_match = re.search(r'### 作者\n\n(.*?)(?=\n\n|$)', body, re.DOTALL)
    blog_focus_match = re.search(r'### 主要领域\n\n(.*?)(?=\n\n|$)', body, re.DOTALL)
    
    # Add error checking for each field
    if not all([blog_name_match, blog_url_match, blog_author_match, blog_focus_match]):
        missing_fields = []
        if not blog_name_match: missing_fields.append("博客名称")
        if not blog_url_match: missing_fields.append("博客链接")
        if not blog_author_match: missing_fields.append("作者")
        if not blog_focus_match: missing_fields.append("主要领域")
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Clean up the extracted text (remove extra whitespace and newlines)
    blog_data = {
        'name': blog_name_match.group(1).strip(),
        'url': blog_url_match.group(1).strip(),
        'author': blog_author_match.group(1).strip(),
        'focus': blog_focus_match.group(1).strip()
    }
    
    # Debug print to verify extracted data
    print("Extracted blog data:", blog_data)
    
    return blog_data

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