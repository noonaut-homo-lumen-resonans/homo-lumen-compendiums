#!/usr/bin/env python3
"""
Parse Learning Points (LP) from SMK files and sync to Notion SLL Database.

SLL = Shared Learning Library
Source: SMK files (SMK/*.md) - LÆRINGSPUNKTER sections

Usage:
    python scripts/parse_lp.py

Environment Variables Required:
    NOTION_API_KEY: Notion integration API key
    SLL_DATABASE_ID: Notion database ID for Shared Learning Library

LP Format in SMK files:
    ## 📚 LEARNING POINTS
    ### LP #042: Title
    **Kategori:** Development
    **Innsikt:** Description of the learning point

    OR

    ## 🎓 LÆRINGSPUNKTER
    **LP #032-1: Title**
    Description of the learning

Author: Code (Claude Code Agent)
Date: 28. oktober 2025
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
NOTION_API_KEY = os.environ.get('NOTION_API_KEY', '***REMOVED***')
SLL_DATABASE_ID = os.environ.get('SLL_DATABASE_ID', '84da6cbd09d640fb868e41444b941991')
NOTION_API_VERSION = '2022-06-28'

HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_API_VERSION
}

# Norwegian month to number mapping
MONTH_MAP = {
    'januar': '01', 'februar': '02', 'mars': '03', 'april': '04',
    'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
    'september': '09', 'oktober': '10', 'november': '11', 'desember': '12'
}

def parse_norwegian_date(date_str):
    """Parse Norwegian date format to ISO format."""
    match = re.search(r'(\d+)\.\s*(\w+)\s*(\d+)', date_str)
    if not match:
        return None

    day = match.group(1).zfill(2)
    month_name = match.group(2).lower()
    year = match.group(3)

    month = MONTH_MAP.get(month_name, '01')

    return f"{year}-{month}-{day}"

def infer_lp_category(title, content):
    """
    Infer LP category from title and content.

    Returns:
        Category string
    """
    combined = (title + " " + content).lower()

    if any(keyword in combined for keyword in ['development', 'code', 'implementation', 'technical', 'teknisk']):
        return 'Development'
    elif any(keyword in combined for keyword in ['architecture', 'arkitektur', 'design', 'structure']):
        return 'Architecture'
    elif any(keyword in combined for keyword in ['philosophy', 'filosofi', 'bohm', 'spira', 'ontological']):
        return 'Philosophy'
    elif any(keyword in combined for keyword in ['collaboration', 'coordination', 'multi-agent', 'coalition']):
        return 'Collaboration'
    elif any(keyword in combined for keyword in ['infrastructure', 'system', 'deployment', 'infra']):
        return 'Infrastructure'
    elif any(keyword in combined for keyword in ['learning', 'insight', 'discovery', 'pattern']):
        return 'Learning'
    else:
        return 'General'

def find_existing_lp(lp_id):
    """
    Search for existing LP entry by LP_ID (including archived pages).
    Returns page if found, None otherwise.
    """
    url = f'https://api.notion.com/v1/databases/{SLL_DATABASE_ID}/query'

    # First, try to find active (non-archived) pages with title filter
    try:
        payload = {
            'filter': {
                'property': 'LP_ID',
                'title': {
                    'equals': lp_id
                }
            }
        }
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                return results[0]
    except Exception as e:
        print(f"  Error searching for {lp_id}: {e}")

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

        # Check all pages (including archived) for matching LP_ID
        for page in all_pages:
            try:
                props = page.get('properties', {})
                lp_id_prop = props.get('LP_ID', {})
                if lp_id_prop.get('title'):
                    page_lp_id = lp_id_prop['title'][0].get('text', {}).get('content', '')
                    if page_lp_id == lp_id:
                        return page
            except:
                continue
    except Exception as e:
        print(f"  Error in full page search: {e}")

    return None

def create_or_update_notion_page(lp_data):
    """
    Create or update a page in the Notion SLL Database.

    Args:
        lp_data: Dictionary with LP data

    Returns:
        True if successful, False otherwise
    """
    properties = {
        'LP_ID': {
            'title': [{'text': {'content': lp_data['id']}}]
        },
        'Content': {
            'rich_text': [{'text': {'content': lp_data['content'][:2000]}}]
        },
        'Category': {
            'select': {'name': lp_data['category']}
        },
        'Source': {
            'url': lp_data.get('source', '')
        }
    }

    # Add date if available
    if lp_data.get('date'):
        properties['Date'] = {
            'date': {'start': lp_data['date']}
        }

    # Add tags if available
    if lp_data.get('tags'):
        properties['Tags'] = {
            'multi_select': [{'name': tag} for tag in lp_data['tags']]
        }

    # Search for existing page
    existing_page = find_existing_lp(lp_data['id'])

    try:
        if existing_page:
            # Update existing page
            page_id = existing_page['id']

            # If page is archived, unarchive it first
            if existing_page.get('archived'):
                print(f"  Unarchiving {lp_data['id']}...")
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
                print(f"✅ Updated: {lp_data['id']} - {lp_data['content'][:50]}...")
                return True
            else:
                print(f"❌ Failed to update: {lp_data['id']} - Status {response.status_code}")
                return False
        else:
            # Create new page (only if doesn't exist)
            payload = {
                'parent': {'database_id': SLL_DATABASE_ID},
                'properties': properties
            }

            response = requests.post(
                'https://api.notion.com/v1/pages',
                headers=HEADERS,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                print(f"✅ Created: {lp_data['id']} - {lp_data['content'][:50]}...")
                return True
            else:
                print(f"❌ Failed to create: {lp_data['id']} - Status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ Error syncing {lp_data['id']}: {e}")
        return False

def process_smk_file(smk_path):
    """
    Process a single SMK file for Learning Points.

    SMK files have sections like:
    ## 📚 LEARNING POINTS
    ## 🎓 LÆRINGSPUNKTER
    ## LÆRINGSINNSIKTER

    Format variations:
    - ### LP #042: Title (subtitle format)
    - **LP #032-1: Title** (bold format)
    """
    print(f"\n📄 Processing SMK: {smk_path.name}")

    try:
        with open(smk_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return 0

    # Extract SMK date if available (from filename or content)
    smk_date = None
    date_match = re.search(r'(\d+)\.\s*(\w+)\s*(\d+)', content[:500])
    if date_match:
        smk_date = parse_norwegian_date(date_match.group(0))

    # Find LP section (various formats)
    lp_patterns = [
        r'##\s*📚\s*LEARNING POINTS.*?\n(.*)(?=\n##[^#]|\Z)',
        r'##\s*🎓\s*LÆRINGSPUNKTER.*?\n(.*)(?=\n##[^#]|\Z)',
        r'##\s*📖\s*Learning Points Generert.*?\n(.*)(?=\n##[^#]|\Z)',
        r'##\s*🔍\s*NØKKEL-LÆRINGSPUNKTER.*?\n(.*)(?=\n##[^#]|\Z)',
        r'##\s*3\.\s*LEARNING PATTERNS.*?\n(.*)(?=\n##[^#]|\Z)',
        r'##\s*LÆRINGSINNSIKTER.*?\n(.*)(?=\n##[^#]|\Z)',
    ]

    lp_section = None
    for pattern in lp_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            lp_section = match.group(1)
            break

    if not lp_section:
        print(f"⚠️  No LP section found")
        return 0

    created_count = 0

    # Try Pattern 1: ### LP #042: Title (subtitle format)
    subtitle_lps = re.findall(
        r'###\s+(?:LP|Learning Point)\s*[#\s]*(\d+[-\d]*):?\s*(.+?)\n\n?(.+?)(?=\n###|\Z)',
        lp_section,
        re.DOTALL | re.IGNORECASE
    )

    if subtitle_lps:
        print(f"   Found {len(subtitle_lps)} subtitle-format LPs")
        for lp_number, title, description in subtitle_lps:
            content_text = f"{title.strip()} - {' '.join(description.strip().split())}"

            lp_data = {
                'id': f"LP #{lp_number}",
                'content': content_text[:2000],
                'category': infer_lp_category(title, description),
                'date': smk_date,
                'source': f"SMK/{smk_path.name}",
                'tags': []
            }

            if create_or_update_notion_page(lp_data):
                created_count += 1

    # Try Pattern 2: **LP #042: Title** (bold format)
    bold_lps = re.findall(
        r'\*\*(?:LP|Learning Point)\s*[#\s]*(\d+[-\d]*):?\s*(.+?)\*\*\s*\n(.+?)(?=\n\*\*|\n##|\Z)',
        lp_section,
        re.DOTALL | re.IGNORECASE
    )

    if bold_lps:
        print(f"   Found {len(bold_lps)} bold-format LPs")
        for lp_number, title, description in bold_lps:
            content_text = f"{title.strip()} - {' '.join(description.strip().split())}"

            lp_data = {
                'id': f"LP #{lp_number}",
                'content': content_text[:2000],
                'category': infer_lp_category(title, description),
                'date': smk_date,
                'source': f"SMK/{smk_path.name}",
                'tags': []
            }

            if create_or_update_notion_page(lp_data):
                created_count += 1

    return created_count

def main():
    """Main execution function."""

    if not NOTION_API_KEY or not SLL_DATABASE_ID:
        print("❌ Missing required configuration")
        return

    print("🚀 Starting LP sync to SLL Database...")
    print(f"📊 Database ID: {SLL_DATABASE_ID}")

    total_created = 0

    # Process SMK files
    print("\n" + "="*70)
    print("PROCESSING SMK FILES FOR LEARNING POINTS")
    print("="*70)

    smk_dir = Path('SMK')
    smk_files = list(smk_dir.glob('*.md'))

    print(f"📚 Found {len(smk_files)} SMK files")

    for smk_path in smk_files:
        count = process_smk_file(smk_path)
        total_created += count

    print("\n" + "="*70)
    print(f"✅ LP sync complete! {total_created} learning points synced to SLL")
    print("="*70)

if __name__ == '__main__':
    main()
