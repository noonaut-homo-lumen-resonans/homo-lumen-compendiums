#!/usr/bin/env python3
"""
Deep analysis of all 23 Notion databases to find new and important information.
"""

import os
import sys
import io
import json
import requests
from datetime import datetime
from collections import defaultdict

# Force UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API Configuration
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found in environment")
    print("Set it with: export NOTION_API_KEY='your_key_here'")
    sys.exit(1)

NOTION_VERSION = "2022-06-28"

HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Notion-Version': NOTION_VERSION,
    'Content-Type': 'application/json'
}

def search_all_databases():
    """Search for all databases in the workspace."""
    url = 'https://api.notion.com/v1/search'
    data = {
        'filter': {
            'value': 'database',
            'property': 'object'
        },
        'page_size': 100
    }

    response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code == 200:
        results = response.json().get('results', [])
        databases = []

        for db in results:
            title_parts = db.get('title', [])
            title = title_parts[0].get('plain_text', 'Untitled') if title_parts else 'Untitled'
            db_id = db.get('id', '').replace('-', '')
            created = db.get('created_time', 'N/A')
            last_edited = db.get('last_edited_time', 'N/A')

            databases.append({
                'id': db_id,
                'title': title,
                'created': created,
                'last_edited': last_edited,
                'url': db.get('url', '')
            })

        # Sort by last edited (most recent first)
        databases.sort(key=lambda x: x['last_edited'], reverse=True)
        return databases
    else:
        print(f"ERROR: {response.status_code} - {response.text}")
        return []

def query_database_detailed(db_id, db_title):
    """Query a database for detailed information."""
    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    data = {
        'page_size': 100
    }

    response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code != 200:
        return {
            'error': f"{response.status_code}: {response.text[:100]}",
            'entries': 0
        }

    results = response.json().get('results', [])

    # Analyze properties
    property_types = defaultdict(set)
    sample_entries = []

    for entry in results[:5]:  # Analyze first 5 entries
        entry_data = {
            'id': entry.get('id', ''),
            'created': entry.get('created_time', ''),
            'last_edited': entry.get('last_edited_time', ''),
            'properties': {}
        }

        props = entry.get('properties', {})
        for prop_name, prop_value in props.items():
            prop_type = prop_value.get('type')
            property_types[prop_name].add(prop_type)

            # Extract value
            value = extract_property_value(prop_value)
            if value:
                entry_data['properties'][prop_name] = value

        sample_entries.append(entry_data)

    return {
        'entries': len(results),
        'properties': dict(property_types),
        'sample_entries': sample_entries,
        'has_relations': any('relation' in types for types in property_types.values())
    }

def extract_property_value(prop_data):
    """Extract value from property based on its type."""
    prop_type = prop_data.get('type')

    if prop_type == 'title':
        texts = prop_data.get('title', [])
        return ''.join([t.get('plain_text', '') for t in texts])
    elif prop_type == 'rich_text':
        texts = prop_data.get('rich_text', [])
        text = ''.join([t.get('plain_text', '') for t in texts])
        return text[:200] if len(text) > 200 else text
    elif prop_type == 'select':
        select = prop_data.get('select')
        return select.get('name', None) if select else None
    elif prop_type == 'multi_select':
        options = prop_data.get('multi_select', [])
        return [opt.get('name') for opt in options]
    elif prop_type == 'date':
        date = prop_data.get('date')
        return date.get('start', None) if date else None
    elif prop_type == 'relation':
        relations = prop_data.get('relation', [])
        return f"{len(relations)} relation(s)"
    elif prop_type == 'url':
        return prop_data.get('url', None)
    elif prop_type == 'number':
        return prop_data.get('number', None)
    elif prop_type == 'checkbox':
        return prop_data.get('checkbox', None)
    elif prop_type == 'people':
        people = prop_data.get('people', [])
        return f"{len(people)} person/people"
    elif prop_type == 'files':
        files = prop_data.get('files', [])
        return f"{len(files)} file(s)"
    elif prop_type == 'created_time':
        return prop_data.get('created_time', None)
    elif prop_type == 'last_edited_time':
        return prop_data.get('last_edited_time', None)
    elif prop_type == 'email':
        return prop_data.get('email', None)
    elif prop_type == 'phone_number':
        return prop_data.get('phone_number', None)
    else:
        return None

def categorize_databases(databases_with_data):
    """Categorize databases by purpose and relevance."""
    categories = {
        'core_system': [],      # SLL, ARF, SMK, LK, EM
        'knowledge_mgmt': [],   # Databases for knowledge/learning
        'project_mgmt': [],     # Task/project databases
        'personal': [],         # Personal logs/journals
        'metadata': [],         # Audit logs, etc.
        'unknown': []
    }

    core_keywords = ['SLL', 'ARF', 'SMK', 'Living Compendium', 'Emergent Pattern']
    knowledge_keywords = ['Case Stud', 'Shadow Log', 'Critical Decision', 'Agent', 'Kunnskapsbase', 'Dokumenter']
    project_keywords = ['Oppgaver', 'Milepæler', 'Task', 'Project']
    personal_keywords = ['Dagbok', 'How we feel', 'Puls', 'Phoenix', 'EchoBook']
    metadata_keywords = ['Audit', 'MCP', 'Log']

    for db in databases_with_data:
        title = db['title']

        # Determine category
        if any(kw in title for kw in core_keywords):
            categories['core_system'].append(db)
        elif any(kw in title for kw in knowledge_keywords):
            categories['knowledge_mgmt'].append(db)
        elif any(kw in title for kw in project_keywords):
            categories['project_mgmt'].append(db)
        elif any(kw in title for kw in personal_keywords):
            categories['personal'].append(db)
        elif any(kw in title for kw in metadata_keywords):
            categories['metadata'].append(db)
        else:
            categories['unknown'].append(db)

    return categories

def print_database_analysis(db, data):
    """Print detailed analysis of a database."""
    print(f"\n{'='*80}")
    print(f"📊 {db['title']}")
    print(f"{'='*80}")
    print(f"ID: {db['id']}")
    print(f"Created: {db['created']}")
    print(f"Last Edited: {db['last_edited']}")
    print(f"Entries: {data['entries']}")
    print(f"Has Relations: {'✓' if data.get('has_relations') else '✗'}")

    if data.get('error'):
        print(f"ERROR: {data['error']}")
        return

    # Properties
    properties = data.get('properties', {})
    print(f"\nProperties ({len(properties)}):")
    for prop_name, types in sorted(properties.items()):
        type_str = ', '.join(types)
        relation_marker = " 🔗" if 'relation' in types else ""
        print(f"  • {prop_name}: {type_str}{relation_marker}")

    # Sample entries
    sample_entries = data.get('sample_entries', [])
    if sample_entries and sample_entries[0].get('properties'):
        print(f"\nSample Entry (Most Recent):")
        entry = sample_entries[0]
        print(f"  Created: {entry['created']}")
        print(f"  Last Edited: {entry['last_edited']}")

        for prop_name, prop_value in entry['properties'].items():
            if prop_value:
                val_str = str(prop_value)
                if len(val_str) > 100:
                    val_str = val_str[:100] + "..."
                print(f"    • {prop_name}: {val_str}")

def create_comprehensive_report(categories, all_data):
    """Create comprehensive markdown report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"NOTION_ALL_DATABASES_ANALYSIS_{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Complete Notion Workspace Analysis\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Databases: {sum(len(dbs) for dbs in categories.values())}\n\n")

        # Executive Summary
        f.write("## Executive Summary\n\n")
        for category, dbs in categories.items():
            if dbs:
                f.write(f"### {category.replace('_', ' ').title()} ({len(dbs)} databases)\n\n")
                total_entries = sum(all_data[db['id']]['entries'] for db in dbs if db['id'] in all_data)
                f.write(f"**Total Entries**: {total_entries}\n\n")
                for db in dbs:
                    data = all_data.get(db['id'], {})
                    entries = data.get('entries', 0)
                    has_rel = "🔗" if data.get('has_relations') else ""
                    f.write(f"- **{db['title']}**: {entries} entries {has_rel}\n")
                f.write("\n")

        # Detailed Analysis by Category
        f.write("## Detailed Database Analysis\n\n")

        for category, dbs in categories.items():
            if not dbs:
                continue

            f.write(f"### {category.replace('_', ' ').title()}\n\n")

            for db in dbs:
                data = all_data.get(db['id'], {})

                f.write(f"#### {db['title']}\n\n")
                f.write(f"- **ID**: `{db['id']}`\n")
                f.write(f"- **Created**: {db['created']}\n")
                f.write(f"- **Last Edited**: {db['last_edited']}\n")
                f.write(f"- **Entries**: {data.get('entries', 0)}\n")
                f.write(f"- **URL**: {db['url']}\n\n")

                if data.get('error'):
                    f.write(f"*Error: {data['error']}*\n\n")
                    continue

                # Properties
                properties = data.get('properties', {})
                if properties:
                    f.write("**Properties**:\n\n")
                    for prop_name, types in sorted(properties.items()):
                        type_str = ', '.join(types)
                        relation_marker = " 🔗" if 'relation' in types else ""
                        f.write(f"- `{prop_name}`: {type_str}{relation_marker}\n")
                    f.write("\n")

                # Sample data
                sample_entries = data.get('sample_entries', [])
                if sample_entries and sample_entries[0].get('properties'):
                    f.write("**Most Recent Entry**:\n\n")
                    entry = sample_entries[0]

                    for prop_name, prop_value in entry['properties'].items():
                        if prop_value and prop_name not in ['created_time', 'last_edited_time']:
                            val_str = str(prop_value)
                            if len(val_str) > 150:
                                val_str = val_str[:150] + "..."
                            f.write(f"- *{prop_name}*: {val_str}\n")
                    f.write("\n")

        # Integration Opportunities
        f.write("## Integration Opportunities\n\n")
        f.write("### Databases with Relations\n\n")

        for category, dbs in categories.items():
            for db in dbs:
                data = all_data.get(db['id'], {})
                if data.get('has_relations'):
                    properties = data.get('properties', {})
                    relation_props = [p for p, types in properties.items() if 'relation' in types]
                    f.write(f"- **{db['title']}**: {', '.join(relation_props)}\n")

        f.write("\n### Potential New Integrations\n\n")
        f.write("Based on database purposes and content, these integrations could be valuable:\n\n")

        # Suggest integrations
        for category, dbs in categories.items():
            if category in ['knowledge_mgmt', 'project_mgmt']:
                for db in dbs:
                    data = all_data.get(db['id'], {})
                    if data.get('entries', 0) > 0:
                        f.write(f"1. **{db['title']}** ({data['entries']} entries)\n")
                        f.write(f"   - Could link to: SLL (learning points), LK (documentation)\n")
                        f.write(f"   - Integration value: Cross-reference project work with learning\n\n")

        f.write("## Recommendations\n\n")
        f.write("1. **Priority 1**: Integrate databases with existing relations (already partially connected)\n")
        f.write("2. **Priority 2**: Connect project management databases to learning databases\n")
        f.write("3. **Priority 3**: Link personal reflection databases to ARF (Agent Reflection Forum)\n")
        f.write("4. **Priority 4**: Consolidate duplicate databases (multiple SLL, EM databases found)\n\n")

        f.write("---\n\n")
        f.write("*Generated by Claude Code for Homo Lumen Resonans*\n")

    return filename

def main():
    """Main execution."""
    print("="*80)
    print("COMPREHENSIVE NOTION WORKSPACE ANALYSIS")
    print("Analyzing all 23 databases for integration opportunities")
    print("="*80)

    # Get all databases
    print("\n🔍 Searching for all databases...")
    all_databases = search_all_databases()
    print(f"✓ Found {len(all_databases)} databases")

    # Query each database
    print("\n📊 Analyzing each database in detail...")
    all_data = {}

    for i, db in enumerate(all_databases, 1):
        print(f"\n[{i}/{len(all_databases)}] Querying: {db['title']}")
        data = query_database_detailed(db['id'], db['title'])
        all_data[db['id']] = data

        # Print brief summary
        if data.get('error'):
            print(f"  ⚠ Error: {data['error'][:50]}")
        else:
            print(f"  ✓ {data['entries']} entries, {len(data.get('properties', {}))} properties")
            if data.get('has_relations'):
                print(f"  🔗 Has relation properties")

    # Categorize databases
    print("\n\n📋 Categorizing databases...")
    databases_with_data = [{**db, **all_data[db['id']]} for db in all_databases]
    categories = categorize_databases(databases_with_data)

    print("\n" + "="*80)
    print("CATEGORIZATION SUMMARY")
    print("="*80)
    for category, dbs in categories.items():
        if dbs:
            total = sum(all_data[db['id']]['entries'] for db in dbs if db['id'] in all_data)
            print(f"\n{category.replace('_', ' ').title()}: {len(dbs)} databases, {total} total entries")
            for db in dbs:
                data = all_data.get(db['id'], {})
                entries = data.get('entries', 0)
                rel = "🔗" if data.get('has_relations') else "  "
                print(f"  {rel} {db['title']}: {entries} entries")

    # Print detailed analysis for each database
    print("\n\n" + "="*80)
    print("DETAILED ANALYSIS")
    print("="*80)

    for category, dbs in categories.items():
        if dbs:
            print(f"\n\n{'='*80}")
            print(f"{category.replace('_', ' ').upper()}")
            print(f"{'='*80}")

            for db in dbs:
                data = all_data.get(db['id'], {})
                print_database_analysis(db, data)

    # Create comprehensive report
    print("\n\n" + "="*80)
    print("GENERATING COMPREHENSIVE REPORT")
    print("="*80)

    report_file = create_comprehensive_report(categories, all_data)
    print(f"\n✓ Report saved: {report_file}")

    # Summary statistics
    total_entries = sum(data.get('entries', 0) for data in all_data.values())
    total_with_relations = sum(1 for data in all_data.values() if data.get('has_relations'))

    print(f"\n{'='*80}")
    print("FINAL STATISTICS")
    print(f"{'='*80}")
    print(f"Total Databases: {len(all_databases)}")
    print(f"Total Entries: {total_entries}")
    print(f"Databases with Relations: {total_with_relations}")
    print(f"Core System Databases: {len(categories['core_system'])}")
    print(f"Knowledge Management: {len(categories['knowledge_mgmt'])}")
    print(f"Project Management: {len(categories['project_mgmt'])}")
    print(f"Personal: {len(categories['personal'])}")
    print(f"Metadata: {len(categories['metadata'])}")
    print(f"Unknown: {len(categories['unknown'])}")

if __name__ == "__main__":
    main()