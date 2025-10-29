#!/usr/bin/env python3
"""Check GENOMOS blockchain database directly"""
import sqlite3
import json

conn = sqlite3.connect('data/genomos.db')
cursor = conn.cursor()

# Count blocks
cursor.execute('SELECT COUNT(*) FROM dna_blocks')
total = cursor.fetchone()[0]
print(f'Total blocks in GENOMOS database: {total}')

# Count by gene type
cursor.execute('SELECT gene_type, COUNT(*) FROM dna_blocks GROUP BY gene_type')
counts = cursor.fetchall()
print('\nGene type counts:')
for gene_type, count in counts:
    print(f'  {gene_type}: {count}')

# Get consultation blocks
cursor.execute('SELECT idx, hash, gene_type, agent, timestamp FROM dna_blocks WHERE gene_type = "consultation" ORDER BY idx DESC')
consultations = cursor.fetchall()

print(f'\nConsultation blocks: {len(consultations)}')
for idx, hash_val, gene_type, agent, timestamp in consultations:
    print(f'  Block #{idx}: {hash_val[:16]}... by {agent} at {timestamp}')

    # Get block data
    cursor.execute('SELECT data FROM dna_blocks WHERE idx = ?', (idx,))
    data_json = cursor.fetchone()[0]
    data = json.loads(data_json)
    question = data.get('question', 'N/A')[:70]
    requester = data.get('requester', 'N/A')
    print(f'    Question: {question}')
    print(f'    Requester: {requester}')

# Get latest block
cursor.execute('SELECT idx, gene_type, agent, timestamp FROM dna_blocks ORDER BY idx DESC LIMIT 1')
latest = cursor.fetchone()
print(f'\nLatest block: #{latest[0]} ({latest[1]}) by {latest[2]} at {latest[3]}')

conn.close()
