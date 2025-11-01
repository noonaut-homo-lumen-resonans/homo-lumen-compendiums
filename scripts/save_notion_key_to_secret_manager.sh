#!/bin/bash
# Save Notion API Key to Google Secret Manager
# Usage: ./scripts/save_notion_key_to_secret_manager.sh

echo ""
echo "=== Lagrer Notion API Key til Secret Manager ==="
echo ""

# Hent project ID
PROJECT_ID="dotted-stage-476513-r4"
SECRET_NAME="notion-api-key"

# Be om API key
read -sp "Lim inn Notion API Key (starter med 'secret_' eller 'notion_'): " NOTION_KEY
echo ""

if [ -z "$NOTION_KEY" ]; then
    echo "❌ Ingen API key gitt"
    exit 1
fi

# Lagre til Secret Manager
echo "💾 Lagrer til Secret Manager..."
echo -n "$NOTION_KEY" | gcloud secrets create $SECRET_NAME --data-file=- --project=$PROJECT_ID 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Notion API Key lagret!"
    echo ""
    echo "For å hente token:"
    echo "  gcloud secrets versions access latest --secret=$SECRET_NAME --project=$PROJECT_ID"
else
    echo ""
    echo "⚠️  Secret finnes kanskje allerede. Prøver å oppdatere..."
    echo -n "$NOTION_KEY" | gcloud secrets versions add $SECRET_NAME --data-file=- --project=$PROJECT_ID

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Notion API Key oppdatert!"
    else
        echo ""
        echo "❌ Kunne ikke lagre/oppdatere secret"
        exit 1
    fi
fi

echo ""
echo "✅ Ferdig!"



