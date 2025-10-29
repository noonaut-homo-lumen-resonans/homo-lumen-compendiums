#!/usr/bin/env python3
"""
Audit All 6 Notion Databases
Quick status check for: SMK, CS, KD, EM, SLL, SL

Author: Code (Claude Code Agent)
Date: 29. oktober 2025
"""

import os
import sys
import io
from notion_client import Client
from datetime import datetime

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get Notion API key
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found in environment")
    sys.exit(1)

notion = Client(auth=NOTION_API_KEY)

# Database IDs
DATABASES = {
    'SMK': 'ba1d4a4407a5425fafd81d27dc02cc1c',
    'CS': '2988fec9293180bfa32ac404a311a07e',
    'KD': '2988fec9293180838c4bd5e13138ddf2',
    'EM': '2988fec9-2931-8050-9658-e93447b3b259',
    'SLL': '84da6cbd09d640fb868e41444b941991',
    'SL': '2988fec929318045a354ffe8d2f13fe1'
}

def get_database_stats(db_id, db_name):
    """Get statistics for a database."""
    try:
        # Query database
        response = notion.databases.query(database_id=db_id, page_size=100)

        total_entries = len(response['results'])
        active_entries = sum(1 for entry in response['results'] if not entry.get('archived', False))
        archived_entries = total_entries - active_entries

        # Get latest update
        latest_update = None
        if response['results']:
            latest_update = max(
                entry['last_edited_time']
                for entry in response['results']
            )

        # Count by agent if property exists
        agents = {}
        for entry in response['results']:
            props = entry.get('properties', {})

            # Try different agent property names
            agent_prop = props.get('Agent') or props.get('Agents Involved')

            if agent_prop:
                if agent_prop.get('type') == 'select' and agent_prop.get('select'):
                    agent_name = agent_prop['select']['name']
                    agents[agent_name] = agents.get(agent_name, 0) + 1
                elif agent_prop.get('type') == 'multi_select':
                    for agent in agent_prop.get('multi_select', []):
                        agent_name = agent['name']
                        agents[agent_name] = agents.get(agent_name, 0) + 1

        return {
            'name': db_name,
            'total': total_entries,
            'active': active_entries,
            'archived': archived_entries,
            'latest_update': latest_update,
            'agents': agents,
            'success': True
        }

    except Exception as e:
        return {
            'name': db_name,
            'error': str(e),
            'success': False
        }

def main():
    """Main audit function."""
    print("\n" + "="*70)
    print("DATABASE INFRASTRUCTURE AUDIT - BASELINE")
    print("="*70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    results = {}

    for db_name, db_id in DATABASES.items():
        print(f"Querying {db_name}...", end=" ")
        stats = get_database_stats(db_id, db_name)
        results[db_name] = stats

        if stats['success']:
            print(f"✅ {stats['active']} active entries")
        else:
            print(f"❌ Error: {stats.get('error', 'Unknown error')}")

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    total_entries = 0

    for db_name in ['SMK', 'CS', 'KD', 'EM', 'SLL', 'SL']:
        stats = results[db_name]

        if stats['success']:
            print(f"\n**{db_name}** - {stats['name']}")
            print(f"  Total Entries: {stats['total']}")
            print(f"  Active: {stats['active']}")
            print(f"  Archived: {stats['archived']}")

            if stats['latest_update']:
                print(f"  Latest Update: {stats['latest_update']}")

            if stats['agents']:
                print(f"  By Agent:")
                for agent, count in sorted(stats['agents'].items(), key=lambda x: -x[1]):
                    print(f"    - {agent}: {count}")

            total_entries += stats['active']
        else:
            print(f"\n**{db_name}** - ERROR")
            print(f"  {stats.get('error', 'Unknown error')}")

    print("\n" + "="*70)
    print(f"TOTAL ACTIVE ENTRIES ACROSS ALL DATABASES: {total_entries}")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
