#!/usr/bin/env python3
# Quick test av Anthropic Claude SDK

import anthropic
import os

# Hent API key
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("[X] ANTHROPIC_API_KEY ikke funnet")
    print("   Sett med: export ANTHROPIC_API_KEY=\"sk-ant-...\"")
    exit(1)

# Opprett client
client = anthropic.Anthropic(api_key=api_key)

# Send melding
print("[*] Sender melding til Claude Sonnet 4.5...")
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude! Kan du bekrefte at du fungerer? Svar på norsk."}
    ]
)

# Vis svar
print("\n" + "=" * 60)
print("Claude Response:")
print("=" * 60)
print(message.content[0].text)
print("=" * 60)

