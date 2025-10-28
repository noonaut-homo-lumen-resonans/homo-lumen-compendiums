#!/usr/bin/env python3
"""
Analyze duplicates in Critical Decisions (KD) Notion database.

This script identifies duplicate KD entries by KD Number (Name property).
For example, multiple entries with "KD #009" are considered duplicates.

Usage:
    python analyze_kd_duplicates.py

Environment Variables:
    NOTION_API_KEY: Your Notion integration API key

Author: Code (Claude Code Agent)
Date: 28. oktober 2025
"""

import os
import sys
import io
import json
from datetime import datetime
from collections import defaultdict
from notion_client import Client

# Force UTF-8 encoding for stdout (Windows compatibility)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
KD_DATABASE_ID = '2988fec9-2931-8083-8c4b-d5e13138ddf2'  # Critical Decisions database (CORRECT ID)

# Try to get API key from environment or use hardcoded for testing
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
if not NOTION_API_KEY:
    # Use provided key
    NOTION_API_KEY = '***REMOVED***'

if not NOTION_API_KEY:
    print("❌ ERROR: NOTION_API_KEY not found")
    exit(1)

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)

class KDAnalyzer:
    def __init__(self):
        self.entries = []
        self.duplicates = defaultdict(list)

    def fetch_all_kd_entries(self):
        """Fetch all entries from KD database (including archived)."""
        print("\n🔍 Fetching all KD entries...")

        has_more = True
        start_cursor = None

        while has_more:
            try:
                if start_cursor:
                    response = notion.databases.query(
                        database_id=KD_DATABASE_ID,
                        start_cursor=start_cursor
                    )
                else:
                    response = notion.databases.query(database_id=KD_DATABASE_ID)

                self.entries.extend(response['results'])
                has_more = response.get('has_more', False)
                start_cursor = response.get('next_cursor')

            except Exception as e:
                print(f"❌ Error fetching entries: {e}")
                return False

        print(f"✅ Fetched {len(self.entries)} total entries")
        return True

    def extract_kd_data(self, entry):
        """Extract KD data from Notion entry."""
        props = entry.get('properties', {})

        # KD Number (from Name/title property)
        kd_number = None
        name_prop = props.get('Name', {})
        if name_prop.get('title'):
            kd_number = name_prop['title'][0].get('text', {}).get('content', '')

        # Title
        title = ""
        title_prop = props.get('Title', {})
        if title_prop.get('rich_text'):
            title = title_prop['rich_text'][0].get('text', {}).get('content', '')

        # Agent
        agent = ""
        agent_prop = props.get('Agent', {})
        if agent_prop.get('select'):
            agent = agent_prop['select'].get('name', '')

        # Date
        date = None
        date_prop = props.get('Date', {})
        if date_prop.get('date'):
            date = date_prop['date'].get('start')

        # Count relations
        relation_count = 0
        for prop_name, prop_value in props.items():
            if prop_value.get('type') == 'relation' and prop_value.get('relation'):
                relation_count += len(prop_value['relation'])

        # Count filled fields
        filled_fields = 0
        for prop_value in props.values():
            prop_type = prop_value.get('type')
            if prop_type == 'title' and prop_value.get('title'):
                filled_fields += 1
            elif prop_type == 'rich_text' and prop_value.get('rich_text'):
                filled_fields += 1
            elif prop_type == 'select' and prop_value.get('select'):
                filled_fields += 1
            elif prop_type == 'date' and prop_value.get('date'):
                filled_fields += 1
            elif prop_type == 'relation' and prop_value.get('relation'):
                filled_fields += 1

        return {
            'id': entry['id'],
            'kd_number': kd_number or 'NO_NUMBER',
            'title': title,
            'agent': agent,
            'date': date,
            'relation_count': relation_count,
            'filled_fields': filled_fields,
            'last_edited_time': entry.get('last_edited_time'),
            'archived': entry.get('archived', False)
        }

    def find_duplicates(self):
        """Group entries by KD Number to find duplicates."""
        print("\n🔎 Analyzing for duplicates...")

        kd_groups = defaultdict(list)

        for entry in self.entries:
            kd_data = self.extract_kd_data(entry)
            kd_groups[kd_data['kd_number']].append(kd_data)

        # Identify duplicates
        unique_count = 0
        duplicate_count = 0

        for kd_number, entries in kd_groups.items():
            if len(entries) == 1:
                unique_count += 1
            else:
                duplicate_count += len(entries)
                self.duplicates[kd_number] = entries

        print(f"\n📊 Analysis Results:")
        print(f"   Total entries: {len(self.entries)}")
        print(f"   Unique KD numbers: {len(kd_groups)}")
        print(f"   Clean entries (no duplicates): {unique_count}")
        print(f"   Duplicate entries: {duplicate_count}")
        print(f"   Duplicate groups: {len(self.duplicates)}")

        if self.duplicates:
            duplication_rate = (duplicate_count / len(self.entries)) * 100
            print(f"   Duplication rate: {duplication_rate:.1f}%")

        return len(self.duplicates) > 0

    def display_duplicates(self):
        """Display duplicate groups in detail."""
        if not self.duplicates:
            print("\n✅ No duplicates found!")
            return

        print(f"\n🔴 Found {len(self.duplicates)} duplicate groups:\n")

        for kd_number, entries in sorted(self.duplicates.items()):
            print(f"{'='*70}")
            print(f"KD Number: {kd_number} ({len(entries)} copies)")
            print(f"{'='*70}")

            for i, entry in enumerate(entries, 1):
                archived_marker = " 🗄️ ARCHIVED" if entry['archived'] else ""
                print(f"\n  Copy {i}:{archived_marker}")
                print(f"    ID: {entry['id']}")
                print(f"    Title: {entry['title'][:60]}...")
                print(f"    Agent: {entry['agent']}")
                print(f"    Date: {entry['date']}")
                print(f"    Relations: {entry['relation_count']}")
                print(f"    Filled fields: {entry['filled_fields']}")
                print(f"    Last edited: {entry['last_edited_time']}")

            print()

    def save_report(self):
        """Save duplicate analysis to JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'kd_duplicates_analysis_{timestamp}.json'

        report = {
            'timestamp': timestamp,
            'total_entries': len(self.entries),
            'unique_groups': len(set(e['kd_number'] for e in [self.extract_kd_data(entry) for entry in self.entries])),
            'duplicate_groups': len(self.duplicates),
            'duplicates': {}
        }

        for kd_number, entries in self.duplicates.items():
            report['duplicates'][kd_number] = [
                {
                    'id': e['id'],
                    'title': e['title'],
                    'agent': e['agent'],
                    'date': e['date'],
                    'relations': e['relation_count'],
                    'filled_fields': e['filled_fields'],
                    'last_edited': e['last_edited_time'],
                    'archived': e['archived']
                }
                for e in entries
            ]

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Report saved to: {filename}")

def main():
    print("="*70)
    print("  Critical Decisions (KD) Duplicate Analysis")
    print("="*70)

    analyzer = KDAnalyzer()

    # Fetch all entries
    if not analyzer.fetch_all_kd_entries():
        return

    # Find duplicates
    has_duplicates = analyzer.find_duplicates()

    # Display results
    if has_duplicates:
        analyzer.display_duplicates()
        analyzer.save_report()

        print("\n" + "="*70)
        print("Next steps:")
        print("  1. Review the duplicates above")
        print("  2. Run: python deduplicate_kd.py --dry-run")
        print("  3. Approve and run actual deduplication")
        print("="*70)
    else:
        print("\n✅ Critical Decisions database is clean - no duplicates found!")

if __name__ == '__main__':
    main()