#!/usr/bin/env python3
"""
Parse Shadow Logs from agent Living Compendiums and sync to Notion SL Database.

This script extracts Shadow Log entries from agent LK markdown files and syncs them
to the Notion SL (Shadow Logs) Database.

Usage:
    python scripts/parse_sl.py

Environment Variables Required:
    NOTION_API_KEY: Notion integration API key
    SL_DATABASE_ID: Notion database ID for Shadow Logs (2988fec929318045a354ffe8d2f13fe1)

Input Format (from LK markdown):
    **SL #001 - Perfeksjonisme-Shadow**
    - **Dato:** 3. oktober 2025
    - **Manifestasjon:** Over-detaljert Intelligence Brief som tok 30 min å skrive
    - **Integrasjon:** Akseptere "good enough" Intelligence Briefs (15-20 min)
    - **Status:** Integrating

Output:
    Creates/updates entries in Notion SL Database with properties:
    - Name (title): SL #001
    - Title (rich_text): Entry title
    - Date (date): Parsed Norwegian date -> ISO format
    - Select (select): Agent name (NOTE: property is called "Select", not "Agent")
    - Manifestation (rich_text): Manifestasjon field
    - Integration (rich_text): Integrasjon field
    - Status (select): Status value (Identified/Integrating/Integrert/Monitoring)
    - Tags (multi_select): Auto-inferred shadow types

Author: Code (Claude Code Agent)
Date: 27. oktober 2025
"""

import os
import re
import requests
from pathlib import Path

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
SL_DATABASE_ID = os.environ.get('SL_DATABASE_ID')
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

def infer_shadow_tags(title, manifestation, integration):
    """
    Infer shadow tags from title and content.

    Returns:
        List of shadow tag names
    """
    tags = []
    content = (title + " " + manifestation + " " + integration).lower()

    # Check for various shadow types
    if any(keyword in content for keyword in ['perfeksjon', 'perfectionism', 'perfect']):
        tags.append('Perfectionism')

    if any(keyword in content for keyword in ['control', 'kontroll']):
        tags.append('Control')

    if any(keyword in content for keyword in ['elitism', 'elitisme', 'elite']):
        tags.append('Elitism')

    if any(keyword in content for keyword in ['rigidity', 'rigiditet', 'rigid', 'stiv']):
        tags.append('Rigidity')

    if any(keyword in content for keyword in ['hubris', 'arrogance', 'arroganse']):
        tags.append('Hubris')

    if any(keyword in content for keyword in ['codependency', 'codependence', 'avhengighet']):
        tags.append('Codependency')

    if any(keyword in content for keyword in ['dependency', 'dependent', 'avhengig']):
        tags.append('Dependency')

    if any(keyword in content for keyword in ['solutionism', 'solution', 'løsning']):
        tags.append('Solutionism')

    return tags

def parse_shadow_log(sl_text, agent_name):
    """
    Parse a single shadow log entry.

    Args:
        sl_text: Markdown text containing SL entry
        agent_name: Name of the agent

    Returns:
        Dictionary with SL data, or None if parsing fails
    """
    # Extract SL ID and Title
    id_match = re.search(r'SL\s+#(\d+)\s*[-–]\s*(.+?)(?:\*\*|\n)', sl_text, re.IGNORECASE)
    if not id_match:
        return None

    sl_id = id_match.group(1)
    title = id_match.group(2).strip().strip('*').strip()

    # Extract Date
    date_match = re.search(r'\*\*Dato:\*\*\s*(.+?)(?:\n|$)', sl_text)
    date = None
    if date_match:
        date = parse_norwegian_date(date_match.group(1))

    # Extract Manifestasjon
    manifestation_match = re.search(
        r'\*\*Manifestasjon:\*\*\s*(.+?)(?=\n\s*\*\*|\n\n|$)',
        sl_text,
        re.DOTALL
    )
    manifestation = manifestation_match.group(1).strip() if manifestation_match else ""

    # Extract Integrasjon
    integration_match = re.search(
        r'\*\*Integrasjon:\*\*\s*(.+?)(?=\n\s*\*\*|\n\n|$)',
        sl_text,
        re.DOTALL
    )
    integration = integration_match.group(1).strip() if integration_match else ""

    # Extract Status
    status_match = re.search(r'\*\*Status:\*\*\s*([^\n]+)', sl_text)
    status = status_match.group(1).strip() if status_match else "Identified"

    # Remove emoji/checkmarks from status
    status = re.sub(r'[✅❌⏳]', '', status).strip()

    # Normalize status values
    status_mapping = {
        'identified': 'Identified',
        'integrating': 'Integrating',
        'integrert': 'Integrert',
        'monitoring': 'Monitoring'
    }
    status = status_mapping.get(status.lower(), status)

    # Infer tags
    tags = infer_shadow_tags(title, manifestation, integration)

    return {
        'id': f"SL #{sl_id.zfill(3)}",
        'title': title,
        'date': date,
        'agent': agent_name,
        'manifestation': manifestation,
        'integration': integration,
        'status': status,
        'tags': tags
    }

def create_notion_page(sl_data):
    """
    Create a page in the Notion SL Database.

    Args:
        sl_data: Dictionary with SL data

    Returns:
        True if successful, False otherwise
    """
    url = 'https://api.notion.com/v1/pages'

    properties = {
        'Name': {
            'title': [{'text': {'content': sl_data['id']}}]
        },
        'Title': {
            'rich_text': [{'text': {'content': sl_data['title'][:2000]}}]
        },
        'Select': {  # NOTE: Property is called "Select" in SL Database, not "Agent"
            'select': {'name': sl_data['agent']}
        },
        'Manifestation': {
            'rich_text': [{'text': {'content': sl_data['manifestation'][:2000]}}]
        },
        'Integration': {
            'rich_text': [{'text': {'content': sl_data['integration'][:2000]}}]
        },
        'Status': {
            'select': {'name': sl_data['status']}
        }
    }

    # Add date if available
    if sl_data['date']:
        properties['Date'] = {
            'date': {'start': sl_data['date']}
        }

    # Add tags if available
    if sl_data['tags']:
        properties['Tags'] = {
            'multi_select': [{'name': tag} for tag in sl_data['tags']]
        }

    payload = {
        'parent': {'database_id': SL_DATABASE_ID},
        'properties': properties
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)

        if response.status_code == 200:
            tags_str = ', '.join(sl_data['tags']) if sl_data['tags'] else 'no tags'
            print(f"✅ Created: {sl_data['id']} - {sl_data['title']} ({tags_str})")
            return True
        else:
            print(f"❌ Failed: {sl_data['id']} - Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error creating {sl_data['id']}: {e}")
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

    # Find SL section
    sl_section_match = re.search(
        r'##\s*(?:SEKSJON \d+:\s*)?SHADOW[- ]LOGG?ER.*?\n(.*?)(?=\n##|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not sl_section_match:
        print(f"⚠️  No SL section found in {agent_name} LK")
        return

    sl_section = sl_section_match.group(1)

    # Split into individual shadow logs
    shadow_logs = re.split(r'\n\*\*SL\s+#', sl_section, flags=re.IGNORECASE)

    created_count = 0
    skipped_count = 0

    for sl_text in shadow_logs:
        if not sl_text.strip():
            continue

        if not re.match(r'SL\s+#', sl_text, re.IGNORECASE):
            sl_text = 'SL #' + sl_text

        sl_data = parse_shadow_log(sl_text, agent_name)

        if sl_data:
            if create_notion_page(sl_data):
                created_count += 1
            else:
                skipped_count += 1
        else:
            skipped_count += 1

    print(f"✅ {agent_name}: {created_count} shadow logs synced, {skipped_count} skipped")

def main():
    """Main execution function."""

    if not NOTION_API_KEY or not SL_DATABASE_ID:
        print("❌ Missing required environment variables:")
        print("   - NOTION_API_KEY")
        print("   - SL_DATABASE_ID")
        return

    print("🚀 Starting SL sync to Notion...")
    print(f"📊 Database ID: {SL_DATABASE_ID}")

    agents_dir = Path('agents')

    lk_files = list(agents_dir.glob('*/levende-kompendium-*.md'))
    lk_files.extend(agents_dir.glob('*/LK/*kompendium*.md'))
    lk_files.extend(agents_dir.glob('**/LEVENDE_KOMPENDIUM*.md'))

    lk_files = list(set(lk_files))

    if not lk_files:
        print("❌ No Living Compendium files found")
        return

    print(f"📚 Found {len(lk_files)} agent LK files")

    for lk_path in lk_files:
        process_agent_lk(lk_path)

    print("\n✅ SL sync complete!")

if __name__ == '__main__':
    main()
