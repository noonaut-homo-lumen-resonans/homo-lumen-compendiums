import requests
import os
import sys
import io

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found in environment")
    print("Set it with: export NOTION_API_KEY='your_key_here'")
    sys.exit(1)

url = 'https://api.notion.com/v1/search'
headers = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json'
}
data = {
    'filter': {
        'value': 'database',
        'property': 'object'
    }
}

response = requests.post(url, headers=headers, json=data)
print("Status:", response.status_code)

if response.status_code == 200:
    databases = response.json()
    print(f"\nFound {len(databases.get('results', []))} databases:\n")
    for db in databases.get('results', []):
        title_parts = db.get('title', [])
        if title_parts:
            title = title_parts[0].get('plain_text', 'Untitled')
        else:
            title = 'Untitled'
        db_id = db.get('id', 'Unknown')
        
        # Look for CS/SL/KD/EM databases
        if any(keyword in title for keyword in ['Case Stud', 'Shadow', 'Critical', 'Emergent', 'CS', 'SL', 'KD', 'EM']):
            print(f"🎯 {title}")
            print(f"   ID: {db_id}")
            print(f"   ID (no hyphens): {db_id.replace('-', '')}")
            print()
else:
    print("Error:", response.text)
