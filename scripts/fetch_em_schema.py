#!/usr/bin/env python3
"""
Fetch EM Database Schema
Quick inspection of Emergent Patterns database properties

Author: Code (Claude Code Agent)
Date: 29. oktober 2025
"""

import os
import sys
import io
from notion_client import Client
import json

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get Notion API key
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found in environment")
    sys.exit(1)

notion = Client(auth=NOTION_API_KEY)

# EM Database ID
EM_DATABASE_ID = '2988fec9-2931-8050-9658-e93447b3b259'

def main():
    """Fetch and display EM database schema."""
    print("\n" + "="*70)
    print("EM DATABASE SCHEMA INSPECTION")
    print("="*70)
    print(f"Database ID: {EM_DATABASE_ID}\n")

    try:
        # Retrieve database
        database = notion.databases.retrieve(database_id=EM_DATABASE_ID)

        print("DATABASE PROPERTIES:\n")

        properties = database.get('properties', {})

        if not properties:
            print("⚠️  NO PROPERTIES FOUND")
        else:
            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get('type', 'unknown')
                print(f"  - {prop_name}: {prop_type}")

                # Show select/multi_select options
                if prop_type == 'select':
                    options = prop_data.get('select', {}).get('options', [])
                    if options:
                        print(f"    Options: {', '.join([opt['name'] for opt in options])}")

                if prop_type == 'multi_select':
                    options = prop_data.get('multi_select', {}).get('options', [])
                    if options:
                        print(f"    Options: {', '.join([opt['name'] for opt in options])}")

                # Show relation target
                if prop_type == 'relation':
                    relation_db = prop_data.get('relation', {}).get('database_id')
                    print(f"    → Database: {relation_db}")

        print(f"\n**Total Properties**: {len(properties)}")

        # Fetch one entry to see actual data
        print("\n" + "="*70)
        print("SAMPLE ENTRY (First Entry)")
        print("="*70 + "\n")

        response = notion.databases.query(database_id=EM_DATABASE_ID, page_size=1)

        if response.get('results'):
            entry = response['results'][0]
            entry_props = entry.get('properties', {})

            for prop_name, prop_value in entry_props.items():
                prop_type = prop_value.get('type')

                value_str = ""

                if prop_type == 'title':
                    if prop_value.get('title'):
                        value_str = prop_value['title'][0].get('plain_text', '')
                elif prop_type == 'rich_text':
                    if prop_value.get('rich_text'):
                        value_str = prop_value['rich_text'][0].get('plain_text', '')
                elif prop_type == 'select':
                    if prop_value.get('select'):
                        value_str = prop_value['select'].get('name', '')
                elif prop_type == 'multi_select':
                    if prop_value.get('multi_select'):
                        value_str = ', '.join([tag['name'] for tag in prop_value['multi_select']])
                elif prop_type == 'number':
                    value_str = str(prop_value.get('number', ''))
                elif prop_type == 'date':
                    if prop_value.get('date'):
                        value_str = prop_value['date'].get('start', '')

                print(f"  {prop_name} ({prop_type}): {value_str}")

        else:
            print("⚠️  No entries found in database")

        print("\n" + "="*70 + "\n")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
