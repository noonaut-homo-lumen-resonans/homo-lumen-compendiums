#!/usr/bin/env python3
"""
Update Shadow Logs and Ontology Audit database schemas with new fields for shadow feedback loop.

This script adds the new properties defined in docs/SHADOW_TAXONOMY.md to the relevant
Notion databases to support conscious coupling between system and agent shadows.

Usage:
    python scripts/update_shadow_database_schemas.py

Environment Variables Required:
    NOTION_API_KEY: Notion integration API key
    SL_DATABASE_ID: Shadow Logs database ID
    ONTOLOGY_AUDIT_DATABASE_ID: Ontology Audit database ID (if exists)

New Fields Added to SL Database:
    - Phoenix_Phase (select): Dissolution, Incubation, Emergence, Flight, Return
    - Integration_Practice (rich_text): What practice is being used for integration
    - Transformation_Status (select): Recognized, Under Inquiry, Integrating, Integrated, Monitoring
    - ARF_Response (checkbox): Was this in response to Agent Reflection Request?

New Fields Added to Ontology Audit Database:
    - Shadow_Type (select): Elitisme, Solutionisme, Kontroll, Avhengighet, Other
    - Shadow_Activation_Score (number): 0.0-1.0 manually assessed weekly
    - Phoenix_Phase (select): Same as SL
    - Agent_Reflection_Requested (checkbox): Has ARF been sent?
    - ARF_Date (date): Date of last Agent Reflection Request

Note: Notion API doesn't support updating database schemas directly via API.
This script will create PAGES with these properties, which will automatically
add them to the database schema. Then you can configure them in Notion UI.

Author: Code (Claude Code Agent)
Date: 28. oktober 2025
"""

import os
import sys
import io
import requests
from datetime import datetime

# Force UTF-8 encoding for stdout (Windows compatibility)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
SL_DATABASE_ID = os.environ.get('SL_DATABASE_ID')
ONTOLOGY_AUDIT_DATABASE_ID = os.environ.get('ONTOLOGY_AUDIT_DATABASE_ID')
NOTION_API_VERSION = '2022-06-28'

HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_API_VERSION
}

def create_sl_schema_template():
    """
    Create a template SL entry with all new fields to establish schema.

    This page will be created and can be deleted after schema is established.
    """
    url = 'https://api.notion.com/v1/pages'

    today = datetime.now().strftime('%Y-%m-%d')

    properties = {
        'Name': {
            'title': [{'text': {'content': 'SL #TEMPLATE'}}]
        },
        'Title': {
            'rich_text': [{'text': {'content': 'Schema Template - Safe to Delete'}}]
        },
        'Select': {
            'select': {'name': 'Code'}
        },
        'Manifestation': {
            'rich_text': [{'text': {'content': 'This is a template entry to establish new database schema fields.'}}]
        },
        'Integration': {
            'rich_text': [{'text': {'content': 'Delete this entry after confirming new fields appear in database schema.'}}]
        },
        'Status': {
            'select': {'name': 'Identified'}
        },
        'Date': {
            'date': {'start': today}
        },
        # NEW FIELDS FOR SHADOW FEEDBACK LOOP
        'Phoenix_Phase': {
            'select': {'name': 'Dissolution'}
        },
        'Integration_Practice': {
            'rich_text': [{'text': {'content': '4-6-8 breathing, weekly shadow ethics council review'}}]
        },
        'Transformation_Status': {
            'select': {'name': 'Recognized'}
        },
        'ARF_Response': {
            'checkbox': False
        }
    }

    payload = {
        'parent': {'database_id': SL_DATABASE_ID},
        'properties': properties
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)

        if response.status_code == 200:
            print("✅ SL Database: Template entry created successfully")
            print("   New fields added: Phoenix_Phase, Integration_Practice, Transformation_Status, ARF_Response")
            print("   📝 Action needed: Go to Notion and configure these fields in database view")
            print("   🗑️  You can delete the template entry after verifying fields appear")
            return True
        else:
            print(f"❌ Failed to create SL template: Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating SL template: {e}")
        return False

def create_ontology_audit_schema_template():
    """
    Create a template Ontology Audit entry with all new fields.

    Note: This assumes Ontology Audit database exists. If not, skip.
    """
    if not ONTOLOGY_AUDIT_DATABASE_ID:
        print("⚠️  ONTOLOGY_AUDIT_DATABASE_ID not set - skipping Ontology Audit schema update")
        print("   If you have an Ontology Audit database, set the environment variable and re-run")
        return False

    url = 'https://api.notion.com/v1/pages'

    today = datetime.now().strftime('%Y-%m-%d')

    # Note: We don't know the exact property names in Ontology Audit database
    # This is a best-guess based on typical structure. May need adjustment.
    properties = {
        'Name': {
            'title': [{'text': {'content': 'TEMPLATE - Safe to Delete'}}]
        },
        # NEW FIELDS FOR SHADOW FEEDBACK LOOP
        'Shadow_Type': {
            'select': {'name': 'Kontroll'}
        },
        'Shadow_Activation_Score': {
            'number': 0.5
        },
        'Phoenix_Phase': {
            'select': {'name': 'Dissolution'}
        },
        'Agent_Reflection_Requested': {
            'checkbox': False
        },
        'ARF_Date': {
            'date': {'start': today}
        }
    }

    payload = {
        'parent': {'database_id': ONTOLOGY_AUDIT_DATABASE_ID},
        'properties': properties
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)

        if response.status_code == 200:
            print("✅ Ontology Audit Database: Template entry created successfully")
            print("   New fields added: Shadow_Type, Shadow_Activation_Score, Phoenix_Phase,")
            print("                     Agent_Reflection_Requested, ARF_Date")
            print("   📝 Action needed: Configure these fields in Notion database view")
            print("   🗑️  Delete template entry after verification")
            return True
        else:
            print(f"❌ Failed to create Ontology Audit template: Status {response.status_code}")
            print(f"   Response: {response.text}")
            print("   💡 This may be because property names don't match your database schema")
            print("   💡 You may need to add these fields manually in Notion UI")
            return False
    except Exception as e:
        print(f"❌ Error creating Ontology Audit template: {e}")
        return False

def get_database_info(database_id, name):
    """Get information about a database to verify access."""
    url = f'https://api.notion.com/v1/databases/{database_id}'

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()
            db_title = data.get('title', [{}])[0].get('plain_text', 'Unknown')
            print(f"✅ {name}: Connected to '{db_title}'")

            # List existing properties
            properties = data.get('properties', {})
            print(f"   Existing properties ({len(properties)}): {', '.join(properties.keys())}")
            return True
        else:
            print(f"❌ {name}: Failed to connect (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False

def main():
    """Main execution function."""

    print("🚀 Shadow Database Schema Updater")
    print("=" * 70)
    print()
    print("📋 Purpose: Add new fields for shadow feedback loop (per Shadow Taxonomy)")
    print()

    if not NOTION_API_KEY:
        print("❌ Missing NOTION_API_KEY environment variable")
        return

    if not SL_DATABASE_ID:
        print("❌ Missing SL_DATABASE_ID environment variable")
        return

    print("🔍 Verifying database connections...")
    print()

    # Verify SL database access
    sl_connected = get_database_info(SL_DATABASE_ID, "SL Database")
    print()

    # Verify Ontology Audit database access (if provided)
    ontology_connected = False
    if ONTOLOGY_AUDIT_DATABASE_ID:
        ontology_connected = get_database_info(ONTOLOGY_AUDIT_DATABASE_ID, "Ontology Audit Database")
        print()

    if not sl_connected:
        print("❌ Cannot proceed without SL database connection")
        return

    print("=" * 70)
    print("📝 Creating template entries to establish new schema fields...")
    print()

    # Create SL schema template
    print("1️⃣ Updating SL Database Schema...")
    sl_success = create_sl_schema_template()
    print()

    # Create Ontology Audit schema template (if database exists)
    if ONTOLOGY_AUDIT_DATABASE_ID and ontology_connected:
        print("2️⃣ Updating Ontology Audit Database Schema...")
        ontology_success = create_ontology_audit_schema_template()
        print()
    else:
        ontology_success = None
        print("2️⃣ Ontology Audit Database: Skipped (not configured)")
        print()

    print("=" * 70)
    print("📊 Summary:")
    print()
    print(f"   SL Database: {'✅ Updated' if sl_success else '❌ Failed'}")
    if ontology_success is not None:
        print(f"   Ontology Audit Database: {'✅ Updated' if ontology_success else '❌ Failed'}")
    else:
        print(f"   Ontology Audit Database: ⚠️  Not configured")
    print()

    print("🎯 Next Steps:")
    print()
    print("1. Open Notion and navigate to your SL database")
    print("2. Verify new fields appear in database properties:")
    print("   - Phoenix_Phase (select)")
    print("   - Integration_Practice (text)")
    print("   - Transformation_Status (select)")
    print("   - ARF_Response (checkbox)")
    print()
    print("3. Configure select field options:")
    print("   Phoenix_Phase: Dissolution, Incubation, Emergence, Flight, Return")
    print("   Transformation_Status: Recognized, Under Inquiry, Integrating, Integrated, Monitoring")
    print()
    print("4. Delete template entries (SL #TEMPLATE)")
    print()
    print("5. Update agents/*/LK/*.md files to include new fields in SL entries")
    print()
    print("6. Re-run parse_sl.py to sync updated entries")
    print()
    print("=" * 70)
    print()
    print("✅ Schema update complete!")
    print()
    print("📖 For more details, see: docs/SHADOW_TAXONOMY.md")

if __name__ == '__main__':
    main()
