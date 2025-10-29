#!/usr/bin/env python3
"""
Phase 1 Verification Script
Verifies that all Phase 1 changes have been implemented correctly in Notion.
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

# Expected database IDs
EXPECTED_DBS = {
    'sll_primary': '84da6cbd09d640fb868e41444b941991',
    'arf': 'da4a5c2e7028492f91bfec7c88b7efce',
    'lk': '784556781fc14a14afc733f4eb51e0bc',
    'smk': 'ba1d4a4407a5425fafd81d27dc02cc1c',
    'em_primary': '2988fec9293180509658e93447b3b259'
}

# Databases that should be deleted
DUPLICATE_DBS = {
    'sll_duplicate': 'fda5f6dac3544d81a257a07685f674ed',
    'em_duplicate': '078f70c98954496c8b581e0a87c12127'
}

class Phase1Verifier:
    """Verifies Phase 1 implementation."""

    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        self.total_checks = 0
        self.passed_checks = 0

    def verify_all(self):
        """Run all verification checks."""
        print("🧬 PHASE 1 VERIFICATION - MICHAEL LEVIN FRAMEWORK")
        print("="*70)
        print()

        # Check 1: Verify duplicates are deleted
        print("✓ Check 1: Verifying duplicate databases are deleted...")
        self.check_duplicates_deleted()

        # Check 1.5: Verify SMK has no duplicates
        print("\n✓ Check 1.5: Verifying SMK database has no duplicates...")
        self.check_smk_duplicates()

        # Check 2: Verify ARF relations
        print("\n✓ Check 2: Verifying ARF has 8 new relations...")
        self.check_arf_relations()

        # Check 3: Verify LK relations
        print("\n✓ Check 3: Verifying LK has 7 new relations...")
        self.check_lk_relations()

        # Check 4: Verify EM setup
        print("\n✓ Check 4: Verifying EM database setup...")
        self.check_em_setup()

        # Check 5: Verify test entries
        print("\n✓ Check 5: Verifying test entries exist...")
        self.check_test_entries()

        # Check 6: Network connectivity
        print("\n✓ Check 6: Verifying network connectivity...")
        self.check_network_connectivity()

        # Final report
        print("\n" + "="*70)
        self.print_final_report()

        return self.passed_checks == self.total_checks

    def check_duplicates_deleted(self):
        """Verify that duplicate databases have been deleted."""

        for db_name, db_id in DUPLICATE_DBS.items():
            self.total_checks += 1
            try:
                # Try to retrieve the database
                notion.databases.retrieve(database_id=db_id)
                # If we get here, database still exists
                print(f"  ❌ FAIL: {db_name} still exists (should be deleted)")
                print(f"     ID: {db_id}")
                self.results['failed'].append(f"{db_name} not deleted")
            except Exception as e:
                # If we get an error, database is deleted (good!)
                if "not_found" in str(e) or "Could not find" in str(e):
                    print(f"  ✅ PASS: {db_name} successfully deleted")
                    self.passed_checks += 1
                    self.results['passed'].append(f"{db_name} deleted")
                else:
                    print(f"  ⚠️  WARNING: Could not verify {db_name}: {e}")
                    self.results['warnings'].append(f"{db_name}: {e}")

    def check_smk_duplicates(self):
        """Verify SMK database has no duplicates."""
        self.total_checks += 1

        try:
            # Query SMK database
            smk_database_id = EXPECTED_DBS.get('smk', 'ba1d4a4407a5425fafd81d27dc02cc1c')

            # Fetch all entries
            has_more = True
            start_cursor = None
            entries = []

            while has_more:
                if start_cursor:
                    response = notion.databases.query(
                        database_id=smk_database_id,
                        start_cursor=start_cursor
                    )
                else:
                    response = notion.databases.query(database_id=smk_database_id)

                entries.extend(response['results'])
                has_more = response.get('has_more', False)
                start_cursor = response.get('next_cursor')

            # Group by SMK Number to find duplicates
            smk_numbers = {}
            for entry in entries:
                props = entry['properties']

                # Extract SMK Number
                smk_number = None
                if 'SMK Number' in props and props['SMK Number']['number'] is not None:
                    smk_number = props['SMK Number']['number']

                if smk_number is not None:
                    if smk_number not in smk_numbers:
                        smk_numbers[smk_number] = []
                    smk_numbers[smk_number].append(entry)

            # Find duplicates (SMK numbers with 2+ entries)
            duplicates = {k: v for k, v in smk_numbers.items() if len(v) > 1}

            if len(duplicates) == 0:
                print(f"  ✅ PASS: SMK has no duplicates ({len(entries)} unique entries)")
                self.passed_checks += 1
                self.results['passed'].append(f"SMK clean: {len(entries)} entries")
            else:
                duplicate_count = sum(len(v) - 1 for v in duplicates.values())
                print(f"  ❌ FAIL: SMK has {len(duplicates)} duplicate groups ({duplicate_count} duplicate entries)")
                for smk_num, dupes in list(duplicates.items())[:3]:  # Show first 3
                    print(f"     • SMK #{smk_num}: {len(dupes)} entries")
                if len(duplicates) > 3:
                    print(f"     ... and {len(duplicates) - 3} more")
                print(f"     Run: python deduplicate_smk.py --auto")
                self.results['failed'].append(f"SMK has {duplicate_count} duplicates")

        except Exception as e:
            print(f"  ❌ ERROR: Could not check SMK duplicates: {e}")
            self.results['failed'].append(f"SMK duplicate check error: {e}")

    def check_arf_relations(self):
        """Verify ARF has all required relations."""

        expected_relations = [
            '📚 Related Learning Points',
            '✅ Strategic Decisions',
            '📖 Source Compendium',
            '🌟 Emergent Patterns',
            '🧬 Related Agents',
            '📝 Personal Reflections',
            '📔 Journal Entries',
            '💚 Wellness Context'
        ]

        try:
            arf = notion.databases.retrieve(database_id=EXPECTED_DBS['arf'])
            properties = arf['properties']

            print(f"  ARF has {len(properties)} total properties")

            for relation_name in expected_relations:
                self.total_checks += 1
                # Check if property exists (with or without emoji)
                found = False
                actual_name = None

                for prop_name, prop_data in properties.items():
                    # Remove emojis for comparison
                    clean_prop_name = ''.join(c for c in prop_name if c.isalnum() or c.isspace())
                    clean_expected = ''.join(c for c in relation_name if c.isalnum() or c.isspace())

                    if clean_expected.strip().lower() in clean_prop_name.strip().lower():
                        if prop_data['type'] == 'relation':
                            found = True
                            actual_name = prop_name
                            break

                if found:
                    print(f"  ✅ PASS: {actual_name}")
                    self.passed_checks += 1
                    self.results['passed'].append(f"ARF: {actual_name}")
                else:
                    print(f"  ❌ FAIL: {relation_name} not found")
                    self.results['failed'].append(f"ARF missing: {relation_name}")

            # Check total property count
            self.total_checks += 1
            if len(properties) >= 13:  # 5 original + 8 relations
                print(f"  ✅ PASS: ARF has {len(properties)} properties (expected ≥13)")
                self.passed_checks += 1
                self.results['passed'].append(f"ARF property count: {len(properties)}")
            else:
                print(f"  ❌ FAIL: ARF has {len(properties)} properties (expected ≥13)")
                self.results['failed'].append(f"ARF property count: {len(properties)} < 13")

        except Exception as e:
            print(f"  ❌ ERROR: Could not verify ARF: {e}")
            self.results['failed'].append(f"ARF verification error: {e}")

    def check_lk_relations(self):
        """Verify LK has all required relations."""

        expected_relations = [
            '📚 Source Learning Points',
            '🧠 Related Reflections',
            '✅ Strategic Decisions',
            '🌟 Patterns Identified',
            '🧬 Agent Profile',
            '🧘 Practices Documented',
            '🌟 Wisdom Sources'
        ]

        try:
            lk = notion.databases.retrieve(database_id=EXPECTED_DBS['lk'])
            properties = lk['properties']

            print(f"  LK has {len(properties)} total properties")

            for relation_name in expected_relations:
                self.total_checks += 1
                found = False
                actual_name = None

                for prop_name, prop_data in properties.items():
                    clean_prop_name = ''.join(c for c in prop_name if c.isalnum() or c.isspace())
                    clean_expected = ''.join(c for c in relation_name if c.isalnum() or c.isspace())

                    if clean_expected.strip().lower() in clean_prop_name.strip().lower():
                        if prop_data['type'] == 'relation':
                            found = True
                            actual_name = prop_name
                            break

                if found:
                    print(f"  ✅ PASS: {actual_name}")
                    self.passed_checks += 1
                    self.results['passed'].append(f"LK: {actual_name}")
                else:
                    print(f"  ❌ FAIL: {relation_name} not found")
                    self.results['failed'].append(f"LK missing: {relation_name}")

            # Check total property count
            self.total_checks += 1
            if len(properties) >= 19:  # 12 original + 7 relations
                print(f"  ✅ PASS: LK has {len(properties)} properties (expected ≥19)")
                self.passed_checks += 1
                self.results['passed'].append(f"LK property count: {len(properties)}")
            else:
                print(f"  ❌ FAIL: LK has {len(properties)} properties (expected ≥19)")
                self.results['failed'].append(f"LK property count: {len(properties)} < 19")

        except Exception as e:
            print(f"  ❌ ERROR: Could not verify LK: {e}")
            self.results['failed'].append(f"LK verification error: {e}")

    def check_em_setup(self):
        """Verify EM database has all properties and relations."""

        expected_properties = {
            'Pattern ID': 'title',
            'Pattern Name': 'rich_text',
            'Description': 'rich_text',
            'Confidence Score': 'number',
            'First Detected': 'date',
            'Frequency': 'select',
            'Status': 'select',
            'Tags': 'multi_select'
        }

        expected_relations = [
            '📖 Source Compendium',
            '🧠 Source Reflections',
            '📚 Related Learning Points',
            '✅ Strategic Impact',
            '📋 Related Case Studies',
            '✅ Related Decisions',
            '🌑 Shadow Patterns'
        ]

        try:
            em = notion.databases.retrieve(database_id=EXPECTED_DBS['em_primary'])
            properties = em['properties']

            print(f"  EM has {len(properties)} total properties")

            # Check base properties
            for prop_name, prop_type in expected_properties.items():
                self.total_checks += 1
                found = False
                actual_name = None

                for p_name, p_data in properties.items():
                    clean_p_name = ''.join(c for c in p_name if c.isalnum() or c.isspace())
                    clean_expected = ''.join(c for c in prop_name if c.isalnum() or c.isspace())

                    if clean_expected.strip().lower() in clean_p_name.strip().lower():
                        if p_data['type'] == prop_type:
                            found = True
                            actual_name = p_name
                            break

                if found:
                    print(f"  ✅ PASS: {actual_name} ({prop_type})")
                    self.passed_checks += 1
                    self.results['passed'].append(f"EM: {actual_name}")
                else:
                    print(f"  ❌ FAIL: {prop_name} ({prop_type}) not found")
                    self.results['failed'].append(f"EM missing property: {prop_name}")

            # Check relations
            for relation_name in expected_relations:
                self.total_checks += 1
                found = False
                actual_name = None

                for p_name, p_data in properties.items():
                    clean_p_name = ''.join(c for c in p_name if c.isalnum() or c.isspace())
                    clean_expected = ''.join(c for c in relation_name if c.isalnum() or c.isspace())

                    if clean_expected.strip().lower() in clean_p_name.strip().lower():
                        if p_data['type'] == 'relation':
                            found = True
                            actual_name = p_name
                            break

                if found:
                    print(f"  ✅ PASS: {actual_name}")
                    self.passed_checks += 1
                    self.results['passed'].append(f"EM: {actual_name}")
                else:
                    print(f"  ❌ FAIL: {relation_name} not found")
                    self.results['failed'].append(f"EM missing relation: {relation_name}")

            # Check total property count
            self.total_checks += 1
            if len(properties) >= 16:  # 9 base + 7 relations
                print(f"  ✅ PASS: EM has {len(properties)} properties (expected ≥16)")
                self.passed_checks += 1
                self.results['passed'].append(f"EM property count: {len(properties)}")
            else:
                print(f"  ❌ FAIL: EM has {len(properties)} properties (expected ≥16)")
                self.results['failed'].append(f"EM property count: {len(properties)} < 16")

        except Exception as e:
            print(f"  ❌ ERROR: Could not verify EM: {e}")
            self.results['failed'].append(f"EM verification error: {e}")

    def check_test_entries(self):
        """Verify that test entries have been created."""

        # Check for ARF test entry
        self.total_checks += 1
        try:
            arf_query = notion.databases.query(database_id=EXPECTED_DBS['arf'])
            test_entries = [
                entry for entry in arf_query['results']
                if 'Test Integration' in str(entry.get('properties', {}).get('Name', {}).get('title', []))
                or 'Phase 1' in str(entry.get('properties', {}).get('Name', {}).get('title', []))
            ]

            if len(test_entries) > 0:
                print(f"  ✅ PASS: Found {len(test_entries)} test entry(ies) in ARF")
                self.passed_checks += 1
                self.results['passed'].append(f"ARF test entries: {len(test_entries)}")
            else:
                print("  ⚠️  WARNING: No test entries found in ARF")
                self.results['warnings'].append("No ARF test entries")

        except Exception as e:
            print(f"  ❌ ERROR: Could not check ARF test entries: {e}")
            self.results['failed'].append(f"ARF test entry check error: {e}")

        # Check for EM test entry
        self.total_checks += 1
        try:
            em_query = notion.databases.query(database_id=EXPECTED_DBS['em_primary'])
            em_entries = len(em_query['results'])

            if em_entries > 0:
                print(f"  ✅ PASS: Found {em_entries} pattern(s) in EM")
                self.passed_checks += 1
                self.results['passed'].append(f"EM entries: {em_entries}")
            else:
                print("  ⚠️  WARNING: No patterns found in EM yet")
                self.results['warnings'].append("No EM patterns yet")

        except Exception as e:
            print(f"  ❌ ERROR: Could not check EM entries: {e}")
            self.results['failed'].append(f"EM entry check error: {e}")

    def check_network_connectivity(self):
        """Verify that databases are connected (sample check)."""

        self.total_checks += 1
        try:
            # Query SLL for entries with relations
            sll_query = notion.databases.query(database_id=EXPECTED_DBS['sll_primary'])
            connected_count = 0

            for entry in sll_query['results']:
                properties = entry.get('properties', {})
                # Check if any relation properties exist and have values
                for prop_name, prop_data in properties.items():
                    if prop_data.get('type') == 'relation':
                        if len(prop_data.get('relation', [])) > 0:
                            connected_count += 1
                            break

            if connected_count > 0:
                print(f"  ✅ PASS: {connected_count}/{len(sll_query['results'])} SLL entries have relations")
                self.passed_checks += 1
                self.results['passed'].append(f"SLL connectivity: {connected_count} connected")
            else:
                print("  ⚠️  WARNING: No SLL entries have relations yet (add test data)")
                self.results['warnings'].append("No SLL relations yet")

        except Exception as e:
            print(f"  ⚠️  WARNING: Could not check network connectivity: {e}")
            self.results['warnings'].append(f"Connectivity check error: {e}")

    def print_final_report(self):
        """Print final verification report."""

        print("\n🎯 PHASE 1 VERIFICATION REPORT")
        print("="*70)

        score = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0

        print(f"\n📊 Score: {self.passed_checks}/{self.total_checks} checks passed ({score:.1f}%)")

        if self.results['passed']:
            print(f"\n✅ Passed ({len(self.results['passed'])}):")
            for item in self.results['passed'][:10]:  # Show first 10
                print(f"   • {item}")
            if len(self.results['passed']) > 10:
                print(f"   ... and {len(self.results['passed']) - 10} more")

        if self.results['failed']:
            print(f"\n❌ Failed ({len(self.results['failed'])}):")
            for item in self.results['failed']:
                print(f"   • {item}")

        if self.results['warnings']:
            print(f"\n⚠️  Warnings ({len(self.results['warnings'])}):")
            for item in self.results['warnings']:
                print(f"   • {item}")

        print("\n" + "="*70)

        if score >= 90:
            print("🎉 EXCELLENT! Phase 1 implementation is nearly complete!")
            print("   Review warnings and proceed to Phase 2")
        elif score >= 70:
            print("✅ GOOD! Most checks passed")
            print("   Review failed items and fix before Phase 2")
        elif score >= 50:
            print("⚠️  PARTIAL: Several items need attention")
            print("   Complete remaining tasks before Phase 2")
        else:
            print("❌ INCOMPLETE: Phase 1 needs more work")
            print("   Follow FASE_1_MANUELL_IMPLEMENTERING.md")

        print("="*70)

        # Save report
        report_filename = f"phase1_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'score': score,
                'checks_passed': self.passed_checks,
                'checks_total': self.total_checks,
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Detailed report saved to: {report_filename}")


def main():
    """Main execution."""
    verifier = Phase1Verifier()
    success = verifier.verify_all()

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
