#!/bin/bash
# Script for å oppdatere GitHub token i Google Secret Manager
# Usage: bash scripts/update_github_token.sh

echo ""
echo "=== Oppdater GitHub Token i Secret Manager ==="
echo "Prosjekt: dotted-stage-476513-r4"
echo "Secret: github-token"
echo ""

# Be bruker om nytt token (skjul input)
echo "Lim inn ditt nye GitHub token (tokenet vises ikke):"
read -s token

# Verifiser at token ikke er tomt
if [ -z "$token" ]; then
    echo ""
    echo "❌ Ingen token gitt. Avslutter."
    exit 1
fi

# Verifiser token format
if [[ ! "$token" =~ ^gh(p|o|u)_ ]]; then
    echo ""
    echo "⚠️  ADVARSEL: Token ser ikke ut som et gyldig GitHub token format"
    echo "Forventet format: ghp_..., gho_..., eller ghu_..."
    read -p "Fortsett likevel? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Avbrutt."
        exit 1
    fi
fi

# Lagre token i Secret Manager
echo ""
echo "💾 Lagrer nytt token i Secret Manager..."

echo -n "$token" | gcloud secrets versions add github-token --data-file=- --project=dotted-stage-476513-r4

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Token oppdatert vellykket!"
    echo ""
    echo "📋 Verifiser med:"
    echo "   gcloud secrets versions access latest --secret=github-token"
else
    echo ""
    echo "❌ Feil ved lagring. Sjekk feilmeldingen over."
    exit 1
fi

echo ""
echo "✅ Ferdig!"

