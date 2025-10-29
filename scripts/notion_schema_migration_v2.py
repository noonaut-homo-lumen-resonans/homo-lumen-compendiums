#!/usr/bin/env python3
"""
SMK V2.0 - Notion Schema Migration Script
Automatically adds properties to SLL database and creates Visual Essence Library

Usage:
  pip install notion-client
  export NOTION_TOKEN="secret_..."
  export SLL_DATABASE_ID="..."

  python scripts/notion_schema_migration_v2.py --create-ve-database
"""

import os
import sys
import argparse
from notion_client import Client

# SLL New Properties Configuration
SLL_NEW_PROPERTIES = [
    {
        "name": "temporal_weight_raw",
        "type": "number",
        "number": {"format": "number"},
        "description": "Raw temporal weight computed by script (0.0-1.0)"
    },
    # Temporal weight formula - will add manually in Notion UI
    # Notion API formula syntax is complex, easier to add via UI
    # {
    #     "name": "temporal_weight",
    #     "type": "formula",
    #     "formula": {"expression": 'if(prop("phase") == "published", prop("temporal_weight_raw"), 0)'},
    #     "description": "Temporal weight (0.0-1.0) - only for published LPs"
    # },
    {
        "name": "half_life_days",
        "type": "number",
        "number": {"format": "number"},
        "description": "Domain-specific half-life in days"
    },
    {
        "name": "last_cited_timestamp",
        "type": "date",
        "date": {},
        "description": "Last time this LP was cited"
    },
    {
        "name": "reactivation_count",
        "type": "number",
        "number": {"format": "number"},
        "description": "Number of times LP has been cited"
    },
    {
        "name": "freshness_status",
        "type": "select",
        "select": {
            "options": [
                {"name": "fresh", "color": "green"},
                {"name": "aging", "color": "yellow"},
                {"name": "stale", "color": "gray"}
            ]
        },
        "description": "Computed freshness based on temporal_weight"
    },
    {
        "name": "provenance_block",
        "type": "rich_text",
        "rich_text": {},
        "description": "JSON PROVENANCE block from source SMK"
    },
    {
        "name": "shadow_flags",
        "type": "checkbox",
        "checkbox": {},
        "description": "Flagged during shadow audit"
    },
    {
        "name": "shadow_notes",
        "type": "rich_text",
        "rich_text": {},
        "description": "Details about shadow concern"
    }
]

# Visual Essence Library Properties
VE_PROPERTIES = {
    "ve_id": {"title": {}},
    "name": {"rich_text": {}},
    "description": {"rich_text": {}},
    "image_media": {"files": {}},
    "palette": {
        "multi_select": {
            "options": [
                {"name": "warm", "color": "red"},
                {"name": "cool", "color": "blue"},
                {"name": "earth", "color": "brown"},
                {"name": "neon", "color": "pink"},
                {"name": "monochrome", "color": "gray"},
                {"name": "vibrant", "color": "orange"}
            ]
        }
    },
    "archetype_tags": {
        "multi_select": {
            "options": [
                {"name": "emergence", "color": "green"},
                {"name": "connection", "color": "purple"},
                {"name": "transformation", "color": "yellow"},
                {"name": "flow", "color": "blue"},
                {"name": "clarity", "color": "default"},
                {"name": "depth", "color": "blue"},
                {"name": "cycles", "color": "green"},
                {"name": "resonance", "color": "pink"}
            ]
        }
    },
    "license": {
        "select": {
            "options": [
                {"name": "CC0 (Public Domain)", "color": "green"},
                {"name": "CC-BY (Attribution)", "color": "yellow"},
                {"name": "Internal Use", "color": "gray"}
            ]
        }
    },
    "created_by": {"people": {}},
    "created_at": {"date": {}}
}


def update_sll_schema(notion, sll_database_id, dry_run=False):
    """Add new properties to SLL database"""
    print("\n" + "="*80)
    print("UPDATING SLL DATABASE SCHEMA")
    print("="*80)

    try:
        # Get current database schema
        database = notion.databases.retrieve(database_id=sll_database_id)
        existing_properties = database.get("properties", {})

        print(f"\nCurrent SLL properties: {len(existing_properties)}")

        # Check which properties need to be added
        to_add = []
        for prop_config in SLL_NEW_PROPERTIES:
            prop_name = prop_config["name"]
            if prop_name not in existing_properties:
                to_add.append(prop_config)
                print(f"  [NEW] {prop_name} ({prop_config['type']})")
            else:
                print(f"  [EXISTS] {prop_name} - skipping")

        if not to_add:
            print("\nAll properties already exist. No updates needed.")
            return True

        print(f"\nWill add {len(to_add)} new properties")

        if dry_run:
            print("\nDRY RUN - No changes made")
            return True

        # Add new properties
        new_properties = {}
        for prop_config in to_add:
            prop_name = prop_config.pop("name")
            new_properties[prop_name] = prop_config

        # Update database
        notion.databases.update(
            database_id=sll_database_id,
            properties=new_properties
        )

        print(f"\n[SUCCESS] Added {len(to_add)} properties to SLL database")
        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to update SLL database: {e}")
        return False


def create_ve_database(notion, parent_page_id, sll_database_id, dry_run=False):
    """Create Visual Essence Library database"""
    print("\n" + "="*80)
    print("CREATING VISUAL ESSENCE LIBRARY DATABASE")
    print("="*80)

    if dry_run:
        print("\nDRY RUN - Would create VE database with these properties:")
        for prop_name in VE_PROPERTIES.keys():
            print(f"  - {prop_name}")
        return None

    try:
        # Add relation to SLL
        ve_properties_with_relation = VE_PROPERTIES.copy()
        ve_properties_with_relation["related_lps"] = {
            "relation": {
                "database_id": sll_database_id,
                "type": "dual_property",
                "dual_property": {
                    "synced_property_name": "illustrated_by",
                    "synced_property_id": None
                }
            }
        }

        # Create database
        new_database = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": "Visual Essence Library"}}],
            icon={"type": "emoji", "emoji": "🎨"},
            properties=ve_properties_with_relation
        )

        database_id = new_database["id"]
        print(f"\n[SUCCESS] Created Visual Essence Library")
        print(f"Database ID: {database_id}")
        print(f"URL: {new_database.get('url', 'N/A')}")

        return database_id

    except Exception as e:
        print(f"\n[ERROR] Failed to create VE database: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Migrate Notion databases to SMK V2.0")
    parser.add_argument("--notion-token", help="Notion API token (or set NOTION_TOKEN env var)")
    parser.add_argument("--sll-database-id", help="SLL database ID (or set SLL_DATABASE_ID env var)")
    parser.add_argument("--parent-page-id", help="Parent page ID for VE database (or set PARENT_PAGE_ID env var)")
    parser.add_argument("--create-ve-database", action="store_true", help="Create Visual Essence Library")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")

    args = parser.parse_args()

    # Get credentials
    notion_token = args.notion_token or os.getenv("NOTION_TOKEN")
    sll_database_id = args.sll_database_id or os.getenv("SLL_DATABASE_ID")
    parent_page_id = args.parent_page_id or os.getenv("PARENT_PAGE_ID")

    if not notion_token:
        print("ERROR: NOTION_TOKEN required (--notion-token or env var)")
        sys.exit(1)

    if not sll_database_id:
        print("ERROR: SLL_DATABASE_ID required (--sll-database-id or env var)")
        sys.exit(1)

    # Initialize Notion client
    notion = Client(auth=notion_token)

    print("\n" + "#"*80)
    print("#  SMK V2.0 - NOTION SCHEMA MIGRATION")
    print("#"*80)

    # Update SLL schema
    success = update_sll_schema(notion, sll_database_id, dry_run=args.dry_run)

    if not success:
        print("\n[FAILED] SLL schema update failed")
        sys.exit(1)

    # Create VE database if requested
    if args.create_ve_database:
        if not parent_page_id:
            print("\nERROR: PARENT_PAGE_ID required for creating VE database")
            sys.exit(1)

        ve_database_id = create_ve_database(notion, parent_page_id, sll_database_id, dry_run=args.dry_run)

        if ve_database_id:
            print(f"\nSave this VE database ID: {ve_database_id}")

    print("\n" + "="*80)
    print("MIGRATION COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("1. Verify properties in Notion UI")
    print("2. Test relation between SLL and VE")
    print("3. Create pilot VE entries (5 recommended)")
    print("4. Proceed to Week 1 Day 3-4: SMK Template creation")


if __name__ == "__main__":
    main()
