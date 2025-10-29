import requests
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

# Search for all databases to find LK, SLL, SMK
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

if response.status_code == 200:
    databases = response.json()
    print(f"🔍 Found {len(databases.get('results', []))} databases total\n")
    print("="*60)
    print("DATABASES FOR GITHUB SECRETS:")
    print("="*60 + "\n")
    
    for db in databases.get('results', []):
        title_parts = db.get('title', [])
        if title_parts:
            title = title_parts[0].get('plain_text', 'Untitled')
        else:
            title = 'Untitled'
        db_id = db.get('id', 'Unknown')
        
        # Check for relevant databases
        if any(keyword in title for keyword in [
            'Case Stud', 'Shadow', 'Critical', 'Emergent',
            'SLL', 'Shared Learning', 'SMK', 'Symbiotisk',
            'Learning Points', 'LK'
        ]):
            print(f"📊 {title}")
            print(f"   ID: {db_id}")
            
            # Suggest secret name
            if 'Case Stud' in title:
                print(f"   Secret: CS_DATABASE_ID")
            elif 'Shadow' in title:
                print(f"   Secret: SL_DATABASE_ID")
            elif 'Critical' in title:
                print(f"   Secret: KD_DATABASE_ID")
            elif 'Emergent' in title:
                print(f"   Secret: EM_DATABASE_ID")
            elif 'SLL' in title or 'Shared Learning' in title:
                print(f"   Secret: SLL_DATABASE_ID")
            elif 'SMK' in title or 'Symbiotisk' in title:
                print(f"   Secret: SMK_DATABASE_ID")
            elif 'Learning Points' in title:
                print(f"   Secret: LK_DATABASE_ID")
            print()
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
