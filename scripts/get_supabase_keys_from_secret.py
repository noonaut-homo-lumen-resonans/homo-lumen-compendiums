#!/usr/bin/env python3
"""
Hent Supabase API Keys fra Google Secret Manager
Brukes av andre scripts og applikasjoner
"""

import sys
import os
from google.cloud import secretmanager

PROJECT_ID = "dotted-stage-476513-r4"

def get_supabase_anon_key():
    """Hent Supabase Anon Key fra Secret Manager"""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/supabase-anon-key/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error: Could not retrieve Supabase Anon Key from Secret Manager: {e}", file=sys.stderr)
        print(f"\nTroubleshooting:", file=sys.stderr)
        print(f"  1. Check authentication: gcloud auth application-default login", file=sys.stderr)
        print(f"  2. Check secret exists: gcloud secrets list --project={PROJECT_ID}", file=sys.stderr)
        sys.exit(1)

def get_supabase_service_role_key():
    """Hent Supabase Service Role Key fra Secret Manager

    ⚠️ WARNING: Service Role Key has FULL database access!
    Never expose this in frontend or client code!
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/supabase-service-role-key/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error: Could not retrieve Supabase Service Role Key from Secret Manager: {e}", file=sys.stderr)
        print(f"\nTroubleshooting:", file=sys.stderr)
        print(f"  1. Check authentication: gcloud auth application-default login", file=sys.stderr)
        print(f"  2. Check secret exists: gcloud secrets list --project={PROJECT_ID}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get Supabase keys from Secret Manager")
    parser.add_argument(
        "--type",
        choices=["anon", "service-role", "both"],
        default="both",
        help="Which key(s) to retrieve"
    )

    args = parser.parse_args()

    if args.type in ["anon", "both"]:
        anon_key = get_supabase_anon_key()
        if args.type == "anon":
            print(anon_key)
        else:
            print(f"ANON_KEY={anon_key}")

    if args.type in ["service-role", "both"]:
        service_role_key = get_supabase_service_role_key()
        if args.type == "service-role":
            print(service_role_key)
        else:
            print(f"SERVICE_ROLE_KEY={service_role_key}")


