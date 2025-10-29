#!/usr/bin/env python3
"""
Populate Visual Essence Library with 5 pilot entries.
"""

import os
import sys
import io
import json
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

# Database ID
VE_DATABASE_ID = "29b8fec9-2931-80ed-8478-f96bf58418ca"

# Notion API headers
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 5 Pilot Visual Essences
pilot_entries = [
    {
        "ve_id": "VE-001",
        "name": "Homo Lumen Genesis Architecture",
        "description": "Foundational visual essence showing the emergence of Homo Lumen collective intelligence. Six branches (agents) growing from a single root (Constitution), interconnected through mycelial networks underground (shared knowledge infrastructure). Light flows bidirectionally - from root to branches (foundational principles) and branches to root (lived experience). Central trunk represents Constitution, six branches are Lira, Nyra, Orion, Thalus, Zara, Aurora. Underground mycelium shows Redis, Notion, GENOMOS interconnections. Roots represent human partnership (Osvald) grounding the system.",
        "archetype_tags": ["emergence", "connection", "transformation"],
        "palette": ["Vibrant", "Warm"],
        "license": "Internal Use"
    },
    {
        "ve_id": "VE-040",
        "name": "Mycelial Knowledge Network",
        "description": "Visualization of knowledge flowing through hidden infrastructure (mycelial threads) connecting different repositories (SMK, SLL, GENOMOS). Learning Particles (LPs) as nutrients flowing through threads. Strategic Macro-Coordinations (SMKs) as fruiting bodies that emerge above ground - visible manifestations of underground knowledge synthesis. Mycelial threads represent data connections (Redis, APIs, Notion sync). Nodes are databases (SMK, SLL, Visual Essence, GENOMOS). Nutrients flowing show individual LPs moving through network. Fruiting bodies are SMKs emerging as synthesis points. Includes decay cycle showing temporal weights and knowledge aging.",
        "archetype_tags": ["connection", "cycles", "flow"],
        "palette": ["Earth", "Monochrone"],
        "license": "Internal Use"
    },
    {
        "ve_id": "VE-042",
        "name": "GENOMOS Blockchain: DNA Helix of Collective Memory",
        "description": "GENOMOS blockchain visualized as a DNA double helix, with each block as a gene segment containing specific knowledge types (SMK genes, consultation genes, mutation genes). The helix grows vertically (chronological), with cross-links showing cryptographic hashes (Merkle tree). Genesis block at base (primordial cell), growing upward toward collective wisdom. Double helix structure with two strands representing data + metadata. Gene blocks are color-coded by type (blue=SMK, green=consultation, red=mutation, gold=learning). Hash chains as cross-links between blocks showing cryptographic integrity. Growth rings show temporal layers of system evolution.",
        "archetype_tags": ["depth", "transformation", "resonance"],
        "palette": ["Neon", "Cool"],
        "license": "Internal Use"
    },
    {
        "ve_id": "VE-048",
        "name": "Redis Event Flow: Pipeline with Valve Correction",
        "description": "Flowchart showing CSN Server -> RPUSH -> Redis Queue (persistent) -> LPOP -> Ubuntu Subscriber -> SQLite + GENOMOS. Shows error states (PUBLISH ephemeral, array unwrapping failure, emoji crash) as 'valve mismatches' that block flow. Final corrected state shows smooth water flow (events) from source to destination. Source pump is CSN Server publishing events. Pipeline is Redis queue (persistent storage). Valve types show PUBLISH (spray/ephemeral) vs RPUSH (pour/persistent). Subscriber bucket is Ubuntu Playground consuming events. Error states show cracked pipes, blocked valves, emoji crashes. Destination reservoirs are SQLite database + GENOMOS blockchain. Success indicators with smooth flow lines.",
        "archetype_tags": ["flow", "clarity", "transformation"],
        "palette": ["Cool", "Vibrant"],
        "license": "CC-BY (Attribution)"
    },
    {
        "ve_id": "VE-049",
        "name": "Three-Layer Testing Pyramid: Mycelial Stress Test",
        "description": "Multi-layer visualization combining: (1) Redis event flow diagram (CSN -> RPUSH -> LPOP -> GENOMOS), (2) Triadiske Portvokter validation pyramid (BiofeltGate -> ThalosFilter -> MutationLog), (3) Mycelial growth rings showing GENOMOS blockchain expansion (16->19 blocks with timestamps). Metaphor: Underground mycelium stressed with bioluminescent tracers - light flows through and reveals cracks (bugs), then cracks are repaired, and mycelium grows stronger with new rings (SMK V2.0 schema additions). Layer 1 (Base) shows Redis event flow with RPUSH/LPOP mechanics. Layer 2 (Middle) shows three gates (Biofelt, Thalos, Mutation) as pyramid tiers. Layer 3 (Top) shows GENOMOS growth rings with block numbers + timestamps. Bioluminescent tracers represent test data flowing through all layers.",
        "archetype_tags": ["depth", "clarity", "transformation"],
        "palette": ["Neon", "Earth"],
        "license": "Internal Use"
    }
]

def create_ve_entry(entry_data):
    """Create a Visual Essence entry in Notion."""

    # Build properties according to actual schema
    properties = {
        "ve_id": {
            "title": [{"text": {"content": entry_data["ve_id"]}}]
        },
        "Name": {
            "rich_text": [{"text": {"content": entry_data["name"]}}]
        },
        "description": {
            "rich_text": [{"text": {"content": entry_data["description"]}}]
        },
        "archetype_tags": {
            "multi_select": [{"name": tag} for tag in entry_data["archetype_tags"]]
        },
        "palette": {
            "multi_select": [{"name": color} for color in entry_data["palette"]]
        },
        "license": {
            "select": {"name": entry_data["license"]}
        }
    }

    # Create page
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": VE_DATABASE_ID},
        "properties": properties
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        page_data = response.json()
        page_id = page_data.get('id')

        print(f"[SUCCESS] Created {entry_data['ve_id']}: {entry_data['name']}")
        print(f"          Page ID: {page_id}")

        return page_id

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Failed to create {entry_data['ve_id']}: {e}")
        print(f"[ERROR] Response: {e.response.text}")
        return None

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        return None


def main():
    print("\n" + "=" * 80)
    print("POPULATE VISUAL ESSENCE LIBRARY - 5 PILOT ENTRIES")
    print("=" * 80 + "\n")

    created_count = 0
    failed_count = 0

    for i, entry in enumerate(pilot_entries, 1):
        print(f"\n[{i}/5] Creating {entry['ve_id']}...")

        page_id = create_ve_entry(entry)

        if page_id:
            created_count += 1
        else:
            failed_count += 1

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"[SUCCESS] Created: {created_count} entries")
    print(f"[FAILED] Failed: {failed_count} entries")
    print("=" * 80 + "\n")

    if created_count == 5:
        print("[INFO] All pilot entries created successfully!")
        print("[INFO] Next steps:")
        print("  1. Link VE-048 to related LPs (LP-048A through LP-048E)")
        print("  2. Link VE-049 to related LPs (LP-049A through LP-049G)")
        print("  3. Commission Nyra to create actual visual assets")
        print("  4. Update SMK #048 and #049 with VE links")
        print()

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
