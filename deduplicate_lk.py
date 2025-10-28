#!/usr/bin/env python3
"""
Deduplicate Living Compendiums (LK) entries in Notion database.

This script removes duplicate LK entries by LK Number, keeping the best version
based on a weighted scoring algorithm.

Scoring factors:
- Filled fields (5 points each)
- Number of relations (3 points each)
- Recency (up to 20 points - newer = better)

Usage:
    python deduplicate_lk.py --dry-run          # Preview what will be done
    python deduplicate_lk.py --dry-run --auto   # Preview with auto-selection
    python deduplicate_lk.py --auto             # Execute with auto-selection
    python deduplicate_lk.py                    # Interactive mode

Environment Variables:
    NOTION_API_KEY: Your Notion integration API key

Author: Code (Claude Code Agent)
Date: 28. oktober 2025
"""

import os
import sys
import io
import json
import argparse
from datetime import datetime
from collections import defaultdict
from notion_client import Client

# Force UTF-8 encoding for stdout (Windows compatibility)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
if not NOTION_API_KEY:
    # Use provided key
    NOTION_API_KEY = '***REMOVED***'
LK_DATABASE_ID = '784556781fc14a14afc733f4eb51e0bc'  # Living Compendiums database (CORRECT ID)

if not NOTION_API_KEY:
    print("❌ ERROR: NOTION_API_KEY not found in environment")
    print("\nSet it with:")
    print("  set NOTION_API_KEY=your_key_here")
    exit(1)

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)

class LKDeduplicator:
    def __init__(self, dry_run=False, auto_select=False):
        self.entries = []
        self.duplicates = defaultdict(list)
        self.to_keep = []
        self.to_archive = []
        self.dry_run = dry_run
        self.auto_select = auto_select

    def fetch_all_lk_entries(self):
        """Fetch all active entries from LK database."""
        print("\n🔍 Fetching all LK entries...")

        has_more = True
        start_cursor = None

        while has_more:
            try:
                if start_cursor:
                    response = notion.databases.query(
                        database_id=LK_DATABASE_ID,
                        start_cursor=start_cursor
                    )
                else:
                    response = notion.databases.query(database_id=LK_DATABASE_ID)

                # Only include non-archived entries
                active_entries = [e for e in response['results'] if not e.get('archived', False)]
                self.entries.extend(active_entries)

                has_more = response.get('has_more', False)
                start_cursor = response.get('next_cursor')

            except Exception as e:
                print(f"❌ Error fetching entries: {e}")
                return False

        print(f"✅ Fetched {len(self.entries)} active entries")
        return True

    def extract_lk_data(self, entry):
        """Extract LK data from Notion entry."""
        props = entry.get('properties', {})

        # LK Number (from Name/title property)
        lk_number = None
        name_prop = props.get('Name', {})
        if name_prop.get('title'):
            lk_number = name_prop['title'][0].get('text', {}).get('content', '')

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
            'lk_number': lk_number or 'NO_NUMBER',
            'title': title,
            'agent': agent,
            'date': date,
            'relation_count': relation_count,
            'filled_fields': filled_fields,
            'last_edited_time': entry.get('last_edited_time'),
        }

    def find_duplicates(self):
        """Group entries by LK Number to find duplicates."""
        print("\n🔎 Finding duplicates...")

        lk_groups = defaultdict(list)

        for entry in self.entries:
            lk_data = self.extract_lk_data(entry)
            lk_groups[lk_data['lk_number']].append(lk_data)

        # Keep only groups with duplicates
        for lk_number, entries in lk_groups.items():
            if len(entries) > 1:
                self.duplicates[lk_number] = entries

        unique_count = len(lk_groups) - len(self.duplicates)
        duplicate_count = sum(len(entries) for entries in self.duplicates.values())

        print(f"\n📊 Found:")
        print(f"   Unique entries: {unique_count}")
        print(f"   Duplicate entries: {duplicate_count}")
        print(f"   Duplicate groups: {len(self.duplicates)}")

        return len(self.duplicates) > 0

    def score_entry(self, entry):
        """Calculate quality score for an entry."""
        score = 0

        # Filled fields (5 points each, max ~40 points)
        score += entry['filled_fields'] * 5

        # Relations (3 points each, max ~30 points)
        score += entry['relation_count'] * 3

        # Recency (20 points max)
        try:
            last_edited = datetime.fromisoformat(entry['last_edited_time'].replace('Z', '+00:00'))
            days_ago = (datetime.now(last_edited.tzinfo) - last_edited).days
            recency_score = max(0, 20 - days_ago)
            score += recency_score
        except:
            pass

        return score

    def select_best_entries(self):
        """For each duplicate group, select the best entry to keep."""
        print("\n🎯 Selecting best entries...")

        for lk_number, entries in self.duplicates.items():
            # Calculate scores
            scored_entries = []
            for entry in entries:
                score = self.score_entry(entry)
                scored_entries.append((entry, score))

            # Sort by score (highest first)
            scored_entries.sort(key=lambda x: x[1], reverse=True)

            if self.auto_select:
                # Auto-select highest score
                best_entry, best_score = scored_entries[0]
                self.to_keep.append(best_entry)

                for entry, score in scored_entries[1:]:
                    self.to_archive.append(entry)

                print(f"  {lk_number}: Auto-selected entry with score {best_score}")

            else:
                # Interactive selection
                print(f"\n{'='*70}")
                print(f"LK Number: {lk_number} ({len(entries)} copies)")
                print(f"{'='*70}")

                for i, (entry, score) in enumerate(scored_entries, 1):
                    print(f"\n  [{i}] Score: {score}")
                    print(f"      Title: {entry['title'][:60]}...")
                    print(f"      Agent: {entry['agent']}")
                    print(f"      Date: {entry['date']}")
                    print(f"      Relations: {entry['relation_count']}")
                    print(f"      Filled: {entry['filled_fields']}")
                    print(f"      Edited: {entry['last_edited_time']}")

                # Ask user to select
                while True:
                    choice = input(f"\n  Keep which entry? [1-{len(entries)}] or 'a' for auto: ").strip()

                    if choice.lower() == 'a':
                        best_entry, best_score = scored_entries[0]
                        self.to_keep.append(best_entry)
                        for entry, score in scored_entries[1:]:
                            self.to_archive.append(entry)
                        print(f"  ✅ Auto-selected entry 1 (score {best_score})")
                        break
                    elif choice.isdigit() and 1 <= int(choice) <= len(entries):
                        idx = int(choice) - 1
                        self.to_keep.append(scored_entries[idx][0])
                        for i, (entry, score) in enumerate(scored_entries):
                            if i != idx:
                                self.to_archive.append(entry)
                        print(f"  ✅ Keeping entry {choice}")
                        break
                    else:
                        print("  Invalid choice. Try again.")

        print(f"\n✅ Selection complete:")
        print(f"   To keep: {len(self.to_keep)}")
        print(f"   To archive: {len(self.to_archive)}")

    def save_backup(self):
        """Save backup of entries to be archived."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'lk_backup_{timestamp}.json'

        backup = {
            'timestamp': timestamp,
            'to_archive': [entry['id'] for entry in self.to_archive],
            'entries': self.to_archive
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(backup, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Backup saved to: {filename}")
        return filename

    def archive_duplicates(self):
        """Archive duplicate entries."""
        if self.dry_run:
            print("\n🔍 DRY RUN - Would archive these entries:")
            for entry in self.to_archive:
                print(f"  - {entry['lk_number']}: {entry['title'][:50]}...")
            return True

        print("\n🗄️  Archiving duplicates...")

        success_count = 0
        fail_count = 0

        for entry in self.to_archive:
            try:
                notion.pages.update(
                    page_id=entry['id'],
                    archived=True
                )
                print(f"  ✅ Archived: {entry['lk_number']}")
                success_count += 1
            except Exception as e:
                print(f"  ❌ Failed: {entry['lk_number']} - {e}")
                fail_count += 1

        print(f"\n📊 Results:")
        print(f"   Archived: {success_count}")
        print(f"   Failed: {fail_count}")

        return fail_count == 0

def main():
    parser = argparse.ArgumentParser(description='Deduplicate LK entries in Notion')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    parser.add_argument('--auto', action='store_true', help='Automatically select best entries')
    args = parser.parse_args()

    print("="*70)
    print("  Living Compendiums (LK) Deduplication")
    print("="*70)

    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made")

    deduper = LKDeduplicator(dry_run=args.dry_run, auto_select=args.auto)

    # Fetch all entries
    if not deduper.fetch_all_lk_entries():
        return

    # Find duplicates
    if not deduper.find_duplicates():
        print("\n✅ No duplicates found - database is clean!")
        return

    # Select best entries
    deduper.select_best_entries()

    if not args.dry_run:
        # Save backup
        backup_file = deduper.save_backup()

        # Confirm (skip if auto mode)
        if not args.auto:
            print("\n⚠️  WARNING: This will archive duplicate entries!")
            print(f"   Backup saved to: {backup_file}")
            confirm = input("\n  Proceed with archiving? [y/N]: ").strip().lower()

            if confirm != 'y':
                print("\n❌ Cancelled by user")
                return
        else:
            print("\n⚠️  AUTO MODE: Proceeding with archiving...")
            print(f"   Backup saved to: {backup_file}")

    # Archive duplicates
    if deduper.archive_duplicates():
        print("\n✅ Deduplication complete!")
        if not args.dry_run:
            print(f"\n💡 To restore: python restore_lk_from_backup.py {backup_file}")
    else:
        print("\n⚠️  Deduplication completed with errors")

if __name__ == '__main__':
    main()
