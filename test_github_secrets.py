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

# IDs that SHOULD be in GitHub Secrets
GITHUB_SECRETS = {
    'CS_DATABASE_ID': '2988fec9-2931-80bf-a32a-c404a311a07e',
    'SL_DATABASE_ID': '2988fec9-2931-8045-a354-ffe8d2f13fe1',
    'KD_DATABASE_ID': '2988fec9-2931-8083-8c4b-d5e13138ddf2',
    'EM_DATABASE_ID': '2988fec9-2931-8050-9658-e93447b3b259',
}

print("🧪 Testing GitHub Secrets by querying Notion databases...\n")

for secret_name, db_id in GITHUB_SECRETS.items():
    url = f'https://api.notion.com/v1/databases/{db_id}'
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': '2022-06-28'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        db_data = response.json()
        title_parts = db_data.get('title', [])
        if title_parts:
            title = title_parts[0].get('plain_text', 'Untitled')
        else:
            title = 'Untitled'
        print(f"✅ {secret_name}")
        print(f"   Database: {title}")
        print(f"   ID: {db_id}")
        print(f"   Status: ACCESSIBLE ✓")
    else:
        print(f"❌ {secret_name}")
        print(f"   ID: {db_id}")
        print(f"   Status: FAILED (HTTP {response.status_code})")
        print(f"   Error: {response.text[:100]}")
    print()

print("\n" + "="*60)
print("VERIFICATION COMPLETE")
print("="*60)
