#!/usr/bin/env python3
"""
Inspect SLL (Shared Learning Library) database schema and count LPs.
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
NOTION_API_KEY = None
env_file = os.path.join(os.path.dirname(__file__), 'ama-backend', '.env')
if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('NOTION_API_KEY='):
                NOTION_API_KEY = line.split('=', 1)[1].strip()
                break

if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found")
    sys.exit(1)

notion = Client(auth=NOTION_API_KEY)

# SLL Database ID
SLL_DB_ID = '84da6cbd09d640fb868e41444b941991'

print("Fetching SLL database schema...")
db = notion.databases.retrieve(database_id=SLL_DB_ID)

print("\n" + "="*70)
print("SLL DATABASE PROPERTIES")
print("="*70)

# Temporal weight related properties
temporal_props = [
    'temporal_weight_raw',
    'temporal_weight',
    'half_life_days',
    'last_cited_timestamp',
    'reactivation_count',
    'freshness_status'
]

for prop_name in temporal_props:
    if prop_name in db['properties']:
        prop = db['properties'][prop_name]
        prop_type = prop['type']
        print(f"\n{prop_name}:")
        print(f"  Type: {prop_type}")

        if prop_type == 'formula':
            formula = prop['formula'].get('expression', 'N/A')
            print(f"  Formula: {formula}")
        elif prop_type == 'select':
            options = prop['select'].get('options', [])
            print(f"  Options: {[opt['name'] for opt in options]}")
    else:
        print(f"\n{prop_name}: NOT FOUND")

print("\n" + "="*70)

# Count LPs
print("\nFetching LPs...")
result = notion.databases.query(database_id=SLL_DB_ID)
lp_count = len(result['results'])

print(f"\nTotal LPs in SLL: {lp_count}")

# Show first LP if exists
if lp_count > 0:
    print("\nFirst LP sample:")
    first_lp = result['results'][0]
    props = first_lp['properties']

    print(f"  Name: {props['Name']['title'][0]['plain_text'] if props['Name']['title'] else 'N/A'}")
    print(f"  Created: {first_lp['created_time']}")

    for tprop in temporal_props:
        if tprop in props:
            val = props[tprop]
            if val['type'] == 'number':
                print(f"  {tprop}: {val['number']}")
            elif val['type'] == 'date':
                print(f"  {tprop}: {val['date']['start'] if val['date'] else None}")
            elif val['type'] == 'select':
                print(f"  {tprop}: {val['select']['name'] if val['select'] else None}")
            elif val['type'] == 'formula':
                print(f"  {tprop}: {val['formula'].get('number', 'N/A')}")

print("\n" + "="*70)
