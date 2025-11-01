#!/usr/bin/env python3
"""
Hent Notion API Key fra Google Secret Manager
Brukes av andre scripts og applikasjoner
"""

import sys
import os
from google.cloud import secretmanager

PROJECT_ID = "dotted-stage-476513-r4"
SECRET_NAME = "notion-api-key"

def get_notion_api_key():
    """Hent Notion API Key fra Secret Manager"""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{SECRET_NAME}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error: Could not retrieve Notion API key from Secret Manager: {e}", file=sys.stderr)
        print(f"\nTroubleshooting:", file=sys.stderr)
        print(f"  1. Check authentication: gcloud auth application-default login", file=sys.stderr)
        print(f"  2. Check secret exists: gcloud secrets list --project={PROJECT_ID}", file=sys.stderr)
        print(f"  3. Check permissions: gcloud projects get-iam-policy {PROJECT_ID}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    key = get_notion_api_key()
    print(key)

