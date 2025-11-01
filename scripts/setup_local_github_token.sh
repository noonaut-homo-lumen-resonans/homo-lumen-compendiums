#!/bin/bash
# Setup Local GitHub Token Storage (Bash version)
# Henter token fra Secret Manager og lagrer lokalt

echo ""
echo "=== Setup Lokal GitHub Token ==="
echo "Henter token fra Google Secret Manager..."

# Hent token fra Secret Manager
token=$(gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$token" ]; then
    echo ""
    echo "❌ Kunne ikke hente token fra Secret Manager"
    echo ""
    echo "💡 Sjekk at du er autentisert:"
    echo "   gcloud auth login"
    exit 1
fi

echo "✅ Token hentet (starter med: ${token:0:15}...)"

# Test token før lagring
echo ""
echo "🔍 Tester token mot GitHub API..."
response=$(curl -s -H "Authorization: token $token" https://api.github.com/user)
login=$(echo "$response" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)

if [ -z "$login" ]; then
    echo "❌ Token fungerer ikke"
    exit 1
fi

echo "✅ Token fungerer! (Bruker: $login)"

# For Git Bash/Windows, bruk Windows Credential Manager via PowerShell
echo ""
echo "💾 Lagrer token i Windows Credential Manager..."

# Bruk PowerShell for å lagre i Windows Credential Manager (fungerer fra Git Bash)
powershell.exe -Command "cmdkey /generic:git:https://github.com /user:noonaut-homo-lumen-resonans /pass:$token" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Token lagret lokalt!"
    echo ""
    echo "📋 Du kan nå bruke Git normalt:"
    echo "   git push origin main"
    echo "   git pull origin main"
    echo ""
    echo "💡 Token hentes automatisk fra Windows Credential Manager"
else
    echo ""
    echo "❌ Kunne ikke lagre token"
    exit 1
fi

echo ""
echo "✅ Ferdig!"

