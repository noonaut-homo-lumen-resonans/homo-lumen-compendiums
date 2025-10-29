#!/usr/bin/env python3
"""
Sync Learning Point to Notion SLL database.
"""

import os
import json
import sys
from datetime import datetime
from notion_client import Client

def sync_to_notion(lp_data):
    """
    Create a new page in Notion SLL database with LP data.
    """
    
    notion_api_key = os.getenv('NOTION_API_KEY')
    sll_database_id = os.getenv('SLL_DATABASE_ID')
    
    if not notion_api_key or not sll_database_id:
        print("❌ Missing Notion credentials")
        sys.exit(1)
    
    # Initialize Notion client
    notion = Client(auth=notion_api_key)
    
    # Prepare properties for Notion database
    properties = {
        "LP_ID": {
            "title": [
                {
                    "text": {
                        "content": lp_data['lp_id']
                    }
                }
            ]
        },
        "Agent": {
            "select": {
                "name": lp_data['agent']
            }
        },
        "Date": {
            "date": {
                "start": datetime.now().strftime("%Y-%m-%d")
            }
        },
        "Content": {
            "rich_text": [
                {
                    "text": {
                        "content": lp_data['description']
                    }
                }
            ]
        },
        "Source": {
            "url": lp_data['commit_url']
        }
    }
    
    # Add categories if present
    if lp_data.get('categories'):
        properties["Category"] = {
            "multi_select": [{"name": cat} for cat in lp_data['categories']]
        }
    
    # Add tags if present
    if lp_data.get('tags'):
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in lp_data['tags']]
        }
    
    try:
        # Create page in Notion database
        response = notion.pages.create(
            parent={"database_id": sll_database_id},
            properties=properties
        )
        
        notion_url = response['url']
        print(f"✅ Learning Point synced to Notion SLL")
        print(f"   Notion URL: {notion_url}")
        print(f"::set-output name=notion_url::{notion_url}")
        
        return notion_url
        
    except Exception as e:
        print(f"❌ Failed to sync to Notion: {e}")
        sys.exit(1)

def main():
    lp_data_json = os.getenv('LP_DATA', '{}')
    
    try:
        lp_data = json.loads(lp_data_json)
    except json.JSONDecodeError:
        print("❌ Invalid LP data JSON")
        sys.exit(1)
    
    if not lp_data:
        print("❌ No LP data provided")
        sys.exit(1)
    
    sync_to_notion(lp_data)

if __name__ == '__main__':
    main()

