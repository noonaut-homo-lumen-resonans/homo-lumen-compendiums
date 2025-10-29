#!/usr/bin/env python3
"""
Parse Emergent Patterns from SMK files and LK files, sync to Notion EM Database.

UPDATED: Now reads from BOTH:
- SMK files (SMK/*.md) - EMERGENT PATTERNS/INSIGHTS sections
- Living Compendiums (agents/*/LK/*.md) - EMERGENTE MØNSTRE sections

Usage:
    python scripts/parse_em_v2.py

Environment Variables Required:
    NOTION_API_KEY: Notion integration API key
    EM_DATABASE_ID: Notion database ID for Emergent Patterns

Author: Code (Claude Code Agent)
Date: 28. oktober 2025 (V2 - SMK + LK support)
"""

import os
import re
import requests
from pathlib import Path
import sys
import io

# Force UTF-8 encoding for stdout (Windows compatibility)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
if not NOTION_API_KEY:
    raise ValueError("NOTION_API_KEY environment variable not set")
EM_DATABASE_ID = os.environ.get('EM_DATABASE_ID', '2988fec9-2931-8050-9658-e93447b3b259')
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

    if any(keyword in content for keyword in ['intelligence', 'insight', 'learning', 'consciousness', 'awareness', 'emergence']):
        tags.append('Intelligence')

    if any(keyword in content for keyword in ['system', 'systemic', 'emergent', 'network', 'infrastructure', 'ecosystem']):
        tags.append('Systems')

    return tags

def find_existing_em(em_id):
    """
    Search for existing EM entry by ID (including archived pages).
    Returns page if found, None otherwise.
    """
    url = f'https://api.notion.com/v1/databases/{EM_DATABASE_ID}/query'

    # First, try to find active (non-archived) pages with title filter
    try:
        payload = {
            'filter': {
                'property': 'Pattern ID',
                'title': {
                    'equals': em_id
                }
            }
        }
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                return results[0]
    except Exception as e:
        print(f"  Error searching for {em_id}: {e}")

    # If no active page found, search ALL pages (including archived)
    try:
        all_pages = []
        has_more = True
        start_cursor = None

        while has_more:
            query_params = {}
            if start_cursor:
                query_params['start_cursor'] = start_cursor

            response = requests.post(url, headers=HEADERS, json=query_params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                all_pages.extend(data.get('results', []))
                has_more = data.get('has_more', False)
                start_cursor = data.get('next_cursor')
            else:
                break

        # Check all pages (including archived) for matching ID
        for page in all_pages:
            try:
                props = page.get('properties', {})
                name_prop = props.get('Pattern ID', {})
                if name_prop.get('title'):
                    page_id = name_prop['title'][0].get('text', {}).get('content', '')
                    if page_id == em_id:
                        return page
            except:
                continue
    except Exception as e:
        print(f"  Error in full page search: {e}")

    return None

def create_or_update_notion_page(em_data):
    """
    Create or update a page in the Notion EM Database.

    Args:
        em_data: Dictionary with EM data

    Returns:
        True if successful, False otherwise
    """
    properties = {
        'Pattern ID': {  # ID field in database schema (corrected from 'Name')
            'title': [{'text': {'content': em_data['id']}}]
        },
        'Pattern Name': {  # Corrected from 'Title'
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

    # TEMP: Skip duplicate check for faster sync
    existing_page = None  # find_existing_em(em_data['id'])

    try:
        if existing_page:
            # Update existing page
            page_id = existing_page['id']

            # If page is archived, unarchive it first
            if existing_page.get('archived'):
                print(f"  Unarchiving {em_data['id']}...")
                requests.patch(
                    f'https://api.notion.com/v1/pages/{page_id}',
                    headers=HEADERS,
                    json={'archived': False},
                    timeout=10
                )

            # Update the page
            response = requests.patch(
                f'https://api.notion.com/v1/pages/{page_id}',
                headers=HEADERS,
                json={'properties': properties},
                timeout=10
            )

            if response.status_code == 200:
                tags_str = ', '.join(em_data['tags']) if em_data['tags'] else 'no tags'
                print(f"✅ Updated: {em_data['id']} - {em_data['title'][:50]}... ({tags_str})")
                return True
            else:
                print(f"❌ Failed to update: {em_data['id']} - Status {response.status_code}")
                return False
        else:
            # Create new page (only if doesn't exist)
            payload = {
                'parent': {'database_id': EM_DATABASE_ID},
                'properties': properties
            }

            response = requests.post(
                'https://api.notion.com/v1/pages',
                headers=HEADERS,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                tags_str = ', '.join(em_data['tags']) if em_data['tags'] else 'no tags'
                print(f"✅ Created: {em_data['id']} - {em_data['title'][:50]}... ({tags_str})")
                return True
            else:
                print(f"❌ Failed to create: {em_data['id']} - Status {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Error syncing {em_data['id']}: {e}")
        return False

def process_smk_file(smk_path):
    """
    Process a single SMK file for Emergent Patterns.

    SMK files have sections like:
    ## 🔄 EMERGENT PATTERNS
    ## 🌟 EMERGENT INSIGHTS
    ## EMERGENT PATTERNS

    Format variations:
    - ### Pattern: Title (as subtitle)
    - 1. **Pattern** - Description (numbered list)
    """
    print(f"\n📄 Processing SMK: {smk_path.name}")

    try:
        with open(smk_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

    # Find EM section (various formats)
    em_patterns = [
        r'##\s*🔄\s*EMERGENT PATTERNS.*?\n(.*)(?=\n##[^#]|\Z)',
        r'##\s*🌟\s*EMERGENT INSIGHTS.*?\n(.*)(?=\n##[^#]|\Z)',
        r'##\s*EMERGENT PATTERNS.*?\n(.*)(?=\n##[^#]|\Z)',
        r'##\s*5\.\s*EMERGENT INSIGHTS.*?\n(.*)(?=\n##[^#]|\Z)',
    ]

    em_section = None
    for pattern in em_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            em_section = match.group(1)
            break

    if not em_section:
        print(f"⚠️  No EM section found")
        return 0

    created_count = 0

    # Try Pattern 1: ### Pattern: Title format
    subtitle_patterns = re.findall(
        r'###\s+(?:Pattern:?\s+)?(.+?)\n\n?(.+?)(?=\n###|\Z)',
        em_section,
        re.DOTALL
    )

    if subtitle_patterns:
        print(f"   Found {len(subtitle_patterns)} subtitle-format patterns")
        for i, (title, description) in enumerate(subtitle_patterns, 1):
            em_data = {
                'id': f"EM #{str(i).zfill(3)}",
                'title': title.strip()[:200],
                'description': ' '.join(description.strip().split())[:2000],
                'agent': 'SMK',
                'tags': infer_pattern_tags(title, description)
            }

            if create_or_update_notion_page(em_data):
                created_count += 1
    else:
        # Try Pattern 2: Numbered list format
        numbered_patterns = re.findall(
            r'(\d+)\.\s+\*\*(.+?)\*\*\s*[-–]\s*(.+?)(?=\n\d+\.|\Z)',
            em_section,
            re.DOTALL
        )

        if numbered_patterns:
            print(f"   Found {len(numbered_patterns)} numbered-list patterns")
            for em_number, title, description in numbered_patterns:
                em_data = {
                    'id': f"EM #{em_number.zfill(3)}",
                    'title': title.strip()[:200],
                    'description': ' '.join(description.strip().split())[:2000],
                    'agent': 'SMK',
                    'tags': infer_pattern_tags(title, description)
                }

                if create_or_update_notion_page(em_data):
                    created_count += 1

    return created_count

def process_lk_file(lk_path):
    """
    Process a single LK file for Emergent Patterns.

    Format: ## EMERGENTE MØNSTRE
    1. **Pattern** - Description
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
        return 0

    # Find EM section
    em_section_match = re.search(
        r'##\s*(?:SEKSJON \d+:\s*)?EMERGENTE MØNSTRE.*?\n(.*)(?=\n##[^#]|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not em_section_match:
        print(f"⚠️  No EM section found")
        return 0

    em_section = em_section_match.group(1)

    # Extract numbered patterns
    pattern_lines = re.findall(
        r'(\d+)\.\s+\*\*(.+?)\*\*\s*[-–]\s*(.+?)(?=\n\d+\.|\Z)',
        em_section,
        re.DOTALL
    )

    if not pattern_lines:
        print(f"⚠️  No numbered patterns found")
        return 0

    created_count = 0

    for em_number, title, description in pattern_lines:
        em_data = {
            'id': f"EM #{em_number.zfill(3)}",
            'title': title.strip()[:200],
            'description': ' '.join(description.strip().split())[:2000],
            'agent': agent_name,
            'tags': infer_pattern_tags(title, description)
        }

        if create_or_update_notion_page(em_data):
            created_count += 1

    return created_count

def main():
    """Main execution function."""

    if not NOTION_API_KEY or not EM_DATABASE_ID:
        print("❌ Missing required configuration")
        return

    print("🚀 Starting EM sync to Notion (SMK + LK)...")
    print(f"📊 Database ID: {EM_DATABASE_ID}")

    total_created = 0

    # Process SMK files
    print("\n" + "="*70)
    print("PROCESSING SMK FILES")
    print("="*70)

    smk_dir = Path('SMK')
    smk_files = list(smk_dir.glob('*.md'))

    print(f"📚 Found {len(smk_files)} SMK files")

    for smk_path in smk_files:
        count = process_smk_file(smk_path)
        total_created += count

    # Process LK files
    print("\n" + "="*70)
    print("PROCESSING LK FILES")
    print("="*70)

    agents_dir = Path('agents')
    lk_files = list(agents_dir.glob('*/levende-kompendium-*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*kompendium*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*KOMPENDIUM*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*COMPENDIUM*.md'))
    lk_files.extend(agents_dir.glob('**/LEVENDE_KOMPENDIUM*.md'))
    lk_files = list(set(lk_files))

    print(f"📚 Found {len(lk_files)} LK files")

    for lk_path in lk_files:
        count = process_lk_file(lk_path)
        total_created += count

    print("\n" + "="*70)
    print(f"✅ EM sync complete! {total_created} patterns synced")
    print("="*70)

if __name__ == '__main__':
    main()
