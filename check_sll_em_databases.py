#!/usr/bin/env python3
"""Check SLL and Emergent Patterns databases"""
import sys
import io
from notion_client import Client

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

notion = Client(auth='***REMOVED***')

databases = {
    'Emergent Patterns 1': '2988fec9293180509658e93447b3b259',
    'Emergent Patterns 2': '078f70c98954496c8b581e0a87c12127',
    'SLL 1': '84da6cbd09d640fb868e41444b941991',
    'SLL 2': 'fda5f6dac3544d81a257a07685f674ed'
}

print('=' * 70)
print('CHECKING SLL AND EMERGENT PATTERNS DATABASES')
print('=' * 70)

for name, db_id in databases.items():
    try:
        response = notion.databases.query(database_id=db_id)
        count = len(response['results'])
        has_more = response.get('has_more', False)

        # Get database info
        db_info = notion.databases.retrieve(database_id=db_id)
        title = db_info.get('title', [{}])[0].get('plain_text', 'No title')
        archived = db_info.get('archived', False)

        if archived:
            status = 'ARCHIVED'
        elif count > 0:
            status = 'OK'
        else:
            status = 'EMPTY'
        arch_status = ' [ARCHIVED]' if archived else ''
        print(f'\n[{status}] {name}{arch_status}')
        print(f'   Title: {title}')
        print(f'   ID: {db_id}')
        print(f'   Entries: {count}')
        if has_more:
            print(f'   Note: Has more pages (paginated)')
    except Exception as e:
        print(f'\n[ERROR] {name}')
        print(f'   ID: {db_id}')
        print(f'   Error: {e}')

print('\n' + '=' * 70)
