#!/bin/bash
# Sjekk om ANTHROPIC_API_KEY er satt og fungerer

echo ""
echo "=== Sjekker ANTHROPIC_API_KEY ==="
echo ""

# Sjekk om key er satt
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "[X] ANTHROPIC_API_KEY er IKKE satt"
    echo ""
    echo "Sett med:"
    echo "  export ANTHROPIC_API_KEY=\"sk-ant-api03-DIN_KEY\""
    echo ""
    exit 1
fi

# Vis første del av key (for verifisering)
echo "[OK] ANTHROPIC_API_KEY er satt"
echo "Starter med: ${ANTHROPIC_API_KEY:0:20}..."
echo ""

# Sjekk format
if [[ ! "$ANTHROPIC_API_KEY" =~ ^sk-ant- ]]; then
    echo "[!] ADVARSEL: API key ser ikke ut til å ha riktig format"
    echo "Forventet format: sk-ant-api03-..."
    echo ""
fi

# Test med Python
echo "Tester med Anthropic SDK..."
echo ""

if command -v python &> /dev/null; then
    python scripts/test_anthropic_sdk.py
elif command -v python3 &> /dev/null; then
    python3 scripts/test_anthropic_sdk.py
else
    echo "[X] Python ikke funnet"
    echo ""
    echo "Men API key er satt, så du kan bruke den i Python kode:"
    echo ""
    echo "import os"
    echo "api_key = os.getenv('ANTHROPIC_API_KEY')"
    exit 1
fi

