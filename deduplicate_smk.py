#!/usr/bin/env python3
"""
SMK Deduplication Script
Removes duplicate entries from SMK (Strategic Macro-Coordination) database.

Modes:
--dry-run: Show what would be deleted without deleting
--auto: Automatically keep best entry and archive duplicates
--manual: Manually choose which entry to keep

Safety:
- Creates backup before any changes
- Logs all deletions
- Can be rolled back with restore_smk_from_backup.py
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
    print("❌ ERROR: NOTION_API_KEY not found in environment")
    print("Set it with: set NOTION_API_KEY=your_key_here (Windows)")
    print("Or: export NOTION_API_KEY='your_key_here' (Linux/Mac)")
    sys.exit(1)

notion = Client(auth=NOTION_API_KEY)

# SMK Database ID
SMK_DATABASE_ID = 'ba1d4a4407a5425fafd81d27dc02cc1c'


class SMKDeduplicator:
    """Deduplicates SMK database entries."""

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
        """Fetch all entries from SMK database."""
        print("📥 Fetching all SMK entries...")

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

        print(f"   ✅ Fetched {len(self.entries)} entries\n")

    def extract_entry_data(self, entry):
        """Extract relevant data from entry."""
        props = entry['properties']

        name = ''
        if 'Name' in props and props['Name']['title']:
            name = props['Name']['title'][0]['plain_text']

        smk_number = None
        if 'SMK Number' in props and props['SMK Number']['number'] is not None:
            smk_number = props['SMK Number']['number']

        agent = None
        if 'Agent' in props and props['Agent']['select']:
            agent = props['Agent']['select']['name']

        date = None
        if 'Date' in props and props['Date']['date']:
            date = props['Date']['date']['start']

        status = None
        if 'Status' in props and props['Status']['select']:
            status = props['Status']['select']['name']

        commit_sha = ''
        if 'Commit SHA' in props and props['Commit SHA']['rich_text']:
            commit_sha = props['Commit SHA']['rich_text'][0]['plain_text'] if props['Commit SHA']['rich_text'] else ''

        github_url = ''
        if 'GitHub URL' in props and props['GitHub URL']['url']:
            github_url = props['GitHub URL']['url']

        tags = []
        if 'Tags' in props and props['Tags']['multi_select']:
            tags = [tag['name'] for tag in props['Tags']['multi_select']]

        # Count filled fields
        filled_fields = sum([
            bool(name),
            smk_number is not None,
            agent is not None,
            date is not None,
            status is not None,
            bool(commit_sha),
            bool(github_url),
            len(tags) > 0
        ])

        # Count relations
        relation_count = 0
        for prop_name, prop_data in props.items():
            if prop_data.get('type') == 'relation':
                relation_count += len(prop_data.get('relation', []))

        return {
            'id': entry['id'],
            'name': name,
            'smk_number': smk_number,
            'agent': agent,
            'date': date,
            'status': status,
            'commit_sha': commit_sha,
            'github_url': github_url,
            'tags': tags,
            'created_time': entry['created_time'],
            'last_edited_time': entry['last_edited_time'],
            'filled_fields': filled_fields,
            'relation_count': relation_count,
            'raw_entry': entry
        }

    def identify_duplicates(self):
        """Group entries by SMK Number to find duplicates."""
        print("🔍 Identifying duplicates by SMK Number...")

        for entry in self.entries:
            data = self.extract_entry_data(entry)
            if data['smk_number'] is not None:
                self.duplicates[data['smk_number']].append(data)

        # Keep only groups with 2+ entries
        self.duplicates = {
            k: v for k, v in self.duplicates.items()
            if len(v) > 1
        }

        print(f"   ✅ Found {len(self.duplicates)} duplicate groups\n")

    def score_entry(self, entry):
        """Score an entry to determine which is "best"."""
        score = 0

        # Most filled fields (40 points max)
        score += entry['filled_fields'] * 5

        # Most relations (30 points max)
        score += entry['relation_count'] * 3

        # Newest last edited (20 points)
        try:
            last_edited = datetime.fromisoformat(entry['last_edited_time'].replace('Z', '+00:00'))
            days_ago = (datetime.now(last_edited.tzinfo) - last_edited).days
            score += max(0, 20 - days_ago)  # More recent = higher score
        except:
            pass

        # Status bonus (10 points)
        if entry['status'] == 'COMPLETE':
            score += 10
        elif entry['status'] == 'IN_PROGRESS':
            score += 5

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
        print("🤖 AUTOMATIC MODE: Choosing best entry for each group...\n")

        for smk_num, entries in sorted(self.duplicates.items()):
            print(f"SMK #{smk_num} - {len(entries)} duplicates")

            best, others = self.choose_best_entry(entries)

            print(f"   ✅ KEEP:    {best['name']} (ID: {best['id'][:8]}...)")
            print(f"              Score: {self.score_entry(best)}, Filled: {best['filled_fields']}/8, Relations: {best['relation_count']}")
            print(f"              Last Edited: {best['last_edited_time']}")

            for other in others:
                print(f"   ❌ ARCHIVE: {other['name']} (ID: {other['id'][:8]}...)")
                print(f"              Score: {self.score_entry(other)}, Filled: {other['filled_fields']}/8, Relations: {other['relation_count']}")
                self.to_archive.append(other)

            self.to_keep.append(best)
            print()

    def process_duplicates_manual(self):
        """Manually process each duplicate group."""
        print("👤 MANUAL MODE: Choose which entry to keep for each group...\n")

        for smk_num, entries in sorted(self.duplicates.items()):
            print("="*70)
            print(f"SMK #{smk_num} - {len(entries)} duplicates")
            print("="*70)

            # Show all options
            for idx, entry in enumerate(entries, 1):
                print(f"\n[{idx}] {entry['name']}")
                print(f"    ID: {entry['id']}")
                print(f"    Agent: {entry['agent']}, Date: {entry['date']}, Status: {entry['status']}")
                print(f"    Filled Fields: {entry['filled_fields']}/8")
                print(f"    Relations: {entry['relation_count']}")
                print(f"    Last Edited: {entry['last_edited_time']}")
                print(f"    Score: {self.score_entry(entry)}")

            # Get user choice
            while True:
                try:
                    choice = input(f"\nWhich entry to KEEP? (1-{len(entries)}, or 's' to skip): ").strip()
                    if choice.lower() == 's':
                        print("⏭️  Skipped this group")
                        break

                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(entries):
                        keep_entry = entries[choice_idx]
                        others = [e for i, e in enumerate(entries) if i != choice_idx]

                        print(f"   ✅ KEEP:    {keep_entry['name']}")
                        for other in others:
                            print(f"   ❌ ARCHIVE: {other['name']}")
                            self.to_archive.append(other)

                        self.to_keep.append(keep_entry)
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(entries)}")
                except ValueError:
                    print("Invalid input. Please enter a number or 's'")

            print()

    def create_backup(self):
        """Create backup of all entries before making changes."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_file = f'smk_backup_{timestamp}.json'

        print(f"💾 Creating backup: {self.backup_file}")

        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'total_entries': len(self.entries),
            'entries': [self.extract_entry_data(e) for e in self.entries]
        }

        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)

        print(f"   ✅ Backup saved ({len(self.entries)} entries)\n")

    def archive_duplicates(self):
        """Archive (soft delete) duplicate entries."""
        if self.dry_run:
            print("🔍 DRY RUN: Would archive the following entries:")
            for entry in self.to_archive:
                print(f"   ❌ {entry['name']} (ID: {entry['id']})")
            print(f"\n   Total: {len(self.to_archive)} entries would be archived")
            print("   (Run without --dry-run to actually archive)")
            return

        print(f"🗑️  Archiving {len(self.to_archive)} duplicate entries...")

        archived_count = 0
        errors = []

        for entry in self.to_archive:
            try:
                # Archive the page (soft delete)
                notion.pages.update(
                    page_id=entry['id'],
                    archived=True
                )
                archived_count += 1
                print(f"   ✅ Archived: {entry['name']} (SMK #{entry['smk_number']})")
            except Exception as e:
                errors.append({
                    'entry': entry,
                    'error': str(e)
                })
                print(f"   ❌ Error archiving {entry['name']}: {e}")

        print(f"\n✅ Successfully archived: {archived_count}/{len(self.to_archive)} entries")

        if errors:
            print(f"❌ Errors: {len(errors)}")
            for err in errors:
                print(f"   • {err['entry']['name']}: {err['error']}")

        return archived_count, errors

    def create_log(self, archived_count, errors):
        """Create log of all changes made."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = f'smk_deduplication_log_{timestamp}.json'

        log_data = {
            'timestamp': datetime.now().isoformat(),
            'mode': 'auto' if self.auto_mode else 'manual',
            'dry_run': self.dry_run,
            'backup_file': self.backup_file,
            'stats': {
                'total_entries': len(self.entries),
                'duplicate_groups': len(self.duplicates),
                'entries_kept': len(self.to_keep),
                'entries_archived': archived_count,
                'errors': len(errors)
            },
            'archived_entries': [
                {
                    'id': e['id'],
                    'name': e['name'],
                    'smk_number': e['smk_number'],
                    'reason': 'duplicate'
                }
                for e in self.to_archive
            ],
            'kept_entries': [
                {
                    'id': e['id'],
                    'name': e['name'],
                    'smk_number': e['smk_number']
                }
                for e in self.to_keep
            ],
            'errors': errors
        }

        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Log saved to: {self.log_file}")

    def run(self):
        """Run deduplication process."""
        self.fetch_all_entries()
        self.identify_duplicates()

        if len(self.duplicates) == 0:
            print("✅ No duplicates found! SMK database is clean.")
            return True

        # Create backup (even for dry-run)
        if not self.dry_run:
            self.create_backup()

        # Process duplicates
        if self.auto_mode:
            self.process_duplicates_auto()
        else:
            self.process_duplicates_manual()

        # Archive duplicates
        if len(self.to_archive) > 0:
            archived_count, errors = self.archive_duplicates()

            if not self.dry_run:
                self.create_log(archived_count, errors)

            print("\n" + "="*70)
            print("📊 DEDUPLICATION SUMMARY")
            print("="*70)
            print(f"Total Entries: {len(self.entries)}")
            print(f"Duplicate Groups: {len(self.duplicates)}")
            print(f"Entries Kept: {len(self.to_keep)}")
            print(f"Entries Archived: {len(self.to_archive)}")
            if not self.dry_run:
                print(f"Backup File: {self.backup_file}")
                print(f"Log File: {self.log_file}")
            print("="*70)

            if not self.dry_run:
                print("\n✅ Deduplication complete!")
                print(f"   Run 'python analyze_smk_duplicates.py' to verify")
                print(f"   To rollback: python restore_smk_from_backup.py {self.backup_file}")
        else:
            print("No entries selected for archiving.")

        return True


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description='Deduplicate SMK database entries'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be deleted without deleting'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Automatically keep best entry and archive duplicates'
    )
    parser.add_argument(
        '--manual',
        action='store_true',
        help='Manually choose which entry to keep'
    )

    args = parser.parse_args()

    # Validate args
    if args.auto and args.manual:
        print("❌ Error: Cannot use both --auto and --manual")
        return 1

    if not args.auto and not args.manual:
        print("❌ Error: Must specify either --auto or --manual mode")
        print("\nUsage:")
        print("  python deduplicate_smk.py --dry-run --auto")
        print("  python deduplicate_smk.py --auto")
        print("  python deduplicate_smk.py --manual")
        return 1

    print("\n🧬 SMK DEDUPLICATION SCRIPT")
    print("="*70)
    print(f"Mode: {'AUTO' if args.auto else 'MANUAL'}")
    print(f"Dry Run: {'YES - No changes will be made' if args.dry_run else 'NO - Will archive duplicates'}")
    print("="*70)
    print()

    if not args.dry_run:
        confirm = input("⚠️  This will archive duplicate entries. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return 0

    deduplicator = SMKDeduplicator(dry_run=args.dry_run, auto_mode=args.auto)
    deduplicator.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
