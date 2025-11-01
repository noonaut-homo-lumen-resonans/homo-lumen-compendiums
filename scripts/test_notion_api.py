#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Notion API Connection
Tests connection to Notion API using key from Secret Manager or environment variable
"""

import os
import sys
from typing import Optional

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from google.cloud import secretmanager
    SECRET_MANAGER_AVAILABLE = True
except ImportError:
    SECRET_MANAGER_AVAILABLE = False
    print("[!] google-cloud-secret-manager ikke installert")
    print("    Installer med: pip install google-cloud-secret-manager")

PROJECT_ID = "dotted-stage-476513-r4"
SECRET_NAME = "notion-api-key"


def get_notion_api_key() -> Optional[str]:
    """Get Notion API key from Secret Manager or environment variable"""

    # Try environment variable first
    api_key = os.getenv("NOTION_API_KEY")
    if api_key:
        print(f"[*] Funnet NOTION_API_KEY i environment variable")
        return api_key

    # Try Secret Manager
    if not SECRET_MANAGER_AVAILABLE:
        print("[X] Secret Manager ikke tilgjengelig")
        return None

    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{SECRET_NAME}/versions/latest"

        print(f"[*] Henter Notion API key fra Secret Manager...")
        response = client.access_secret_version(request={"name": name})
        api_key = response.payload.data.decode("UTF-8")

        print(f"[OK] Notion API key hentet fra Secret Manager")
        return api_key
    except Exception as e:
        print(f"[X] Kunne ikke hente fra Secret Manager: {e}")
        return None


def test_notion_api(api_key: str) -> bool:
    """Test Notion API connection"""
    try:
        import requests

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

        print("[*] Tester Notion API connection...")
        print(f"    URL: https://api.notion.com/v1/users/me")

        response = requests.get(
            "https://api.notion.com/v1/users/me",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            user_data = response.json()
            print("\n[OK] Notion API Connection Successful!")
            print("=" * 60)
            print(f"User ID: {user_data.get('id', 'N/A')}")
            print(f"Name: {user_data.get('name', 'N/A')}")

            if 'bot' in user_data:
                bot_info = user_data['bot']
                print(f"Bot Owner: {bot_info.get('owner', {}).get('user', {}).get('name', 'N/A')}")
                print(f"Workspace: {bot_info.get('workspace_name', 'N/A')}")

            print("=" * 60)
            return True
        else:
            print(f"\n[X] Notion API Error: {response.status_code}")
            print(f"    Response: {response.text}")
            return False

    except ImportError:
        print("[X] requests library ikke installert")
        print("    Installer med: pip install requests")
        return False
    except Exception as e:
        print(f"[X] Feil ved API test: {e}")
        return False


def main():
    print("=" * 60)
    print("Notion API Connection Test")
    print("=" * 60)
    print()

    api_key = get_notion_api_key()

    if not api_key:
        print("\n[X] Notion API Key ikke funnet!")
        print("\n💡 Hvordan sette opp:")
        print("   1. Hent Notion API key fra: https://www.notion.so/my-integrations")
        print("   2. Lagre i Secret Manager:")
        print("      bash scripts/save_notion_key_to_secret_manager.sh")
        print("      eller")
        print("      .\\scripts\\save_notion_key_to_secret_manager.ps1")
        print("   3. Eller sett environment variable:")
        print("      export NOTION_API_KEY='secret_...'")
        print("      eller")
        print("      $env:NOTION_API_KEY = 'secret_...'")
        return False

    if len(api_key) < 20:
        print(f"[X] API key ser for kort ut: {len(api_key)} tegn")
        return False

    print(f"[OK] API key hentet (lengde: {len(api_key)} tegn, starter med: {api_key[:10]}...)")

    success = test_notion_api(api_key)

    if success:
        print("\n[OK] Notion API test vellykket!")
        print("\n💡 Du kan nå bruke Notion MCP i Cursor")
        return True
    else:
        print("\n[X] Notion API test feilet")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)



