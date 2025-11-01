#!/bin/bash
# Forbedret script for å lagre i Secret Manager med bedre feilmeldinger

echo ""
echo "=== Lagre API Key i Google Secret Manager ==="
echo ""

# Sjekk autentisering
echo "[*] Sjekker gcloud autentisering..."
gcloud auth list --filter=status:ACTIVE --format="value(account)" > /dev/null 2>&1
if [ $? -ne 0 ] || [ -z "$(gcloud auth list --filter=status:ACTIVE --format='value(account)')" ]; then
    echo "[X] Ikke autentisert med gcloud"
    echo ""
    echo "Autentiser med:"
    echo "  gcloud auth login"
    exit 1
fi

ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" | head -1)
echo "[OK] Autentisert som: $ACTIVE_ACCOUNT"
echo ""

# Sjekk prosjekt
echo "[*] Sjekker prosjekt..."
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ "$CURRENT_PROJECT" != "dotted-stage-476513-r4" ]; then
    echo "[!] Prosjekt er ikke satt til dotted-stage-476513-r4"
    echo "    Nåværende: $CURRENT_PROJECT"
    echo ""
    read -p "Vil du sette prosjekt til dotted-stage-476513-r4? (y/N): " set_project
    if [ "$set_project" = "y" ] || [ "$set_project" = "Y" ]; then
        gcloud config set project dotted-stage-476513-r4
        echo "[OK] Prosjekt satt"
    else
        echo "Avbrutt."
        exit 1
    fi
else
    echo "[OK] Prosjekt: dotted-stage-476513-r4"
fi
echo ""

# Hent API key
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

# Prøv å opprette eller oppdatere
echo ""
echo "Lagrer i Secret Manager..."

# Sjekk om secret allerede eksisterer
gcloud secrets describe anthropic-api-key --project=dotted-stage-476513-r4 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    # Secret eksisterer - oppdater
    echo "[*] Secret eksisterer allerede, oppdaterer..."
    echo -n "$ANTHROPIC_API_KEY" | gcloud secrets versions add anthropic-api-key --data-file=- --project=dotted-stage-476513-r4

    if [ $? -eq 0 ]; then
        echo "[OK] API key oppdatert i Google Secret Manager!"
    else
        echo "[X] Kunne ikke oppdatere secret"
        echo ""
        echo "Mulige årsaker:"
        echo "  1. Manglende tilgang til Secret Manager"
        echo "  2. Secret Manager API ikke aktivert"
        echo ""
        echo "Prøv å aktivere API:"
        echo "  gcloud services enable secretmanager.googleapis.com --project=dotted-stage-476513-r4"
        exit 1
    fi
else
    # Secret eksisterer ikke - opprett
    echo "[*] Oppretter ny secret..."
    echo -n "$ANTHROPIC_API_KEY" | gcloud secrets create anthropic-api-key --data-file=- --project=dotted-stage-476513-r4 --replication-policy="automatic"

    if [ $? -eq 0 ]; then
        echo "[OK] API key lagret i Google Secret Manager!"
    else
        echo "[X] Kunne ikke opprette secret"
        echo ""
        echo "Mulige årsaker:"
        echo "  1. Secret Manager API ikke aktivert"
        echo "  2. Manglende tilgang til prosjektet"
        echo ""
        echo "Prøv å aktivere API:"
        echo "  gcloud services enable secretmanager.googleapis.com --project=dotted-stage-476513-r4"
        exit 1
    fi
fi

echo ""
echo "Verifiserer lagring..."
gcloud secrets versions access latest --secret=anthropic-api-key --project=dotted-stage-476513-r4 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "[OK] Secret verifisert - fungerer!"
    echo ""
    echo "Du kan nå bruke Python scripts som henter automatisk:"
    echo "  python scripts/test_anthropic_sdk.py"
else
    echo "[!] Kunne ikke verifisere secret, men lagring kan ha fungert"
fi

