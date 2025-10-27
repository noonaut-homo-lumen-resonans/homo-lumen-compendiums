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

Author: Code (Claude Code Agent)
Date: 27. oktober 2025
"""

import os
import re
import requests
from pathlib import Path

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
        'tags': tags
    }

def create_notion_page(kd_data):
    """
    Create a page in the Notion KD Database.

    Args:
        kd_data: Dictionary with KD data

    Returns:
        True if successful, False otherwise
    """
    url = 'https://api.notion.com/v1/pages'

    properties = {
        'Name': {
            'title': [{'text': {'content': kd_data['id']}}]
        },
        'Title': {
            'rich_text': [{'text': {'content': kd_data['title'][:2000]}}]
        },
        'Agent': {
            # NOTE: Agent is multi_select in KD Database (can have multiple agents)
            'multi_select': [{'name': kd_data['agent']}]
        },
        'Decision': {
            'rich_text': [{'text': {'content': kd_data['decision'][:2000]}}]
        },
        'Rationale': {
            'rich_text': [{'text': {'content': kd_data['rationale'][:2000]}}]
        },
        'Impact': {
            'select': {'name': kd_data['impact']}
        },
        'Status': {
            'select': {'name': kd_data['status']}
        }
    }

    # Add date if available
    if kd_data['date']:
        properties['Date'] = {
            'date': {'start': kd_data['date']}
        }

    # Add tags if available
    if kd_data['tags']:
        properties['Tags'] = {
            'multi_select': [{'name': tag} for tag in kd_data['tags']]
        }

    payload = {
        'parent': {'database_id': KD_DATABASE_ID},
        'properties': properties
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)

        if response.status_code == 200:
            tags_str = ', '.join(kd_data['tags']) if kd_data['tags'] else 'no tags'
            print(f"✅ Created: {kd_data['id']} - {kd_data['title']} (Impact: {kd_data['impact']}, {tags_str})")
            return True
        else:
            print(f"❌ Failed: {kd_data['id']} - Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error creating {kd_data['id']}: {e}")
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
        r'##\s*(?:SEKSJON \d+:\s*)?KRITISKE BESLUTNINGER.*?\n(.*)(?=\n##[^#]|\Z)',
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
            if create_notion_page(kd_data):
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
