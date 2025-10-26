#!/usr/bin/env python3
"""
Parse LK (Levende Kompendium) files with YAML frontmatter and extract metadata for Notion sync.

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
    agent: Orion
    version: V3.7
    date: 2025-10-20
    status: ACTIVE
    tags: [meta-coordinator, learning]
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

def extract_agent_from_filename(filename):
    """Extract agent name from LK filename."""
    # Pattern: <Agent>_LK_V<version>.md
    match = re.match(r'([A-Z][a-z]+)_LK_V([\d\.]+)', filename)
    if match:
        return match.group(1), match.group(2)
    return None, None

def parse_lk_file(filepath):
    """Parse a single LK file and extract metadata."""
    print(f"Parsing: {filepath.name}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = parse_yaml_frontmatter(content)

    # If no YAML frontmatter, try to extract from filename
    if not metadata:
        metadata = {}
        agent, version = extract_agent_from_filename(filepath.name)
        if agent:
            metadata['agent'] = agent
            metadata['version'] = version
            print(f"  ℹ️  No YAML frontmatter, extracted from filename")
        else:
            print(f"  ⚠️  No YAML frontmatter and couldn't parse filename")
            return None

    # Extract title from content if not in YAML
    if 'title' not in metadata or not metadata['title']:
        # Try to find first # heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        else:
            # Default title from agent name and version
            agent = metadata.get('agent', 'Unknown')
            version = metadata.get('version', 'Unknown')
            metadata['title'] = f"{agent} Levende Kompendium {version}"

    # Convert date objects to strings for JSON serialization
    if 'date' in metadata and isinstance(metadata['date'], (date, datetime)):
        metadata['date'] = metadata['date'].isoformat()

    # Add file metadata
    metadata['filename'] = filepath.name
    metadata['filepath'] = str(filepath)

    # Generate GitHub URL
    repo = os.getenv('GITHUB_REPOSITORY', 'noonaut-homo-lumen-resonans/homo-lumen-compendiums')
    branch = 'main'
    relative_path = filepath.relative_to(Path.cwd())
    metadata['github_url'] = f"https://github.com/{repo}/blob/{branch}/{relative_path}"

    print(f"  ✅ Parsed: {metadata.get('agent', '?')} LK {metadata.get('version', '?')} - {metadata.get('title', 'Untitled')}")

    return metadata

def main():
    """Main parsing process."""
    print("=" * 60)
    print("LK File Parser for Notion Sync")
    print("Agent: Claude Code")
    print("=" * 60)

    # Find all LK files in root directory
    root_dir = Path('.')
    lk_files = list(root_dir.glob('*_LK_*.md'))

    # Also check agents/ subdirectory
    agents_dir = Path('agents')
    if agents_dir.exists():
        lk_files.extend(agents_dir.glob('**/*kompendium*.md'))
        lk_files.extend(agents_dir.glob('**/*_LK_*.md'))

    # Sort by name
    lk_files = sorted(lk_files)

    if not lk_files:
        print("No LK files found")
        print("::set-output name=has_lks::false")
        return

    print(f"\nFound {len(lk_files)} LK files")

    # Parse all files
    lk_data = []
    for filepath in lk_files:
        metadata = parse_lk_file(filepath)
        if metadata:
            lk_data.append(metadata)

    if not lk_data:
        print("\nNo valid LK files to sync")
        print("::set-output name=has_lks::false")
        return

    # Output for next step
    print(f"\n✅ Parsed {len(lk_data)} LK files successfully")
    print("::set-output name=has_lks::true")
    print(f"::set-output name=lk_count::{len(lk_data)}")
    print(f"::set-output name=lk_data::{json.dumps(lk_data)}")

if __name__ == '__main__':
    main()
