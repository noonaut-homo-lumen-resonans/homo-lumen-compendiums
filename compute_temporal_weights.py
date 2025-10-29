#!/usr/bin/env python3
"""
Temporal Weight Computation Script
Computes temporal_weight_raw for all LPs in SLL (Shared Learning Library) database.

Formula (designed by Abacus):
- decay_factor = e^(-ln(2) * (age_days / half_life_days))
- reactivation_boost = 1 + (reactivation_count * 0.1)
- temporal_weight_raw = min(1.0, decay_factor * reactivation_boost)

Usage:
  python compute_temporal_weights.py --dry-run  # Preview changes
  python compute_temporal_weights.py           # Execute updates
"""

import os
import sys
import io
import math
import argparse
from datetime import datetime, timezone
from notion_client import Client
import json

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get Notion API key
NOTION_API_KEY = None
env_file = os.path.join(os.path.dirname(__file__), 'ama-backend', '.env')
if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('NOTION_API_KEY='):
                NOTION_API_KEY = line.split('=', 1)[1].strip()
                break

if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found in environment or .env file")
    sys.exit(1)

notion = Client(auth=NOTION_API_KEY)

# SLL Database ID
SLL_DATABASE_ID = '84da6cbd09d640fb868e41444b941991'

# Default half-life values by domain (days)
DEFAULT_HALF_LIFE = 120
DOMAIN_HALF_LIVES = {
    'code': 60,
    'technical': 60,
    'research': 180,
    'ethics': 365,
    'philosophy': 365,
    'architecture': 730,
    'genomos': 1095,
    'blockchain': 1095,
}

# Freshness thresholds
FRESH_THRESHOLD = 0.7
AGING_THRESHOLD = 0.3


class TemporalWeightComputer:
    """Computes temporal weights for Learning Points."""

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.lps = []
        self.updates = []
        self.stats = {
            'total_lps': 0,
            'updated': 0,
            'skipped': 0,
            'fresh': 0,
            'aging': 0,
            'stale': 0,
        }

    def fetch_all_lps(self):
        """Fetch all LPs from SLL database."""
        print("Fetching all LPs from SLL database...")

        has_more = True
        start_cursor = None

        while has_more:
            if start_cursor:
                response = notion.databases.query(
                    database_id=SLL_DATABASE_ID,
                    start_cursor=start_cursor
                )
            else:
                response = notion.databases.query(database_id=SLL_DATABASE_ID)

            self.lps.extend(response['results'])

            has_more = response.get('has_more', False)
            start_cursor = response.get('next_cursor')

        self.stats['total_lps'] = len(self.lps)
        print(f"   Fetched {self.stats['total_lps']} LPs\n")

    def extract_lp_data(self, lp):
        """Extract relevant data from LP entry."""
        props = lp['properties']

        # Get title
        title = 'Untitled'
        if 'Name' in props and props['Name']['title']:
            title = props['Name']['title'][0]['plain_text']
        elif 'Title' in props and props['Title']['title']:
            title = props['Title']['title'][0]['plain_text']

        # Get created date
        created_time = datetime.fromisoformat(lp['created_time'].replace('Z', '+00:00'))

        # Get current temporal_weight_raw (if exists)
        current_weight = None
        if 'temporal_weight_raw' in props and props['temporal_weight_raw']['number'] is not None:
            current_weight = props['temporal_weight_raw']['number']

        # Get half_life_days (default 120)
        half_life = DEFAULT_HALF_LIFE
        if 'half_life_days' in props and props['half_life_days']['number'] is not None:
            half_life = props['half_life_days']['number']

        # Get reactivation_count (default 0)
        reactivation_count = 0
        if 'reactivation_count' in props and props['reactivation_count']['number'] is not None:
            reactivation_count = props['reactivation_count']['number']

        # Get last_cited_timestamp
        last_cited = None
        if 'last_cited_timestamp' in props and props['last_cited_timestamp']['date']:
            last_cited = props['last_cited_timestamp']['date']['start']

        # Get current freshness_status
        current_freshness = None
        if 'freshness_status' in props and props['freshness_status']['select']:
            current_freshness = props['freshness_status']['select']['name']

        return {
            'id': lp['id'],
            'title': title,
            'created_time': created_time,
            'current_weight': current_weight,
            'half_life_days': half_life,
            'reactivation_count': reactivation_count,
            'last_cited': last_cited,
            'current_freshness': current_freshness,
        }

    def compute_temporal_weight(self, lp_data):
        """Compute temporal weight using Abacus' formula."""
        # Calculate age in days
        now = datetime.now(timezone.utc)
        age_days = (now - lp_data['created_time']).days

        # Get half-life
        half_life_days = lp_data['half_life_days']

        # Calculate decay factor (exponential decay)
        # Formula: e^(-ln(2) * (age_days / half_life_days))
        # Equivalent to: 0.5^(age_days / half_life_days)
        decay_factor = math.exp(-math.log(2) * (age_days / half_life_days))

        # Calculate reactivation boost
        # Each citation adds 10% boost
        reactivation_boost = 1 + (lp_data['reactivation_count'] * 0.1)

        # Final temporal weight (clamped to 0.0-1.0)
        temporal_weight_raw = min(1.0, decay_factor * reactivation_boost)

        return temporal_weight_raw, age_days, decay_factor

    def determine_freshness(self, temporal_weight):
        """Determine freshness status based on temporal weight."""
        if temporal_weight >= FRESH_THRESHOLD:
            return 'fresh'
        elif temporal_weight >= AGING_THRESHOLD:
            return 'aging'
        else:
            return 'stale'

    def compute_all_weights(self):
        """Compute temporal weights for all LPs."""
        print("Computing temporal weights...\n")
        print("="*70)

        for lp in self.lps:
            lp_data = self.extract_lp_data(lp)

            # Compute new weight
            new_weight, age_days, decay_factor = self.compute_temporal_weight(lp_data)
            new_freshness = self.determine_freshness(new_weight)

            # Determine if update needed
            weight_changed = lp_data['current_weight'] != new_weight
            freshness_changed = lp_data['current_freshness'] != new_freshness

            if weight_changed or freshness_changed:
                self.updates.append({
                    'id': lp_data['id'],
                    'title': lp_data['title'],
                    'age_days': age_days,
                    'half_life_days': lp_data['half_life_days'],
                    'reactivation_count': lp_data['reactivation_count'],
                    'decay_factor': decay_factor,
                    'old_weight': lp_data['current_weight'],
                    'new_weight': new_weight,
                    'old_freshness': lp_data['current_freshness'],
                    'new_freshness': new_freshness,
                })

                self.stats['updated'] += 1
                self.stats[new_freshness] += 1
            else:
                self.stats['skipped'] += 1

    def print_updates(self):
        """Print all computed updates."""
        if not self.updates:
            print("\nNo updates needed - all LPs have current temporal weights")
            return

        print(f"\n{len(self.updates)} LPs need updates:\n")

        for i, update in enumerate(self.updates[:10], 1):  # Show first 10
            print(f"[{i}] {update['title'][:60]}")
            print(f"    Age: {update['age_days']} days | Half-life: {update['half_life_days']} days")
            print(f"    Reactivations: {update['reactivation_count']}")
            print(f"    Decay factor: {update['decay_factor']:.4f}")
            print(f"    Weight: {update['old_weight'] or 'N/A'} -> {update['new_weight']:.4f}")
            print(f"    Status: {update['old_freshness'] or 'N/A'} -> {update['new_freshness']}")
            print()

        if len(self.updates) > 10:
            print(f"... and {len(self.updates) - 10} more\n")

    def apply_updates(self):
        """Apply updates to Notion database."""
        if not self.updates:
            print("\nNo updates to apply")
            return

        print(f"\nApplying {len(self.updates)} updates to Notion...")

        updated_count = 0
        errors = []

        for update in self.updates:
            try:
                notion.pages.update(
                    page_id=update['id'],
                    properties={
                        'temporal_weight_raw': {'number': update['new_weight']},
                        'freshness_status': {'select': {'name': update['new_freshness']}},
                    }
                )
                updated_count += 1

                # Progress indicator every 10 updates
                if updated_count % 10 == 0:
                    print(f"   Updated {updated_count}/{len(self.updates)}...")

            except Exception as e:
                errors.append({
                    'title': update['title'],
                    'error': str(e)
                })

        print(f"\n   Successfully updated: {updated_count}/{len(self.updates)}")

        if errors:
            print(f"\n   Errors: {len(errors)}")
            for err in errors[:5]:
                print(f"      - {err['title']}: {err['error']}")

    def print_summary(self):
        """Print summary statistics."""
        print("\n" + "="*70)
        print("TEMPORAL WEIGHT COMPUTATION SUMMARY")
        print("="*70)
        print(f"Total LPs: {self.stats['total_lps']}")
        print(f"Updates needed: {self.stats['updated']}")
        print(f"Already current: {self.stats['skipped']}")
        print()
        print(f"Freshness distribution (after update):")
        print(f"   Fresh (>= 0.7): {self.stats['fresh']}")
        print(f"   Aging (0.3-0.7): {self.stats['aging']}")
        print(f"   Stale (< 0.3): {self.stats['stale']}")
        print("="*70)

    def run(self):
        """Run complete computation workflow."""
        self.fetch_all_lps()
        self.compute_all_weights()
        self.print_updates()

        if self.dry_run:
            print("\nDRY RUN: No changes made to Notion database")
            print("Run without --dry-run to apply updates")
        else:
            self.apply_updates()

        self.print_summary()


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description='Compute temporal weights for LPs in SLL database'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without updating database'
    )

    args = parser.parse_args()

    print("\n" + "="*70)
    print("TEMPORAL WEIGHT COMPUTATION SCRIPT")
    print("="*70)
    print(f"Mode: {'DRY RUN - No changes will be made' if args.dry_run else 'LIVE - Will update database'}")
    print("="*70)
    print()

    computer = TemporalWeightComputer(dry_run=args.dry_run)
    computer.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
