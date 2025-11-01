#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Anthropic SDK Integration
Demonstrerer hvordan du bruker official Anthropic SDK
"""

import os
import sys
from typing import Optional

# Fix Windows encoding issues
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.cloud import secretmanager

def get_anthropic_api_key() -> Optional[str]:
    """
    Hent Anthropic API key fra Google Secret Manager.
    Fallback til environment variable for lokal utvikling.
    """
    # Prøv først Google Secret Manager (produksjon)
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = "dotted-stage-476513-r4"
        secret_name = "anthropic-api-key"
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception:
        # Fallback til environment variable (lokal utvikling)
        return os.getenv("ANTHROPIC_API_KEY")

# Test med official Anthropic SDK
def test_anthropic_sdk():
    """Test Anthropic SDK med Claude Sonnet 4.5"""
    try:
        import anthropic

        # Hent API key
        api_key = get_anthropic_api_key()
        if not api_key:
            print("[X] ANTHROPIC_API_KEY ikke funnet")
            print("   Sett environment variable: $env:ANTHROPIC_API_KEY = 'sk-ant-...'")
            print("   Eller lagre i Secret Manager: gcloud secrets create anthropic-api-key")
            return False

        # Opprett client
        client = anthropic.Anthropic(api_key=api_key)

        # Send melding
        print("[*] Sender testmelding til Claude Sonnet 4.5...")
        message = client.messages.create(
            model="claude-sonnet-4-5",  # Eller "claude-3-5-sonnet-20241022"
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Hello, Claude! Can you confirm you're working? Respond in Norwegian."}
            ]
        )

        # Vis svar
        print("\n[OK] Claude Response:")
        print("=" * 60)
        for content_block in message.content:
            if content_block.type == "text":
                print(content_block.text)
        print("=" * 60)

        return True

    except ImportError:
        print("[X] Anthropic SDK ikke installert")
        print("   Installer med: pip install anthropic")
        return False
    except Exception as e:
        print(f"[X] Feil: {e}")
        return False

if __name__ == "__main__":
    print("=== Anthropic SDK Test ===")
    print()
    success = test_anthropic_sdk()
    if success:
        print("\n[OK] Test vellykket!")
    else:
        print("\n[X] Test feilet")

