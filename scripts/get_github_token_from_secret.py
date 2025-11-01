#!/usr/bin/env python3
"""
Hent GitHub token fra Google Secret Manager
For bruk i Git-operasjoner eller Python scripts

Usage:
    python scripts/get_github_token_from_secret.py
"""

import sys
from typing import Optional

def get_github_token(project_id: str = "dotted-stage-476513-r4", secret_name: str = "github-token") -> Optional[str]:
    """
    Hent GitHub token fra Google Secret Manager.

    Args:
        project_id: Google Cloud Project ID
        secret_name: Navn på secret i Secret Manager

    Returns:
        GitHub token som string, eller None hvis feil
    """
    try:
        from google.cloud import secretmanager

        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

        response = client.access_secret_version(request={"name": name})
        token = response.payload.data.decode("UTF-8")

        return token

    except ImportError:
        print("❌ ERROR: google-cloud-secret-manager ikke installert", file=sys.stderr)
        print("   Installer med: pip install google-cloud-secret-manager", file=sys.stderr)
        return None

    except Exception as e:
        print(f"❌ ERROR: Kunne ikke hente secret: {e}", file=sys.stderr)
        return None


def main():
    """Hovedfunksjon - skriv ut token til stdout"""
    token = get_github_token()
    if token:
        print(token, end="")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())

