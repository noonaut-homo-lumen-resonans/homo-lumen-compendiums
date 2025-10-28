#!/usr/bin/env python3
"""Archive empty duplicate databases"""
import sys
import io
from notion_client import Client

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

notion = Client(auth='***REMOVED***')

# Empty databases to archive
databases_to_archive = {
    'SLL 2 (empty duplicate)': 'fda5f6dac3544d81a257a07685f674ed',
    'Emergent Patterns 1 (empty)': '2988fec9293180509658e93447b3b259'
}

print('=' * 70)
print('ARCHIVING EMPTY DUPLICATE DATABASES')
print('=' * 70)

for name, db_id in databases_to_archive.items():
    try:
        # First check current status
        db_info = notion.databases.retrieve(database_id=db_id)
        title = db_info.get('title', [{}])[0].get('plain_text', 'No title')
        archived = db_info.get('archived', False)

        print(f'\n{name}')
        print(f'   Title: {title}')
        print(f'   ID: {db_id}')
        print(f'   Currently archived: {archived}')

        if not archived:
            # Archive the database
            notion.databases.update(
                database_id=db_id,
                archived=True
            )
            print(f'   ✅ Successfully archived')
        else:
            print(f'   ℹ️  Already archived')

    except Exception as e:
        print(f'   ❌ Error: {e}')

print('\n' + '=' * 70)
print('CLEANUP COMPLETE')
print('=' * 70)
