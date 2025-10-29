#!/usr/bin/env python3
"""
Inspect Visual Essence Library database schema.
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

# Database ID from URL
VE_DATABASE_ID = "29b8fec9293180ed8478f96bf58418ca"

# Format database ID (add dashes if needed)
if '-' not in VE_DATABASE_ID:
    # Format: 29b8fec9-2931-80ed-8478-f96bf58418ca
    formatted_id = f"{VE_DATABASE_ID[:8]}-{VE_DATABASE_ID[8:12]}-{VE_DATABASE_ID[12:16]}-{VE_DATABASE_ID[16:20]}-{VE_DATABASE_ID[20:]}"
else:
    formatted_id = VE_DATABASE_ID

print(f"\n[INFO] Inspecting VE Database: {formatted_id}\n")

# Notion API headers
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Fetch database schema
url = f"https://api.notion.com/v1/databases/{formatted_id}"

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    db_data = response.json()

    print(f"[SUCCESS] Database Name: {db_data.get('title', [{}])[0].get('plain_text', 'Unknown')}")
    print(f"[INFO] Database ID: {db_data.get('id')}\n")

    print("=" * 80)
    print("DATABASE PROPERTIES")
    print("=" * 80)

    properties = db_data.get('properties', {})

    for prop_name, prop_data in properties.items():
        prop_type = prop_data.get('type')
        print(f"\n[PROPERTY] {prop_name}")
        print(f"  Type: {prop_type}")

        # Show additional details for specific types
        if prop_type == 'select':
            options = prop_data.get('select', {}).get('options', [])
            if options:
                print(f"  Options: {', '.join([opt['name'] for opt in options])}")

        elif prop_type == 'multi_select':
            options = prop_data.get('multi_select', {}).get('options', [])
            if options:
                print(f"  Options: {', '.join([opt['name'] for opt in options])}")

        elif prop_type == 'relation':
            database_id = prop_data.get('relation', {}).get('database_id')
            print(f"  Related Database ID: {database_id}")

    print("\n" + "=" * 80)
    print(f"[INFO] Total Properties: {len(properties)}")
    print("=" * 80)

    # Check for expected properties
    expected_props = [
        've_id', 'name', 'essence_type', 'description',
        'related_smks', 'related_lps', 'asset_status',
        'asset_format', 'created_date', 'metaphor'
    ]

    print(f"\n[VALIDATION] Expected properties: {len(expected_props)}")
    print(f"[VALIDATION] Found properties: {len(properties)}")

    missing = [prop for prop in expected_props if prop not in properties]
    extra = [prop for prop in properties if prop not in expected_props]

    if missing:
        print(f"\n[WARNING] Missing properties: {', '.join(missing)}")
    else:
        print("\n[SUCCESS] All expected properties found!")

    if extra:
        print(f"[INFO] Additional properties: {', '.join(extra)}")

except requests.exceptions.HTTPError as e:
    print(f"[ERROR] HTTP Error: {e}")
    print(f"[ERROR] Response: {e.response.text}")
    sys.exit(1)

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    sys.exit(1)
