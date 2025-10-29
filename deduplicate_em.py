#!/usr/bin/env python3
"""
EM Deduplication Script
Removes duplicate entries from EM (Emergent Patterns) database.

Modes:
--dry-run: Show what would be deleted without deleting
--auto: Automatically keep best entry and archive duplicates
--manual: Manually choose which entry to keep

Safety:
- Creates backup before any changes
- Logs all deletions
- Can be rolled back
"""

import os
import sys
import io
from notion_client import Client
from datetime import datetime
import json
import argparse
from collections import defaultdict

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get Notion API key
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found in environment")
    sys.exit(1)

notion = Client(auth=NOTION_API_KEY)

# EM Database ID
EM_DATABASE_ID = '2988fec9-2931-8050-9658-e93447b3b259'


class EMDeduplicator:
    """Deduplicates EM database entries."""

    def __init__(self, dry_run=False, auto_mode=False):
        self.dry_run = dry_run
        self.auto_mode = auto_mode
        self.entries = []
        self.duplicates = defaultdict(list)
        self.to_archive = []
        self.to_keep = []
        self.backup_file = None
        self.log_file = None

    def fetch_all_entries(self):
        """Fetch all entries from EM database."""
        print("Fetching all EM entries...")

        has_more = True
        start_cursor = None

        while has_more:
            if start_cursor:
                response = notion.databases.query(
                    database_id=EM_DATABASE_ID,
                    start_cursor=start_cursor
                )
            else:
                response = notion.databases.query(database_id=EM_DATABASE_ID)

            self.entries.extend(response['results'])

            has_more = response.get('has_more', False)
            start_cursor = response.get('next_cursor')

        print(f"   Fetched {len(self.entries)} entries\n")

    def extract_entry_data(self, entry):
        """Extract relevant data from entry."""
        props = entry['properties']

        pattern_id = ''
        if 'Pattern ID' in props and props['Pattern ID']['title']:
            pattern_id = props['Pattern ID']['title'][0]['plain_text']

        pattern_name = ''
        if 'Pattern Name' in props and props['Pattern Name']['rich_text']:
            pattern_name = props['Pattern Name']['rich_text'][0]['plain_text'] if props['Pattern Name']['rich_text'] else ''

        agent = None
        if 'Agent' in props and props['Agent']['select']:
            agent = props['Agent']['select']['name']

        description = ''
        if 'Description' in props and props['Description']['rich_text']:
            description = props['Description']['rich_text'][0]['plain_text'] if props['Description']['rich_text'] else ''

        tags = []
        if 'Tags' in props and props['Tags']['multi_select']:
            tags = [tag['name'] for tag in props['Tags']['multi_select']]

        # Count filled fields
        filled_fields = sum([
            bool(pattern_id),
            bool(pattern_name),
            agent is not None,
            bool(description),
            len(tags) > 0
        ])

        # Count relations
        relation_count = 0
        for prop_name, prop_data in props.items():
            if prop_data.get('type') == 'relation':
                relation_count += len(prop_data.get('relation', []))

        return {
            'id': entry['id'],
            'pattern_id': pattern_id,
            'pattern_name': pattern_name,
            'agent': agent,
            'description': description,
            'tags': tags,
            'created_time': entry['created_time'],
            'last_edited_time': entry['last_edited_time'],
            'filled_fields': filled_fields,
            'relation_count': relation_count,
            'raw_entry': entry
        }

    def identify_duplicates(self):
        """Group entries by Pattern ID to find duplicates."""
        print("Identifying duplicates by Pattern ID...")

        for entry in self.entries:
            data = self.extract_entry_data(entry)
            if data['pattern_id']:
                self.duplicates[data['pattern_id']].append(data)

        # Keep only groups with 2+ entries
        self.duplicates = {
            k: v for k, v in self.duplicates.items()
            if len(v) > 1
        }

        print(f"   Found {len(self.duplicates)} duplicate groups\n")

    def score_entry(self, entry):
        """Score an entry to determine which is "best"."""
        score = 0

        # Most filled fields (40 points max)
        score += entry['filled_fields'] * 8

        # Description length bonus (20 points max)
        if entry['description']:
            score += min(20, len(entry['description']) / 50)

        # Most relations (20 points max)
        score += entry['relation_count'] * 5

        # Most tags (10 points max)
        score += len(entry['tags']) * 2

        # Newest last edited (10 points)
        try:
            last_edited = datetime.fromisoformat(entry['last_edited_time'].replace('Z', '+00:00'))
            days_ago = (datetime.now(last_edited.tzinfo) - last_edited).days
            score += max(0, 10 - days_ago)  # More recent = higher score
        except:
            pass

        return score

    def choose_best_entry(self, entries):
        """Choose the best entry to keep from a duplicate group."""
        # Score all entries
        scored = [(self.score_entry(e), e) for e in entries]
        scored.sort(reverse=True, key=lambda x: x[0])

        best_entry = scored[0][1]
        others = [e for score, e in scored[1:]]

        return best_entry, others

    def process_duplicates_auto(self):
        """Automatically process all duplicate groups."""
        print("AUTOMATIC MODE: Choosing best entry for each group...\n")

        for pattern_id, entries in sorted(self.duplicates.items()):
            print(f"{pattern_id} - {len(entries)} duplicates")

            best, others = self.choose_best_entry(entries)

            print(f"   KEEP:    {best['pattern_name'][:50]} (ID: {best['id'][:8]}...)")
            print(f"            Score: {self.score_entry(best)}, Filled: {best['filled_fields']}/5, Relations: {best['relation_count']}, Tags: {len(best['tags'])}")
            print(f"            Last Edited: {best['last_edited_time']}")

            for other in others:
                print(f"   ARCHIVE: {other['pattern_name'][:50]} (ID: {other['id'][:8]}...)")
                print(f"            Score: {self.score_entry(other)}, Filled: {other['filled_fields']}/5, Relations: {other['relation_count']}, Tags: {len(other['tags'])}")
                self.to_archive.append(other)

            self.to_keep.append(best)
            print()

    def create_backup(self):
        """Create backup of all entries before making changes."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_file = f'em_backup_{timestamp}.json'

        print(f"Creating backup: {self.backup_file}...")

        backup_data = {
            'timestamp': timestamp,
            'total_entries': len(self.entries),
            'entries': [e['raw_entry'] for e in [self.extract_entry_data(e) for e in self.entries]]
        }

        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)

        print(f"   Backup created: {self.backup_file}\n")

    def create_log(self):
        """Create log file for operations."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = f'em_deduplication_log_{timestamp}.txt'

        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"EM Deduplication Log\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Mode: {'DRY-RUN' if self.dry_run else 'AUTO' if self.auto_mode else 'MANUAL'}\n")
            f.write(f"Total entries: {len(self.entries)}\n")
            f.write(f"Duplicate groups: {len(self.duplicates)}\n")
            f.write(f"Entries to keep: {len(self.to_keep)}\n")
            f.write(f"Entries to archive: {len(self.to_archive)}\n\n")

            f.write("="*70 + "\n")
            f.write("ENTRIES TO ARCHIVE\n")
            f.write("="*70 + "\n\n")

            for entry in self.to_archive:
                f.write(f"Pattern ID: {entry['pattern_id']}\n")
                f.write(f"Pattern Name: {entry['pattern_name']}\n")
                f.write(f"Notion ID: {entry['id']}\n")
                f.write(f"Score: {self.score_entry(entry)}\n")
                f.write(f"Filled Fields: {entry['filled_fields']}/5\n")
                f.write(f"Relations: {entry['relation_count']}\n")
                f.write(f"Tags: {', '.join(entry['tags'])}\n")
                f.write(f"Last Edited: {entry['last_edited_time']}\n")
                f.write("-"*70 + "\n\n")

        print(f"   Log created: {self.log_file}\n")

    def execute_archival(self):
        """Archive the duplicate entries."""
        if self.dry_run:
            print("DRY-RUN MODE: No changes will be made.\n")
            return

        print(f"Archiving {len(self.to_archive)} duplicate entries...")

        for idx, entry in enumerate(self.to_archive, 1):
            try:
                notion.pages.update(
                    page_id=entry['id'],
                    archived=True
                )
                print(f"   [{idx}/{len(self.to_archive)}] Archived: {entry['pattern_id']} - {entry['pattern_name'][:40]}")
            except Exception as e:
                print(f"   ERROR archiving {entry['pattern_id']}: {e}")

        print(f"\n   Archived {len(self.to_archive)} entries\n")

    def run(self):
        """Run the deduplication process."""
        print("\n" + "="*70)
        print("EM DEDUPLICATION TOOL")
        print("="*70 + "\n")

        # Fetch entries
        self.fetch_all_entries()

        # Identify duplicates
        self.identify_duplicates()

        if not self.duplicates:
            print("No duplicates found!\n")
            return

        # Process duplicates
        if self.auto_mode:
            self.process_duplicates_auto()
        else:
            print("ERROR: Manual mode not implemented. Use --auto or --dry-run")
            return

        # Create backup and log
        if not self.dry_run:
            self.create_backup()
        self.create_log()

        # Show summary
        print("="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Total entries: {len(self.entries)}")
        print(f"Duplicate groups: {len(self.duplicates)}")
        print(f"Entries to keep: {len(self.to_keep)}")
        print(f"Entries to archive: {len(self.to_archive)}")
        print(f"Final count: {len(self.entries) - len(self.to_archive)}")
        print()

        # Execute
        if self.dry_run:
            print("DRY-RUN MODE: No changes made.")
        else:
            if self.auto_mode:
                # Auto mode: proceed without confirmation
                print("AUTO MODE: Proceeding with archival automatically...\n")
                self.execute_archival()
                print("\nDeduplication complete!")
                print(f"Backup: {self.backup_file}")
                print(f"Log: {self.log_file}")
            else:
                confirm = input("Proceed with archival? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    self.execute_archival()
                    print("\nDeduplication complete!")
                    print(f"Backup: {self.backup_file}")
                    print(f"Log: {self.log_file}")
                else:
                    print("\nAborted. No changes made.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deduplicate EM database entries')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without deleting')
    parser.add_argument('--auto', action='store_true', help='Automatically keep best entry and archive duplicates')

    args = parser.parse_args()

    if not args.dry_run and not args.auto:
        print("ERROR: Must specify --dry-run or --auto")
        sys.exit(1)

    deduplicator = EMDeduplicator(dry_run=args.dry_run, auto_mode=args.auto)
    deduplicator.run()
