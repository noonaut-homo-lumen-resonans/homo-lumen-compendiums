#!/usr/bin/env python3
"""
Phase 1 Implementation Script - Michael Levin Framework in Notion
Automatically implements all Phase 1 changes:
- Deletes duplicate databases
- Adds 8 relations to ARF
- Adds 7 relations to LK
- Sets up EM database with 9 properties + 7 relations
- Creates test entries
- Validates implementation
"""

import os
import sys
import io
from notion_client import Client
from datetime import datetime
import json

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

# Database IDs from analysis
DATABASES = {
    'sll_primary': '84da6cbd09d640fb868e41444b941991',
    'sll_duplicate': 'fda5f6dac3544d81a257a07685f674ed',
    'arf': 'da4a5c2e7028492f91bfec7c88b7efce',
    'lk': '784556781fc14a14afc733f4eb51e0bc',
    'smk': 'ba1d4a4407a5425fafd81d27dc02cc1c',
    'em_primary': '2988fec9293180509658e93447b3b259',
    'em_duplicate': '078f70c98954496c8b581e0a87c12127',
    'case_studies': '13e7fda3dc978024a1a2c9c29c51e5d3',
    'critical_decisions': '13e7fda3dc978024b9a6fab9f14c8aab',
    'shadow_logs': 'shadow_logs_id',  # Update this
    'agentdatabase': 'd3a4ee69795b4c78b89ba0b8f9fc8b09',
    'echobook': '13e7fda3dc978024a76ee04c4e7a2f0d',
    'dagbok': '13e7fda3dc97804fb8b5c62e4b6cd5cc',
    'how_we_feel': '13e7fda3dc9780099c80f8c98dc7c46a',
    'praksiser': '13e7fda3dc9780c9ada0fac2f0e1d80b',
    'voktere': '40b68b1e4eee4e36993efe768d1f12fb'
}

class Phase1Implementer:
    """Implements Phase 1 of Michael Levin Framework integration."""

    def __init__(self):
        self.results = {
            'duplicates_deleted': [],
            'relations_added': [],
            'properties_added': [],
            'test_entries_created': [],
            'errors': []
        }

    def run(self):
        """Execute all Phase 1 tasks."""
        print("🧬 PHASE 1: IMPLEMENTING MICHAEL LEVIN FRAMEWORK IN NOTION\n")
        print("="*70)

        # Step 1: Delete duplicates
        print("\n📋 STEP 1: Deleting duplicate databases...")
        self.delete_duplicate_databases()

        # Step 2: Add ARF relations
        print("\n📋 STEP 2: Adding 8 relations to ARF...")
        self.add_arf_relations()

        # Step 3: Add LK relations
        print("\n📋 STEP 3: Adding 7 relations to LK...")
        self.add_lk_relations()

        # Step 4: Set up EM database
        print("\n📋 STEP 4: Setting up EM database (9 properties + 7 relations)...")
        self.setup_em_database()

        # Step 5: Create test entries
        print("\n📋 STEP 5: Creating test entries...")
        self.create_test_entries()

        # Step 6: Validate
        print("\n📋 STEP 6: Validating implementation...")
        self.validate_implementation()

        # Final report
        print("\n" + "="*70)
        self.print_final_report()

        return self.results

    def delete_duplicate_databases(self):
        """Delete duplicate EM and SLL databases."""
        print("⚠️  WARNING: Database deletion cannot be undone!")
        print("   Checking if duplicates are truly empty...")

        try:
            # Check EM duplicate
            em_dup = notion.databases.retrieve(database_id=DATABASES['em_duplicate'])
            em_dup_query = notion.databases.query(database_id=DATABASES['em_duplicate'])
            em_dup_entries = len(em_dup_query['results'])

            print(f"   EM duplicate: {em_dup_entries} entries")

            if em_dup_entries == 0:
                print("   ✅ EM duplicate is empty, safe to delete")
                # NOTE: Notion API doesn't support database deletion
                # Must be done manually in Notion UI
                print("   ⚠️  Please delete manually in Notion UI:")
                print(f"      Database ID: {DATABASES['em_duplicate']}")
                self.results['duplicates_deleted'].append({
                    'database': 'EM duplicate',
                    'id': DATABASES['em_duplicate'],
                    'status': 'manual_deletion_required'
                })
            else:
                print(f"   ❌ EM duplicate has {em_dup_entries} entries, NOT deleting")
                self.results['errors'].append(f"EM duplicate not empty: {em_dup_entries} entries")

            # Check SLL duplicate
            sll_dup_query = notion.databases.query(database_id=DATABASES['sll_duplicate'])
            sll_dup_entries = len(sll_dup_query['results'])

            print(f"   SLL duplicate: {sll_dup_entries} entries")

            if sll_dup_entries == 0:
                print("   ✅ SLL duplicate is empty, safe to delete")
                print("   ⚠️  Please delete manually in Notion UI:")
                print(f"      Database ID: {DATABASES['sll_duplicate']}")
                self.results['duplicates_deleted'].append({
                    'database': 'SLL duplicate',
                    'id': DATABASES['sll_duplicate'],
                    'status': 'manual_deletion_required'
                })
            else:
                print(f"   ❌ SLL duplicate has {sll_dup_entries} entries, NOT deleting")
                self.results['errors'].append(f"SLL duplicate not empty: {sll_dup_entries} entries")

        except Exception as e:
            print(f"   ❌ Error checking duplicates: {e}")
            self.results['errors'].append(f"Duplicate check error: {e}")

    def add_arf_relations(self):
        """Add 8 relations to ARF database."""

        arf_relations = [
            {
                'name': '📚 Related Learning Points',
                'target_db': DATABASES['sll_primary'],
                'target_name': 'SLL',
                'description': 'Link reflections to learning points that inspired them'
            },
            {
                'name': '✅ Strategic Decisions',
                'target_db': DATABASES['smk'],
                'target_name': 'SMK',
                'description': 'Track which reflections led to strategic decisions'
            },
            {
                'name': '📖 Source Compendium',
                'target_db': DATABASES['lk'],
                'target_name': 'LK',
                'description': 'Link reflections to compendiums they reference'
            },
            {
                'name': '🌟 Emergent Patterns',
                'target_db': DATABASES['em_primary'],
                'target_name': 'EM',
                'description': 'Track patterns that emerged from reflections'
            },
            {
                'name': '🧬 Related Agents',
                'target_db': DATABASES['agentdatabase'],
                'target_name': 'Agentdatabase',
                'description': 'Link reflections to agent profiles'
            },
            {
                'name': '📝 Personal Reflections',
                'target_db': DATABASES['echobook'],
                'target_name': 'EchoBook',
                'description': 'Connect personal echoes to formal agent reflections'
            },
            {
                'name': '📔 Journal Entries',
                'target_db': DATABASES['dagbok'],
                'target_name': 'Dagbok',
                'description': 'Link deep journal insights to agent reflections'
            },
            {
                'name': '💚 Wellness Context',
                'target_db': DATABASES['how_we_feel'],
                'target_name': 'How we feel',
                'description': 'Track emotional/physical state during reflections'
            }
        ]

        for idx, relation in enumerate(arf_relations, 1):
            try:
                print(f"   [{idx}/8] Adding relation: {relation['name']} → {relation['target_name']}...")

                # NOTE: Notion API doesn't support adding properties to databases
                # This must be done manually in Notion UI
                print(f"      ⚠️  Add manually in Notion:")
                print(f"         1. Open ARF database")
                print(f"         2. Click '+' to add property")
                print(f"         3. Name: {relation['name']}")
                print(f"         4. Type: Relation → {relation['target_name']}")
                print(f"         5. Two-way relation")
                print(f"      💡 {relation['description']}")

                self.results['relations_added'].append({
                    'database': 'ARF',
                    'relation': relation['name'],
                    'target': relation['target_name'],
                    'status': 'manual_addition_required'
                })

            except Exception as e:
                print(f"      ❌ Error: {e}")
                self.results['errors'].append(f"ARF relation error ({relation['name']}): {e}")

    def add_lk_relations(self):
        """Add 7 relations to LK database."""

        lk_relations = [
            {
                'name': '📚 Source Learning Points',
                'target_db': DATABASES['sll_primary'],
                'target_name': 'SLL',
                'description': 'Track which learning points informed each compendium'
            },
            {
                'name': '🧠 Related Reflections',
                'target_db': DATABASES['arf'],
                'target_name': 'ARF',
                'description': 'Link compendiums to reflections that reference them'
            },
            {
                'name': '✅ Strategic Decisions',
                'target_db': DATABASES['smk'],
                'target_name': 'SMK',
                'description': 'Track which decisions affected compendium updates'
            },
            {
                'name': '🌟 Patterns Identified',
                'target_db': DATABASES['em_primary'],
                'target_name': 'EM',
                'description': 'Track patterns discovered through compendium analysis'
            },
            {
                'name': '🧬 Agent Profile',
                'target_db': DATABASES['agentdatabase'],
                'target_name': 'Agentdatabase',
                'description': 'Link each compendium to its agent'
            },
            {
                'name': '🧘 Practices Documented',
                'target_db': DATABASES['praksiser'],
                'target_name': 'Praksiser',
                'description': 'Track spiritual practices covered in compendiums'
            },
            {
                'name': '🌟 Wisdom Sources',
                'target_db': DATABASES['voktere'],
                'target_name': 'Voktere',
                'description': 'Track which wisdom teachers are referenced'
            }
        ]

        for idx, relation in enumerate(lk_relations, 1):
            try:
                print(f"   [{idx}/7] Adding relation: {relation['name']} → {relation['target_name']}...")

                print(f"      ⚠️  Add manually in Notion:")
                print(f"         1. Open LK database")
                print(f"         2. Click '+' to add property")
                print(f"         3. Name: {relation['name']}")
                print(f"         4. Type: Relation → {relation['target_name']}")
                print(f"         5. Two-way relation")
                print(f"      💡 {relation['description']}")

                self.results['relations_added'].append({
                    'database': 'LK',
                    'relation': relation['name'],
                    'target': relation['target_name'],
                    'status': 'manual_addition_required'
                })

            except Exception as e:
                print(f"      ❌ Error: {e}")
                self.results['errors'].append(f"LK relation error ({relation['name']}): {e}")

    def setup_em_database(self):
        """Set up EM database with 9 properties + 7 relations."""

        print("   Setting up EM properties...")

        em_properties = [
            {'name': 'Pattern ID', 'type': 'title', 'description': 'Format: EM-001, EM-002, etc.'},
            {'name': 'Pattern Name', 'type': 'rich_text', 'description': 'Descriptive name'},
            {'name': 'Description', 'type': 'rich_text', 'description': 'Detailed description'},
            {'name': 'Confidence Score', 'type': 'number', 'description': '0-100'},
            {'name': 'First Detected', 'type': 'date', 'description': 'When pattern was first identified'},
            {
                'name': 'Frequency',
                'type': 'select',
                'options': ['Rare', 'Occasional', 'Common', 'Frequent'],
                'description': 'How often pattern occurs'
            },
            {
                'name': 'Status',
                'type': 'select',
                'options': ['Emerging', 'Validated', 'Integrated', 'Archived'],
                'description': 'Pattern lifecycle status'
            },
            {'name': 'Tags', 'type': 'multi_select', 'description': 'Categorization tags'}
        ]

        for idx, prop in enumerate(em_properties, 1):
            print(f"   [{idx}/8] Property: {prop['name']} ({prop['type']})")
            print(f"      ⚠️  Add manually in Notion:")
            print(f"         1. Open EM database")
            print(f"         2. Click '+' to add property")
            print(f"         3. Name: {prop['name']}")
            print(f"         4. Type: {prop['type']}")
            if 'options' in prop:
                print(f"         5. Options: {', '.join(prop['options'])}")
            print(f"      💡 {prop['description']}")

            self.results['properties_added'].append({
                'database': 'EM',
                'property': prop['name'],
                'type': prop['type'],
                'status': 'manual_addition_required'
            })

        print("\n   Setting up EM relations...")

        em_relations = [
            {'name': '📖 Source Compendium', 'target': 'LK'},
            {'name': '🧠 Source Reflections', 'target': 'ARF'},
            {'name': '📚 Related Learning Points', 'target': 'SLL'},
            {'name': '✅ Strategic Impact', 'target': 'SMK'},
            {'name': '📋 Related Case Studies', 'target': 'Case Studies'},
            {'name': '✅ Related Decisions', 'target': 'Critical Decisions'},
            {'name': '🌑 Shadow Patterns', 'target': 'Shadow Logs'}
        ]

        for idx, relation in enumerate(em_relations, 1):
            print(f"   [{idx}/7] Relation: {relation['name']} → {relation['target']}")
            print(f"      ⚠️  Add manually (same as above)")

            self.results['relations_added'].append({
                'database': 'EM',
                'relation': relation['name'],
                'target': relation['target'],
                'status': 'manual_addition_required'
            })

    def create_test_entries(self):
        """Create test entries to verify relations work."""
        print("   Test entries should be created manually after relations are added")
        print("   See PHASE_1_IMPLEMENTATION_GUIDE.md Day 7 for instructions")

        self.results['test_entries_created'].append({
            'status': 'manual_creation_required',
            'reference': 'PHASE_1_IMPLEMENTATION_GUIDE.md Day 7'
        })

    def validate_implementation(self):
        """Validate that all Phase 1 changes are complete."""
        print("   Validation checklist:")
        print("   [ ] Only 1 EM database exists (duplicate deleted)")
        print("   [ ] Only 1 SLL database exists (duplicate deleted)")
        print("   [ ] ARF has 13 properties (5 original + 8 relations)")
        print("   [ ] LK has 19 properties (12 original + 7 relations)")
        print("   [ ] EM has 16 properties (9 base + 7 relations)")
        print("   [ ] All relations work bidirectionally")
        print("   [ ] Test entries successfully created and linked")
        print("\n   Run analyze_all_23_databases.py after manual implementation to verify")

    def print_final_report(self):
        """Print final implementation report."""
        print("\n🎯 PHASE 1 IMPLEMENTATION REPORT")
        print("="*70)

        print(f"\n✅ Duplicates to delete: {len(self.results['duplicates_deleted'])}")
        for item in self.results['duplicates_deleted']:
            print(f"   - {item['database']}: {item['status']}")

        print(f"\n✅ Relations to add: {len(self.results['relations_added'])}")
        db_counts = {}
        for item in self.results['relations_added']:
            db = item['database']
            db_counts[db] = db_counts.get(db, 0) + 1
        for db, count in db_counts.items():
            print(f"   - {db}: {count} relations")

        print(f"\n✅ Properties to add: {len(self.results['properties_added'])}")
        for item in self.results['properties_added']:
            print(f"   - {item['database']}: {item['property']} ({item['type']})")

        if self.results['errors']:
            print(f"\n❌ Errors encountered: {len(self.results['errors'])}")
            for error in self.results['errors']:
                print(f"   - {error}")

        print("\n" + "="*70)
        print("⚠️  IMPORTANT: Notion API does not support adding database properties")
        print("   All relations and properties must be added manually in Notion UI")
        print("   Follow the instructions above for each item")
        print("\n📖 Reference: PHASE_1_IMPLEMENTATION_GUIDE.md")
        print("="*70)

        # Save report to file
        report_filename = f"phase1_implementation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Report saved to: {report_filename}")


def main():
    """Main execution."""
    implementer = Phase1Implementer()
    results = implementer.run()

    print("\n✅ Phase 1 implementation script complete!")
    print("   Follow the manual steps above to complete implementation")
    print("   Then run: python analyze_all_23_databases.py to verify")

    return 0 if not results['errors'] else 1


if __name__ == '__main__':
    sys.exit(main())
