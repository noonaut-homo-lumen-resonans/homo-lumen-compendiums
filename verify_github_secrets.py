import sys
import io

# Force UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Correct database IDs from Notion API (discovered earlier)
CORRECT_IDS = {
    'CS_DATABASE_ID': '2988fec9-2931-80bf-a32a-c404a311a07e',
    'SL_DATABASE_ID': '2988fec9-2931-8045-a354-ffe8d2f13fe1',
    'KD_DATABASE_ID': '2988fec9-2931-8083-8c4b-d5e13138ddf2',
    'EM_DATABASE_ID': '2988fec9-2931-8050-9658-e93447b3b259',
}

print("📋 CORRECT DATABASE IDs (from Notion API):\n")

for name, db_id in CORRECT_IDS.items():
    print(f"✅ {name}")
    print(f"   {db_id}")
    print(f"   (no hyphens: {db_id.replace('-', '')})")
    print()

print("\n" + "="*60)
print("COPY THESE VALUES TO GITHUB SECRETS:")
print("="*60 + "\n")

for name, db_id in CORRECT_IDS.items():
    print(f"{name}:")
    print(f"{db_id}")
    print()
