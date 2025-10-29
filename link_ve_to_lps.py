#!/usr/bin/env python3
"""
Link Visual Essence entries to related Learning Particles in SLL.
"""

import os
import sys
import io
import requests
from dotenv import load_dotenv

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv('ama-backend/.env')
NOTION_API_KEY = os.getenv('NOTION_API_KEY')

if not NOTION_API_KEY:
    print("[ERROR] NOTION_API_KEY not found in environment")
    sys.exit(1)

# Database IDs
VE_DATABASE_ID = "29b8fec9-2931-80ed-8478-f96bf58418ca"
SLL_DATABASE_ID = "84da6cbd-09d6-40fb-868e-41444b941991"

# Notion API headers
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# VE Page IDs (from creation)
VE_PAGES = {
    "VE-048": "29b8fec9-2931-81fd-882e-f3c079d916b8",
    "VE-049": "29b8fec9-2931-8157-9089-fc0d3244229b"
}

# LP IDs to link (need to query SLL to find these)
LP_MAPPINGS = {
    "VE-048": [
        "LP-2025-10-28-048A",  # RPUSH/LPOP Pattern
        "LP-2025-10-28-048B",  # Windows Emoji Handling
        "LP-2025-10-28-048C",  # Array Unwrapping
        "LP-2025-10-28-048D",  # GENOMOS Consultation Schema
        "LP-2025-10-28-048E"   # Daemon Thread Failures
    ],
    "VE-049": [
        "LP-2025-10-29-049A",  # Emoji Crashes Hide Failures
        "LP-2025-10-29-049B",  # Test Infrastructure Before Features
        "LP-2025-10-29-049C",  # Triadiske Validation Pattern
        "LP-2025-10-29-049D",  # Provenance Formula Syntax
        "LP-2025-10-29-049E",  # Session Continuity Protocol
        "LP-2025-10-29-049F",  # GENOMOS Living Audit Trail
        "LP-2025-10-29-049G"   # Notion Schema Migration Strategy
    ]
}


def find_lp_page_id(lp_id):
    """Find the Notion page ID for an LP by its ID."""
    url = f"https://api.notion.com/v1/databases/{SLL_DATABASE_ID}/query"

    payload = {
        "filter": {
            "property": "lp_id",
            "title": {
                "equals": lp_id
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        results = response.json().get('results', [])

        if results:
            return results[0]['id']
        else:
            return None

    except Exception as e:
        print(f"[ERROR] Failed to find {lp_id}: {e}")
        return None


def link_ve_to_lps(ve_id, ve_page_id, lp_ids):
    """Link a VE entry to multiple LPs."""

    print(f"\n[INFO] Linking {ve_id} to {len(lp_ids)} LPs...")

    # Find page IDs for all LPs
    lp_page_ids = []
    for lp_id in lp_ids:
        print(f"  [SEARCH] Finding {lp_id}...")
        page_id = find_lp_page_id(lp_id)

        if page_id:
            lp_page_ids.append(page_id)
            print(f"  [FOUND] {lp_id}: {page_id}")
        else:
            print(f"  [WARNING] {lp_id} not found in SLL")

    if not lp_page_ids:
        print(f"[WARNING] No LPs found for {ve_id}")
        return False

    # Update VE entry with LP relations
    url = f"https://api.notion.com/v1/pages/{ve_page_id}"

    payload = {
        "properties": {
            "related_lps": {
                "relation": [{"id": lp_id} for lp_id in lp_page_ids]
            }
        }
    }

    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()

        print(f"[SUCCESS] Linked {ve_id} to {len(lp_page_ids)} LPs")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Failed to link {ve_id}: {e}")
        print(f"[ERROR] Response: {e.response.text}")
        return False

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return False


def main():
    print("\n" + "=" * 80)
    print("LINK VISUAL ESSENCES TO LEARNING PARTICLES")
    print("=" * 80)

    success_count = 0
    fail_count = 0

    for ve_id, lp_ids in LP_MAPPINGS.items():
        ve_page_id = VE_PAGES.get(ve_id)

        if not ve_page_id:
            print(f"[ERROR] VE page ID not found for {ve_id}")
            fail_count += 1
            continue

        result = link_ve_to_lps(ve_id, ve_page_id, lp_ids)

        if result:
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"[SUCCESS] Linked: {success_count} VE entries")
    print(f"[FAILED] Failed: {fail_count} VE entries")
    print("=" * 80 + "\n")

    if success_count > 0:
        print("[INFO] Visual Essence Library is now linked to LPs!")
        print("[INFO] Next steps:")
        print("  1. Conduct first Shadow Audit on SMK #048-049")
        print("  2. Commission Nyra to create actual visual assets")
        print("  3. Update SMK files with VE references")
        print()

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
