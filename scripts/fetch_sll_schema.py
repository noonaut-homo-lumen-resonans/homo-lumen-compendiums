#!/usr/bin/env python3
"""
Fetch SLL Database Schema from Notion
"""

import os
import requests
import json

NOTION_TOKEN = os.getenv("NOTION_API_KEY", "***REMOVED***")
SLL_DATABASE_ID = "84da6cbd09d640fb868e41444b941991"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def fetch_database_schema():
    """Fetch database schema to see all properties"""
    url = f"https://api.notion.com/v1/databases/{SLL_DATABASE_ID}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        data = response.json()

        # Save full schema to file first (avoid encoding issues)
        with open("sll_schema.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("="*80)
        print("SLL Database Schema")
        print("="*80)

        # Windows-safe printing (ASCII only)
        try:
            title_text = data.get('title', [{}])[0].get('plain_text', 'Unknown')
            print(f"\nDatabase Title: {title_text}")
        except:
            print(f"\nDatabase Title: [encoding error - see sll_schema.json]")

        properties = data.get("properties", {})
        print(f"\nProperties ({len(properties)} total):\n")

        for prop_name, prop_config in properties.items():
            prop_type = prop_config.get("type")
            try:
                print(f"  - {prop_name:<30} [{prop_type}]")

                # Show select options if available
                if prop_type == "select" and "select" in prop_config:
                    options = prop_config["select"].get("options", [])
                    if options:
                        opt_names = [opt['name'] for opt in options]
                        print(f"      Options: {', '.join(opt_names)}")

                # Show multi-select options if available
                if prop_type == "multi_select" and "multi_select" in prop_config:
                    options = prop_config["multi_select"].get("options", [])
                    if options:
                        opt_names = [opt['name'] for opt in options]
                        print(f"      Options: {', '.join(opt_names)}")
            except Exception as e:
                print(f"  - {prop_name}: [encoding error]")

        print("\n" + "="*80)
        print("\nFull schema saved to: sll_schema.json")

        return data

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Failed to fetch schema: {e}")
        print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return None


if __name__ == "__main__":
    fetch_database_schema()
