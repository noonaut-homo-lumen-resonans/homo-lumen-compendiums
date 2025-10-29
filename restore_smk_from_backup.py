#!/usr/bin/env python3
"""
SMK Restore Script
Restores SMK entries from backup file after deduplication.

This script unarchives entries that were archived during deduplication,
effectively rolling back the changes.

Usage:
    python restore_smk_from_backup.py smk_backup_YYYYMMDD_HHMMSS.json
    python restore_smk_from_backup.py smk_backup_YYYYMMDD_HHMMSS.json --log smk_deduplication_log_YYYYMMDD_HHMMSS.json
"""

import os
import sys
import io
from notion_client import Client
from datetime import datetime
import json
import argparse

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


class SMKRestorer:
    """Restores SMK entries from backup."""

    def __init__(self, backup_file, log_file=None):
        self.backup_file = backup_file
        self.log_file = log_file
        self.backup_data = None
        self.log_data = None
        self.archived_ids = []
        self.restored = []
        self.errors = []

    def load_backup(self):
        """Load backup file."""
        print(f"📥 Loading backup: {self.backup_file}")

        try:
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                self.backup_data = json.load(f)

            print(f"   ✅ Backup loaded: {self.backup_data['total_entries']} entries")
            print(f"      Created: {self.backup_data['timestamp']}")
            print()
        except FileNotFoundError:
            print(f"   ❌ Error: Backup file not found: {self.backup_file}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"   ❌ Error: Invalid JSON in backup file")
            sys.exit(1)

    def load_log(self):
        """Load deduplication log if provided."""
        if not self.log_file:
            print("⚠️  No log file provided, will attempt to restore all archived entries")
            print()
            return

        print(f"📥 Loading log: {self.log_file}")

        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.log_data = json.load(f)

            archived_entries = self.log_data.get('archived_entries', [])
            self.archived_ids = [e['id'] for e in archived_entries]

            print(f"   ✅ Log loaded: {len(self.archived_ids)} archived entries")
            print(f"      Timestamp: {self.log_data['timestamp']}")
            print()
        except FileNotFoundError:
            print(f"   ⚠️  Warning: Log file not found: {self.log_file}")
            print("   Will attempt to restore all archived entries from backup")
            print()
        except json.JSONDecodeError:
            print(f"   ❌ Error: Invalid JSON in log file")
            sys.exit(1)

    def find_archived_entries(self):
        """Find which entries were archived."""
        if self.archived_ids:
            # Use log file data
            print(f"🔍 Using log file to identify {len(self.archived_ids)} archived entries\n")
            return

        # No log file - check each entry to see if it's archived
        print("🔍 Scanning for archived entries...")

        for entry_data in self.backup_data['entries']:
            entry_id = entry_data['id']

            try:
                # Try to retrieve the page
                page = notion.pages.retrieve(page_id=entry_id)

                # Check if it's archived
                if page.get('archived', False):
                    self.archived_ids.append(entry_id)
                    print(f"   Found archived: {entry_data.get('name', 'Unnamed')} (SMK #{entry_data.get('smk_number', '?')})")

            except Exception as e:
                print(f"   ⚠️  Could not check {entry_id}: {e}")

        print(f"\n   ✅ Found {len(self.archived_ids)} archived entries\n")

    def restore_entries(self):
        """Unarchive archived entries."""
        if len(self.archived_ids) == 0:
            print("✅ No archived entries found. Nothing to restore.")
            return

        print(f"🔄 Restoring {len(self.archived_ids)} entries...\n")

        for entry_id in self.archived_ids:
            # Find entry data in backup
            entry_data = next(
                (e for e in self.backup_data['entries'] if e['id'] == entry_id),
                None
            )

            if not entry_data:
                print(f"   ⚠️  Warning: Entry {entry_id} not found in backup")
                continue

            try:
                # Unarchive the page
                notion.pages.update(
                    page_id=entry_id,
                    archived=False
                )

                self.restored.append(entry_data)
                print(f"   ✅ Restored: {entry_data.get('name', 'Unnamed')} (SMK #{entry_data.get('smk_number', '?')})")

            except Exception as e:
                self.errors.append({
                    'id': entry_id,
                    'name': entry_data.get('name', 'Unknown'),
                    'error': str(e)
                })
                print(f"   ❌ Error restoring {entry_data.get('name', entry_id)}: {e}")

    def verify_restoration(self):
        """Verify that entries were restored successfully."""
        print(f"\n🔍 Verifying restoration...")

        verified = 0
        failed = 0

        for entry_data in self.restored:
            entry_id = entry_data['id']

            try:
                page = notion.pages.retrieve(page_id=entry_id)

                if not page.get('archived', False):
                    verified += 1
                else:
                    failed += 1
                    print(f"   ❌ Entry still archived: {entry_data.get('name', entry_id)}")

            except Exception as e:
                failed += 1
                print(f"   ❌ Could not verify {entry_data.get('name', entry_id)}: {e}")

        print(f"   ✅ Verified: {verified}/{len(self.restored)} entries")

        if failed > 0:
            print(f"   ❌ Failed: {failed} entries")

    def create_restore_log(self):
        """Create log of restoration."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        restore_log_file = f'smk_restore_log_{timestamp}.json'

        log_data = {
            'timestamp': datetime.now().isoformat(),
            'backup_file': self.backup_file,
            'log_file': self.log_file,
            'stats': {
                'entries_to_restore': len(self.archived_ids),
                'entries_restored': len(self.restored),
                'errors': len(self.errors)
            },
            'restored_entries': self.restored,
            'errors': self.errors
        }

        with open(restore_log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Restore log saved to: {restore_log_file}")

    def print_summary(self):
        """Print restoration summary."""
        print("\n" + "="*70)
        print("📊 RESTORATION SUMMARY")
        print("="*70)
        print(f"Backup File: {self.backup_file}")
        if self.log_file:
            print(f"Log File: {self.log_file}")
        print(f"Entries to Restore: {len(self.archived_ids)}")
        print(f"Entries Restored: {len(self.restored)}")
        print(f"Errors: {len(self.errors)}")
        print("="*70)

        if self.errors:
            print("\n❌ Errors encountered:")
            for err in self.errors:
                print(f"   • {err['name']}: {err['error']}")
            print()

    def run(self):
        """Run restoration process."""
        self.load_backup()
        self.load_log()
        self.find_archived_entries()

        if len(self.archived_ids) == 0:
            return True

        confirm = input(f"⚠️  This will restore {len(self.archived_ids)} archived entries. Continue? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return False

        self.restore_entries()
        self.verify_restoration()
        self.create_restore_log()
        self.print_summary()

        print("\n✅ Restoration complete!")
        print("   Run 'python analyze_smk_duplicates.py' to check for duplicates again")

        return True


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description='Restore SMK entries from backup'
    )
    parser.add_argument(
        'backup_file',
        help='Path to backup JSON file (smk_backup_YYYYMMDD_HHMMSS.json)'
    )
    parser.add_argument(
        '--log',
        help='Path to deduplication log file (optional)',
        default=None
    )

    args = parser.parse_args()

    print("\n🔄 SMK RESTORE SCRIPT")
    print("="*70)
    print()

    restorer = SMKRestorer(args.backup_file, args.log)
    success = restorer.run()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
