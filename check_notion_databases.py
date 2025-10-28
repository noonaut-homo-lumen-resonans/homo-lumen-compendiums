#!/usr/bin/env python3
"""
Check Notion database configurations for SMK, LK, SLL, ARF, and EM.
"""

import os
import sys

# Database IDs from documentation
databases = {
    "SLL (Learning Points)": {
        "id": "84da6cbd09d640fb868e41444b941991",
        "url": "https://www.notion.so/84da6cbd09d640fb868e41444b941991",
        "properties": ["LP_ID", "Agent", "Category", "Date", "Content", "Tags", "Source"],
        "status": "Fully operational (verified by Manus)"
    },
    "ARF (Agent Reflections)": {
        "id": "da4a5c2e7028492f91bfec7c88b7efce",
        "url": "https://www.notion.so/da4a5c2e7028492f91bfec7c88b7efce",
        "properties": ["Name", "Agents Involved", "Dato", "Status", "Type"],
        "status": "Fully operational (verified by Manus)"
    },
    "SMK (Strategic Macro-Coordination)": {
        "id": "ba1d4a4407a5425fafd81d27dc02cc1c",
        "url": "https://www.notion.so/ba1d4a4407a5425fafd81d27dc02cc1c",
        "properties": ["Name (title)", "SMK Number", "Agent", "Date", "Type", "Status", "Tags", "GitHub URL"],
        "status": "Created by Manus - NEEDS VERIFICATION"
    },
    "LK (Living Compendiums)": {
        "id": "784556781fc14a14afc733f4eb51e0bc",
        "url": "https://www.notion.so/784556781fc14a14afc733f4eb51e0bc",
        "properties": ["Name", "Agent", "Version", "Last Updated", "Status", "GitHub URL"],
        "status": "Created by Manus - NEEDS VERIFICATION"
    },
    "EM (Emergent Patterns)": {
        "id": "2988fec9293180509658e93447b3b259",
        "url": "https://www.notion.so/2988fec9293180509658e93447b3b259",
        "properties": ["Pattern ID", "Title", "Description", "Agent", "Source LK", "Date Identified", "Status", "Tags", "GitHub URL"],
        "status": "Created by Osvald - 27. oktober 2025"
    }
}

print("=" * 70)
print("NOTION DATABASE STATUS CHECK")
print("Date: 26. Oktober 2025")
print("=" * 70)

for db_name, db_info in databases.items():
    print(f"\n{db_name}:")
    print(f"  ID: {db_info['id']}")
    print(f"  URL: {db_info['url']}")
    print(f"  Status: {db_info['status']}")
    print(f"  Properties ({len(db_info['properties'])}):")
    for prop in db_info['properties']:
        print(f"    - {prop}")

print("\n" + "=" * 70)
print("GITHUB SECRETS NEEDED:")
print("=" * 70)
print("\n1. NOTION_API_KEY (probably already set)")
print("2. SLL_DATABASE_ID = 84da6cbd09d640fb868e41444b941991")
print("3. SMK_DATABASE_ID = ba1d4a4407a5425fafd81d27dc02cc1c")
print("4. LK_DATABASE_ID = 784556781fc14a14afc733f4eb51e0bc")
print("5. EM_DATABASE_ID = 2988fec9293180509658e93447b3b259")

print("\n" + "=" * 70)
print("WORKFLOWS STATUS:")
print("=" * 70)
print("\n1. sync-to-notion.yml (LP Sync)")
print("   - Trigger: Commits with 'LP #XXX'")
print("   - Status: ✅ ACTIVE (verified by Manus)")
print("   - Uses: SLL_DATABASE_ID")

print("\n2. sync-smk-to-notion.yml (SMK Sync)")
print("   - Trigger: Changes to SMK/**/*.md")
print("   - Status: ✅ CREATED (just now)")
print("   - Uses: SMK_DATABASE_ID")

print("\n3. sync-lk-to-notion.yml (LK Sync)")
print("   - Trigger: Changes to *_LK_*.md")
print("   - Status: ✅ CREATED (earlier today)")
print("   - Uses: LK_DATABASE_ID")

print("\n4. sync-em-to-notion.yml (EM Sync)")
print("   - Trigger: Changes to *_LK_*.md (extracts emergent patterns)")
print("   - Status: 🟡 PENDING CREATION")
print("   - Uses: EM_DATABASE_ID")

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("\n1. Verify all 5 databases exist in Notion")
print("2. Ensure GitHub Secrets are configured:")
print("   - Go to: https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/settings/secrets/actions")
print("   - Add SMK_DATABASE_ID, LK_DATABASE_ID, and EM_DATABASE_ID if missing")
print("3. Check workflow runs:")
print("   - Go to: https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums/actions")
print("4. Test by making a small change to an LK file")

print("\n" + "=" * 70)
