#!/usr/bin/env python3
"""
Parse Git commit messages for Learning Points (LP #XXX format)
and extract metadata for Notion SLL sync.
"""

import os
import re
import json
import sys

def parse_commit_message(message):
    """
    Parse commit message for LP metadata.
    
    Expected format:
    LP #XXX: [Title]
    
    [Description]
    
    Agent: [Agent Name]
    Category: [Category1, Category2]
    Tags: [Tag1, Tag2]
    """
    
    # Check if message contains LP marker
    lp_pattern = r'^LP #(\d+):\s*(.+)$'
    match = re.match(lp_pattern, message, re.MULTILINE)
    
    if not match:
        return None
    
    lp_number = match.group(1)
    lp_title = match.group(2).strip()
    
    # Extract description (everything between title and metadata)
    lines = message.split('\n')
    description_lines = []
    metadata_started = False
    
    for i, line in enumerate(lines):
        if i == 0:  # Skip title line
            continue
        if line.startswith('Agent:') or line.startswith('Category:') or line.startswith('Tags:'):
            metadata_started = True
            break
        if line.strip():
            description_lines.append(line)
    
    description = '\n'.join(description_lines).strip()
    
    # Extract metadata
    agent_match = re.search(r'Agent:\s*(.+)$', message, re.MULTILINE)
    category_match = re.search(r'Category:\s*(.+)$', message, re.MULTILINE)
    tags_match = re.search(r'Tags:\s*(.+)$', message, re.MULTILINE)
    
    agent = agent_match.group(1).strip() if agent_match else 'Unknown'
    
    # Parse categories (comma-separated)
    categories = []
    if category_match:
        categories = [c.strip() for c in category_match.group(1).split(',')]
    
    # Parse tags (comma-separated)
    tags = []
    if tags_match:
        tags = [t.strip() for t in tags_match.group(1).split(',')]
    
    return {
        'lp_id': f'LP #{lp_number} - {lp_title}',
        'lp_number': lp_number,
        'title': lp_title,
        'description': description,
        'agent': agent,
        'categories': categories,
        'tags': tags
    }

def main():
    commit_message = os.getenv('COMMIT_MESSAGE', '')
    commit_sha = os.getenv('COMMIT_SHA', '')
    
    if not commit_message:
        print("No commit message provided")
        print("::set-output name=has_lp::false")
        return
    
    lp_data = parse_commit_message(commit_message)
    
    if not lp_data:
        print("No Learning Point found in commit message")
        print("::set-output name=has_lp::false")
        return
    
    # Add commit metadata
    lp_data['commit_sha'] = commit_sha
    lp_data['commit_url'] = f"https://github.com/{os.getenv('GITHUB_REPOSITORY', '')}/commit/{commit_sha}"
    
    print(f"✅ Found Learning Point: {lp_data['lp_id']}")
    print(f"   Agent: {lp_data['agent']}")
    print(f"   Categories: {', '.join(lp_data['categories'])}")
    print(f"   Tags: {', '.join(lp_data['tags'])}")
    
    # Output for next step
    print(f"::set-output name=has_lp::true")
    print(f"::set-output name=lp_id::{lp_data['lp_id']}")
    print(f"::set-output name=agent::{lp_data['agent']}")
    print(f"::set-output name=lp_data::{json.dumps(lp_data)}")

if __name__ == '__main__':
    main()

