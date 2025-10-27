#!/usr/bin/env python3
"""
Parse Case Studies from agent Living Compendiums and sync to Notion CS Database.

This script extracts Case Study entries from agent LK markdown files and syncs them
to the Notion CS (Case Studies) Database.

Usage:
    python scripts/parse_cs.py

Environment Variables Required:
    NOTION_API_KEY: Notion integration API key
    CS_DATABASE_ID: Notion database ID for Case Studies (2988fec9-2931-803a-8703-000bb973304e)

Input Format (from LK markdown):
    **CS #009 - Cross-Agent Intelligence Infrastructure Godkjent**
    - **Dato:** 26. oktober 2025
    - **Situasjon:** Efter LAG 4 complete, hvordan capture CS/SL/KD?
    - **Tilnærming:** Orion presenterte 3 alternativer, Osvald intuited 3 databases
    - **Resultat:** 3 nye Notion databases godkjent. Coalition-wide patterns nå synlige.

Output:
    Creates/updates entries in Notion CS Database with properties:
    - Name (title): CS #009
    - Title (rich_text): Entry title
    - Date (date): Parsed Norwegian date -> ISO format
    - Agent (select): Agent name from file location
    - Situation (rich_text): Situasjon field
    - Approach (rich_text): Tilnærming field
    - Result (rich_text): Resultat field

Author: Code (Claude Code Agent)
Date: 27. oktober 2025
"""

import os
import sys
import io
import re
import requests
from pathlib import Path

# Force UTF-8 encoding for stdout (Windows compatibility)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
CS_DATABASE_ID = os.environ.get('CS_DATABASE_ID')
NOTION_API_VERSION = '2022-06-28'

# Notion API headers
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
    """
    Parse Norwegian date format to ISO format.

    Example: "26. oktober 2025" -> "2025-10-26"
    """
    match = re.search(r'(\d+)\.\s*(\w+)\s*(\d+)', date_str)
    if not match:
        return None

    day = match.group(1).zfill(2)
    month_name = match.group(2).lower()
    year = match.group(3)

    month = MONTH_MAP.get(month_name, '01')

    return f"{year}-{month}-{day}"

def parse_case_study(cs_text, agent_name):
    """
    Parse a single case study entry from markdown text.

    Args:
        cs_text: Markdown text containing CS entry
        agent_name: Name of the agent (from file location)

    Returns:
        Dictionary with CS data, or None if parsing fails
    """
    # Extract CS ID and Title
    # Pattern: **CS #009 - Title**
    id_match = re.search(r'CS\s+#(\d+)\s*[-–]\s*(.+?)(?:\*\*|\n)', cs_text, re.IGNORECASE)
    if not id_match:
        return None

    cs_id = id_match.group(1)
    title = id_match.group(2).strip().strip('*').strip()

    # Extract Date
    date_match = re.search(r'\*\*Dato:\*\*\s*(.+?)(?:\n|$)', cs_text)
    date = None
    if date_match:
        date = parse_norwegian_date(date_match.group(1))

    # Extract Situasjon
    situation_match = re.search(
        r'\*\*Situasjon:\*\*\s*(.+?)(?=\n\s*\*\*|\n\n|$)',
        cs_text,
        re.DOTALL
    )
    situation = situation_match.group(1).strip() if situation_match else ""

    # Extract Tilnærming/Approach
    approach_match = re.search(
        r'\*\*Tilnærming:\*\*\s*(.+?)(?=\n\s*\*\*|\n\n|$)',
        cs_text,
        re.DOTALL
    )
    approach = approach_match.group(1).strip() if approach_match else ""

    # Extract Resultat
    result_match = re.search(
        r'\*\*Resultat:\*\*\s*(.+?)(?=\n\s*\*\*|\n\n|$)',
        cs_text,
        re.DOTALL
    )
    result = result_match.group(1).strip() if result_match else ""

    return {
        'id': f"CS #{cs_id.zfill(3)}",
        'title': title,
        'date': date,
        'agent': agent_name,
        'situation': situation,
        'approach': approach,
        'result': result
    }

def create_notion_page(cs_data):
    """
    Create a page in the Notion CS Database.

    Args:
        cs_data: Dictionary with CS data

    Returns:
        True if successful, False otherwise
    """
    url = 'https://api.notion.com/v1/pages'

    # Build properties
    properties = {
        'Name': {
            'title': [{'text': {'content': cs_data['id']}}]
        },
        'Title': {
            'rich_text': [{'text': {'content': cs_data['title'][:2000]}}]  # Notion limit
        },
        'Agent': {
            'select': {'name': cs_data['agent']}
        },
        'Situation': {
            'rich_text': [{'text': {'content': cs_data['situation'][:2000]}}]
        },
        'Approach': {
            'rich_text': [{'text': {'content': cs_data['approach'][:2000]}}]
        },
        'Result': {
            'rich_text': [{'text': {'content': cs_data['result'][:2000]}}]
        }
    }

    # Add date if available
    if cs_data['date']:
        properties['Date'] = {
            'date': {'start': cs_data['date']}
        }

    payload = {
        'parent': {'database_id': CS_DATABASE_ID},
        'properties': properties
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)

        if response.status_code == 200:
            print(f"✅ Created: {cs_data['id']} - {cs_data['title']}")
            return True
        else:
            print(f"❌ Failed: {cs_data['id']} - Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error creating {cs_data['id']}: {e}")
        return False

def process_agent_lk(lk_path):
    """
    Process a single agent's Living Compendium.

    Args:
        lk_path: Path to LK markdown file
    """
    # Extract agent name from path
    # Example: agents/orion/levende-kompendium-v3_7.md -> Orion
    agent_name = lk_path.parent.parent.name.capitalize()
    if agent_name == 'Agents':
        # If parent.parent is 'agents', try parent
        agent_name = lk_path.parent.name.capitalize()

    print(f"\n📖 Processing {agent_name} LK: {lk_path.name}")

    try:
        with open(lk_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return

    # Find CS section (flexible to handle bold markers, emojis, etc.)
    # Use greedy match and [^#] to ensure we capture until next ## section (not ###)
    cs_section_match = re.search(
        r'##\s*[\*\s]*(?:SEKSJON \d+:\s*)?CASE[- ]STUD(?:IES|IER)[\*\s]*\n(.*)(?=\n##[^#]|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not cs_section_match:
        print(f"⚠️  No CS section found in {agent_name} LK")
        return

    cs_section = cs_section_match.group(1)

    # Split into individual case studies
    # Split on ###**CS # or **CS # pattern (handles heading markers)
    case_studies = re.split(r'\n#{0,6}\s*\*\*CS\s+#', cs_section, flags=re.IGNORECASE)

    created_count = 0
    skipped_count = 0

    for cs_text in case_studies:
        if not cs_text.strip():
            continue

        # Re-add the CS # prefix that was removed by split
        if not re.match(r'CS\s+#', cs_text, re.IGNORECASE):
            cs_text = 'CS #' + cs_text

        cs_data = parse_case_study(cs_text, agent_name)

        if cs_data:
            if create_notion_page(cs_data):
                created_count += 1
            else:
                skipped_count += 1
        else:
            skipped_count += 1

    print(f"✅ {agent_name}: {created_count} case studies synced, {skipped_count} skipped")

def main():
    """Main execution function."""

    if not NOTION_API_KEY or not CS_DATABASE_ID:
        print("❌ Missing required environment variables:")
        print("   - NOTION_API_KEY")
        print("   - CS_DATABASE_ID")
        return

    print("🚀 Starting CS sync to Notion...")
    print(f"📊 Database ID: {CS_DATABASE_ID}")

    # Find all agent LK files
    agents_dir = Path('agents')

    # Support multiple naming patterns (case-insensitive, Norwegian + English)
    lk_files = list(agents_dir.glob('*/levende-kompendium-*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*kompendium*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*KOMPENDIUM*.md'))  # Uppercase Norwegian
    lk_files.extend(agents_dir.glob('*/LK/*COMPENDIUM*.md'))  # English spelling
    lk_files.extend(agents_dir.glob('**/LEVENDE_KOMPENDIUM*.md'))

    # Remove duplicates
    lk_files = list(set(lk_files))

    if not lk_files:
        print("❌ No Living Compendium files found in agents/")
        return

    print(f"📚 Found {len(lk_files)} agent LK files")

    for lk_path in lk_files:
        process_agent_lk(lk_path)

    print("\n✅ CS sync complete!")

if __name__ == '__main__':
    main()
