#!/usr/bin/env python3
"""Quick script to check SQLite events database"""
import sqlite3
import json

conn = sqlite3.connect('data/ubuntu-playground.db')
cursor = conn.cursor()

# Count consultations
cursor.execute('SELECT COUNT(*) FROM events WHERE action = "consultation"')
count = cursor.fetchone()[0]
print(f'Total consultations in SQLite: {count}')

# Get latest consultations
cursor.execute('SELECT id, timestamp, agent, metadata FROM events WHERE action="consultation" ORDER BY id DESC LIMIT 5')
rows = cursor.fetchall()

if rows:
    print(f'\nLatest {len(rows)} consultation(s):')
    for row in rows:
        event_id, timestamp, agent, metadata_str = row
        try:
            metadata = json.loads(metadata_str)
            question = metadata.get('question', 'N/A')[:80]
            requester = metadata.get('requester', 'N/A')
            print(f'  ID {event_id} | {timestamp}')
            print(f'    Requester: {requester}')
            print(f'    Question: {question}')
        except:
            print(f'  ID {event_id} | {timestamp} | Agent: {agent}')
else:
    print('\nNo consultations found')

conn.close()
