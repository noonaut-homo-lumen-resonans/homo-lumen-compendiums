#!/usr/bin/env python3
"""
Parse SMK files with YAML frontmatter and extract metadata for Notion sync.

Agent: Claude Code
Date: 26. oktober 2025
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import date, datetime

def parse_yaml_frontmatter(content):
    """
    Extract YAML frontmatter from markdown content.

    Expected format:
    ---
    smk_number: 19
    title: "SMK Title"
    date: 2025-10-20
    agent: Orion
    tags: [tag1, tag2]
    status: COMPLETE
    ---
    """
    # Check if content starts with YAML frontmatter
    if not content.strip().startswith('---'):
        return None

    # Extract YAML block
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    yaml_content = parts[1].strip()

    try:
        metadata = yaml.safe_load(yaml_content)
        return metadata
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None

def parse_smk_file(filepath):
    """Parse a single SMK file and extract metadata."""
    print(f"Parsing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = parse_yaml_frontmatter(content)

    if not metadata:
        print(f"  [WARN] No YAML frontmatter found")
        return None

    # Extract title from content if not in YAML
    if 'title' not in metadata or not metadata['title']:
        # Try to find first # heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        else:
            metadata['title'] = filepath.stem

    # Convert date objects to strings for JSON serialization
    if 'date' in metadata and isinstance(metadata['date'], (date, datetime)):
        metadata['date'] = metadata['date'].isoformat()

    # Add file metadata
    metadata['filename'] = filepath.name
    metadata['filepath'] = str(filepath)

    # Generate GitHub URL
    repo = os.getenv('GITHUB_REPOSITORY', 'noonaut-homo-lumen-resonans/homo-lumen-compendiums')
    branch = 'main'
    metadata['github_url'] = f"https://github.com/{repo}/blob/{branch}/SMK/{filepath.name}"

    print(f"  [OK] Parsed: SMK #{metadata.get('smk_number', '?')} - {metadata.get('title', 'Untitled')}")

    return metadata

def main():
    """Main parsing process."""
    print("=" * 60)
    print("SMK File Parser for Notion Sync")
    print("Agent: Claude Code")
    print("=" * 60)

    # Find all SMK files
    smk_dir = Path('SMK')
    if not smk_dir.exists():
        print("SMK directory not found")
        print("::set-output name=has_smks::false")
        return

    smk_files = sorted(smk_dir.glob('SMK*.md'))

    if not smk_files:
        print("No SMK files found")
        print("::set-output name=has_smks::false")
        return

    print(f"\nFound {len(smk_files)} SMK files")

    # Parse all files
    smk_data = []
    for filepath in smk_files:
        metadata = parse_smk_file(filepath)
        if metadata:
            smk_data.append(metadata)

    if not smk_data:
        print("\nNo valid SMK files to sync")
        print("::set-output name=has_smks::false")
        return

    # Output for next step
    print(f"\n[OK] Parsed {len(smk_data)} SMK files successfully")
    print("::set-output name=has_smks::true")
    print(f"::set-output name=smk_count::{len(smk_data)}")
    print(f"::set-output name=smk_data::{json.dumps(smk_data)}")

if __name__ == '__main__':
    main()
