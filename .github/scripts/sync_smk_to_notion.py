#!/usr/bin/env python3
"""
Sync SMK metadata to Notion database.

Agent: Claude Code
Date: 26. oktober 2025
"""

import os
import json
from notion_client import Client

def sync_smk_to_notion(smk_metadata, notion, database_id, commit_sha, commit_url):
    """
    Create or update SMK page in Notion database.
    """
    smk_number = smk_metadata.get('smk_number')
    title = smk_metadata.get('title', 'Untitled SMK')
    agent = smk_metadata.get('agent', '')
    date = smk_metadata.get('date', '')
    tags = smk_metadata.get('tags', [])
    status = smk_metadata.get('status', 'COMPLETE')
    github_url = smk_metadata.get('github_url', '')

    print(f"\nSyncing SMK #{smk_number}: {title}")

    # Search for existing page by SMK number (including archived pages)
    existing_page = None
    try:
        # First, try to find active (non-archived) pages
        results = notion.databases.query(
            database_id=database_id,
            filter={
                "property": "SMK Number",
                "number": {
                    "equals": smk_number
                }
            }
        )
        if results['results']:
            existing_page = results['results'][0]
            print(f"  Found existing page: {existing_page['id']}")
        else:
            # If no active page found, search for archived pages
            # Note: Notion API returns only non-archived by default
            # We need to search all pages to find archived ones
            all_pages = []
            start_cursor = None
            while True:
                query_params = {"database_id": database_id}
                if start_cursor:
                    query_params["start_cursor"] = start_cursor

                page_results = notion.databases.query(**query_params)
                all_pages.extend(page_results['results'])

                if not page_results.get('has_more'):
                    break
                start_cursor = page_results.get('next_cursor')

            # Check all pages (including archived) for matching SMK number
            for page in all_pages:
                try:
                    props = page.get('properties', {})
                    page_smk_num = props.get('SMK Number', {}).get('number')
                    if page_smk_num == smk_number:
                        existing_page = page
                        if page.get('archived'):
                            print(f"  Found ARCHIVED page: {page['id']} - will unarchive")
                        else:
                            print(f"  Found existing page: {page['id']}")
                        break
                except:
                    continue
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
        "SMK Number": {
            "number": smk_number
        },
        "Status": {
            "select": {
                "name": status
            }
        },
        "GitHub URL": {
            "url": github_url
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

    # Add agent if present
    if agent:
        properties["Agent"] = {
            "select": {
                "name": agent
            }
        }

    # Add date if present
    if date:
        properties["Date"] = {
            "date": {
                "start": str(date)
            }
        }

    # Add tags if present
    if tags:
        # Ensure tags is a list
        if isinstance(tags, str):
            tags = [tags]
        properties["Tags"] = {
            "multi_select": [
                {"name": tag} for tag in tags if tag
            ]
        }

    # Create or update page
    try:
        if existing_page:
            # If page is archived, unarchive it first
            if existing_page.get('archived'):
                print(f"  Unarchiving page...")
                notion.pages.update(
                    page_id=existing_page['id'],
                    archived=False
                )
                print(f"  [OK] Unarchived page")

            # Update existing page
            notion.pages.update(
                page_id=existing_page['id'],
                properties=properties
            )
            print(f"  [OK] Updated existing page")
            return existing_page['id']
        else:
            # Create new page
            new_page = notion.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            print(f"  [OK] Created new page: {new_page['id']}")
            return new_page['id']
    except Exception as e:
        print(f"  [ERROR] Error syncing to Notion: {e}")
        return None

def main():
    """Main sync process."""
    print("=" * 60)
    print("SMK Notion Sync")
    print("Agent: Claude Code")
    print("=" * 60)

    # Get environment variables
    notion_api_key = os.getenv('NOTION_API_KEY')
    database_id = os.getenv('SMK_DATABASE_ID')
    smk_data_json = os.getenv('SMK_DATA')
    commit_sha = os.getenv('COMMIT_SHA', '')
    commit_url = os.getenv('COMMIT_URL', '')

    if not notion_api_key:
        print("[ERROR] NOTION_API_KEY not set")
        return

    if not database_id:
        print("[ERROR] SMK_DATABASE_ID not set")
        return

    if not smk_data_json:
        print("[ERROR] SMK_DATA not provided")
        return

    # Parse SMK data
    try:
        smk_data = json.loads(smk_data_json)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error parsing SMK_DATA: {e}")
        return

    # Initialize Notion client
    notion = Client(auth=notion_api_key)

    # Sync each SMK
    synced_count = 0
    for smk_metadata in smk_data:
        page_id = sync_smk_to_notion(
            smk_metadata,
            notion,
            database_id,
            commit_sha,
            commit_url
        )
        if page_id:
            synced_count += 1

    print("\n" + "=" * 60)
    print(f"[OK] Synced {synced_count}/{len(smk_data)} SMKs to Notion")
    print("=" * 60)

if __name__ == '__main__':
    main()
