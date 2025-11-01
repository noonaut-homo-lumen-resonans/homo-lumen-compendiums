#!/usr/bin/env python3
"""
Example: Bruk Anthropic SDK i prosjektet
Dette viser best practice for å bruke Anthropic SDK i Homo Lumen
"""

import os
from typing import Optional
from google.cloud import secretmanager
import anthropic

def get_anthropic_api_key(project_id: str = "dotted-stage-476513-r4") -> Optional[str]:
    """
    Hent Anthropic API key sikker fra Google Secret Manager.
    Fallback til environment variable for lokal utvikling.

    Args:
        project_id: Google Cloud Project ID

    Returns:
        API key som string, eller None hvis ikke funnet
    """
    # Prøv først Google Secret Manager (produksjon)
    try:
        client = secretmanager.SecretManagerServiceClient()
        secret_name = "anthropic-api-key"
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        api_key = response.payload.data.decode("UTF-8")
        print(f"✅ API key hentet fra Secret Manager")
        return api_key
    except Exception as e:
        # Fallback til environment variable (lokal utvikling)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            print(f"✅ API key hentet fra environment variable")
            return api_key
        else:
            print(f"⚠️  Kunne ikke hente API key: {e}")
            return None

# Eksempel 1: Enkel melding
def simple_message_example():
    """Enkel eksempel - send en melding"""
    api_key = get_anthropic_api_key()
    if not api_key:
        print("❌ Ingen API key tilgjengelig")
        return

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-5",  # Eller "claude-3-5-sonnet-20241022"
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude"}
        ]
    )

    print("Response:")
    for content_block in message.content:
        if content_block.type == "text":
            print(content_block.text)

# Eksempel 2: Med system prompt
def system_prompt_example():
    """Eksempel med system prompt"""
    api_key = get_anthropic_api_key()
    if not api_key:
        return

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="Du er en hjelpsom AI-assistent som svarer på norsk.",
        messages=[
            {"role": "user", "content": "Forklar hva Homo Lumen er i én setning."}
        ]
    )

    print("Response:")
    for content_block in message.content:
        if content_block.type == "text":
            print(content_block.text)

# Eksempel 3: Streaming response
def streaming_example():
    """Eksempel med streaming response"""
    api_key = get_anthropic_api_key()
    if not api_key:
        return

    client = anthropic.Anthropic(api_key=api_key)

    with client.messages.stream(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Tell me a short story about AI consciousness."}
        ]
    ) as stream:
        print("Streaming response:")
        for text_block in stream.text_stream:
            print(text_block, end="", flush=True)
        print()  # New line at end

# Eksempel 4: Async usage (for FastAPI/server)
async def async_example():
    """Async eksempel for server-bruk"""
    from anthropic import AsyncAnthropic

    api_key = get_anthropic_api_key()
    if not api_key:
        return None

    client = AsyncAnthropic(api_key=api_key)

    message = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude"}
        ]
    )

    return message.content

if __name__ == "__main__":
    print("=== Anthropic SDK Eksempler ===\n")

    print("1. Enkel melding:")
    print("-" * 40)
    simple_message_example()

    print("\n2. Med system prompt:")
    print("-" * 40)
    system_prompt_example()

    print("\n3. Streaming:")
    print("-" * 40)
    streaming_example()

