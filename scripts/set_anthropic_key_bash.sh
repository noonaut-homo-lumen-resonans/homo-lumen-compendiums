#!/bin/bash
# Quick script for å sette ANTHROPIC_API_KEY i bash

echo ""
echo "=== Sett ANTHROPIC_API_KEY ==="
echo ""

# Be om API key
echo "Lim inn din Anthropic API key (starter med sk-ant-api03-...):"
read -s api_key

# Valider
if [ -z "$api_key" ]; then
    echo ""
    echo "[X] Ingen key gitt. Avslutter."
    exit 1
fi

# Sett environment variable
export ANTHROPIC_API_KEY="$api_key"

# Verifiser
echo ""
echo "[OK] API key satt!"
echo ""
echo "Test med:"
echo "  echo \$ANTHROPIC_API_KEY"
echo "  bash scripts/check_anthropic_key.sh"
echo ""
echo "For permanent lagring, legg til i ~/.bashrc:"
echo "  export ANTHROPIC_API_KEY=\"$api_key\""

