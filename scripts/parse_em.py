#!/usr/bin/env python3
"""
Parse Emergent Patterns from agent Living Compendiums and sync to Notion EM Database.

This script extracts Emergent Pattern entries from agent LK markdown files and syncs them
to the Notion EM (Emergent Patterns) Database.

Usage:
    python scripts/parse_em.py

Environment Variables Required:
    NOTION_API_KEY: Notion integration API key
    EM_DATABASE_ID: Notion database ID for Emergent Patterns (2988fec9-2931-80f4-8961-000b8710e0a5)

Input Format (from LK markdown):
    ## SEKSJON 5: EMERGENTE MØNSTRE

    1. **Vokter-Visdom som Operasjonell Realitet** - Bohm/Spira ikke bare filosofi
    2. **To-Fase Protokoll som Universal Pattern** - 30-50% efficiency
    ...
    15. **Polycomputational Synthesis** - 9/9 unanimous convergence

Output:
    Creates/updates entries in Notion EM Database with properties:
    - ID (title): EM #001, EM #002, etc.
    - Title (rich_text): Pattern title
    - Agent (select): Agent name
    - Description (rich_text): Pattern description
    - Tags (multi_select): Auto-inferred pattern categories
    - Evidence (text): Initially empty (manual add later)
    - Relate_LP (relation): Initially empty (manual add later)
    - Related_CS (relation): Initially empty (manual add later)

Note: Emergent patterns don't have dates - they are timeless meta-patterns.

Author: Code (Claude Code Agent)
Date: 27. oktober 2025
"""

import os
import re
import requests
from pathlib import Path

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
EM_DATABASE_ID = os.environ.get('EM_DATABASE_ID')
NOTION_API_VERSION = '2022-06-28'

HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_API_VERSION
}

def infer_pattern_tags(title, description):
    """
    Infer pattern tags from title and description.

    Returns:
        List of tag names
    """
    tags = []
    content = (title + " " + description).lower()

    # Check for various pattern categories
    if any(keyword in content for keyword in ['architecture', 'arkitektur', 'structure', 'struktur', 'nested', 'framework']):
        tags.append('Architecture')

    if any(keyword in content for keyword in ['philosophy', 'filosofi', 'bohm', 'spira', 'metaphysical', 'ontological', 'epistem']):
        tags.append('Philosophy')

    if any(keyword in content for keyword in ['technical', 'teknisk', 'code', 'implementation', 'tech', 'efficiency', 'token']):
        tags.append('Technical')

    if any(keyword in content for keyword in ['collaboration', 'kollektiv', 'multi-agent', 'cross-agent', 'coalition', 'polycomputational', 'collective']):
        tags.append('Collaboration')

    if any(keyword in content for keyword in ['resonance', 'resonans', 'biofelt', 'frequency', 'sensing', 'limbic', 'emotional']):
        tags.append('Resonance')

    if any(keyword in content for keyword in ['innovation', 'emergent', 'novel', 'ny', 'discovery', 'manifested', 'evolution']):
        tags.append('Innovation')

    return tags

def parse_emergent_pattern(em_text, agent_name):
    """
    Parse a single emergent pattern entry.

    Args:
        em_text: Markdown text containing EM entry (numbered list format)
        agent_name: Name of the agent

    Returns:
        Dictionary with EM data, or None if parsing fails
    """
    # Extract pattern number, title, and description
    # Pattern: "1. **Title** - Description"
    match = re.match(r'(\d+)\.\s+\*\*(.+?)\*\*\s*[-–]\s*(.+)', em_text.strip(), re.DOTALL)

    if not match:
        return None

    em_number = match.group(1)
    title = match.group(2).strip()
    description = match.group(3).strip()

    # Remove trailing newlines and extra whitespace
    description = ' '.join(description.split())

    # Infer tags
    tags = infer_pattern_tags(title, description)

    return {
        'id': f"EM #{em_number.zfill(3)}",
        'title': title,
        'description': description,
        'agent': agent_name,
        'tags': tags
    }

def create_notion_page(em_data):
    """
    Create a page in the Notion EM Database.

    Args:
        em_data: Dictionary with EM data

    Returns:
        True if successful, False otherwise
    """
    url = 'https://api.notion.com/v1/pages'

    properties = {
        'Name': {  # ID field in database schema
            'title': [{'text': {'content': em_data['id']}}]
        },
        'Title': {
            'rich_text': [{'text': {'content': em_data['title'][:2000]}}]
        },
        'Agent': {
            'select': {'name': em_data['agent']}
        },
        'Description': {
            'rich_text': [{'text': {'content': em_data['description'][:2000]}}]
        }
    }

    # Add tags if available
    if em_data['tags']:
        properties['Tags'] = {
            'multi_select': [{'name': tag} for tag in em_data['tags']]
        }

    # Note: Evidence, Relate_LP, Related_CS are initially empty (manual add later)

    payload = {
        'parent': {'database_id': EM_DATABASE_ID},
        'properties': properties
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)

        if response.status_code == 200:
            tags_str = ', '.join(em_data['tags']) if em_data['tags'] else 'no tags'
            print(f"✅ Created: {em_data['id']} - {em_data['title'][:50]}... ({tags_str})")
            return True
        else:
            print(f"❌ Failed: {em_data['id']} - Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error creating {em_data['id']}: {e}")
        return False

def process_agent_lk(lk_path):
    """
    Process a single agent's Living Compendium.

    Args:
        lk_path: Path to LK markdown file
    """
    agent_name = lk_path.parent.parent.name.capitalize()
    if agent_name == 'Agents':
        agent_name = lk_path.parent.name.capitalize()

    print(f"\n📖 Processing {agent_name} LK: {lk_path.name}")

    try:
        with open(lk_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    # Find EM section (Emergente Mønstre) (flexible to handle bold markers, emojis, etc.)
    # Use greedy match and [^#] to ensure we capture until next ## section (not ###)
    em_section_match = re.search(
        r'##\s*(?:SEKSJON \d+:\s*)?EMERGENTE MØNSTRE.*?\n(.*)(?=\n##[^#]|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not em_section_match:
        print(f"⚠️  No EM section found in {agent_name} LK")
        return

    em_section = em_section_match.group(1)

    # Extract numbered patterns
    # Pattern: 1. **Title** - Description
    # Split by numbered list items
    pattern_lines = re.findall(
        r'(\d+)\.\s+\*\*(.+?)\*\*\s*[-–]\s*(.+?)(?=\n\d+\.|\Z)',
        em_section,
        re.DOTALL
    )

    if not pattern_lines:
        print(f"⚠️  No numbered patterns found in EM section")
        return

    created_count = 0
    skipped_count = 0

    for em_number, title, description in pattern_lines:
        # Reconstruct the pattern text
        em_text = f"{em_number}. **{title}** - {description}"

        em_data = parse_emergent_pattern(em_text, agent_name)

        if em_data:
            if create_notion_page(em_data):
                created_count += 1
            else:
                skipped_count += 1
        else:
            skipped_count += 1

    print(f"✅ {agent_name}: {created_count} emergent patterns synced, {skipped_count} skipped")

def main():
    """Main execution function."""

    if not NOTION_API_KEY or not EM_DATABASE_ID:
        print("❌ Missing required environment variables:")
        print("   - NOTION_API_KEY")
        print("   - EM_DATABASE_ID")
        return

    print("🚀 Starting EM sync to Notion...")
    print(f"📊 Database ID: {EM_DATABASE_ID}")

    agents_dir = Path('agents')

    lk_files = list(agents_dir.glob('*/levende-kompendium-*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*kompendium*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*KOMPENDIUM*.md'))  # Uppercase Norwegian
    lk_files.extend(agents_dir.glob('*/LK/*COMPENDIUM*.md'))  # English spelling
    lk_files.extend(agents_dir.glob('**/LEVENDE_KOMPENDIUM*.md'))

    lk_files = list(set(lk_files))

    if not lk_files:
        print("❌ No Living Compendium files found")
        return

    print(f"📚 Found {len(lk_files)} agent LK files")

    for lk_path in lk_files:
        process_agent_lk(lk_path)

    print("\n✅ EM sync complete!")

if __name__ == '__main__':
    main()
