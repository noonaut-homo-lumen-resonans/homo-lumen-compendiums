#!/usr/bin/env python3
"""
Lagre GitHub token i Google Secret Manager
For: Homo Lumen Compendiums Project
Project ID: dotted-stage-476513-r4

Usage:
    python scripts/store_github_token_secret.py

Requirements:
    pip install google-cloud-secret-manager
"""

import sys
import os
from typing import Optional

def store_github_token_in_secret_manager(token: str, project_id: str = "dotted-stage-476513-r4") -> bool:
    """
    Lagre GitHub token i Google Secret Manager.

    Args:
        token: GitHub Personal Access Token
        project_id: Google Cloud Project ID

    Returns:
        True hvis lagring lyktes, False ellers
    """
    try:
        from google.cloud import secretmanager

        # Opprett Secret Manager client
        client = secretmanager.SecretManagerServiceClient()

        secret_name = "github-token"
        parent = f"projects/{project_id}"

        # Sjekk om secret allerede eksisterer
        try:
            secret_path = f"{parent}/secrets/{secret_name}"
            existing_secret = client.get_secret(request={"name": secret_path})
            print(f"✅ Secret '{secret_name}' eksisterer allerede")
            print(f"   Legger til ny versjon...")

            # Legg til ny versjon (beholder gamle versjoner)
            version = client.add_secret_version(
                request={
                    "parent": secret_path,
                    "payload": {
                        "data": token.encode("UTF-8")
                    }
                }
            )
            print(f"✅ Ny versjon lagt til: {version.name}")
            return True

        except Exception as e:
            if "not found" in str(e).lower():
                # Secret finnes ikke, opprett ny
                print(f"📝 Oppretter ny secret: {secret_name}")

                # Opprett secret
                secret = client.create_secret(
                    request={
                        "parent": parent,
                        "secret_id": secret_name,
                        "secret": {
                            "replication": {
                                "automatic": {}
                            }
                        }
                    }
                )

                # Legg til første versjon
                version = client.add_secret_version(
                    request={
                        "parent": secret.name,
                        "payload": {
                            "data": token.encode("UTF-8")
                        }
                    }
                )
                print(f"✅ Secret opprettet: {secret.name}")
                print(f"✅ Første versjon lagt til: {version.name}")
                return True
            else:
                raise

    except ImportError:
        print("❌ ERROR: google-cloud-secret-manager ikke installert")
        print("\n📦 Installer med:")
        print("   pip install google-cloud-secret-manager")
        return False

    except Exception as e:
        print(f"❌ ERROR: Kunne ikke lagre secret: {e}")
        print("\n💡 Feilsøking:")
        print("   1. Verifiser at du er autentisert:")
        print("      gcloud auth application-default login")
        print("   2. Eller sett miljøvariabel:")
        print("      $env:GOOGLE_APPLICATION_CREDENTIALS='C:\\path\\to\\service-account-key.json'")
        print("   3. Sjekk at Secret Manager API er aktivert:")
        print("      gcloud services enable secretmanager.googleapis.com")
        return False


def get_token_from_user() -> Optional[str]:
    """Hent token fra brukerinput (sikker metode - ikke viser token i output)"""
    print("\n🔐 GitHub Token Input")
    print("=" * 50)
    print("Lim inn GitHub Personal Access Token (tokenet vises ikke):")

    # Bruk getpass for å skjule input
    try:
        import getpass
        token = getpass.getpass("Token: ")
    except Exception:
        # Fallback hvis getpass ikke fungerer
        token = input("Token: ")

    if not token or len(token) < 10:
        print("❌ Token ser ut til å være ugyldig")
        return None

    return token.strip()


def main():
    """Hovedfunksjon"""
    print("=" * 60)
    print("GitHub Token → Google Secret Manager")
    print("Project: dotted-stage-476513-r4")
    print("=" * 60)

    # Hent token (enten fra argument eller brukerinput)
    if len(sys.argv) > 1:
        token = sys.argv[1]
        print(f"📝 Bruker token fra kommandolinje argument")
    else:
        token = get_token_from_user()
        if not token:
            print("❌ Ingen token gitt. Avslutter.")
            sys.exit(1)

    # Verifiser token format (GitHub tokens starter med ghp_ eller gh_)
    if not (token.startswith("ghp_") or token.startswith("gho_") or token.startswith("ghu_")):
        print("⚠️  ADVARSEL: Token ser ikke ut som et gyldig GitHub token format")
        response = input("Fortsett likevel? (y/N): ")
        if response.lower() != 'y':
            print("❌ Avbrutt.")
            sys.exit(1)

    # Lagre i Secret Manager
    print("\n💾 Lagrer token i Google Secret Manager...")
    success = store_github_token_in_secret_manager(token)

    if success:
        print("\n" + "=" * 60)
        print("✅ GitHub token lagret i Google Secret Manager!")
        print("=" * 60)
        print("\n📋 Neste steg:")
        print("   1. Oppdater Git remote til å ikke inneholde token hardkodet")
        print("   2. Bruk Python script for å hente token fra Secret Manager")
        print("   3. Roter det gamle tokenet på GitHub (hvis det var eksponert)")
        print("\n📖 Se: docs/GOOGLE_SECRET_MANAGER_QUICK_START.md for bruk i kode")
        return 0
    else:
        print("\n" + "=" * 60)
        print("❌ Kunne ikke lagre token")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

