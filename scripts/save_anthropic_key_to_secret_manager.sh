#!/bin/bash
# Lagre Anthropic API Key i Google Secret Manager

echo ""
echo "=== Lagre API Key i Google Secret Manager ==="
echo ""

# Hent API key fra environment variable
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "[X] ANTHROPIC_API_KEY ikke funnet"
    echo ""
    echo "Sett den først med:"
    echo "  export ANTHROPIC_API_KEY=\"sk-ant-api03-DIN_KEY\""
    echo ""
    exit 1
fi

echo "[*] Fant API key: ${ANTHROPIC_API_KEY:0:20}..."
echo ""

# Spør om bekreftelse
read -p "Lagre i Google Secret Manager? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Avbrutt."
    exit 0
fi

# Prøv å opprette nytt secret
echo ""
echo "Lagrer i Secret Manager..."
echo -n "$ANTHROPIC_API_KEY" | gcloud secrets create anthropic-api-key --data-file=- --project=dotted-stage-476513-r4 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[OK] API key lagret i Google Secret Manager!"
    echo ""
    echo "Du kan nå hente den i Python:"
    echo "  python scripts/test_anthropic_sdk.py"
    echo ""
    echo "(Scriptet henter automatisk fra Secret Manager)"
else
    # Secret kan allerede eksistere, prøv å oppdatere
    echo "Secret kan allerede eksistere, prøver å oppdatere..."
    echo -n "$ANTHROPIC_API_KEY" | gcloud secrets versions add anthropic-api-key --data-file=- --project=dotted-stage-476513-r4 2>/dev/null

    if [ $? -eq 0 ]; then
        echo "[OK] API key oppdatert i Google Secret Manager!"
    else
        echo "[X] Kunne ikke lagre. Sjekk:"
        echo "   1. Er du autentisert? (gcloud auth login)"
        echo "   2. Har du tilgang til prosjektet?"
        exit 1
    fi
fi

