#!/bin/bash
# Setup Anthropic API Key - Bash Script
# Usage: bash scripts/setup_anthropic_key.sh

echo ""
echo "=== Setup Anthropic API Key ==="
echo ""

# Be om API key
echo "Lim inn din Anthropic API key (starter med sk-ant-...):"
read -s api_key

# Valider at key ikke er tom
if [ -z "$api_key" ]; then
    echo ""
    echo "[X] Ingen API key gitt. Avslutter."
    exit 1
fi

# Valider format
if [[ ! "$api_key" =~ ^sk-ant- ]]; then
    echo ""
    echo "[!] ADVARSEL: API key ser ikke ut til å ha riktig format (sk-ant-...)"
    read -p "Fortsett likevel? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo "Avbrutt."
        exit 1
    fi
fi

# Spør om lagring
echo ""
echo "Hvor vil du lagre API key?"
echo "1. Environment variable (kun denne sesjonen)"
echo "2. .env file (lokal utvikling - legges til .gitignore)"
echo "3. Google Secret Manager (produksjon - anbefalt)"
read -p "Velg (1/2/3): " choice

case $choice in
    1)
        # Sett environment variable (kun denne sesjonen)
        export ANTHROPIC_API_KEY="$api_key"
        echo ""
        echo "[OK] API key satt som environment variable (kun denne sesjonen)"
        echo ""
        echo "For å gjøre permanent, legg til i ~/.bashrc eller ~/.bash_profile:"
        echo "  export ANTHROPIC_API_KEY=\"$api_key\""
        ;;
    2)
        # Lagre i .env file
        env_file=".env"
        if [ -f "$env_file" ]; then
            # Sjekk om ANTHROPIC_API_KEY allerede finnes
            if grep -q "ANTHROPIC_API_KEY" "$env_file"; then
                # Oppdater eksisterende
                if [[ "$OSTYPE" == "darwin"* ]]; then
                    # macOS
                    sed -i '' "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$api_key|" "$env_file"
                else
                    # Linux/Git Bash
                    sed -i "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$api_key|" "$env_file"
                fi
            else
                # Legg til ny
                echo "" >> "$env_file"
                echo "ANTHROPIC_API_KEY=$api_key" >> "$env_file"
            fi
        else
            # Opprett ny .env file
            echo "ANTHROPIC_API_KEY=$api_key" > "$env_file"
        fi

        # Sett også environment variable
        export ANTHROPIC_API_KEY="$api_key"

        echo ""
        echo "[OK] API key lagret i .env file og satt som environment variable"
        echo ""
        echo "For å laste .env filen automatisk, legg til i ~/.bashrc:"
        echo "  source <path-to-repo>/.env"
        ;;
    3)
        # Lagre i Google Secret Manager
        echo ""
        echo "Lagrer i Google Secret Manager..."
        echo -n "$api_key" | gcloud secrets create anthropic-api-key --data-file=- --project=dotted-stage-476513-r4 2>/dev/null

        if [ $? -eq 0 ]; then
            echo "[OK] API key lagret i Google Secret Manager"
        else
            # Secret kan allerede eksistere, prøv å oppdatere
            echo -n "$api_key" | gcloud secrets versions add anthropic-api-key --data-file=- --project=dotted-stage-476513-r4 2>/dev/null

            if [ $? -eq 0 ]; then
                echo "[OK] API key oppdatert i Google Secret Manager"
            else
                echo "[X] Kunne ikke lagre i Secret Manager"
                echo "    Sjekk at du er autentisert: gcloud auth login"
                exit 1
            fi
        fi

        # Sett også environment variable for testing
        export ANTHROPIC_API_KEY="$api_key"
        ;;
    *)
        echo "[X] Ugyldig valg. Avslutter."
        exit 1
        ;;
esac

# Test at det fungerer
echo ""
echo "Tester API key..."
python scripts/test_anthropic_sdk.py

