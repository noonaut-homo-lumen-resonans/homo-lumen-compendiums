#!/usr/bin/env python3
"""
SMK Duplicate Analysis Script
Identifies duplicate entries in the SMK (Strategic Macro-Coordination) database.

Detects duplicates based on:
1. SMK Number (same number = duplicate)
2. Name (same title = possible duplicate)
3. Commit SHA (same commit = definite duplicate)
4. Date + Agent (same date and agent = possible duplicate)
"""

import os
import sys
import io
from notion_client import Client
from datetime import datetime
import json
from collections import defaultdict

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get Notion API key
NOTION_API_KEY = os.environ.get('NOTION_API_KEY', '***REMOVED***')
if not NOTION_API_KEY:
    print("❌ ERROR: NOTION_API_KEY not found in environment")
    print("Set it with: set NOTION_API_KEY=your_key_here (Windows)")
    print("Or: export NOTION_API_KEY='your_key_here' (Linux/Mac)")
    sys.exit(1)

notion = Client(auth=NOTION_API_KEY)

# SMK Database ID
SMK_DATABASE_ID = 'ba1d4a4407a5425fafd81d27dc02cc1c'


class SMKDuplicateAnalyzer:
    """Analyzes SMK database for duplicate entries."""

    def __init__(self):
        self.entries = []
        self.duplicates = {
            'by_smk_number': defaultdict(list),
            'by_name': defaultdict(list),
            'by_commit_sha': defaultdict(list),
            'by_date_agent': defaultdict(list)
        }
        self.stats = {
            'total_entries': 0,
            'duplicate_groups': 0,
            'total_duplicates': 0,
            'unique_entries': 0
        }

    def fetch_all_smk_entries(self):
        """Fetch all entries from SMK database."""
        print("📥 Fetching all SMK entries from Notion...")

        has_more = True
        start_cursor = None

        while has_more:
            if start_cursor:
                response = notion.databases.query(
                    database_id=SMK_DATABASE_ID,
                    start_cursor=start_cursor
                )
            else:
                response = notion.databases.query(database_id=SMK_DATABASE_ID)

            self.entries.extend(response['results'])

            has_more = response.get('has_more', False)
            start_cursor = response.get('next_cursor')

        self.stats['total_entries'] = len(self.entries)
        print(f"   ✅ Fetched {self.stats['total_entries']} SMK entries\n")

    def extract_entry_data(self, entry):
        """Extract relevant data from a Notion entry."""
        props = entry['properties']

        # Extract Name (title)
        name = ''
        if 'Name' in props and props['Name']['title']:
            name = props['Name']['title'][0]['plain_text']

        # Extract SMK Number
        smk_number = None
        if 'SMK Number' in props and props['SMK Number']['number'] is not None:
            smk_number = props['SMK Number']['number']

        # Extract Agent
        agent = None
        if 'Agent' in props and props['Agent']['select']:
            agent = props['Agent']['select']['name']

        # Extract Date
        date = None
        if 'Date' in props and props['Date']['date']:
            date = props['Date']['date']['start']

        # Extract Status
        status = None
        if 'Status' in props and props['Status']['select']:
            status = props['Status']['select']['name']

        # Extract Commit SHA
        commit_sha = ''
        if 'Commit SHA' in props and props['Commit SHA']['rich_text']:
            commit_sha = props['Commit SHA']['rich_text'][0]['plain_text'] if props['Commit SHA']['rich_text'] else ''

        # Extract GitHub URL
        github_url = ''
        if 'GitHub URL' in props and props['GitHub URL']['url']:
            github_url = props['GitHub URL']['url']

        # Extract Tags
        tags = []
        if 'Tags' in props and props['Tags']['multi_select']:
            tags = [tag['name'] for tag in props['Tags']['multi_select']]

        # Metadata
        created_time = entry['created_time']
        last_edited_time = entry['last_edited_time']
        entry_id = entry['id']

        return {
            'id': entry_id,
            'name': name,
            'smk_number': smk_number,
            'agent': agent,
            'date': date,
            'status': status,
            'commit_sha': commit_sha,
            'github_url': github_url,
            'tags': tags,
            'created_time': created_time,
            'last_edited_time': last_edited_time,
            'notion_url': f"https://www.notion.so/{entry_id.replace('-', '')}"
        }

    def identify_duplicates(self):
        """Identify duplicates based on multiple criteria."""
        print("🔍 Analyzing for duplicates...\n")

        for entry in self.entries:
            data = self.extract_entry_data(entry)

            # Group by SMK Number
            if data['smk_number'] is not None:
                self.duplicates['by_smk_number'][data['smk_number']].append(data)

            # Group by Name (if not empty)
            if data['name']:
                name_key = data['name'].lower().strip()
                self.duplicates['by_name'][name_key].append(data)

            # Group by Commit SHA (if not empty)
            if data['commit_sha']:
                self.duplicates['by_commit_sha'][data['commit_sha']].append(data)

            # Group by Date + Agent (if both exist)
            if data['date'] and data['agent']:
                date_agent_key = f"{data['date']}_{data['agent']}"
                self.duplicates['by_date_agent'][date_agent_key].append(data)

        # Filter to only keep groups with 2+ entries
        for category in self.duplicates:
            self.duplicates[category] = {
                k: v for k, v in self.duplicates[category].items()
                if len(v) > 1
            }

    def calculate_stats(self):
        """Calculate duplication statistics."""
        # Count unique duplicate groups (by SMK Number is most reliable)
        smk_num_duplicates = self.duplicates['by_smk_number']

        self.stats['duplicate_groups'] = len(smk_num_duplicates)

        # Count total duplicate entries
        total_dups = 0
        for group in smk_num_duplicates.values():
            total_dups += len(group) - 1  # -1 because one is the "original"

        self.stats['total_duplicates'] = total_dups
        self.stats['unique_entries'] = self.stats['total_entries'] - total_dups

    def print_report(self):
        """Print detailed analysis report."""
        print("="*70)
        print("📊 SMK DUPLICATE ANALYSIS REPORT")
        print("="*70)
        print()

        print(f"Total SMK Entries: {self.stats['total_entries']}")
        print(f"Unique Entries: {self.stats['unique_entries']}")
        print(f"Duplicate Entries: {self.stats['total_duplicates']}")
        print(f"Duplicate Groups: {self.stats['duplicate_groups']}")
        print()

        if self.stats['duplicate_groups'] == 0:
            print("✅ NO DUPLICATES FOUND!")
            print("   SMK database is clean.")
            return

        print("="*70)
        print("🔴 DUPLICATES DETECTED")
        print("="*70)
        print()

        # Report by SMK Number (primary key)
        if self.duplicates['by_smk_number']:
            print("### Duplicates by SMK Number (CRITICAL)")
            print("-" * 70)
            for smk_num, entries in sorted(self.duplicates['by_smk_number'].items()):
                print(f"\n🔴 SMK #{smk_num} - {len(entries)} entries (should be 1)")
                for idx, entry in enumerate(entries, 1):
                    print(f"   [{idx}] {entry['name']}")
                    print(f"       ID: {entry['id']}")
                    print(f"       Agent: {entry['agent']}")
                    print(f"       Date: {entry['date']}")
                    print(f"       Status: {entry['status']}")
                    print(f"       Created: {entry['created_time']}")
                    print(f"       Last Edited: {entry['last_edited_time']}")
                    print(f"       Commit SHA: {entry['commit_sha'][:8] if entry['commit_sha'] else 'None'}")
                    print(f"       URL: {entry['notion_url']}")
            print()

        # Report by Name
        if self.duplicates['by_name']:
            print("\n### Duplicates by Name")
            print("-" * 70)
            print(f"Found {len(self.duplicates['by_name'])} name duplicates")
            for name, entries in list(self.duplicates['by_name'].items())[:5]:  # Show first 5
                print(f"   • \"{name}\" - {len(entries)} entries")
            if len(self.duplicates['by_name']) > 5:
                print(f"   ... and {len(self.duplicates['by_name']) - 5} more")
            print()

        # Report by Commit SHA
        if self.duplicates['by_commit_sha']:
            print("\n### Duplicates by Commit SHA")
            print("-" * 70)
            print(f"Found {len(self.duplicates['by_commit_sha'])} commit SHA duplicates")
            for sha, entries in list(self.duplicates['by_commit_sha'].items())[:5]:
                print(f"   • {sha[:8]}... - {len(entries)} entries")
            if len(self.duplicates['by_commit_sha']) > 5:
                print(f"   ... and {len(self.duplicates['by_commit_sha']) - 5} more")
            print()

        # Report by Date + Agent
        if self.duplicates['by_date_agent']:
            print("\n### Duplicates by Date + Agent")
            print("-" * 70)
            print(f"Found {len(self.duplicates['by_date_agent'])} date+agent duplicates")
            for key, entries in list(self.duplicates['by_date_agent'].items())[:5]:
                date, agent = key.split('_')
                print(f"   • {date} ({agent}) - {len(entries)} entries")
            if len(self.duplicates['by_date_agent']) > 5:
                print(f"   ... and {len(self.duplicates['by_date_agent']) - 5} more")
            print()

        print("="*70)
        print("💡 RECOMMENDATIONS")
        print("="*70)
        print()
        print("1. Run deduplication script:")
        print("   python deduplicate_smk.py --dry-run")
        print()
        print("2. Review what would be deleted:")
        print("   Check the dry-run output carefully")
        print()
        print("3. Run actual deduplication:")
        print("   python deduplicate_smk.py --auto")
        print("   (or --manual for manual selection)")
        print()
        print("4. Verify results:")
        print("   python analyze_smk_duplicates.py  # Should show 0 duplicates")
        print()

    def save_report(self):
        """Save detailed report to JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'smk_duplicates_analysis_{timestamp}.json'

        report = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'duplicates': {
                'by_smk_number': {
                    str(k): v for k, v in self.duplicates['by_smk_number'].items()
                },
                'by_name': dict(self.duplicates['by_name']),
                'by_commit_sha': dict(self.duplicates['by_commit_sha']),
                'by_date_agent': dict(self.duplicates['by_date_agent'])
            }
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"💾 Detailed report saved to: {filename}")
        print()

    def run(self):
        """Run complete analysis."""
        self.fetch_all_smk_entries()
        self.identify_duplicates()
        self.calculate_stats()
        self.print_report()
        self.save_report()

        return self.stats['duplicate_groups'] == 0


def main():
    """Main execution."""
    analyzer = SMKDuplicateAnalyzer()
    is_clean = analyzer.run()

    return 0 if is_clean else 1


if __name__ == '__main__':
    sys.exit(main())
