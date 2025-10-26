#!/usr/bin/env python3
"""
Sync LK (Levende Kompendium) metadata to Notion database.

Agent: Claude Code
Date: 26. oktober 2025
"""

import os
import json
from notion_client import Client

def sync_lk_to_notion(lk_metadata, notion, database_id, commit_sha, commit_url):
    """
    Create or update LK page in Notion database.
    """
    agent = lk_metadata.get('agent', 'Unknown')
    version = lk_metadata.get('version', 'Unknown')
    title = lk_metadata.get('title', f"{agent} Levende Kompendium {version}")

    print(f"\nSyncing {agent} LK {version}: {title}")

    # Search for existing page by Agent + Version
    existing_page = None
    try:
        results = notion.databases.query(
            database_id=database_id,
            filter={
                "and": [
                    {
                        "property": "Agent",
                        "select": {
                            "equals": agent
                        }
                    },
                    {
                        "property": "Version",
                        "rich_text": {
                            "equals": version
                        }
                    }
                ]
            }
        )
        if results['results']:
            existing_page = results['results'][0]
            print(f"  Found existing page: {existing_page['id']}")
    except Exception as e:
        print(f"  Error searching for existing page: {e}")

    # Prepare properties
    properties = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": title[:2000]  # Notion title limit
                    }
                }
            ]
        },
        "Agent": {
            "select": {
                "name": agent
            }
        },
        "Version": {
            "rich_text": [
                {
                    "text": {
                        "content": version
                    }
                }
            ]
        },
        "GitHub URL": {
            "url": lk_metadata.get('github_url', '')
        },
        "Commit SHA": {
            "rich_text": [
                {
                    "text": {
                        "content": commit_sha[:8] if commit_sha else ''
                    }
                }
            ]
        }
    }

    # Add optional fields
    if 'date' in lk_metadata and lk_metadata['date']:
        properties["Last Updated"] = {
            "date": {
                "start": str(lk_metadata['date'])
            }
        }

    if 'status' in lk_metadata and lk_metadata['status']:
        properties["Status"] = {
            "select": {
                "name": lk_metadata['status']
            }
        }

    if 'role' in lk_metadata and lk_metadata['role']:
        properties["Role"] = {
            "rich_text": [
                {
                    "text": {
                        "content": lk_metadata['role']
                    }
                }
            ]
        }

    if 'word_count' in lk_metadata and lk_metadata['word_count']:
        properties["Word Count"] = {
            "number": lk_metadata['word_count']
        }

    if 'phase' in lk_metadata and lk_metadata['phase']:
        properties["Phase"] = {
            "select": {
                "name": lk_metadata['phase']
            }
        }

    if 'neuroanatomy' in lk_metadata and lk_metadata['neuroanatomy']:
        properties["Neuroanatomy"] = {
            "select": {
                "name": lk_metadata['neuroanatomy']
            }
        }

    if 'key_dimensions' in lk_metadata and lk_metadata['key_dimensions']:
        # Ensure key_dimensions is a list
        dimensions = lk_metadata['key_dimensions']
        if isinstance(dimensions, str):
            dimensions = [dimensions]
        properties["Key Dimensions"] = {
            "multi_select": [
                {"name": dim} for dim in dimensions if dim
            ]
        }

    if 'tags' in lk_metadata and lk_metadata['tags']:
        # Ensure tags is a list
        tags = lk_metadata['tags']
        if isinstance(tags, str):
            tags = [tags]
        # Note: LK database might not have Tags property, handle gracefully
        try:
            properties["Tags"] = {
                "multi_select": [
                    {"name": tag} for tag in tags if tag
                ]
            }
        except:
            pass

    # Create or update page
    try:
        if existing_page:
            # Update existing page
            notion.pages.update(
                page_id=existing_page['id'],
                properties=properties
            )
            print(f"  ✅ Updated existing page")
            return existing_page['id']
        else:
            # Create new page
            new_page = notion.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            print(f"  ✅ Created new page: {new_page['id']}")
            return new_page['id']
    except Exception as e:
        print(f"  ❌ Error syncing to Notion: {e}")
        return None

def main():
    """Main sync process."""
    print("=" * 60)
    print("LK Notion Sync")
    print("Agent: Claude Code")
    print("=" * 60)

    # Get environment variables
    notion_api_key = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('LK_DATABASE_ID')
    lk_data_json = os.getenv('LK_DATA')
    commit_sha = os.getenv('COMMIT_SHA', '')
    commit_url = os.getenv('COMMIT_URL', '')

    if not notion_api_key:
        print("❌ NOTION_API_KEY not set")
        return

    if not database_id:
        print("❌ LK_DATABASE_ID not set")
        return

    if not lk_data_json:
        print("❌ LK_DATA not provided")
        return

    # Parse LK data
    try:
        lk_data = json.loads(lk_data_json)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing LK_DATA: {e}")
        return

    # Initialize Notion client
    notion = Client(auth=notion_api_key)

    # Sync each LK
    synced_count = 0
    for lk_metadata in lk_data:
        page_id = sync_lk_to_notion(
            lk_metadata,
            notion,
            database_id,
            commit_sha,
            commit_url
        )
        if page_id:
            synced_count += 1

    print("\n" + "=" * 60)
    print(f"✅ Synced {synced_count}/{len(lk_data)} LKs to Notion")
    print("=" * 60)

if __name__ == '__main__':
    main()
