#!/usr/bin/env python3
"""
Parse Critical Decisions from agent Living Compendiums and sync to Notion KD Database.

This script extracts Critical Decision entries from agent LK markdown files and syncs them
to the Notion KD (Critical Decisions) Database.

Usage:
    python scripts/parse_kd.py

Environment Variables Required:
    NOTION_API_KEY: Notion integration API key
    KD_DATABASE_ID: Notion database ID for Critical Decisions (2988fec9293180838c4bd5e13138ddf2)

Input Format (from LK markdown):
    **KD #010 - Godkjenne 3 Nye Cross-Agent Databases**
    - **Dato:** 26. oktober 2025
    - **Beslutning:** ✅ 3 nye Notion databases: CS, SL, KD
    - **Rationale:** Muliggjør coalition-wide pattern detection
    - **Impact:** Transformative

Output:
    Creates/updates entries in Notion KD Database with properties:
    - Name (title): KD #010
    - Title (rich_text): Entry title
    - Date (date): Parsed Norwegian date -> ISO format
    - Agent (multi_select): Agent name(s) - NOTE: multi_select, not single select!
    - Decision (rich_text): Beslutning field
    - Rationale (rich_text): Rationale field
    - Impact (select): Impact value (Low/Medium/High/Transformative)
    - Status (select): Status value (default: Implemented)
    - Tags (multi_select): Auto-inferred decision categories
    - Vokter (rich_text): Philosophical grounding (NEW - Week 2)

Philosophical Grounding (Week 2):
    The Vokter field tracks which philosophical wisdom (Bohm, Spira, Eisenstein, etc.)
    informed this decision. This supports Zara's principle of letting Vokter wisdom
    INFORM (not dictate) strategic decisions. Per docs/SHADOW_TAXONOMY.md.

Author: Code (Claude Code Agent)
Date: 27. oktober 2025 (Updated: 28. oktober 2025 - Vokter field added)
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
KD_DATABASE_ID = os.environ.get('KD_DATABASE_ID')
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

def infer_decision_tags(title, decision, rationale):
    """
    Infer decision tags from title and content.

    Returns:
        List of tag names
    """
    tags = []
    content = (title + " " + decision + " " + rationale).lower()

    # Check for various decision categories
    if any(keyword in content for keyword in ['constitution', 'constitutional', 'konstitu']):
        tags.append('Constitutional')

    if any(keyword in content for keyword in ['technical', 'teknisk', 'code', 'implementation', 'tech']):
        tags.append('Technical')

    if any(keyword in content for keyword in ['strategic', 'strategisk', 'strategy']):
        tags.append('Strategic')

    if any(keyword in content for keyword in ['architectural', 'arkitektur', 'architecture', 'structure']):
        tags.append('Architectural')

    if any(keyword in content for keyword in ['operational', 'operasjonell', 'operation']):
        tags.append('Operational')

    if any(keyword in content for keyword in ['philosophical', 'filosofisk', 'philosophy', 'bohm', 'spira']):
        tags.append('Philosophical')

    return tags

def parse_critical_decision(kd_text, agent_name):
    """
    Parse a single critical decision entry.

    Args:
        kd_text: Markdown text containing KD entry
        agent_name: Name of the agent

    Returns:
        Dictionary with KD data, or None if parsing fails
    """
    # Extract KD ID and Title
    id_match = re.search(r'KD\s+#(\d+)\s*[-–]\s*(.+?)(?:\*\*|\n)', kd_text, re.IGNORECASE)
    if not id_match:
        return None

    kd_id = id_match.group(1)
    title = id_match.group(2).strip().strip('*').strip()

    # Extract Date
    date_match = re.search(r'\*\*Dato:\*\*\s*(.+?)(?:\n|$)', kd_text)
    date = None
    if date_match:
        date = parse_norwegian_date(date_match.group(1))

    # Extract Beslutning/Decision
    decision_match = re.search(
        r'\*\*Beslutning:\*\*\s*(.+?)(?=\n\s*\*\*|\n\n|$)',
        kd_text,
        re.DOTALL
    )
    decision = decision_match.group(1).strip() if decision_match else ""

    # Remove emoji/checkmarks from decision
    decision = re.sub(r'[✅❌⏳]', '', decision).strip()

    # Extract Rationale
    rationale_match = re.search(
        r'\*\*Rationale:\*\*\s*(.+?)(?=\n\s*\*\*|\n\n|$)',
        kd_text,
        re.DOTALL
    )
    rationale = rationale_match.group(1).strip() if rationale_match else ""

    # Extract Impact
    impact_match = re.search(r'\*\*Impact:\*\*\s*([^\n]+)', kd_text)
    impact = impact_match.group(1).strip() if impact_match else "Medium"

    # Normalize impact values
    impact_mapping = {
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
        'transformative': 'Transformative'
    }
    impact = impact_mapping.get(impact.lower(), impact)

    # Extract Status (if present)
    status_match = re.search(r'\*\*Status:\*\*\s*([^\n]+)', kd_text)
    status = status_match.group(1).strip() if status_match else "Implemented"

    # Remove emoji from status
    status = re.sub(r'[✅❌⏳]', '', status).strip()

    # Normalize status values
    status_mapping = {
        'proposed': 'Proposed',
        'approved': 'Approved',
        'implemented': 'Implemented',
        'deprecated': 'Deprecated',
        'revisiting': 'Revisiting'
    }
    status = status_mapping.get(status.lower(), status)

    # Extract Vokter/Voktere (NEW - Week 2: Philosophical Grounding)
    # This field tracks which Vokter (Bohm, Spira, Eisenstein, etc.) informs this decision
    vokter_match = re.search(
        r'\*\*Vokter(?:e)?:\*\*\s*(.+?)(?=\n\s*\*\*|\n\n|$)',
        kd_text,
        re.DOTALL | re.IGNORECASE
    )
    vokter = None
    if vokter_match:
        vokter = vokter_match.group(1).strip()
        # Clean up common formats
        vokter = re.sub(r'[•\-]\s*', '', vokter)  # Remove bullet points
        vokter = vokter.strip()

    # Infer tags
    tags = infer_decision_tags(title, decision, rationale)

    return {
        'id': f"KD #{kd_id.zfill(3)}",
        'title': title,
        'date': date,
        'agent': agent_name,
        'decision': decision,
        'rationale': rationale,
        'impact': impact,
        'status': status,
        'tags': tags,
        'vokter': vokter  # NEW - Week 2
    }

def create_notion_page(kd_data):
    """
    Create a page in the Notion KD Database.

    Args:
        kd_data: Dictionary with KD data

    Returns:
        True if successful, False otherwise
def find_existing_kd(kd_number):
    """
    Search for existing KD entry by KD Number (including archived pages).

    Args:
        kd_number: KD identifier (e.g., "KD #001")

    Returns:
        Existing page dict if found, None otherwise
    """
    url = f'https://api.notion.com/v1/databases/{KD_DATABASE_ID}/query'

    # First, try to find active (non-archived) pages with title filter
    try:
        payload = {
            'filter': {
                'property': 'Name',
                'title': {
                    'equals': kd_number
                }
            }
        }
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)

        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                page = results[0]
                print(f"  Found existing page: {page['id']}")
                return page
    except Exception as e:
        print(f"  Error searching for {kd_number}: {e}")

    # If no active page found, search ALL pages (including archived)
    try:
        # Fetch all pages without filter
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

        # Check all pages (including archived) for matching KD number
        for page in all_pages:
            try:
                props = page.get('properties', {})
                name_prop = props.get('Name', {})
                if name_prop.get('title'):
                    page_kd_number = name_prop['title'][0].get('text', {}).get('content', '')
                    if page_kd_number == kd_number:
                        if page.get('archived'):
                            print(f"  Found ARCHIVED page: {page['id']} - will unarchive")
                        else:
                            print(f"  Found existing page: {page['id']}")
                        return page
            except:
                continue

    except Exception as e:
        print(f"  Error in full page search: {e}")

    return None

def create_or_update_notion_page(kd_data):
    """
    Create or update a page in the Notion KD Database.

    First checks if a page with the same KD Number exists (including archived pages).
    If found, unarchives (if needed) and updates it. Otherwise creates a new page.

    Args:
        kd_data: Dictionary with KD data

    Returns:
        True if successful, False otherwise
    """
    # Build properties
    properties = {
        'Name': {
            'title': [{'text': {'content': kd_data['id']}}]
        },
        'Title': {
            'rich_text': [{'text': {'content': kd_data['title'][:2000]}}]  # Notion limit
        },
        'Agent': {
            'select': {'name': kd_data['agent']}
        },
        'Situation': {
            'rich_text': [{'text': {'content': kd_data['situation'][:2000]}}]
        },
        'Approach': {
            'rich_text': [{'text': {'content': kd_data['approach'][:2000]}}]
        },
        'Result': {
            'rich_text': [{'text': {'content': kd_data['result'][:2000]}}]
        }
    }

    # Add date if available
    if kd_data['date']:
        properties['Date'] = {
            'date': {'start': kd_data['date']}
        }

    # Search for existing page
    existing_page = find_existing_kd(kd_data['id'])

    try:
        if existing_page:
            # Update existing page
            page_id = existing_page['id']

            # If page is archived, unarchive it first
            if existing_page.get('archived'):
                print(f"  Unarchiving page...")
                unarchive_url = f'https://api.notion.com/v1/pages/{page_id}'
                unarchive_payload = {'archived': False}
                unarchive_response = requests.patch(unarchive_url, headers=HEADERS, json=unarchive_payload, timeout=10)

                if unarchive_response.status_code == 200:
                    print(f"  [OK] Unarchived page")
                else:
                    print(f"  [WARNING] Failed to unarchive: {unarchive_response.status_code}")

            # Update the page
            update_url = f'https://api.notion.com/v1/pages/{page_id}'
            update_payload = {'properties': properties}
            response = requests.patch(update_url, headers=HEADERS, json=update_payload, timeout=10)

            if response.status_code == 200:
                print(f"✅ Updated: {kd_data['id']} - {kd_data['title']}")
                return True
            else:
                print(f"❌ Failed to update: {kd_data['id']} - Status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
        else:
            # Create new page
            create_url = 'https://api.notion.com/v1/pages'
            create_payload = {
                'parent': {'database_id': KD_DATABASE_ID},
                'properties': properties
            }
            response = requests.post(create_url, headers=HEADERS, json=create_payload, timeout=10)

            if response.status_code == 200:
                print(f"✅ Created: {kd_data['id']} - {kd_data['title']}")
                return True
            else:
                print(f"❌ Failed to create: {kd_data['id']} - Status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False

    except Exception as e:
        print(f"❌ Error processing {kd_data['id']}: {e}")
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

    # Find KD section (flexible to handle bold markers, emojis, etc.)
    # Use greedy match and [^#] to ensure we capture until next ## section (not ###)
    kd_section_match = re.search(
        r'##\s*[\*\s]*(?:SEKSJON \d+:\s*)?KRITISKE BESLUTNINGER[\*\s]*\n(.*)(?=\n##[^#]|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    if not kd_section_match:
        print(f"⚠️  No KD section found in {agent_name} LK")
        return

    kd_section = kd_section_match.group(1)

    # Split into individual critical decisions (handles heading markers)
    decisions = re.split(r'\n#{0,6}\s*\*\*KD\s+#', kd_section, flags=re.IGNORECASE)

    created_count = 0
    skipped_count = 0

    for kd_text in decisions:
        if not kd_text.strip():
            continue

        if not re.match(r'KD\s+#', kd_text, re.IGNORECASE):
            kd_text = 'KD #' + kd_text

        kd_data = parse_critical_decision(kd_text, agent_name)

        if kd_data:
            if create_or_update_notion_page(kd_data):
                created_count += 1
            else:
                skipped_count += 1
        else:
            skipped_count += 1

    print(f"✅ {agent_name}: {created_count} critical decisions synced, {skipped_count} skipped")

def main():
    """Main execution function."""

    if not NOTION_API_KEY or not KD_DATABASE_ID:
        print("❌ Missing required environment variables:")
        print("   - NOTION_API_KEY")
        print("   - KD_DATABASE_ID")
        return

    print("🚀 Starting KD sync to Notion...")
    print(f"📊 Database ID: {KD_DATABASE_ID}")

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

    print("\n✅ KD sync complete!")

if __name__ == '__main__':
    main()
