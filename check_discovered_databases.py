#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check discovered Notion databases and extract their schemas.

This script queries the Notion API to get database schemas for the discovered databases.
"""

import os
import sys
import io
import requests
import json

# Force UTF-8 encoding for stdout
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
NOTION_API_VERSION = '2022-06-28'

HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': NOTION_API_VERSION
}

# Extracted database IDs from URLs and relations
DATABASES = {
    # Already retrieved
    'Puls': '1dd8fec9293180298d8bd2c5d5330563',
    'EchoBook': '1dd8fec92931808ebc38ce8fc988b1a0',
    'Agentdatabase': '1dd8fec929318061be62facd8439da53',
    'Praksiser': '1e68fec9293180ba9264dd5dafbf53b6',
    'Voktere': '1e68fec929318052afe2fe6ee282108e',
    'Kunnskapsbase': '1e68fec929318069bd61e2a8f22221f7',
    'Ontology Audit': '28e8fec9293180cbaa57d99549147b97',
    'MCP Audit Log': '28e8fec929318056a2dcc2bb28fd166d',
    'NAV-Losen Oppgaver': '8b18dd1769ab48a6a70ec38b74e5140f',
    'Emergent Patterns': '2988fec9293180509658e93447b3b259',
    # Database IDs found via relations (these are the actual database IDs, not page IDs)
    'Spektral Dimensjoner': '1d48fec929318080ba8aa5d6b099021ccd',
    'Phoenix-syklus': '1d48fec92931800289ddeba82b94fbe3',
    'How we feel': '1d48fec929318054ae54f583f6c08f72',
    'Dagbok 2020': '1db8fec9293180a9a0eec9f7508588f3',
}

def get_database_schema(db_id, db_name):
    """Get database schema from Notion API."""
    url = f'https://api.notion.com/v1/databases/{db_id}'

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            data = response.json()

            print(f"\n{'='*80}")
            print(f"DATABASE: {db_name}")
            print(f"{'='*80}")
            print(f"ID: {db_id}")

            # Safely extract title
            title = 'N/A'
            if data.get('title'):
                try:
                    title = data['title'][0].get('plain_text', 'N/A')
                except (IndexError, KeyError):
                    title = 'N/A'

            # Safely extract description
            description = 'N/A'
            if data.get('description'):
                try:
                    description = data['description'][0].get('plain_text', 'N/A')
                except (IndexError, KeyError):
                    description = 'N/A'

            print(f"Title: {title}")
            print(f"Description: {description}")

            print(f"\nProperties:")
            properties = data.get('properties', {})
            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get('type', 'unknown')
                try:
                    print(f"  - {prop_name}: {prop_type}")

                    # Show additional details for select/multi_select
                    if prop_type in ['select', 'multi_select']:
                        options = prop_data.get(prop_type, {}).get('options', [])
                        if options and len(options) <= 10:  # Limit to 10 options for readability
                            option_names = [opt.get('name', '?') for opt in options]
                            print(f"    Options: {', '.join(option_names)}")
                        elif options:
                            print(f"    Options: {len(options)} total")
                except Exception as prop_error:
                    print(f"  - {prop_name}: {prop_type} (error displaying: {prop_error})")

            return data
        else:
            print(f"\nFAILED to fetch {db_name}")
            print(f"   Status: {response.status_code}")

            # Try to extract error message
            try:
                error_data = response.json()
                error_msg = error_data.get('message', response.text[:200])
                print(f"   Message: {error_msg}")
            except:
                print(f"   Response: {response.text[:200]}")

            return None

    except Exception as e:
        print(f"\nERROR fetching {db_name}: {str(e)}")
        return None

def main():
    """Main execution."""
    print("Checking discovered Notion databases...")

    schemas = {}
    for db_name, db_id in DATABASES.items():
        schema = get_database_schema(db_id, db_name)
        if schema:
            schemas[db_name] = schema

    print(f"\n{'='*80}")
    print(f"Successfully retrieved {len(schemas)}/{len(DATABASES)} database schemas")
    print(f"{'='*80}")

    # Save schemas to file
    with open('discovered_database_schemas.json', 'w', encoding='utf-8') as f:
        json.dump(schemas, f, indent=2, ensure_ascii=False)

    print(f"\nSchemas saved to: discovered_database_schemas.json")

if __name__ == '__main__':
    main()
